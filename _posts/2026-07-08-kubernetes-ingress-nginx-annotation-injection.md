---
title: "ingress-nginx annotation injection allows cluster secret theft"
date: 2026-07-08 11:30:00 +0000
categories: [Daily Signal]
tags: [kubernetes, privesc, cloud, rce]
severity: medium
must_know: false
cve: CVE-2025-1974
cvss: 9.8
epss: 0.28
kev: false
sources:
  - name: Kubernetes Security Announce
    url: https://groups.google.com/g/kubernetes-security-announce
---

I keep seeing clusters where the ingress-nginx admission webhook is reachable
from pods that should never talk to it. The annotation injection family of
bugs lets an attacker with the ability to create an Ingress object smuggle
configuration into the controller and read secrets across namespaces. Patch
the controller, and also network-policy the admission webhook so only the API
server can reach it. Severity here reflects my exposure read, not the raw
CVSS: exploitation needs in-cluster access first.
