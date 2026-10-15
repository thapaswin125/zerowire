---
title: Cisco Secure Email Gateway Arbitrary File Write Vulnerability
date: 2026-10-15 09:15:41 +0000
categories:
- Daily Signal
tags:
- email
- malware
- path-traversal
severity: critical
must_know: true
sources:
- name: Cisco Security Advisories
  url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-afw-zqYJkjxp?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Secure%20Email%20Gateway%20Arbitrary%20File%20Write%20Vulnerability%26vs_k=1
cve: CVE-2026-76519
cvss: 9.8
kev: true
---

A vulnerability in the Advanced Malware Protection (AMP) feature of Cisco Secure Email Gateway could allow an unauthenticated, remote attacker to write arbitrary files on the underlying operating system. This vulnerability is due to improper handling of email attachments when the file reputation service is enabled. An attacker could exploit this vulnerability by sending an email that contains a crafted attachment through an affected device.
