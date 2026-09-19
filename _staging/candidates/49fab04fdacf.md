---
id: 49fab04fdacf
candidate: true
title: CVE-2026-84750 - Ultimate Addons for Contact Form 7 3.2.4 - 3.5.50 - Unauthenticated Arbitrary File Upload via Signature Field
date: 2026-09-19 08:52:55 +0000
categories:
- Daily Signal
tags:
- wordpress
- security-news
- advisory
severity: info
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-84750
cve: CVE-2026-84750
kev: false
---

CVE ID : CVE-2026-84750 Published : Sept. 19, 2026, 6 a.m. | 56 minutes ago Description : The Ultra Addons for Contact Form 7 WordPress plugin before 3.5.51 does not validate the type or extension of files uploaded through one of its form fields, and stores them at a predictable public path with the attacker-chosen extension intact, allowing unauthenticated users to upload arbitrary files.
