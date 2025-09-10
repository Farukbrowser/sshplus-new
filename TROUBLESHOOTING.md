# SSH Plus Troubleshooting Guide

## Overview
This guide provides solutions to common issues encountered when using SSH Plus. Issues are organized by category for easy navigation.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Connection Problems](#connection-problems)
3. [User Management Issues](#user-management-issues)
4. [Protocol-Specific Problems](#protocol-specific-problems)
5. [System Performance Issues](#system-performance-issues)
6. [Firewall and Network Issues](#firewall-and-network-issues)
7. [Database and File Issues](#database-and-file-issues)
8. [Service Management Problems](#service-management-problems)

---

## Installation Issues

### Issue: "Key Invalid" Error During Installation
**Symptoms**: Installation fails with "INVALID KEY!" message

**Solutions**:
1. **Check internet connection**:
   ```bash
   ping -c 4 google.com
   curl -I https://github.com
   ```

2. **Verify installation source**:
   ```bash
   # Re-download the installation script
   rm -f Plus
   wget https://raw.githubusercontent.com/Farukbrowser/sshplus-new/main/Plus
   chmod +x Plus
   ```

3. **Clear temporary files**:
   ```bash
   rm -rf /tmp/*
   rm -rf $HOME/fim
   ```

### Issue: Permission Denied During Installation
**Symptoms**: Script fails with permission errors

**Solutions**:
1. **Run as root**:
   ```bash
   sudo su -
   ./Plus
   ```

2. **Check file permissions**:
   ```bash
   chmod +x Plus
   ls -la Plus
   ```

### Issue: Package Installation Failures
**Symptoms**: APT errors during package installation

**Solutions**:
1. **Update package lists**:
   ```bash
   apt update
   apt upgrade -y
   ```

2. **Fix broken packages**:
   ```bash
   apt --fix-broken install
   dpkg --configure -a
   ```

3. **Clear APT cache**:
   ```bash
   apt clean
   apt autoclean
   ```

---

## Connection Problems

### Issue: SSH Connection Refused
**Symptoms**: Cannot connect via SSH after installation

**Solutions**:
1. **Check SSH service status**:
   ```bash
   systemctl status ssh
   systemctl restart ssh
   ```

2. **Verify SSH configuration**:
   ```bash
   nano /etc/ssh/sshd_config
   # Check Port, PermitRootLogin, PasswordAuthentication
   ```

3. **Check firewall rules**:
   ```bash
   ufw status
   iptables -L
   ```

### Issue: V2Ray/Trojan Connection Failures
**Symptoms**: Proxy connections not working

**Solutions**:
1. **Check service status**:
   ```bash
   systemctl status v2ray
   systemctl status trojan-go
   ```

2. **Verify configuration files**:
   ```bash
   # V2Ray config
   cat /etc/v2ray/config.json
   
   # Trojan-Go config
   cat /usr/local/etc/trojan-go/config.json
   ```

3. **Check port availability**:
   ```bash
   netstat -tlnp | grep :443
   netstat -tlnp | grep :80
   ```

---

## User Management Issues

### Issue: Cannot Create New Users
**Symptoms**: User creation fails or users don't appear in list

**Solutions**:
1. **Check user database**:
   ```bash
   cat /root/usuarios.db
   ls -la /root/usuarios.db
   ```

2. **Verify system users**:
   ```bash
   cat /etc/passwd | grep -v nologin
   ```

3. **Fix database permissions**:
   ```bash
   chmod 644 /root/usuarios.db
   chown root:root /root/usuarios.db
   ```

### Issue: User Limit Not Working
**Symptoms**: Users can connect beyond set limits

**Solutions**:
1. **Check limiter service**:
   ```bash
   ps aux | grep limiter
   ```

2. **Restart monitoring services**:
   ```bash
   pkill -f limiter
   /bin/limiter
   ```

3. **Verify user database format**:
   ```bash
   # Format should be: username limit
   head -5 /root/usuarios.db
   ```

---

## Protocol-Specific Problems

### V2Ray Issues

#### Issue: V2Ray Service Won't Start
**Solutions**:
1. **Check configuration syntax**:
   ```bash
   v2ray -test -config /etc/v2ray/config.json
   ```

2. **Review logs**:
   ```bash
   journalctl -u v2ray -f
   ```

3. **Reinstall V2Ray**:
   ```bash
   # From SSH Plus menu
   menu -> V2Ray Manager -> Uninstall V2Ray
   menu -> V2Ray Manager -> Install V2Ray
   ```

#### Issue: WebSocket Connection Problems
**Solutions**:
1. **Check Nginx/Apache configuration**:
   ```bash
   nginx -t
   systemctl status nginx
   ```

2. **Verify domain resolution**:
   ```bash
   nslookup yourdomain.com
   ```

### Trojan-Go Issues

#### Issue: Certificate Problems
**Solutions**:
1. **Check certificate validity**:
   ```bash
   openssl x509 -in /path/to/cert.pem -text -noout
   ```

2. **Renew certificates**:
   ```bash
   certbot renew
   ```

---

## System Performance Issues

### Issue: High CPU Usage
**Symptoms**: System becomes slow or unresponsive

**Solutions**:
1. **Identify resource-heavy processes**:
   ```bash
   top
   htop
   ps aux --sort=-%cpu | head -10
   ```

2. **Check for memory leaks**:
   ```bash
   free -h
   cat /proc/meminfo
   ```

3. **Optimize system**:
   ```bash
   # From SSH Plus menu
   menu -> System Options -> Optimize System
   ```

### Issue: Disk Space Full
**Symptoms**: "No space left on device" errors

**Solutions**:
1. **Check disk usage**:
   ```bash
   df -h
   du -sh /* | sort -hr
   ```

2. **Clean temporary files**:
   ```bash
   apt autoremove -y
   apt autoclean
   rm -rf /tmp/*
   journalctl --vacuum-time=7d
   ```

3. **Clean log files**:
   ```bash
   find /var/log -name "*.log" -type f -size +100M
   > /var/log/syslog
   > /var/log/auth.log
   ```

---

## Firewall and Network Issues

### Issue: Ports Not Accessible
**Symptoms**: Services running but not reachable from outside

**Solutions**:
1. **Check firewall status**:
   ```bash
   ufw status verbose
   firewall-cmd --list-all
   ```

2. **Open required ports**:
   ```bash
   # UFW
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   
   # Firewalld
   firewall-cmd --permanent --add-port=80/tcp
   firewall-cmd --permanent --add-port=443/tcp
   firewall-cmd --reload
   ```

3. **Check iptables rules**:
   ```bash
   iptables -L -n
   iptables -t nat -L -n
   ```

### Issue: DNS Resolution Problems
**Solutions**:
1. **Test DNS resolution**:
   ```bash
   nslookup google.com
   dig google.com
   ```

2. **Check DNS configuration**:
   ```bash
   cat /etc/resolv.conf
   ```

3. **Use alternative DNS**:
   ```bash
   echo "nameserver 8.8.8.8" > /etc/resolv.conf
   echo "nameserver 8.8.4.4" >> /etc/resolv.conf
   ```

---

## Database and File Issues

### Issue: Corrupted User Database
**Symptoms**: Users missing or duplicate entries

**Solutions**:
1. **Backup and clean database**:
   ```bash
   cp /root/usuarios.db /root/usuarios.db.backup
   sort /root/usuarios.db | uniq > /root/usuarios.db.tmp
   mv /root/usuarios.db.tmp /root/usuarios.db
   ```

2. **Recreate database**:
   ```bash
   # Backup existing users
   awk -F : '$3 >= 500 { print $1 " 1" }' /etc/passwd | grep -v '^nobody' > /root/usuarios.db
   ```

### Issue: Configuration Files Missing
**Solutions**:
1. **Restore from backup**:
   ```bash
   # Check for backups
   find /root -name "*.backup" -o -name "*.bak"
   ```

2. **Reinstall SSH Plus**:
   ```bash
   # Download fresh installation
   wget https://raw.githubusercontent.com/Farukbrowser/sshplus-new/main/Plus
   chmod +x Plus
   ./Plus
   ```

---

## Service Management Problems

### Issue: Services Not Starting Automatically
**Solutions**:
1. **Enable services**:
   ```bash
   systemctl enable ssh
   systemctl enable v2ray
   systemctl enable nginx
   ```

2. **Check service dependencies**:
   ```bash
   systemctl list-dependencies ssh
   ```

3. **Review service logs**:
   ```bash
   journalctl -u ssh -n 50
   journalctl -u v2ray -n 50
   ```

---

## Advanced Troubleshooting

### Collecting System Information
```bash
# System info script
echo "=== System Information ==="
uname -a
cat /etc/os-release
echo "\n=== Memory Usage ==="
free -h
echo "\n=== Disk Usage ==="
df -h
echo "\n=== Network Interfaces ==="
ip addr show
echo "\n=== Active Services ==="
systemctl list-units --type=service --state=active
echo "\n=== SSH Plus Status ==="
ls -la /usr/share/.plus/
cat /usr/share/.plus/.plus 2>/dev/null
```

### Log Analysis
```bash
# Check recent errors
journalctl --since "1 hour ago" --priority=err

# Monitor real-time logs
tail -f /var/log/syslog /var/log/auth.log

# Search for specific errors
grep -i "error\|failed\|denied" /var/log/syslog | tail -20
```

### Network Diagnostics
```bash
# Test connectivity
ping -c 4 8.8.8.8
traceroute google.com

# Check listening ports
netstat -tlnp
ss -tlnp

# Test specific ports
telnet localhost 22
nc -zv localhost 80
```

---

## Getting Help

If you cannot resolve your issue using this guide:

1. **Gather information**:
   - Run the system information script above
   - Note exact error messages
   - Document steps that led to the issue

2. **Check logs**:
   - System logs: `/var/log/syslog`
   - SSH logs: `/var/log/auth.log`
   - Service-specific logs via `journalctl`

3. **Contact support**:
   - **Telegram**: @ceofarukbrowser
   - **GitHub Issues**: Create detailed bug reports
   - **Community forums**: Search for similar issues

4. **Provide details**:
   - Operating system and version
   - SSH Plus version/installation date
   - Complete error messages
   - Steps to reproduce the issue

---

**Remember**: Always backup important data before making system changes or reinstalling components.