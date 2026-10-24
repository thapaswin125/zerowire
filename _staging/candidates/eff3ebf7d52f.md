---
id: eff3ebf7d52f
candidate: true
title: New QPACK Flaws Can Crash HTTP/3 Servers, Trigger Up to 4,000-Fold Memory Amplification
date: 2026-10-24 08:58:36 +0000
categories:
- Daily Signal
tags:
- poc
- security-news
- advisory
severity: info
must_know: false
sources:
- name: The Hacker News
  url: https://thehackernews.com/2026/10/new-qpack-flaws-can-crash-http3-servers.html
---

A remote attacker who has not logged in can crash many HTTP/3 web servers with a single connection, security firm FoxIO disclosed, releasing working proof-of-concept code. By sending a small batch of compressed HTTP headers that expands in memory to a much larger set, the attacker can force the server to use thousands of times more memory than it received, enough to run a default server
