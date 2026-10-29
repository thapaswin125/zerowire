---
title: 'Inside KeyDrift: Analyzing historical UAT-11473 activity on Cisco SD-WAN'
date: 2026-10-29 10:59:25 +0000
categories:
- Threat Research
tags:
- auth-bypass
- apt
- security-news
severity: critical
must_know: true
sources:
- name: Cisco Talos Intelligence
  url: https://blog.talosintelligence.com/uat-11473-keydrift/
cve: CVE-2026-20127
cvss: 10.0
epss: 0.893
kev: true
mitre:
- T1556
---

Talos has identified UAT-11473, a highly sophisticated APT, who exploited CVE-2026-20127, an authentication bypass vulnerability in Cisco SD-WAN Catalyst Controller instances to bypass authentication and gain unauthorized access to affected systems to deploy KeyDrift.
