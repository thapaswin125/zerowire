---
id: ac3cddb8c967
candidate: true
title: CVE-2026-81343 - Frontend Admin by DynamiApps <= 3.29.13 - Unauthenticated ACF Options Page Field Update via Form Submission
date: 2026-10-17 08:41:19 +0000
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
  url: https://cvefeed.io/vuln/detail/CVE-2026-81343
cve: CVE-2026-81343
kev: false
---

CVE ID : CVE-2026-81343 Published : Oct. 17, 2026, 6:16 a.m. | 2 hours, 24 minutes ago Description : The ACF Frontend Admin by DynamiApps WordPress plugin through 3.29.13 does not perform a capability check on one of its form-submission actions before writing submitted values into the site's global ACF options store, allowing unauthenticated visitors to overwrite site-wide option values via a public form.
