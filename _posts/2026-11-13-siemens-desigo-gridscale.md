---
title: Siemens Desigo, Gridscale
date: 2026-11-13 12:26:08 +0000
categories:
- Daily Signal
tags:
- memory-corruption
- patch
- security-news
severity: critical
must_know: true
sources:
- name: CISA advisories and alerts
  url: https://www.cisa.gov/news-events/ics-advisories/icsa-26-316-02
cve: CVE-2026-111497
cvss: 9.2
kev: true
---

View CSAF Summary On October 21, 2026, the Node.js project released security updates addressing a critical vulnerability in the Brotli decoder bundled with Node.js, commonly referred to as "Node2Shell" (tracked as CVE-2026-111497). The vulnerability is an out-of-bounds write that could allow a remote attacker to cause memory corruption and potentially execute arbitrary code.
