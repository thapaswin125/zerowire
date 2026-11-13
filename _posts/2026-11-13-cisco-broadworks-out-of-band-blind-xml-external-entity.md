---
title: Cisco BroadWorks Out-of-Band Blind XML External Entity Injection Vulnerability
date: 2026-11-13 12:26:11 +0000
categories:
- Daily Signal
tags:
- security-news
- advisory
- watchlist
severity: critical
must_know: true
sources:
- name: Cisco Security Advisories
  url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-bworks-xxe-uwUd7CEt?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20BroadWorks%20Out-of-Band%20Blind%20XML%20External%20Entity%20Injection%20Vulnerability%26vs_k=1
cve: CVE-2026-20320
cvss: 7.5
kev: true
---

A vulnerability in the Open Client Interface (OCI) XML Parser of Cisco BroadWorks could allow an unauthenticated, remote attacker to read sensitive configuration information on an affected system. This vulnerability exists because XML entries are improperly parsed due to external entity resolution being allowed by default.
