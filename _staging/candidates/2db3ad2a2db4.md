---
id: 2db3ad2a2db4
candidate: true
title: CVE-2026-71888 - CMS AuthenticatedData exposes attacker-inserted authAttrs when digestAlgorithm is absent
date: 2026-10-03 09:57:19 +0000
categories:
- Daily Signal
tags:
- security-news
- advisory
- watchlist
severity: high
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-71888
cve: CVE-2026-71888
cvss: 8.7
kev: false
---

CVE ID : CVE-2026-71888 Published : Oct. 3, 2026, 9:17 a.m. | 22 minutes ago Description : In Bouncy Castle for Java before 1.86, the streaming CMS AuthenticatedData parser accepted a message whose digestAlgorithm and authAttrs fields disagreed about whether authenticated attributes were present.
