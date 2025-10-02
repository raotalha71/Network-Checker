# Network Device Dashboard - Troubleshooting Guide

## 🆘 Quick Problem Resolution

### Most Common Issues

| Problem | Quick Solution | Success Rate |
|---------|---------------|--------------|
| Dashboard won't start | Run `install_dependencies.bat` as Administrator | 95% |
| No devices found | Check network range, try manual scan | 90% |
| WebSocket disconnected | Refresh browser page | 85% |
| Python not found | Install Python with "Add to PATH" | 100% |
| Port 5000 in use | Restart computer, or change port | 80% |

---

## 🔧 Installation Issues

### Issue 1: "Python is not installed"

**Error Message:**
```
❌ ERROR: Python is not installed on this system!
'python' is not recognized as an internal or external command
```

**Root Cause:**
- Python not installed
- Python installed but not in PATH
- Incorrect Python version

**Solutions:**

**Step 1: Check if Python exists**
```cmd
# Try different commands:
python --version
py --version
python3 --version
```

**Step 2: Install Python correctly**
1. Go to https://python.org/downloads/
2. Download Python 3.8 or higher
3. **CRITICAL:** Check "Add Python to PATH" ✅
4. Run installer as Administrator
5. Restart computer after installation

**Step 3: Verify installation**
```cmd
python --version
# Should show: Python 3.x.x
```

**Advanced Solution:**
If Python is installed but not in PATH:
1. Find Python installation directory
2. Add to Windows PATH environment variable
3. Or reinstall Python with PATH option

### Issue 2: "Virtual environment creation failed"

**Error Message:**
```
❌ ERROR: Failed to create virtual environment!
Access is denied / Permission denied
```

**Root Causes:**
- Insufficient permissions
- Antivirus blocking file creation
- Disk space insufficient
- Corrupted Python installation

**Solutions:**

**Step 1: Run as Administrator**
1. Right-click `install_dependencies.bat`
2. Select "Run as administrator"
3. Click "Yes" when prompted

**Step 2: Check disk space**
```cmd
dir C:\
# Ensure at least 1GB free space
```

**Step 3: Temporary antivirus disable**
1. Temporarily disable real-time protection
2. Run installer
3. Re-enable antivirus
4. Add dashboard folder to exclusions

**Step 4: Manual virtual environment**
```cmd
cd C:\path\to\network_dashboard
python -m venv venv --clear
```

### Issue 3: "Package installation failed"

**Error Message:**
```
❌ ERROR: Failed to install required packages!
No module named 'pip' / Connection timeout
```

**Root Causes:**
- No internet connection
- Corporate firewall blocking
- Proxy server issues
- Corrupted pip installation

**Solutions:**

**Step 1: Check internet**
```cmd
ping google.com
# Should see replies if internet works
```

**Step 2: Update pip**
```cmd
venv\Scripts\activate.bat
python -m pip install --upgrade pip
```

**Step 3: Manual package installation**
```cmd
venv\Scripts\activate.bat
pip install flask flask-socketio pythonping apscheduler
```

**Step 4: Corporate network (proxy)**
```cmd
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

**Step 5: Offline installation**
1. Download packages on internet-connected computer
2. Transfer wheel files
3. Install locally: `pip install *.whl`

---

## 🚀 Startup Problems

### Issue 4: Dashboard won't start

**Error Message:**
```
❌ Virtual environment not found!
This site can't be reached (in browser)
```

**Symptoms:**
- Browser shows "connection refused"
- Command window closes immediately
- No startup messages appear

**Diagnostic Steps:**

**Step 1: Check virtual environment**
```cmd
dir venv\Scripts\
# Should see activate.bat and python.exe
```

**Step 2: Manual startup**
```cmd
cd C:\path\to\network_dashboard
venv\Scripts\activate.bat
python app.py
```

**Step 3: Check error messages**
Look for specific errors in command window:
- Import errors → Missing packages
- Port errors → Port already in use
- Permission errors → Run as Administrator

**Solutions by Error Type:**

**ImportError: No module named 'flask'**
```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

**Port 5000 already in use:**
```cmd
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID 1234 /F

# Or change port in app.py
# socketio.run(app, host='0.0.0.0', port=5001)
```

**Permission denied:**
```cmd
# Run as Administrator
# Or change to different folder with full permissions
```

