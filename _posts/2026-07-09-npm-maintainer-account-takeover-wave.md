---
title: "Phished npm maintainer accounts push malicious package updates"
date: 2026-07-09 14:05:00 +0000
categories: [Daily Signal]
tags: [supply-chain, npm, phishing, credential-theft]
severity: high
must_know: false
sources:
  - name: The Hacker News
    url: https://thehackernews.com/
  - name: GitHub Advisory Database
    url: https://github.com/advisories
---

Another wave of npm maintainer phishing is landing malicious versions of
mid-popularity packages. The lures spoof npm support emails and harvest 2FA
codes in real time. Payloads I looked at exfiltrate environment variables and
CI tokens on install. My take: pin dependencies with a lockfile, turn on
provenance checks where you can, and audit anything your pipelines pulled in
the last week that bumped a patch version without a changelog.
