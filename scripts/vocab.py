"""Controlled vocabulary for rules-based triage.

TAG_KEYWORDS maps a canonical tag to the keywords that imply it. Matching is
case-insensitive whole-word matching against the candidate title plus body.
MITRE_MAP maps a canonical tag to ATT&CK technique IDs, used only for
threat-research candidates. RESEARCH_SOURCES marks feeds whose items default
to the Threat Research category.

Enrichment values (cvss, epss, kev, severity) are never set from here; those
come only from scripts/enrich.py.
"""

TAG_KEYWORDS = {
    "zero-day": ["zero-day", "zero day", "0day", "0-day", "in the wild", "actively exploited"],
    "ransomware": ["ransomware", "lockbit", "blackcat", "alphv", "akira", "ransomhub", "extortion", "double extortion"],
    "supply-chain": ["supply chain", "supply-chain", "dependency confusion", "typosquat", "malicious package", "software supply", "build pipeline", "third-party library"],
    "rce": ["remote code execution", "rce", "arbitrary code execution", "command injection", "code injection", "unauthenticated attacker"],
    "privesc": ["privilege escalation", "privesc", "elevation of privilege", "eop", "root access", "system privileges"],
    "auth-bypass": ["authentication bypass", "auth bypass", "bypass authentication", "improper authentication", "missing authentication"],
    "sqli": ["sql injection", "sqli"],
    "xss": ["cross-site scripting", "xss"],
    "ssrf": ["server-side request forgery", "ssrf"],
    "deserialization": ["deserialization", "insecure deserialization", "unsafe deserialization"],
    "path-traversal": ["path traversal", "directory traversal", "arbitrary file read", "arbitrary file write"],
    "memory-corruption": ["buffer overflow", "stack overflow", "heap overflow", "use-after-free", "use after free", "out-of-bounds", "memory corruption"],
    "phishing": ["phishing", "spearphishing", "spear phishing", "credential harvesting", "smishing", "quishing", "business email compromise", "bec"],
    "credential-theft": ["infostealer", "info-stealer", "credential theft", "stolen credentials", "password stealer", "session hijacking", "token theft", "stealer log"],
    "malware": ["malware", "trojan", "backdoor", "loader", "botnet", "rootkit", "implant", "rat "],
    "apt": ["apt", "nation-state", "state-sponsored", "threat actor", "espionage", "lazarus", "apt28", "apt29", "volt typhoon", "salt typhoon"],
    "ddos": ["ddos", "denial of service", "denial-of-service", "amplification attack"],
    "data-breach": ["data breach", "data leak", "records exposed", "database exposed", "breach notification"],
    "data-exfiltration": ["exfiltration", "exfiltrate", "data theft", "stolen data"],
    "vpn": ["vpn", "connect secure", "globalprotect", "anyconnect", "fortios ssl-vpn", "pulse secure", "ssl vpn", "ssl-vpn"],
    "edge-device": ["firewall", "gateway appliance", "edge device", "load balancer", "citrix netscaler", "big-ip", "ivanti", "fortinet", "fortios", "pan-os", "sonicwall"],
    "aws": ["aws", "amazon web services", "s3 bucket", "iam role", "lambda"],
    "azure": ["azure", "entra", "microsoft 365", "m365", "office 365", "sharepoint online", "exchange online"],
    "gcp": ["gcp", "google cloud"],
    "cloud": ["cloud", "saas", "multi-tenant", "cloud misconfiguration"],
    "kubernetes": ["kubernetes", "k8s", "kubectl", "ingress-nginx", "containerd", "cluster admin"],
    "container": ["container escape", "docker", "container image", "registry poisoning"],
    "linux": ["linux", "glibc", "systemd", "kernel vulnerability", "sudo"],
    "windows": ["windows", "active directory", "ntlm", "kerberos", "domain controller", "group policy"],
    "macos": ["macos", "os x", "gatekeeper", "xprotect"],
    "android": ["android", "google play", "play store"],
    "ios": ["ios ", "iphone", "imessage", "webkit"],
    "browser": ["chrome", "firefox", "chromium", "browser extension", "v8 engine"],
    "npm": ["npm", "node package", "javascript package"],
    "pypi": ["pypi", "python package"],
    "git": ["github actions", "gitlab", "git repository", "repojacking"],
    "llm": ["llm", "large language model", "chatgpt", "copilot", "generative ai", "ai model", "ai agent", "mcp server"],
    "prompt-injection": ["prompt injection", "jailbreak the model", "indirect prompt"],
    "ot-ics": ["scada", "industrial control", "ics", "plc", "operational technology", "modbus"],
    "iot": ["iot", "firmware vulnerability", "router vulnerability", "ip camera", "nvr"],
    "email": ["exchange server", "smtp", "email gateway", "proofpoint", "mimecast"],
    "poc": ["proof of concept", "proof-of-concept", "poc released", "public exploit", "exploit code", "metasploit module"],
    "patch": ["patch tuesday", "security update", "hotfix", "patched", "fix released", "security advisory"],
    "kev": ["known exploited vulnerabilities", "kev catalog", "cisa kev"],
    "mfa": ["mfa", "multi-factor", "2fa", "passkey", "mfa fatigue", "aitm", "adversary-in-the-middle"],
    "insider-threat": ["insider threat", "rogue employee", "north korean it worker"],
    "cryptomining": ["cryptomining", "cryptojacking", "coin miner", "xmrig"],
    "wordpress": ["wordpress", "wp plugin", "woocommerce"],
    "vmware": ["vmware", "esxi", "vcenter", "vsphere", "hypervisor escape"],
    "firmware": ["uefi", "bios", "bootkit", "secure boot bypass", "baseboard management", "bmc"],
    "dns": ["dns hijacking", "dns poisoning", "domain hijacking", "dangling dns"],
    "lateral-movement": ["lateral movement", "pass-the-hash", "pass the hash", "rdp brute", "psexec", "wmi execution"],
}

