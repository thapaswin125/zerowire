---
id: 5e9fb36b9eac
candidate: true
title: CVE-2026-80071 - User Registration & Membership < 5.2.8 - Author+ Privilege Escalation to Administrator
date: 2026-09-13 09:38:14 +0000
categories:
- Daily Signal
tags:
- privesc
- wordpress
- security-news
severity: info
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-80071
cve: CVE-2026-80071
kev: false
---

CVE ID : CVE-2026-80071 Published : Sept. 13, 2026, 6:16 a.m. | 2 hours, 36 minutes ago Description : The User Registration & Membership WordPress plugin before 5.2.8 does not properly restrict who may author a membership plan or validate the plan a user attaches to their own account, allowing authenticated users with Author-level access and above to assign themselves an arbitrary role and escalate their privileges to Administrator.
