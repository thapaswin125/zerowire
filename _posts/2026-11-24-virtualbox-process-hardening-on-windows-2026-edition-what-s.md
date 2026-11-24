---
title: 'VirtualBox Process Hardening on Windows 2026 Edition: What’s a Single Bit Between Friends?'
date: 2026-11-24 15:03:16 +0000
categories:
- Threat Research
tags:
- privesc
- windows
- security-news
severity: info
must_know: false
sources:
- name: Google Project Zero
  url: https://projectzero.google/2026/11/virtualbox-process-hardening.html
mitre:
- T1068
- T1078.002
---

Back in 2017 I did some research into Oracle VirtualBox on Windows. Specifically I focussed on their mechanism to protect their VM processes from the user on the host. The protection was to gate who could open the kernel driver, which might allow for privilege escalation due to the way it was designed.
