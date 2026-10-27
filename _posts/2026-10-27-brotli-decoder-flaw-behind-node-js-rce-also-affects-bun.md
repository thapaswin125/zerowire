---
title: Brotli Decoder Flaw Behind Node.js RCE Also Affects Bun, Python and Other Widely Used Software
date: 2026-10-27 09:55:47 +0000
categories:
- Daily Signal
tags:
- rce
- security-news
- advisory
severity: critical
must_know: false
sources:
- name: The Hacker News
  url: https://thehackernews.com/2026/10/brotli-decoder-flaw-behind-nodejs-rce.html
cve: CVE-2026-111497
cvss: 9.2
kev: false
---

A memory-corruption flaw in Google's Brotli decoder sits in many programs that unpack Brotli-compressed data, among them Bun, Microsoft's .NET, the Python Brotli and brotlicffi packages, and Envoy proxies set up to decompress Brotli. Tracked as CVE-2026-111497, the flaw allows crafted compressed data to overwrite past the end of a buffer and corrupt a program's memory,
