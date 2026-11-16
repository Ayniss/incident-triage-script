import os
import platform
import subprocess
import zipfile
import datetime
import shutil

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=10)
        return output
    except Exception as e:
        return f"Error executing {command}: {str(e)}"

def collect_triage_data():
    print("[*] Starting Incident Response Triage Collection...")
    
  
    triage_dir = f"triage_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(triage_dir, exist_ok=True)
    
    os_type = platform.system()
    print(("[+] Detected OS: " + os_type))
    
    reports = {}
    
    if os_type == "Windows":
        reports["system_info.txt"] = run_command("systeminfo")
        reports["running_processes.txt"] = run_command("tasklist /v")
        reports["network_connections.txt"] = run_command("netstat -ano")
        reports["active_users.txt"] = run_command("net user")
        reports["startup_programs.txt"] = run_command("wmic startup get caption,command")
    elif os_type == "Linux":
        reports["system_info.txt"] = run_command("uname -a && cat /etc/os-release")
        reports["running_processes.txt"] = run_command("ps auxf")
        reports["network_connections.txt"] = run_command("ss -tulnp || netstat -tulnp")
        reports["active_users.txt"] = run_command("cat /etc/passwd")
        reports["logged_in_users.txt"] = run_command("who -a")
    elif os_type == "Darwin": # macOS
        reports["system_info.txt"] = run_command("sw_vers && uname -a")
        reports["running_processes.txt"] = run_command("ps aux")
        reports["network_connections.txt"] = run_command("netstat -an")
        reports["active_users.txt"] = run_command("dscl . -list /Users")

    for filename, content in reports.items():
        file_path = os.path.join(triage_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Collected: {filename}")

    archive_name = f"{triage_dir}.zip"
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(triage_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), triage_dir))
                
    shutil.rmtree(triage_dir)
    print(f"[+] Triage complete! Archive created: {archive_name}")

if __name__ == "__main__":
    collect_triage_data()