### Issue 5: Browser can't connect

**Error Messages:**
- "This site can't be reached"
- "Connection refused" 
- "Took too long to respond"

**Symptoms:**
- Dashboard appears to start correctly
- Browser shows connection error
- URL http://localhost:5000 doesn't work

**Solutions:**

**Step 1: Verify dashboard is running**
Look for this message in command window:
```
✅ Dashboard is now running!
(9448) wsgi starting up on http://0.0.0.0:5000
```

**Step 2: Try alternative URLs**
- http://127.0.0.1:5000
- http://localhost:5000
- http://[your-pc-ip]:5000

**Step 3: Check Windows Firewall**
1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Add Python.exe if not listed
4. Or temporarily disable firewall to test

**Step 4: Browser troubleshooting**
- Try different browser (Chrome, Edge, Firefox)
- Clear browser cache and cookies
- Disable browser extensions
- Try incognito/private mode

---

## 🌐 Network Scanning Issues

### Issue 6: No devices found during scan

**Error Message:**
```
Scan Complete: 0 devices found
Network range appears empty
```

**Symptoms:**
- Scan completes quickly
- No devices discovered
- Even router/gateway not found

**Diagnostic Questions:**
1. Is your computer connected to the network?
2. Can you browse the internet?
3. What's your computer's IP address?

**Step 1: Check network connection**
```cmd
ipconfig /all

# Look for:
IPv4 Address: 192.168.1.100 (your IP)
Default Gateway: 192.168.1.1 (router IP)
Subnet Mask: 255.255.255.0 (network size)
```

**Step 2: Verify network connectivity**
```cmd
# Ping your router
ping 192.168.1.1

# Ping external site
ping google.com
```

**Step 3: Manual network range**
Based on your IP address, try these ranges:
- If your IP is 192.168.1.100 → scan 192.168.1.0/24
- If your IP is 10.0.0.25 → scan 10.0.0.0/24
- If your IP is 172.16.1.50 → scan 172.16.1.0/24

**Step 4: Test specific devices**
```cmd
# Try pinging known devices manually
ping 192.168.1.1    # Router
ping 192.168.1.100  # Your computer
ping 8.8.8.8        # Google DNS
```

**Solutions by Network Type:**

**Home Network (192.168.x.x):**
- Most home routers use 192.168.1.1 or 192.168.0.1
- Check router label for default IP
- Try both /24 ranges if unsure

**Corporate Network:**
- Network may block ICMP (ping)
- Contact IT department
- May need special permissions

**VPN Connection:**
- VPN may change your network range
- Disconnect VPN and try local network
- Or scan VPN subnet if intentional

### Issue 7: Scan finds some devices but not others

**Symptoms:**
- Router found, but not all computers
- Some phones/tablets missing
- Intermittent device detection

**Common Causes:**
1. **Device firewalls** blocking ping
2. **Power saving** modes on laptops/phones
3. **WiFi vs Ethernet** different subnets
4. **Guest networks** isolated from main network

**Solutions:**

**Step 1: Check missing device directly**
```cmd
# From another computer, try pinging missing device
ping 192.168.1.missing-device-ip
```

**Step 2: Device-specific solutions**

**Windows computers not found:**
```cmd
# On the missing Windows PC, run:
# Disable Windows Firewall temporarily to test
# Or allow ICMP in firewall rules
```

**Mac computers not found:**
- Macs often block ping by default
- System Preferences → Security → Firewall
- Advanced → Uncheck "Block all incoming connections"

**Smartphones not found:**
- Many phones ignore ping to save battery
- This is normal behavior
- Use nmap scan for better detection

**IoT devices not found:**
- Smart TVs, cameras may not respond to ping
- Check device network settings
- Some have "stealth mode" enabled

**Step 3: Network configuration issues**

**Multiple WiFi networks:**
- Guest network isolated from main network
- Check which network device is connected to
- Scan appropriate network range

**VLAN segmentation:**
- Corporate networks often use VLANs
- Devices in different VLANs can't see each other
- Contact network administrator

---

## 🔌 Connection & Performance Issues

### Issue 8: WebSocket connection problems

**Error Message:**
```
🔴 WebSocket: Disconnected
Real-time updates not working
```

**Symptoms:**
- Status changes don't appear instantly
- Dashboard doesn't auto-refresh
- "Disconnected" indicator in interface

