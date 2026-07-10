"""Enrich staged candidates with CVSS, EPSS, and KEV data.

For every staged candidate that mentions a CVE ID, this script:
  * queries NVD API 2.0 for the CVSS base score (NVD_API_KEY optional, free),
  * queries FIRST EPSS for the exploit prediction score,
  * checks the CISA KEV catalog for known-exploited status,
  * optionally cross-checks the GitHub Advisory database when GITHUB_TOKEN
    is available.

Every API result is cached in .cache/enrichment.json so repeat runs do not
re-hit the APIs. Severity and must_know are computed HERE and only here:
  kev or epss >= 0.5 or cvss >= 9.0  -> critical
  cvss >= 7.0                        -> high
  cvss >= 4.0                        -> medium
  cvss present otherwise             -> low
  must_know when kev or epss >= 0.5
"""

from __future__ import annotations

import json
import os
import re
import sys
import time

import requests

from pipeline_io import CACHE_DIR, dump_front_matter, iter_staging, load_front_matter

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
EPSS_API_URL = "https://api.first.org/data/v1/epss"
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)
CACHE_FILE = CACHE_DIR / "enrichment.json"
KEV_CACHE_FILE = CACHE_DIR / "kev.json"
KEV_TTL_SECONDS = 12 * 3600
USER_AGENT = "ZeroWire/1.0 (+https://github.com/thapaswin125/zerowire)"

# NVD public rate limit is 5 requests per rolling 30s; 50 with a free key.
NVD_DELAY_NO_KEY = 6.5
NVD_DELAY_WITH_KEY = 0.8
NVD_MAX_RETRIES = 4


def load_cache() -> dict:
    if CACHE_FILE.is_file():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def save_cache(cache: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=1, sort_keys=True), encoding="utf-8")


def load_kev_ids() -> set[str]:
    if KEV_CACHE_FILE.is_file():
        try:
            blob = json.loads(KEV_CACHE_FILE.read_text(encoding="utf-8"))
            if time.time() - blob.get("fetched_at", 0) < KEV_TTL_SECONDS:
                return set(blob["cve_ids"])
        except (json.JSONDecodeError, KeyError):
            pass
    print("fetching CISA KEV catalog ...")
    try:
        resp = requests.get(KEV_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
        resp.raise_for_status()
        ids = {v["cveID"].upper() for v in resp.json().get("vulnerabilities", [])}
    except (requests.RequestException, ValueError, KeyError) as exc:
        print(f"  warn: KEV fetch failed, treating catalog as empty: {exc}", file=sys.stderr)
        return set()
    KEV_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEV_CACHE_FILE.write_text(
        json.dumps({"fetched_at": time.time(), "cve_ids": sorted(ids)}), encoding="utf-8"
    )
    return ids


def fetch_nvd_cvss(cve: str, api_key: str | None) -> float | None:
    headers = {"User-Agent": USER_AGENT}
    if api_key:
        headers["apiKey"] = api_key
    delay = NVD_DELAY_WITH_KEY if api_key else NVD_DELAY_NO_KEY
    for attempt in range(NVD_MAX_RETRIES):
        time.sleep(delay)
        try:
            resp = requests.get(NVD_API_URL, params={"cveId": cve}, headers=headers, timeout=60)
        except requests.RequestException as exc:
            print(f"  warn: NVD request error for {cve}: {exc}", file=sys.stderr)
            continue
        if resp.status_code in (403, 429, 503):
            wait = 15 * (attempt + 1)
            print(f"  NVD rate limited ({resp.status_code}), backing off {wait}s ...")
            time.sleep(wait)
            continue
        if resp.status_code != 200:
            print(f"  warn: NVD returned {resp.status_code} for {cve}", file=sys.stderr)
            return None
        vulns = resp.json().get("vulnerabilities", [])
        if not vulns:
            return None
        metrics = vulns[0].get("cve", {}).get("metrics", {})
        for key in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if metrics.get(key):
                return float(metrics[key][0]["cvssData"]["baseScore"])
        return None
    return None


def fetch_epss_scores(cves: list[str]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for i in range(0, len(cves), 50):
        batch = cves[i : i + 50]
        try:
            resp = requests.get(
                EPSS_API_URL,
                params={"cve": ",".join(batch)},
                headers={"User-Agent": USER_AGENT},
                timeout=60,
            )
            resp.raise_for_status()
            for row in resp.json().get("data", []):
                scores[row["cve"].upper()] = float(row["epss"])
        except (requests.RequestException, ValueError, KeyError) as exc:
            print(f"  warn: EPSS lookup failed for batch: {exc}", file=sys.stderr)
    return scores


def fetch_github_advisory(cve: str, token: str) -> str | None:
    query = """
    query($cve: String!) {
      securityAdvisories(identifier: {type: CVE, value: $cve}, first: 1) {
        nodes { ghsaId permalink }
      }
    }
    """
    try:
        resp = requests.post(
            GITHUB_GRAPHQL_URL,
            json={"query": query, "variables": {"cve": cve}},
            headers={"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT},
            timeout=60,
        )
        resp.raise_for_status()
        nodes = resp.json()["data"]["securityAdvisories"]["nodes"]
        return nodes[0]["ghsaId"] if nodes else None
    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        print(f"  warn: GitHub advisory lookup failed for {cve}: {exc}", file=sys.stderr)
        return None


def compute_severity(cvss: float | None, epss: float | None, kev: bool) -> str:
    if kev or (epss is not None and epss >= 0.5) or (cvss is not None and cvss >= 9.0):
        return "critical"
    if cvss is not None and cvss >= 7.0:
        return "high"
    if cvss is not None and cvss >= 4.0:
        return "medium"
    if cvss is not None:
        return "low"
    return "info"


def main() -> int:
    api_key = os.environ.get("NVD_API_KEY") or None
    gh_token = os.environ.get("GITHUB_TOKEN") or None
    cache = load_cache()
    kev_ids = load_kev_ids()

    candidates = []
    wanted_cves: set[str] = set()
    for path in iter_staging():
        meta, body = load_front_matter(path)
        cves = [c.upper() for c in CVE_RE.findall(f"{meta.get('title', '')} {body}")]
        if not cves:
            continue
        candidates.append((path, meta, body, cves[0]))
        wanted_cves.add(cves[0])

    if not candidates:
        print("no CVE-bearing candidates to enrich")
        return 0

    uncached_epss = [c for c in wanted_cves if "epss" not in cache.get(c, {})]
    epss_scores = fetch_epss_scores(uncached_epss) if uncached_epss else {}

    enriched = 0
    for path, meta, body, cve in candidates:
        entry = cache.setdefault(cve, {})

        if "cvss" not in entry:
            print(f"querying NVD for {cve} ...")
            entry["cvss"] = fetch_nvd_cvss(cve, api_key)
        if "epss" not in entry:
            entry["epss"] = epss_scores.get(cve)
        if gh_token and "ghsa" not in entry:
            entry["ghsa"] = fetch_github_advisory(cve, gh_token)

        cvss = entry.get("cvss")
        epss = entry.get("epss")
        kev = cve in kev_ids

        meta["cve"] = cve
        if cvss is not None:
            meta["cvss"] = cvss
        if epss is not None:
            meta["epss"] = round(epss, 3)
        meta["kev"] = kev
        if entry.get("ghsa"):
            meta["ghsa"] = entry["ghsa"]
        meta["severity"] = compute_severity(cvss, epss, kev)
        meta["must_know"] = bool(kev or (epss is not None and epss >= 0.5))

        dump_front_matter(path, meta, body)
        enriched += 1

    save_cache(cache)
    print(f"enriched {enriched} candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
