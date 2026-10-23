---
title: Siemens Software Center
date: 2026-10-23 09:27:12 +0000
categories:
- Daily Signal
tags:
- rce
- security-news
- advisory
severity: critical
must_know: true
sources:
- name: CISA advisories and alerts
  url: https://www.cisa.gov/news-events/ics-advisories/icsa-26-295-03
cve: CVE-2026-110936
cvss: 8.4
epss: 0.001
kev: true
---

View CSAF Summary The affected application loads dynamic-link libraries (DLLs) from an uncontrolled search path. This could allow an authenticated local attacker to place a specially crafted DLL in a directory that the application searches, leading to arbitrary code execution with the privileges of the affected application. Siemens has released a new version for Siemens Software Center and recommends to update to the latest version.
