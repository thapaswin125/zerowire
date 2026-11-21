---
id: a97dd0d2deed
candidate: true
title: CVE-2026-126705 - WP Job Portal <= 2.8.0 - Authenticated (Subscriber+) SQL Injection via 'columns' Parameter
date: 2026-11-21 12:51:51 +0000
categories:
- Daily Signal
tags:
- sqli
- wordpress
- security-news
severity: medium
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-126705
cve: CVE-2026-126705
cvss: 6.5
kev: false
---

CVE ID : CVE-2026-126705 Published : Nov. 21, 2026, 11:30 a.m. | 55 minutes ago Description : The WP Job Portal – AI-Powered Recruitment System for Company or Job Board website plugin for WordPress is vulnerable to time-based SQL Injection via the 'columns[]' parameter in all versions up to, and including, 2.8.0 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.
