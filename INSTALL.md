# SSH Plus Installation Guide

## Overview
SSH Plus is a comprehensive SSH management script that provides tools for network management, system administration, and user management. This guide will walk you through the complete installation process.

## System Requirements

### Supported Operating Systems
- **Debian 9+** (Recommended)
- **Ubuntu 18.04+** (Recommended)
- **CentOS 7+**
- Other Debian-based distributions

### Minimum Hardware Requirements
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 2GB free space minimum
- **CPU**: 1 core minimum
- **Network**: Internet connection required for installation

### Required Privileges
- Root access or sudo privileges
- SSH access to the server

## Pre-Installation Checklist

1. **Update your system**:
   ```bash
   apt update && apt upgrade -y
   ```

2. **Install essential tools**:
   ```bash
   apt install curl wget git -y
   ```

3. **Check system compatibility**:
   ```bash
   # Check OS version
   cat /etc/os-release
   
   # Check available space
   df -h
   
   # Check memory
   free -h
   ```

## Installation Methods

### Method 1: Direct Installation (Recommended)

1. **Download the installation script**:
   ```bash
   wget https://raw.githubusercontent.com/Farukbrowser/sshplus-new/main/Plus
   ```

2. **Make the script executable**:
   ```bash
   chmod +x Plus
   ```

3. **Run the installation**:
   ```bash
   ./Plus
   ```

### Method 2: One-Line Installation

```bash
bash <(curl -sL https://raw.githubusercontent.com/Farukbrowser/sshplus-new/main/Plus)
```

## Installation Process

### Step 1: Initial Setup
The installation script will:
- Display welcome message and warnings
- Request confirmation to proceed
- Validate the installation key
- Configure SSH settings

### Step 2: System Updates
The script automatically:
- Updates package repositories
- Installs visual enhancement tools (lolcat, figlet)
- Installs development tools (git, curl)
- Creates system directories

### Step 3: Python Environment Setup
The installer will:
- Install multiple Python versions (2.7, 3.6, 3.7, 3.8, 3.9)
- Configure Python alternatives system
- Install essential Python packages (speedtest-cli)
- Set up pip package managers

### Step 4: Package Installation
Essential packages installed:
- **System tools**: bc, screen, nano, unzip, lsof, netstat, net-tools
- **Network tools**: dos2unix, nload, jq, curl
- **Security tools**: firewalld, ufw
- **Text processing**: figlet, python3, python-pip

### Step 5: Firewall Configuration
The script configures firewall rules for:
- **HTTP**: Port 80/tcp
- **HTTPS**: Port 443/tcp
- **Custom services**: Ports 8989, 5454, 8888, 8080/tcp
- **DNS**: Port 7300/udp
- **Proxy**: Port 3128/tcp

### Step 6: Final Configuration
- Downloads and installs management scripts
- Sets up user database
- Configures bash profile with custom motd
- Creates menu shortcuts

## Post-Installation Setup

### 1. Access the Menu
After installation, access the main menu:
```bash
menu
```

### 2. Initial Configuration
1. **Set up users**: Use the user management options
2. **Configure protocols**: Set up V2Ray, Trojan-Go, or other protocols
3. **Network settings**: Configure ports and domains as needed

### 3. User Database
The script maintains user databases in:
- `/root/usuarios.db` - Main user database
- `/etc/SSHPlus/RegV2ray` - V2Ray user registry

## Verification

### Check Installation Status
```bash
# Verify SSH Plus is installed
ls -la /usr/share/.plus/

# Check if menu is accessible
which menu

# Verify services
systemctl status ssh
```

### Test Basic Functionality
```bash
# Access main menu
menu

# Check system information
cat /etc/IP

# Verify Python installation
python3 --version
```

## Troubleshooting Installation Issues

### Common Issues

1. **Permission Denied**:
   ```bash
   # Ensure you're running as root
   sudo su -
   ```

2. **Network Connection Issues**:
   ```bash
   # Test internet connectivity
   ping -c 4 google.com
   
   # Check DNS resolution
   nslookup github.com
   ```

3. **Package Installation Failures**:
   ```bash
   # Update package lists
   apt update
   
   # Fix broken packages
   apt --fix-broken install
   ```

4. **Key Validation Errors**:
   - Ensure you have a stable internet connection
   - Verify the installation source is correct
   - Check if firewall is blocking connections

### Log Files
Installation logs can be found in:
- System logs: `/var/log/syslog`
- SSH logs: `/var/log/auth.log`
- Installation timestamp: `/usr/share/.plus/.plus`

## Security Considerations

### Default Settings
- SSH port remains on default (22)
- Firewall rules are automatically configured
- User authentication is required for all operations

### Recommended Security Steps
1. **Change default SSH port**:
   ```bash
   nano /etc/ssh/sshd_config
   # Change Port 22 to desired port
   systemctl restart ssh
   ```

2. **Configure fail2ban** (optional):
   ```bash
   apt install fail2ban -y
   systemctl enable fail2ban
   ```

3. **Regular updates**:
   ```bash
   # Use the built-in update function
   menu -> System Options -> Update Script
   ```

## Next Steps

After successful installation:
1. Read the [Configuration Guide](CONFIG.md) for detailed setup options
2. Check the [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues
3. Explore the menu system to familiarize yourself with available features

## Support

For additional support:
- **Telegram**: @vrhostinggp
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check other .md files in this repository

---

**Note**: This installation will modify system configurations. Ensure you have backups of important data before proceeding.
