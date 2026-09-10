---
title: Cisco Secure Firewall Management Center Software Authentication Bypass Vulnerability
date: 2026-09-10 09:02:17 +0000
categories:
- Daily Signal
tags:
- auth-bypass
- edge-device
- privesc
severity: critical
must_know: true
sources:
- name: Cisco Security Advisories
  url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-onprem-fmc-authbypass-5JPp45V2?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Secure%20Firewall%20Management%20Center%20Software%20Authentication%20Bypass%20Vulnerability%26vs_k=1
cve: CVE-2026-20079
cvss: 10.0
epss: 0.387
kev: true
---

A vulnerability in the web interface of Cisco Secure Firewall Management Center (FMC) Software could allow an unauthenticated, remote attacker to bypass authentication and execute script files on an affected device to obtain root access to the underlying operating system. This vulnerability is due to an improper system process that is created at boot time.
