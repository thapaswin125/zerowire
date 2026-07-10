---
title: "Tracking a ransomware intrusion from edge appliance to encryption"
date: 2026-07-08 09:00:00 +0000
categories: [Threat Research]
tags: [ransomware, vpn, lateral-movement, detection-engineering]
severity: high
mitre: [T1190, T1078, T1021.001, T1486, T1567.002]
related_detections:
  - name: Sigma, RDP lateral movement from VPN subnet
    url: https://github.com/SigmaHQ/sigma
  - name: Sigma, volume shadow copy deletion
    url: https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_shadow_copies_deletion.yml
sources:
  - name: CISA StopRansomware advisories
    url: https://www.cisa.gov/stopransomware
---

I walked through a composite intrusion chain built from several public
incident reports, because the pattern keeps repeating and the detections are
cheap to deploy.

## The chain

Initial access came through an unpatched edge VPN appliance (T1190). Within
hours the operators pivoted to valid domain accounts harvested from the
appliance itself (T1078), then moved laterally over RDP from the VPN subnet
into server VLANs (T1021.001). Staging and exfiltration went to consumer
cloud storage over HTTPS (T1567.002) roughly a day before encryption (T1486).

## What I would detect first

The highest-signal, lowest-effort detections in this chain:

1. RDP sessions originating from VPN or appliance management subnets. That
   traffic should not exist in most networks, so alert on any of it.
2. Volume shadow copy deletion. It fires late, but it fires reliably.
3. Outbound transfer volume to consumer cloud storage domains from servers.

## My takeaways

Edge appliances remain the front door. If I cannot patch within days, I plan
compensating controls around the assumption of compromise: segment the
appliance subnet, alert on authentication from it, and rehearse credential
rotation so it takes hours, not weeks.
