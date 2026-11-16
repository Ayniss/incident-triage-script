# Lightweight Incident Response Triage Script

A Python-based cross-platform utility designed to automate the collection of volatile system artifacts during the initial stages of an incident response (IR) process.

## Features
- **Cross-Platform Support:** Automatically detects OS (Windows, Linux, macOS) and executes relevant triage commands.
- **Artifacts Collected:**
  - System configuration and OS details
  - Running processes and services
  - Active network connections (`netstat`/`ss`)
  - Local users and current sessions
- **Secure Packaging:** Automatically compiles all collected logs into a timestamped `.zip` archive for safe transport and analysis.

## Usage
Run the script with administrative/root privileges to ensure full access to system diagnostic commands:
```bash
python triage.py
