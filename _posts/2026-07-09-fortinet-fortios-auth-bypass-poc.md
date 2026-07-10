---
title: "Public PoC lands for FortiOS SSL-VPN authentication bypass"
date: 2026-07-09 08:20:00 +0000
categories: [Daily Signal]
tags: [vpn, auth-bypass, poc, edge-device]
severity: high
must_know: true
cve: CVE-2024-55591
cvss: 9.6
epss: 0.71
kev: true
sources:
  - name: Fortinet PSIRT
    url: https://www.fortiguard.com/psirt
  - name: BleepingComputer
    url: https://www.bleepingcomputer.com/
---

A working proof of concept is now public for the FortiOS and FortiProxy
authentication bypass in the Node.js websocket module. EPSS jumped sharply
after the PoC dropped, and this one is already in KEV. I would prioritize it
above almost everything else this week: check for rogue admin accounts and
unexpected automation stanzas in the config, because attackers were creating
persistence before the advisory even shipped.