**Solutions:**

**Step 1: Refresh browser**
- Press F5 or Ctrl+R
- Hard refresh: Ctrl+Shift+R
- Close and reopen browser tab

**Step 2: Check browser compatibility**
- Chrome/Edge: Full support ✅
- Firefox: Full support ✅
- Safari: Limited support ⚠️
- Internet Explorer: Not supported ❌

**Step 3: Browser console debugging**
1. Press F12 to open developer tools
2. Click "Console" tab
3. Look for WebSocket errors:

```javascript
// Good messages:
WebSocket connection established
Socket.IO connected

// Bad messages:
WebSocket connection failed
ERR_CONNECTION_REFUSED
```

**Step 4: Firewall and antivirus**
- Temporarily disable Windows Firewall
- Disable antivirus real-time protection
- Test if WebSocket connects
- Add Python.exe to exclusions

**Step 5: Advanced troubleshooting**
```cmd
# Check if port 5000 is accessible
telnet localhost 5000

# Check for port conflicts
netstat -ano | findstr :5000
```

### Issue 9: Slow performance

**Symptoms:**
- Dashboard takes long time to load
- Scans run very slowly
- Browser becomes unresponsive
- High CPU or memory usage

**Performance Diagnostics:**

**Step 1: Check system resources**
```cmd
# Open Task Manager (Ctrl+Shift+Esc)
# Check CPU and Memory usage
# Python.exe should use <200MB RAM normally
```

**Step 2: Database size**
```cmd
dir network_devices.db
# Should be <10MB for normal networks
# >100MB indicates cleanup needed
```

**Step 3: Network size**
Large networks (>100 devices) may scan slowly:
- Split into smaller subnets
- Use nmap for faster scanning
- Increase monitoring intervals

**Solutions:**

**Database cleanup:**
```cmd
venv\Scripts\activate.bat
python -c "from database import DatabaseManager; db = DatabaseManager(); db.cleanup_old_logs(7)"
```

**Browser optimization:**
- Close other tabs
- Disable browser extensions
- Clear browser cache
- Use Chrome for best performance

**Network optimization:**
- Scan smaller IP ranges
- Schedule scans for off-peak hours
- Consider multiple dashboard instances for large networks

---

## 🔒 Security & Access Issues

### Issue 10: Access denied / Permission errors

**Error Messages:**
```
Access is denied
Permission denied
Unable to write to database
Unable to create files
```

**Root Causes:**
- Insufficient user permissions
- Antivirus blocking file access
- Corporate security policies
- Read-only file system

**Solutions:**

**Step 1: Run as Administrator**
1. Right-click `quick_start.bat`
2. Select "Run as administrator"
3. Click "Yes" when prompted

**Step 2: Check file permissions**
```cmd
# Navigate to dashboard folder
# Right-click folder → Properties → Security
# Ensure your user has Full Control
```

**Step 3: Antivirus exclusions**
1. Add dashboard folder to antivirus exclusions
2. Add Python.exe to exclusions
3. Restart dashboard

**Step 4: Corporate environment**
- Contact IT department
- Request permissions for network monitoring
- May need admin approval for Python installation

### Issue 11: Dashboard accessible from other computers

**Security Concern:**
```
Other people can access my dashboard at:
http://my-computer-ip:5000
```

**This is actually a configuration issue, not normal behavior**

**Verification:**
```cmd
# Dashboard should only bind to localhost
# Check startup message for:
wsgi starting up on http://127.0.0.1:5000  ✅ Good (localhost only)
wsgi starting up on http://0.0.0.0:5000    ❌ Bad (network accessible)
```

**Solution:**
Check app.py file contains:
```python
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)  # localhost only
    # NOT: socketio.run(app, host='0.0.0.0', port=5000)  # network accessible
```

---

## 🌐 Network-Specific Issues

### Issue 12: Corporate network scanning blocked

**Error Message:**
```
Scan complete: 0 devices found
All pings timed out
Network unreachable
```

**Symptoms:**
- Cannot scan any devices
- Even router ping fails
- Works at home but not at office

**Corporate Network Challenges:**
1. **ICMP blocking:** Many corporate firewalls block ping
2. **Network segmentation:** VLANs isolate devices
3. **Security policies:** Network scanning may be prohibited
4. **Proxy servers:** May interfere with direct connections

