---
title: GitLab CVSS 10 File-Read Flaw Draws In-the-Wild Probes After Disclosure
date: 2026-09-12 08:43:27 +0000
categories:
- Daily Signal
tags:
- git
- path-traversal
- security-news
severity: critical
must_know: true
sources:
- name: The Hacker News
  url: https://thehackernews.com/2026/09/gitlab-cvss-10-file-read-flaw-draws-in.html
cve: CVE-2026-85706
cvss: 10.0
kev: true
---

GitLab has released patches to address multiple flaws, including a maximum-severity security vulnerability that has witnessed in-the-wild probes within hours of public disclosure. The vulnerability in question is CVE-2026-85706 (CVSS score: 10.0), a path traversal issue in the repository commits API that could allow an unauthenticated user to read arbitrary files from the GitLab server under
