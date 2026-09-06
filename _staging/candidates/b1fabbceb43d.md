---
id: b1fabbceb43d
candidate: true
title: CVE-2026-75793 - SureCart < 4.7.0 - Unauthenticated Account Creation with Automatic Login
date: 2026-09-06 08:45:02 +0000
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
  url: https://cvefeed.io/vuln/detail/CVE-2026-75793
cve: CVE-2026-75793
kev: false
---

CVE ID : CVE-2026-75793 Published : Sept. 6, 2026, 7:16 a.m. | 1 hour, 28 minutes ago Description : The SureCart WordPress plugin before 4.7.0 does not consult the site's user registration setting before creating WordPress accounts, allowing unauthenticated users to create an account and receive a logged-in session even when registration is disabled.
