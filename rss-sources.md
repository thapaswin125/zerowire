# RSS sources

This file is the single source of truth for the ingestion pipeline.
`scripts/fetch_feeds.py` reads every markdown link in a bullet line below.
I keep one feed per line, and I comment a feed out by removing the leading
dash. Lines starting with `#` are headings, not feeds.

## Vulnerability data

- [NVD recent CVEs](https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml)
- [CISA advisories and alerts](https://www.cisa.gov/cybersecurity-advisories/all.xml)

## News

- [BleepingComputer](https://www.bleepingcomputer.com/feed/)
- [The Hacker News](https://feeds.feedburner.com/TheHackersNews)

## Research

- [Google Project Zero](https://googleprojectzero.blogspot.com/feeds/posts/default?alt=rss)
- [GitHub Security Blog](https://github.blog/security/feed/)

## Vendor advisories

- [Microsoft MSRC Blog](https://msrc.microsoft.com/blog/feed)
- [Cisco Security Advisories](https://sec.cloudapps.cisco.com/security/center/psirtrss20/CiscoSecurityAdvisory.xml)
