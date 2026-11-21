---
id: ef3cecb6fd50
candidate: true
title: Ruby Ships Fixes for 7 Flaws, Including Critical Ruby2Shell, Said to Hit Default Rails Apps Pre-Auth
date: 2026-11-21 12:51:52 +0000
categories:
- Daily Signal
tags:
- poc
- rce
- security-news
severity: info
must_know: false
sources:
- name: The Hacker News
  url: https://thehackernews.com/2026/11/ruby-releases-fixes-for-7-regex-and.html
---

Ruby contains seven memory-safety flaws in its regular expression engine and its string case-conversion code. For five of them, its maintainers say, proof-of-concept exploits, or PoCs, have shown that crafted input can run code on the machine. "We are aware of PoCs that prove some of them can be used to trigger remote code execution," the maintainers said.