# Tag to ATT&CK technique IDs. Applied only to Threat Research candidates,
# only for tags that actually matched.
MITRE_MAP = {
    "zero-day": ["T1190", "T1203"],
    "rce": ["T1190"],
    "privesc": ["T1068"],
    "auth-bypass": ["T1556"],
    "phishing": ["T1566"],
    "credential-theft": ["T1555", "T1539"],
    "malware": ["T1105"],
    "ransomware": ["T1486", "T1490"],
    "data-exfiltration": ["T1567"],
    "data-breach": ["T1530"],
    "supply-chain": ["T1195"],
    "lateral-movement": ["T1021"],
    "ddos": ["T1498"],
    "vpn": ["T1133"],
    "edge-device": ["T1190"],
    "kubernetes": ["T1610"],
    "container": ["T1611"],
    "windows": ["T1078.002"],
    "cloud": ["T1078.004"],
    "mfa": ["T1621", "T1557"],
    "prompt-injection": ["T1204"],
    "cryptomining": ["T1496"],
    "dns": ["T1584.001"],
    "firmware": ["T1542"],
    "insider-threat": ["T1078"],
    "deserialization": ["T1190"],
    "sqli": ["T1190"],
    "ssrf": ["T1190"],
    "path-traversal": ["T1190"],
    "memory-corruption": ["T1203"],
}

# Source names (as written in rss-sources.md) whose items I treat as
# Threat Research candidates instead of Daily Signal.
RESEARCH_SOURCES = {
    "Google Project Zero",
    "GitHub Security Blog",
}

# Cap and floor for how many tags rules-based triage assigns.
MIN_TAGS = 3
MAX_TAGS = 5

# Fallback tags used to pad up to MIN_TAGS when few keywords match.
FALLBACK_TAGS = ["security-news", "advisory", "watchlist"]
