---
id: bd0e1be2ec6d
candidate: true
title: 'CVE-2026-42049 - jadx: RCE Via Groovy Code Injection in Gradle Export'
date: 2026-07-14 22:56:21 +0000
categories:
- Daily Signal
tags:
- rce
- android
- security-news
severity: high
must_know: false
sources:
- name: Recent CVEs (CVEFeed mirror of NVD)
  url: https://cvefeed.io/vuln/detail/CVE-2026-42049
cve: CVE-2026-42049
cvss: 8.4
kev: false
---

CVE ID : CVE-2026-42049 Published : July 14, 2026, 9:44 p.m. | 32 minutes ago Description : jadx is a Dex to Java decompiler. Prior to 1.5.6, jadx inserts the android:versionName value from an AndroidManifest into the generated app/build.gradle Groovy template without proper sanitization when exporting a decompiled APK as an Android Gradle project.
