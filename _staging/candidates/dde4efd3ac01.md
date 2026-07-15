---
id: dde4efd3ac01
candidate: true
title: 'CVE-2026-48808 - Twig: Sandbox property allowlist bypass via the `column` filter under `SourcePolicyInterface`'
date: 2026-07-14 22:56:21 +0000
categories:
- Daily Signal
tags:
- security-news
- advisory
- watchlist
severity: medium
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-48808
cve: CVE-2026-48808
cvss: 6.0
kev: false
ghsa: GHSA-h8vq-8gpg-mhcg
---

CVE ID : CVE-2026-48808 Published : July 14, 2026, 9:27 p.m. | 49 minutes ago Description : Twig is a template language for PHP. Prior to 3.27.0, the column filter passes the active sandbox state as a boolean but does not forward the current Source to SandboxExtension::checkPropertyAllowed(), so SourcePolicyInterface decisions are lost and a template author can read public or magic properties not allowed by the sandbox policy.