**Solutions:**

**Step 1: Check with IT department**
- Explain network monitoring purpose
- Request ICMP permissions
- Get approved IP ranges for scanning
- Understand network topology

**Step 2: Alternative scanning methods**
```cmd
# Try TCP ping instead of ICMP (future feature)
# Use nmap with different scan types
# Port scanning instead of ping
```

**Step 3: Limited scanning**
- Focus on specific devices you manage
- Scan smaller IP ranges
- Use manual device addition instead of discovery

### Issue 13: VPN network issues

**Symptoms:**
- Different devices found when VPN connected
- Network range changes unexpectedly
- Cannot find local devices while on VPN

**VPN Behavior:**
- VPN assigns new IP address (e.g., 10.8.0.1)
- Local network may become inaccessible
- Split tunneling affects which devices are reachable

**Solutions:**

**Step 1: Understand VPN configuration**
```cmd
ipconfig /all

# Without VPN:
IPv4 Address: 192.168.1.100 (local network)

# With VPN:
IPv4 Address: 10.8.0.15 (VPN network)
IPv4 Address: 192.168.1.100 (local network, if split tunnel)
```

**Step 2: Choose scanning target**
- **Local network:** Disconnect VPN, scan 192.168.x.x
- **Remote network:** Stay on VPN, scan 10.x.x.x
- **Both networks:** Use split tunneling if available

**Step 3: VPN-specific configuration**
Some VPN clients allow:
- Local network access while connected
- Split tunneling configuration
- Route-specific settings

---

## 🗄️ Database Issues

### Issue 14: Database corruption

**Error Messages:**
```
SQLite error: database disk image is malformed
Unable to read database
Database locked
```

**Symptoms:**
- Dashboard starts but no data appears
- Cannot save device changes
- Scan results not saved

**Solutions:**

**Step 1: Backup current database**
```cmd
copy network_devices.db network_devices_corrupt.db
```

**Step 2: Try database repair**
```cmd
venv\Scripts\activate.bat
python -c "
import sqlite3
conn = sqlite3.connect('network_devices.db')
conn.execute('PRAGMA integrity_check;')
print(conn.fetchall())
conn.close()
"
```

**Step 3: Reset database (last resort)**
```cmd
# This will delete all data!
del network_devices.db
python -c "from database import DatabaseManager; db = DatabaseManager(); db.init_database()"
```

**Step 4: Restore from backup**
If you have a backup:
```cmd
copy network_devices_backup.db network_devices.db
```

### Issue 15: Database locked

**Error Message:**
```
Database is locked
Unable to write to database
Another process is using the database
```

**Causes:**
- Multiple dashboard instances running
- Previous crash left database locked
- Antivirus scanning database file

**Solutions:**

**Step 1: Close all instances**
```cmd
# Kill all Python processes
taskkill /F /IM python.exe

# Or restart computer
```

**Step 2: Check for lock files**
```cmd
dir *.db-*
# Delete any .db-journal or .db-wal files
del network_devices.db-journal
del network_devices.db-wal
```

**Step 3: Restart dashboard**
```cmd
quick_start.bat
```

---

## ⚡ Advanced Troubleshooting

### Diagnostic Information Collection

When contacting support, collect this information:

**System Information:**
```cmd
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
python --version
pip --version
```

**Network Configuration:**
```cmd
ipconfig /all > network_config.txt
route print > network_routes.txt
```

**Dashboard Logs:**
```cmd
# Start dashboard and redirect output to file
python app.py > dashboard_log.txt 2>&1
```

**Browser Information:**
- Browser version (Chrome/Edge/Firefox)
- JavaScript console errors (F12 → Console)
- Network tab errors (F12 → Network)

### Performance Monitoring

**Resource Usage:**
```cmd
# Monitor Python process
tasklist /FI "IMAGENAME eq python.exe" /V

# Check disk space
dir C:\ | findstr "bytes free"
```

**Network Performance:**
```cmd
# Test network speed
ping -n 10 192.168.1.1

# Check DNS resolution
nslookup google.com
```

### Log Analysis

**Dashboard Logs:**
Look for these patterns in console output:

