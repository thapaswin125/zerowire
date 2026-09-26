---
title: MikroTrick Chain Let Attackers Take Over MikroTik Routers Without a Password or SSH Key
date: 2026-09-26 09:26:29 +0000
categories:
- Daily Signal
tags:
- security-news
- advisory
- watchlist
severity: critical
must_know: true
sources:
- name: The Hacker News
  url: https://thehackernews.com/2026/09/mikrotrick-chain-let-attackers-take.html
cve: CVE-2026-67279
cvss: 6.9
epss: 0.004
kev: true
---

Two MikroTik RouterOS SSH vulnerabilities chained together let attackers take full administrative control of Internet-exposed routers without a password, SSH key, or completed authentication. The chain, which CERT Polska calls MikroTrick, combines an SSH state-machine flaw (CVE-2026-67279) with an argument-injection bug in the RouterOS login process (CVE-2026-86060). Attack logs date to at
