---
id: bea1ecc84d11
candidate: true
title: CVE-2026-112207 - Download Monitor < 5.3.4 - Reflected XSS via Cross-Origin Download Link
date: 2026-10-24 08:58:32 +0000
categories:
- Daily Signal
tags:
- rce
- wordpress
- xss
severity: info
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-112207
cve: CVE-2026-112207
kev: false
---

CVE ID : CVE-2026-112207 Published : Oct. 24, 2026, 6:16 a.m. | 54 minutes ago Description : The Download Monitor WordPress plugin before 5.3.4 does not properly validate that a clicked link belongs to the site before fetching it client-side and rendering part of the response in the page, which allows unauthenticated attackers to execute arbitrary JavaScript in the browser of any user who is tricked into clicking a crafted link.
