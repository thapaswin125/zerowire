---
title: 'When LLM Gateways Go Wrong: Findings from LiteLLM'
date: 2026-10-14 09:37:31 +0000
categories:
- Threat Research
tags:
- llm
- security-news
- advisory
severity: high
must_know: false
sources:
- name: Check Point Research
  url: https://research.checkpoint.com/2026/when-llm-gateways-go-wrong-findings-from-litellm/
cve: CVE-2026-35029
cvss: 8.7
epss: 0.04
kev: false
---

TL;DR; Our security assessment of LiteLLM (v1.77.7), a widely used open-source LLM gateway, uncovered multiple high-impact vulnerabilities (tracked as CVE-2026-35029, CVE-2026-59823) which have been resolved as of LiteLLM version 1.83.9. The most significant issues stemmed from a missing authorization check on the /config/update endpoint, which allowed any authenticated user (including low-privileged accounts) to modify the […] The post When LLM ...