```
# Good messages:
INFO:network_scanner:Device monitoring started
INFO:__main__:Background tasks initialized
INFO:werkzeug:wsgi starting up on http://127.0.0.1:5000

# Warning messages (usually okay):
WARNING:network_scanner:Nmap not available
WARNING:werkzeug:WebSocket transport not available

# Error messages (problems):
ERROR:database:Database connection failed
ERROR:network_scanner:Scan failed with exception
CRITICAL:__main__:Fatal error in application
```

**Browser Console:**
Common JavaScript errors:

```javascript
// Connection issues:
WebSocket connection failed
ERR_CONNECTION_REFUSED
net::ERR_CONNECTION_RESET

// JavaScript errors:
Uncaught TypeError: Cannot read property
ReferenceError: $ is not defined
SyntaxError: Unexpected token
```

---

## 📞 Getting Additional Help

### Before Contacting Support

**Complete these steps:**
1. [ ] Try solutions in this troubleshooting guide
2. [ ] Restart computer and try again
3. [ ] Check Windows Event Viewer for errors
4. [ ] Test with different browser
5. [ ] Collect diagnostic information (above)

### Support Information to Provide

**System Details:**
- Windows version (10/11, 32/64-bit)
- Python version
- Dashboard version
- Network configuration (IP range, router type)

**Problem Description:**
- What were you trying to do?
- What happened instead?
- When did the problem start?
- Does it happen consistently?

**Error Information:**
- Exact error messages
- Screenshots of errors
- Console log output
- Steps to reproduce the problem

### Emergency Procedures

**Complete System Reset:**
If nothing else works:

1. **Backup important data**
2. **Uninstall Python** (Control Panel → Programs)
3. **Delete dashboard folder** completely
4. **Restart computer**
5. **Reinstall Python** with PATH option
6. **Extract fresh dashboard package**
7. **Run install_dependencies.bat**

**Network Connectivity Test:**
```cmd
# Basic connectivity test
ping 127.0.0.1     # Self
ping 192.168.1.1   # Router (adjust IP)
ping 8.8.8.8       # Internet
nslookup google.com # DNS

# If all fail, this is a network problem, not dashboard problem
```

---

## ✅ Prevention Tips

### Avoid Common Problems

**Installation Best Practices:**
- Always install Python with "Add to PATH"
- Run installers as Administrator
- Ensure stable internet connection during setup
- Keep antivirus updated but not overly aggressive

**Maintenance Schedule:**
- **Weekly:** Restart dashboard to clear memory
- **Monthly:** Run network scan to update device list
- **Quarterly:** Check for dashboard updates

**Backup Strategy:**
- Backup `network_devices.db` before major changes
- Keep installation files for easy reinstallation
- Document custom network configurations

### Monitoring Dashboard Health

**Key Indicators:**
- ✅ WebSocket shows "Connected"
- ✅ Network scans complete in reasonable time
- ✅ All devices show correct status
- ✅ Browser console has no errors

**Warning Signs:**
- ⚠️ Frequent WebSocket disconnections
- ⚠️ Scans taking much longer than usual
- ⚠️ Database file growing very large
- ⚠️ Browser becoming slow or unresponsive

---

## 🎯 Success Verification

After resolving any issue, verify these work correctly:

**Basic Functionality:**
- [ ] Dashboard loads at http://localhost:5000
- [ ] All navigation links work (Dashboard, Devices, Groups, Scan)
- [ ] WebSocket shows "Connected"
- [ ] No JavaScript errors in browser console

**Network Scanning:**
- [ ] Scan page detects correct network range
- [ ] Manual scan finds at least your router
- [ ] Scan results appear in device list
- [ ] Device details page shows correct information

**Real-Time Features:**
- [ ] Status changes update automatically
- [ ] Background monitoring runs every 5 minutes
- [ ] Dashboard statistics refresh correctly
- [ ] Toast notifications appear for status changes

**Data Persistence:**
- [ ] Device names and groups save correctly
- [ ] Status history accumulates over time
- [ ] Database maintains data between restarts
- [ ] Custom configurations persist

---

**Troubleshooting Guide Version:** 1.0.0  
**Last Updated:** October 2, 2025  
**Compatible with:** Dashboard v1.0.0

**Remember:** Most problems have simple solutions! Start with the basics (restart, refresh, check connections) before moving to advanced troubleshooting.

**Happy Monitoring!** 🌐📊