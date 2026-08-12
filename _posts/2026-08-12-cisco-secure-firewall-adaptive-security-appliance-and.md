---
title: Cisco Secure Firewall Adaptive Security Appliance and Secure Firewall Threat Defense Software Remote Access SSL VPN Denial of Service Vulnerability
date: 2026-08-12 05:51:41 +0000
categories:
- Daily Signal
tags:
- vpn
- ddos
- edge-device
severity: critical
must_know: true
sources:
- name: Cisco Security Advisories
  url: https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-vpn-dos-dzv4mQFF?vs_f=Cisco%20Security%20Advisory%26vs_cat=Security%20Intelligence%26vs_type=RSS%26vs_p=Cisco%20Secure%20Firewall%20Adaptive%20Security%20Appliance%20and%20Secure%20Firewall%20Threat%20Defense%20Software%20Remote%20Access%20SSL%20VPN%20Denial%20of%20Service%20Vulnerability%26vs_k=1
cve: CVE-2026-20349
cvss: 8.6
kev: true
---

A vulnerability in the Remote Access SSL VPN service for Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause the device to reload unexpectedly, resulting in a denial of service (DoS) condition. This vulnerability is due to insufficient error checking when processing HTTP requests.
