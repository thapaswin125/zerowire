---
title: Cisco Catalyst SD-WAN Manager API Authentication Bypass Vulnerability
date: 2026-10-01 11:04:55 +0000
categories:
- Daily Signal
tags:
- auth-bypass
- security-news
- advisory
severity: critical
must_know: true
sources:
- name: Cisco Security Advisories
  url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-webauth-xr8beuuU?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Catalyst%20SD-WAN%20Manager%20API%20Authentication%20Bypass%20Vulnerability%26vs_k=1
cve: CVE-2026-76504
cvss: 9.8
kev: true
---

A vulnerability in the API session-based authentication management of Cisco Catalyst SD-WAN Manager could allow an unauthenticated, remote attacker to access an affected system with privileges of the admin user. This vulnerability is due to improper handling of URI encoding in an HTTP request, which allows the request to bypass an authentication rule that is intended to restrict access to a specific API endpoint.
