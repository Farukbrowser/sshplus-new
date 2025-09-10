# SSH Plus Configuration Guide

## Overview
This guide provides detailed information about all configuration options available in SSH Plus, their effects, and recommended settings for different use cases.

## Table of Contents
1. [System Configuration](#system-configuration)
2. [SSH Configuration](#ssh-configuration)
3. [User Management Configuration](#user-management-configuration)
4. [Protocol Configurations](#protocol-configurations)
5. [Network and Firewall Settings](#network-and-firewall-settings)
6. [Performance Optimization](#performance-optimization)
7. [Security Settings](#security-settings)
8. [Monitoring and Logging](#monitoring-and-logging)

---

## System Configuration

### Core System Files

#### `/usr/share/.plus/.plus`
**Purpose**: Main SSH Plus configuration and status file

**Format**:
```
SSHPLUS-MANAGER (Version)
Installation Date: DD/MM/YYYY
License Status: ACTIVE/INACTIVE
```

**Effects**:
- Controls SSH Plus menu access
- Validates installation integrity
- Tracks license status

**Recommended Settings**:
- Keep file permissions at `644`
- Do not modify manually
- Backup before system updates

#### `/root/usuarios.db`
**Purpose**: User database with connection limits

**Format**:
```
username1 limit1
username2 limit2
```

**Configuration Options**:
- **Username**: System username (must exist in `/etc/passwd`)
- **Limit**: Maximum concurrent connections (1-999)

**Effects**:
- Controls user connection limits
- Used by monitoring scripts
- Affects user creation/deletion

**Recommended Settings**:
```bash
# Standard users
user1 2
user2 1

# Premium users
premium1 5
premium2 10

# Test users
test1 1
```

---

## SSH Configuration

### `/etc/ssh/sshd_config`
**Purpose**: Main SSH daemon configuration

#### Key Configuration Options:

##### Port Configuration
```bash
Port 22
# Additional ports
Port 2222
Port 443
```
**Effects**:
- Changes SSH listening ports
- Affects firewall rules
- Impacts client connections

**Recommendations**:
- Use non-standard ports for security
- Ensure firewall allows configured ports
- Document port changes for users

##### Authentication Settings
```bash
PasswordAuthentication yes
PubkeyAuthentication yes
PermitRootLogin yes
```
**Effects**:
- `PasswordAuthentication`: Enables/disables password login
- `PubkeyAuthentication`: Enables/disables key-based auth
- `PermitRootLogin`: Controls root access

**Security Recommendations**:
```bash
# High security
PasswordAuthentication no
PubkeyAuthentication yes
PermitRootLogin no

# Balanced security
PasswordAuthentication yes
PubkeyAuthentication yes
PermitRootLogin yes

# Development/testing
PasswordAuthentication yes
PubkeyAuthentication yes
PermitRootLogin yes
```

##### Connection Limits
```bash
MaxAuthTries 3
MaxSessions 10
MaxStartups 10:30:100
```
**Effects**:
- `MaxAuthTries`: Failed login attempts before disconnect
- `MaxSessions`: Concurrent sessions per connection
- `MaxStartups`: Concurrent unauthenticated connections

**Tuning Guidelines**:
```bash
# Low-resource servers
MaxSessions 5
MaxStartups 5:30:50

# High-capacity servers
MaxSessions 20
MaxStartups 20:30:200
```

---

## User Management Configuration

### User Creation Settings

#### Default Shell Configuration
```bash
# In user creation scripts
DEFAULT_SHELL="/bin/false"
ALLOWED_SHELLS=("/bin/bash" "/bin/sh" "/bin/false")
```
**Effects**:
- Controls user shell access
- Affects SSH tunneling capabilities
- Impacts security posture

**Options**:
- `/bin/false`: SSH tunneling only (most secure)
- `/bin/bash`: Full shell access
- `/bin/sh`: Basic shell access

#### Password Policy
```bash
# Password generation settings
PASSWORD_LENGTH=8
USE_SPECIAL_CHARS=true
AUTO_GENERATE=true
```
**Effects**:
- Determines password complexity
- Affects user security
- Impacts user experience

**Recommendations**:
```bash
# High security
PASSWORD_LENGTH=12
USE_SPECIAL_CHARS=true

# Standard security
PASSWORD_LENGTH=8
USE_SPECIAL_CHARS=true

# Basic security
PASSWORD_LENGTH=6
USE_SPECIAL_CHARS=false
```

### Connection Monitoring

#### Limiter Configuration
```bash
# Connection limit enforcement
CHECK_INTERVAL=30  # seconds
KILL_EXCESS=true
LOG_VIOLATIONS=true
```
**Effects**:
- `CHECK_INTERVAL`: How often to check connections
- `KILL_EXCESS`: Automatically disconnect excess connections
- `LOG_VIOLATIONS`: Record limit violations

**Performance Impact**:
- Lower intervals = more CPU usage, better enforcement
- Higher intervals = less CPU usage, delayed enforcement

---

## Protocol Configurations

### V2Ray Configuration

#### `/etc/v2ray/config.json`
**Purpose**: V2Ray proxy server configuration

##### Basic Structure
```json
{
  "log": {
    "loglevel": "warning"
  },
  "inbounds": [
    {
      "port": 80,
      "protocol": "vmess",
      "settings": {
        "clients": []
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom"
    }
  ]
}
```

##### Key Configuration Options:

###### Logging
```json
"log": {
  "loglevel": "warning",
  "access": "/var/log/v2ray/access.log",
  "error": "/var/log/v2ray/error.log"
}
```
**Options**: `debug`, `info`, `warning`, `error`, `none`
**Effects**:
- `debug`: Detailed logging (high disk usage)
- `warning`: Balanced logging (recommended)
- `none`: No logging (best performance)

###### Inbound Protocols
```json
// VMess Protocol
{
  "port": 80,
  "protocol": "vmess",
  "settings": {
    "clients": [
      {
        "id": "uuid-here",
        "level": 1,
        "alterId": 64
      }
    ]
  }
}

// WebSocket Transport
{
  "streamSettings": {
    "network": "ws",
    "wsSettings": {
      "path": "/path",
      "headers": {
        "Host": "domain.com"
      }
    }
  }
}
```

**Protocol Comparison**:
- **VMess**: Balanced security and performance
- **VLESS**: Better performance, newer protocol
- **Trojan**: Good for bypassing detection

###### Transport Options
```json
// TCP (fastest)
"streamSettings": {
  "network": "tcp"
}

// WebSocket (HTTP compatible)
"streamSettings": {
  "network": "ws",
  "wsSettings": {
    "path": "/ws"
  }
}

// HTTP/2 (multiplexing)
"streamSettings": {
  "network": "h2",
  "httpSettings": {
    "host": ["domain.com"]
  }
}
```

**Performance Ranking**:
1. TCP (fastest, least compatible)
2. WebSocket (balanced)
3. HTTP/2 (slower, best compatibility)

### Trojan-Go Configuration

#### `/usr/local/etc/trojan-go/config.json`
**Purpose**: Trojan-Go proxy server configuration

##### Basic Structure
```json
{
  "run_type": "server",
  "local_addr": "0.0.0.0",
  "local_port": 443,
  "remote_addr": "127.0.0.1",
  "remote_port": 80,
  "password": ["password1", "password2"],
  "ssl": {
    "cert": "/path/to/cert.pem",
    "key": "/path/to/key.pem"
  }
}
```

##### Key Configuration Options:

###### SSL/TLS Settings
```json
"ssl": {
  "cert": "/etc/letsencrypt/live/domain.com/fullchain.pem",
  "key": "/etc/letsencrypt/live/domain.com/privkey.pem",
  "sni": "domain.com",
  "alpn": ["http/1.1"],
  "reuse_session": true,
  "session_ticket": false
}
```
**Effects**:
- `sni`: Server Name Indication for domain validation
- `alpn`: Application Layer Protocol Negotiation
- `reuse_session`: Improves performance, may affect security

###### WebSocket Support
```json
"websocket": {
  "enabled": true,
  "path": "/trojan",
  "host": "domain.com"
}
```
**Benefits**:
- Better firewall traversal
- HTTP-compatible traffic
- CDN compatibility

### OpenVPN Configuration

#### Client Configuration Generation
**File**: Generated `.ovpn` files

##### Key Settings
```
# Connection settings
remote SERVER_IP 1194 udp
proto udp
port 1194

# Security settings
cipher AES-256-CBC
auth SHA256
tls-auth ta.key 1

# Compression
comp-lzo

# Routing
redirect-gateway def1
dhcp-option DNS 8.8.8.8
```

**Protocol Options**:
- **UDP**: Faster, less reliable
- **TCP**: Slower, more reliable

**Port Recommendations**:
- `1194`: Standard OpenVPN port
- `443`: HTTPS port (better firewall traversal)
- `53`: DNS port (best firewall traversal)

---

## Network and Firewall Settings

### UFW (Uncomplicated Firewall)

#### Default SSH Plus Rules
```bash
# SSH access
ufw allow 22/tcp
ufw allow 2222/tcp

# Web services
ufw allow 80/tcp
ufw allow 443/tcp

# OpenVPN
ufw allow 1194/udp

# Custom ports
ufw allow 8080/tcp
ufw allow 8443/tcp
```

#### Advanced Rules
```bash
# Rate limiting for SSH
ufw limit 22/tcp

# Specific IP access
ufw allow from 192.168.1.0/24 to any port 22

# Port ranges
ufw allow 8000:8999/tcp
```

### IPTables Rules

#### SSH Plus Generated Rules
```bash
# NAT rules for port forwarding
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8443

# Connection tracking
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Rate limiting
iptables -A INPUT -p tcp --dport 22 -m limit --limit 3/min -j ACCEPT
```

**Effects**:
- Port redirection for non-root services
- Connection state tracking
- DDoS protection

---

## Performance Optimization

### System Limits

#### `/etc/security/limits.conf`
```bash
# SSH Plus optimizations
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768

# Root limits
root soft nofile 65536
root hard nofile 65536
```

**Effects**:
- Increases file descriptor limits
- Allows more concurrent connections
- Improves system stability under load

#### Kernel Parameters
**File**: `/etc/sysctl.conf`
```bash
# Network optimizations
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# Connection handling
net.ipv4.tcp_max_syn_backlog = 8192
net.core.netdev_max_backlog = 5000
net.core.somaxconn = 1024

# Security
net.ipv4.tcp_syncookies = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
```

**Tuning Guidelines**:
```bash
# Low-resource servers (1GB RAM)
net.core.somaxconn = 512
net.ipv4.tcp_max_syn_backlog = 2048

# High-resource servers (8GB+ RAM)
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 16384
```

### Service Optimization

#### SSH Daemon Tuning
```bash
# /etc/ssh/sshd_config optimizations
ClientAliveInterval 60
ClientAliveCountMax 3
TCPKeepAlive yes
Compression delayed
```

**Effects**:
- `ClientAliveInterval`: Prevents idle disconnections
- `Compression`: Reduces bandwidth usage
- `TCPKeepAlive`: Maintains connection health

#### V2Ray Performance
```json
{
  "policy": {
    "levels": {
      "0": {
        "handshake": 4,
        "connIdle": 300,
        "uplinkOnly": 2,
        "downlinkOnly": 5,
        "bufferSize": 10240
      }
    }
  }
}
```

**Parameters**:
- `handshake`: Connection establishment timeout
- `connIdle`: Idle connection timeout
- `bufferSize`: Memory buffer size per connection

---

## Security Settings

### Access Control

#### SSH Access Restrictions
```bash
# /etc/ssh/sshd_config
AllowUsers user1 user2 admin
DenyUsers baduser
AllowGroups sshusers
```

**Effects**:
- `AllowUsers`: Whitelist specific users
- `DenyUsers`: Blacklist specific users
- `AllowGroups`: Allow group-based access

#### IP-based Restrictions
```bash
# Using hosts.allow/hosts.deny
echo "sshd: 192.168.1.0/24" >> /etc/hosts.allow
echo "sshd: ALL" >> /etc/hosts.deny

# Using UFW
ufw deny from 1.2.3.4
ufw allow from 192.168.1.0/24
```

### Encryption Settings

#### SSH Cipher Configuration
```bash
# Strong ciphers only
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha2-256,hmac-sha2-512
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
```

**Security Levels**:
```bash
# Maximum security (may break older clients)
Ciphers aes256-gcm@openssh.com
MACs hmac-sha2-256-etm@openssh.com

# Balanced security (recommended)
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com

# Compatibility mode (less secure)
# Use default ciphers
```

### Certificate Management

#### Let's Encrypt Integration
```bash
# Automatic certificate renewal
# /etc/crontab entry
0 3 * * * root certbot renew --quiet --post-hook "systemctl reload nginx"
```

**Configuration**:
```bash
# Certificate paths
SSL_CERT="/etc/letsencrypt/live/domain.com/fullchain.pem"
SSL_KEY="/etc/letsencrypt/live/domain.com/privkey.pem"

# Renewal settings
RENEW_DAYS_BEFORE=30
AUTO_RELOAD_SERVICES=true
```

---

## Monitoring and Logging

### Log Configuration

#### System Logging
```bash
# /etc/rsyslog.conf additions
# SSH Plus logs
local0.*    /var/log/sshplus.log
local1.*    /var/log/sshplus-users.log
```

#### Service-Specific Logs
```bash
# SSH logs
auth.log     # Authentication attempts
syslog       # General system messages

# V2Ray logs
/var/log/v2ray/access.log   # Connection logs
/var/log/v2ray/error.log    # Error messages

# Nginx logs (if used)
/var/log/nginx/access.log   # HTTP requests
/var/log/nginx/error.log    # HTTP errors
```

### Monitoring Scripts

#### Connection Monitoring
```bash
# Monitor active connections
#!/bin/bash
MONITOR_INTERVAL=60
LOG_FILE="/var/log/sshplus-monitor.log"

while true; do
    CONNECTIONS=$(ss -tn | grep :22 | wc -l)
    echo "$(date): Active SSH connections: $CONNECTIONS" >> $LOG_FILE
    sleep $MONITOR_INTERVAL
done
```

#### Resource Monitoring
```bash
# System resource usage
#!/bin/bash
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
MEM_USAGE=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')
DISK_USAGE=$(df -h / | awk 'NR==2{print $5}' | cut -d'%' -f1)

echo "CPU: ${CPU_USAGE}%, Memory: ${MEM_USAGE}%, Disk: ${DISK_USAGE}%"
```

### Alert Configuration

#### Email Alerts
```bash
# Install mail utilities
apt install mailutils -y

# Alert script
#!/bin/bash
ALERT_EMAIL="admin@domain.com"
CPU_THRESHOLD=80
MEM_THRESHOLD=90

if [ $CPU_USAGE -gt $CPU_THRESHOLD ]; then
    echo "High CPU usage: ${CPU_USAGE}%" | mail -s "SSH Plus Alert" $ALERT_EMAIL
fi
```

#### Telegram Notifications
```bash
# Telegram bot configuration
TELEGRAM_BOT_TOKEN="your_bot_token"
TELEGRAM_CHAT_ID="your_chat_id"

# Send notification function
send_telegram() {
    MESSAGE="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        -d text="$MESSAGE"
}
```

---

## Environment-Specific Configurations

### Development Environment
```bash
# Relaxed security for testing
PasswordAuthentication yes
PermitRootLogin yes
MaxAuthTries 10

# Verbose logging
LogLevel DEBUG
SyslogFacility AUTH

# No connection limits
# Comment out user limits in usuarios.db
```

### Production Environment
```bash
# Enhanced security
PasswordAuthentication no  # Use keys only
PermitRootLogin no
MaxAuthTries 3

# Minimal logging
LogLevel INFO

# Strict connection limits
# Enforce user limits strictly
CHECK_INTERVAL=15
KILL_EXCESS=true
```

### High-Traffic Environment
```bash
# Performance optimizations
MaxSessions 50
MaxStartups 50:30:100

# System limits
ulimit -n 65536

# Kernel parameters
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 16384
```

---

## Configuration Backup and Recovery

### Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/root/sshplus-backup-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# System configurations
cp /etc/ssh/sshd_config $BACKUP_DIR/
cp /root/usuarios.db $BACKUP_DIR/
cp -r /usr/share/.plus $BACKUP_DIR/

# Service configurations
cp -r /etc/v2ray $BACKUP_DIR/ 2>/dev/null
cp -r /usr/local/etc/trojan-go $BACKUP_DIR/ 2>/dev/null

# Create archive
tar -czf "sshplus-backup-$(date +%Y%m%d).tar.gz" -C /root $BACKUP_DIR
echo "Backup created: sshplus-backup-$(date +%Y%m%d).tar.gz"
```

### Recovery Procedure
```bash
#!/bin/bash
BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

# Extract backup
tar -xzf $BACKUP_FILE -C /tmp/

# Restore configurations
cp /tmp/sshplus-backup-*/sshd_config /etc/ssh/
cp /tmp/sshplus-backup-*/usuarios.db /root/
cp -r /tmp/sshplus-backup-*/.plus /usr/share/

# Restart services
systemctl restart ssh
systemctl restart v2ray 2>/dev/null
systemctl restart trojan-go 2>/dev/null

echo "Configuration restored from $BACKUP_FILE"
```

---

## Best Practices

### Security Best Practices
1. **Regular Updates**: Keep system and SSH Plus updated
2. **Strong Authentication**: Use key-based authentication when possible
3. **Access Control**: Implement IP whitelisting for admin access
4. **Monitoring**: Set up alerts for suspicious activities
5. **Backups**: Regular configuration backups

### Performance Best Practices
1. **Resource Monitoring**: Track CPU, memory, and network usage
2. **Connection Limits**: Set appropriate user connection limits
3. **System Tuning**: Optimize kernel parameters for your workload
4. **Log Rotation**: Prevent log files from consuming disk space
5. **Service Optimization**: Tune service-specific parameters

### Maintenance Best Practices
1. **Documentation**: Keep configuration changes documented
2. **Testing**: Test changes in development environment first
3. **Rollback Plan**: Always have a rollback strategy
4. **Monitoring**: Monitor system health after changes
5. **User Communication**: Notify users of maintenance windows

---

**Note**: Always test configuration changes in a non-production environment before applying them to production systems. Keep backups of working configurations before making modifications.
