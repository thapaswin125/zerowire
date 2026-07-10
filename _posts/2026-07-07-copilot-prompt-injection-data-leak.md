---
title: "Indirect prompt injection exfiltrates data through AI coding assistants"
date: 2026-07-07 16:10:00 +0000
categories: [Daily Signal]
tags: [llm, prompt-injection, data-exfiltration, supply-chain]
severity: low
must_know: false
sources:
  - name: Project Zero
    url: https://googleprojectzero.blogspot.com/
---

New research shows hidden instructions in README files and code comments can
steer AI coding assistants into leaking repository contents through crafted
URLs in generated output. Nothing here is wormable, but it is a good reminder
that anything an assistant reads is input, including files an attacker
controls. I am tagging this low severity for now and watching for the first
in-the-wild campaign that chains it with CI access.
