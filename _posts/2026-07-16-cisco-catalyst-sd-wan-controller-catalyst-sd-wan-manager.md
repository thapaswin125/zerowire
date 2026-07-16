---
title: Cisco Catalyst SD-WAN Controller, Catalyst SD-WAN Manager, and Catalyst SD-WAN Validator Authenticated Privilege Escalation Vulnerability
date: 2026-07-16 06:39:49 +0000
categories:
- Daily Signal
tags:
- privesc
- security-news
- advisory
severity: critical
must_know: true
sources:
- name: Cisco Security Advisories
  url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Catalyst%20SD-WAN%20Controller,%20Catalyst%20SD-WAN%20Manager,%20and%20Catalyst%20SD-WAN%20Validator%20Authenticated%20Privilege%20Escalation%20Vulnerability%26vs_k=1
cve: CVE-2026-20182
cvss: 10.0
epss: 0.885
kev: true
---

A vulnerability in the CLI of Cisco Catalyst SD-WAN Controller, formerly SD-WAN vSmart, Cisco Catalyst SD-WAN Manager, formerly SD-WAN vManage, and Cisco Catalyst SD-WAN Validator, formerly SD-WAN vBond, could allow an authenticated, local attacker to execute arbitrary commands as root by supplying a crafted file to the affected system. This vulnerability is due to insufficient validation of user-supplied input.
