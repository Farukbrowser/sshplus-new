# SSH Plus Multiport Fix

## Problem Description

When configuring multiport settings with ports like `80,2082,8080`, the ports may not activate properly due to missing firewall rules. This happens because:

1. Port 2082 was not included in the default firewall configuration
2. The multiport configuration didn't automatically open firewall rules for each individual port
3. Only the first port in the list was being processed for firewall rules

## Solution Applied

The following fixes have been implemented:

### 1. Updated Installation Scripts

- **Plus**: Added port 2082 to default firewall configuration
- **S/install**: Added port 2082 to SlowDNS installation firewall rules

### 2. Enhanced Multiport Handling

- **M/conexao**: Updated both SOCKS and WebSocket proxy sections to:
  - Parse comma-separated ports correctly
  - Open firewall rules for each individual port
  - Support firewalld, UFW, and iptables
  - Apply rules both temporarily and permanently

### 3. Manual Fix Script

- **M/fix-multiport**: Created a standalone script to fix existing installations

## How to Use

### For New Installations

The fix is automatically applied during installation. Multiport functionality will work out of the box.

### For Existing Installations

#### Option 1: Run the Fix Script

```bash
# Make the script executable
chmod +x /path/to/sshplus/M/fix-multiport

# Run the fix
./M/fix-multiport
```

#### Option 2: Manual Firewall Configuration

```bash
# For firewalld
sudo firewall-cmd --zone=public --add-port=80/tcp
sudo firewall-cmd --zone=public --add-port=2082/tcp
sudo firewall-cmd --zone=public --add-port=8080/tcp
sudo firewall-cmd --permanent --zone=public --add-port=80/tcp
sudo firewall-cmd --permanent --zone=public --add-port=2082/tcp
sudo firewall-cmd --permanent --zone=public --add-port=8080/tcp
sudo firewall-cmd --reload

# For UFW
sudo ufw allow 80/tcp
sudo ufw allow 2082/tcp
sudo ufw allow 8080/tcp

# For iptables
sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 2082 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT
```

## Testing Multiport Configuration

1. Access SSH Plus menu
2. Go to Connection Tools → SOCKS Proxy or WebSocket
3. Enter ports: `80,2082,8080`
4. The system should now properly:
   - Validate all ports
   - Open firewall rules for each port
   - Start the proxy service on all specified ports

## Supported Port Formats

- Single port: `80`
- Multiple ports: `80,2082,8080`
- With spaces: `80, 2082, 8080` (automatically trimmed)

## Firewall Systems Supported

- **firewalld**: Primary firewall system (CentOS/RHEL/Fedora)
- **UFW**: Ubuntu/Debian simplified firewall
- **iptables**: Direct iptables rules for advanced configurations

## Technical Details

### Code Changes Made

1. **Enhanced Port Parsing**: Improved comma-separated port handling with proper whitespace trimming

2. **Firewall Rule Generation**: Added automatic firewall rule creation for each port in multiport configuration

3. **Multiple Firewall Support**: Added detection and configuration for firewalld, UFW, and iptables

4. **Permanent Rule Storage**: Ensured rules persist across reboots

### Files Modified

- `Plus`: Main installation script
- `S/install`: SlowDNS installation script
- `M/conexao`: Connection management script
- `M/fix-multiport`: New manual fix script

## Troubleshooting

### If Multiport Still Doesn't Work

1. **Check Firewall Status**:
   ```bash
   # For firewalld
   sudo firewall-cmd --list-ports
   
   # For UFW
   sudo ufw status
   
   # For iptables
   sudo iptables -L -n
   ```

2. **Verify Port Availability**:
   ```bash
   netstat -tlpn | grep -E ':(80|2082|8080)'
   ```

3. **Check Proxy Process**:
   ```bash
   ps aux | grep -E '(proxy|wsproxy)'
   screen -ls
   ```

4. **Test Port Connectivity**:
   ```bash
   telnet localhost 80
   telnet localhost 2082
   telnet localhost 8080
   ```

### Common Issues

- **Permission Denied**: Run fix script with sudo
- **Firewall Not Detected**: Manually configure using appropriate firewall commands
- **Ports Already in Use**: Check for conflicting services on the same ports

## Support

If you continue experiencing issues after applying this fix:

1. Verify your system's firewall configuration
2. Check for conflicting services on the specified ports
3. Ensure the SSH Plus scripts have proper permissions
4. Review system logs for any error messages

The multiport functionality should now work correctly with ports `80,2082,8080` and any other valid port combinations.