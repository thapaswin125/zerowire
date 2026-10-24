---
id: eebdb3f4f6ae
candidate: true
title: Two CVSS 9.0 Linux KSMBD RCE Flaws Disclosed on Public Mailing Lists Before Kernel Fixes
date: 2026-10-24 08:58:36 +0000
categories:
- Daily Signal
tags:
- rce
- linux
- zero-day
severity: info
must_know: false
sources:
- name: The Hacker News
  url: https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html
---

Linux servers running KSMBD, the kernel's built-in SMB server, are exposed to two publicly reported remote code execution flaws rated 9.0 by Trend Micro's Zero Day Initiative, with no fix yet in the mainline kernel. One of them, ZDI-CAN-33774, can be triggered before any network authentication. The other, ZDI-CAN-33549, requires the SMB Direct transport and an RDMA-capable network
