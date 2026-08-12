---
id: 37c73ea4fcef
candidate: true
title: 'CVE-2026-68447 - drm/amdkfd: clamp v9 CRIU control stack checkpoint copy to BO size'
date: 2026-08-12 05:51:38 +0000
categories:
- Daily Signal
tags:
- linux
- security-news
- advisory
severity: info
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-68447
cve: CVE-2026-68447
kev: false
---

CVE ID : CVE-2026-68447 Published : Aug. 12, 2026, 1:17 a.m. | 4 hours, 11 minutes ago Description : In the Linux kernel, the following vulnerability has been resolved: drm/amdkfd: clamp v9 CRIU control stack checkpoint copy to BO size CRIU checkpoint copies the MQD control stack using cp_hqd_cntl_stack_size from hardware without bounding it to the allocated BO region.
