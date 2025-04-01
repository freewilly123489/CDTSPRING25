# Service Saboteur Tool
## Author: William Faber  
**Email**: wmf1426@rit.edu
---
## Description
The **Service Saboteur** is a Python-based tool designed to sabotage critical services during red team operations, specifically targeting services such as **nginx**, **mysql**, and **samba**. The tool provides functionality to:
- **Stop and disable services**.
- **Inject invalid configurations** to cause disruptions.
- **Restore services** to their original state after sabotage.

This tool is designed to simulate attacks during the **CSEC 473 – Cyber Defense Techniques** competition, where the objective is to disrupt services and challenge the blue team's ability to react and recover.
---
## Features
- **Service Sabotage**: Stops and disables services like `nginx`, `mysql`, `samba`, and more.
- **Configuration Injection**: Injects invalid configurations to break the target services.
- **Service Restoration**: Restores services from their backup configurations.
- **Stealthy Execution**: Commands are executed quietly, with no output to the user unless verbose mode is enabled.
- **Flexible**: Can be extended to support additional services.
---
## Requirements
- **Python 3.x**
- **Administrative privileges** on the target system (to stop/start services and modify configurations)
---
## Installation
1. **Clone the repository** to your local machine:
   - https://github.com/CSEC-559-659-SPRING25/red-team-tool-systemsabotage
2. **Navigate to the directory** where the repository is cloned:
   - `cd red-team-tool-systemsabotage`
3. **Ensure Python 3 is installed**:
   - If it is not, you can install it via your package manager or from [python.org](https://www.python.org).
---
## Usage
### To Sabotage a Service:
Run the tool with the **`sabotage`** mode, followed by the service you want to target (e.g., `nginx`, `mysql`, `smb`).

Example:
```bash
python3 service_saboteur.py sabotage nginx
```

This will:
* Stop and disable the `nginx` service.
* Inject an invalid configuration into `/etc/nginx/nginx.conf`.
* Lock the configuration file, making it unreadable.

### To Restore a Service:
Run the tool with the `restore` mode, followed by the service you want to restore.

Example:
```bash
python3 service_saboteur.py restore smb
```

This will:
* Restore the service's configuration from its backup.
* Enable and start the service again.

### Verbose Mode:
You can enable **verbose output** to see detailed steps of what the script is doing by adding the `--verbose` flag.

Example:
```bash
python3 service_saboteur.py restore smb --verbose
```

This will print additional information about the restoration process.

---
## How to Use the Tool in a Red Team Competition
1. **Initiate a Reverse Shell** (using a C2 system like `SabTounge`).
2. **Use the** `TCP-CONNECT` command to connect to the target system.
3. **Execute the sabotage command** for a specific service.
4. **Observe the disruption** caused by the tool.
5. **Use the restore command** to restore the target system and services back to their original state.

---
## Customization and Extensibility
You can easily extend this tool by adding support for other services. Simply:
1. Add the service name and the path to its configuration file in the `config_paths` dictionary.
2. Ensure that the restore functionality handles the specific restart and enable commands for the new service.

For example, to add a new service:
```python
"new_service": "/etc/new_service/config.conf"
```

---
## Testing the Tool
To test the tool:
1. **Run the sabotage command** for a specific service.
2. **Verify the disruption** by checking if the service is still running (e.g., using `systemctl status` or checking service logs).
3. **Run the restore command** to ensure the service is restored successfully.
4. Optionally, test it in a **virtual machine environment** to avoid disrupting production systems.

---
## Important Notes
* **Use with caution**: This tool is intended for use in controlled environments (e.g., red team vs. blue team exercises). It may cause critical services to stop on the target machine.
* **Permissions**: Ensure you have the required administrative privileges on the target machine to stop and start services, as well as modify configuration files.
* **Backups**: Always ensure you have a proper backup of critical configurations before using the sabotage functionality.
