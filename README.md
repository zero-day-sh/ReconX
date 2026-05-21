# 🔍 RECONX

RECONX is a fast and lightweight web reconnaissance tool designed for subdomain enumeration, path scanning, and domain intelligence gathering.
It helps security learners and penetration testers discover exposed web assets and analyze target surfaces efficiently.

---

## ⚡ Features

* 🌐 Subdomain enumeration (multi-threaded)
* 📁 Directory / path brute-force scanner
* 🧠 Domain WHOIS information gathering
* 📡 IP resolution & reverse DNS lookup
* 📊 Status code detection & tracking (200, 301, 403, 404, 500…)
* ⚡ High-speed threaded scanning
* 💾 Auto-save results to file (`results.txt`)
* 🎨 Colored terminal interface (Rich UI)

---

## 🧰 Requirements

Make sure Python 3 is installed.

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements File

```txt
requests
rich
python-whois
```

---

## 🚀 Installation

### 📌 Linux / Kali / Ubuntu

```bash
git clone https://github.com/zero-day-sh/reconx.git
cd reconx
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the tool:

```bash
python3 main.py
```

---

## 📌 Menu

```
[1] Path Scan
[2] Subdomain Scan
[3] Domain Info
[4] Run All
[5] Exit
```

---

## 📊 Output

All results are saved automatically in:

```
results.txt
```

Example output:

```
200 | https://example.com/admin
403 | https://example.com/login
404 | https://example.com/test
```

---

## ⚙️ Configuration

Inside the script:

```python
THREADS = 100
TIMEOUT = 5
```

* Increase THREADS = faster scanning
* Lower TIMEOUT = more strict requests

---

## ⚠️ Disclaimer

This tool is created for **educational purposes only**.
Do not use it on systems you do not own or without permission.

The developer is not responsible for misuse.

---

## 👨‍💻 Author

* Created by: **nabil_jakoubi**
* Instagram: @nabil_jakoubi

---
