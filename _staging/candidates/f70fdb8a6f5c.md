---
id: f70fdb8a6f5c
candidate: true
title: 'CVE-2026-48807 - Twig: Sandbox `__toString()` policy bypass via `Traversable` in `join` and `replace` filters'
date: 2026-07-14 22:56:21 +0000
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
  url: https://cvefeed.io/vuln/detail/CVE-2026-48807
cve: CVE-2026-48807
cvss: 7.1
kev: false
ghsa: GHSA-8x9c-rmqh-456c
---

CVE ID : CVE-2026-48807 Published : July 14, 2026, 9:29 p.m. | 47 minutes ago Description : Twig is a template language for PHP. Prior to 3.27.0, the sandbox __toString() checks do not fully cover Traversable values passed to join and replace filters or operands evaluated by the in and not in operators, allowing contained Stringable objects to be coerced to strings without consulting the sandbox policy.
