# Network Device Dashboard - Installation Guide

## 📋 Pre-Installation Checklist

Before starting the installation, please verify:

- [ ] Windows 10/11 (64-bit) operating system
- [ ] Administrator access for initial setup
- [ ] Internet connection for downloading packages
- [ ] At least 1GB free disk space
- [ ] Network connection (WiFi or Ethernet)

---

## 🔧 Step 1: Python Installation

### If Python is Already Installed:
1. Press `Windows + R`, type `cmd`, and press Enter
2. Type: `python --version`
3. If you see "Python 3.8" or higher, skip to Step 2
4. If you see an error or older version, continue below

### Installing Python:

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (latest version)
   - Save the installer file

2. **Run Python Installer:**
   - Double-click the downloaded installer
   - ⚠️ **CRITICAL**: Check "Add Python to PATH" ✅
   - Click "Install Now"
   - Wait for installation to complete (5-10 minutes)
   - Click "Close" when finished

3. **Verify Installation:**
   - Press `Windows + R`, type `cmd`, press Enter
   - Type: `python --version`
   - You should see: `Python 3.11.x`
   - If you see an error, restart your computer and try again

---

## 📦 Step 2: Dashboard Installation

### Method 1: Automatic Installation (Recommended)

1. **Extract Files:**
   - Extract the dashboard package to: `C:\NetworkDashboard\`
   - You should see folders like: `network_dashboard`, `Documentation`

2. **Run Installer:**
   - Navigate to the extracted folder
   - Right-click on `install_dependencies.bat`
   - Select "Run as administrator"
   - Click "Yes" when prompted by Windows

3. **Installation Process:**
   ```
   ============================================
   Network Device Dashboard - Setup
   ============================================
   
   [1/5] Checking Python installation...
   ✅ Python found!
   
   [2/5] Verifying Python version...
   ✅ Python version is compatible!
   
   [3/5] Creating isolated environment...
   ✅ Virtual environment created!
   
   [4/5] Activating environment...
   
   [5/5] Installing dashboard components...
   This may take 2-3 minutes...
   ```

4. **Installation Complete:**
   ```
   ============================================
   ✅ Installation Complete!
   ============================================
   
   Your Network Device Dashboard is ready to use!
   ```

5. **Press any key to continue**

### Method 2: Manual Installation (Advanced Users)

If the automatic installer doesn't work:

1. **Open Command Prompt as Administrator:**
   - Press `Windows + X`
   - Select "Command Prompt (Admin)" or "PowerShell (Admin)"

2. **Navigate to Dashboard Directory:**
   ```cmd
   cd C:\NetworkDashboard\network_dashboard
   ```

3. **Create Virtual Environment:**
   ```cmd
   python -m venv venv
   ```

4. **Activate Virtual Environment:**
   ```cmd
   venv\Scripts\activate.bat
   ```

5. **Install Dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Initialize Database:**
   ```cmd
   python -c "from database import DatabaseManager; db = DatabaseManager(); db.init_database()"
   ```

---

## 🚀 Step 3: First Launch

### Starting the Dashboard:

1. **Run the Dashboard:**
   - Navigate to the dashboard folder
   - Double-click `quick_start.bat`
   - You'll see the startup screen:

   ```
   ╔══════════════════════════════════════════════════════════╗
   ║                 Network Device Dashboard                 ║
   ║                                                          ║
   ║  🌐 Dashboard URL: http://localhost:5000                 ║
   ║                                                          ║
   ║  📊 The dashboard will automatically detect and scan     ║
   ║     YOUR network (not the developer's network)          ║
   ║                                                          ║
   ║  🔍 Network auto-detection:                              ║
   ║     • Home networks (192.168.x.x)                       ║
   ║     • Office networks (10.x.x.x)                        ║
   ║     • Corporate networks (172.16.x.x)                   ║
   ║                                                          ║
   ║  ⏹️  Press Ctrl+C to stop the server                     ║
   ╚══════════════════════════════════════════════════════════╝
   
   ✅ Dashboard is now running!
   
   👉 Open your web browser and go to: http://localhost:5000
   ```

2. **Open Your Browser:**
   - Open Chrome, Edge, or Firefox
   - Go to: `http://localhost:5000`
   - You should see the Network Device Dashboard

### First Time Setup:

1. **Dashboard Loads:**
   - You'll see the main dashboard page
   - Statistics will show: 0 devices initially
   - This is normal for first run

2. **Initial Network Detection:**
   - Click "Scan" in the navigation menu
   - The dashboard automatically detects your network range
   - Example: If your PC is 192.168.1.100, it scans 192.168.1.0/24

3. **Run First Scan:**
   - Click "Start Scan" button
   - Select "Ping Scan" (recommended for first use)
   - Watch the progress bar as it scans your network
   - Devices will appear as they're discovered

4. **View Results:**
   - Go back to "Dashboard" to see discovered devices
   - Click "Devices" to see detailed list
   - Click on any device to view more information

---

## 🔍 Step 4: Verify Installation

### System Check:

1. **Dashboard Page Loads:**
   - [ ] Main dashboard displays without errors
   - [ ] Navigation menu works (Dashboard, Devices, Groups, Scan)
   - [ ] Statistics cards show numbers (even if 0)

2. **Network Detection:**
   - [ ] Scan page shows your correct network range
   - [ ] Example: 192.168.1.0/24 or 10.0.0.0/24
   - [ ] Range matches your computer's IP address

3. **Device Discovery:**
   - [ ] First scan finds at least 1 device (your router)
   - [ ] Your computer appears in device list
   - [ ] Devices show online/offline status

4. **Real-time Features:**
   - [ ] WebSocket connection shows "Connected" 
   - [ ] Dashboard updates automatically
   - [ ] No JavaScript errors in browser console (F12)

### Expected First Scan Results:

Your scan should find devices similar to these:

```
Network Range: 192.168.1.0/24
Scanning 254 IP addresses...

✅ 192.168.1.1 (router) - Gateway/Router
✅ 192.168.1.100 (YOUR-PC-NAME) - Your Computer  
✅ 192.168.1.45 (android-device) - Smartphone
✅ 192.168.1.75 (printer) - Network Printer

Scan Complete: 4 devices found in 25 seconds
```

---

## 🎯 Step 5: Basic Configuration

### Organize Your Devices:

1. **Create Device Groups:**
   - Click "Groups" in navigation
   - Click "Add Group" button
   - Create groups like:
     - "Network Equipment" (routers, switches)
     - "Computers" (PCs, laptops)
     - "Mobile Devices" (phones, tablets)
     - "Printers" (network printers)
     - "Smart Home" (IoT devices)

2. **Assign Devices to Groups:**
   - Go to "Devices" page
   - Click "Edit" next to any device
   - Select appropriate group from dropdown
   - Add custom name (e.g., "Main Router", "John's Laptop")
   - Click "Save"

3. **Set Up Monitoring:**
   - Dashboard automatically monitors devices every 5 minutes
   - Green = Online, Red = Offline
   - View status history for any device
   - Real-time updates via WebSocket

### Configure Dashboard Preferences:

1. **Device Names:**
   - Give meaningful names to important devices
   - Example: "192.168.1.1" → "Main Router"
   - Example: "192.168.1.100" → "Reception PC"

2. **Group Colors:**
   - Assign different colors to each group
   - Makes it easy to identify device types
   - Colors appear throughout the interface

---

## 📊 Step 6: Daily Usage

### Starting the Dashboard (Daily):

1. **Method 1: Desktop Shortcut**
   - Create shortcut to `quick_start.bat` on desktop
   - Double-click to start

2. **Method 2: Windows Startup (Optional)**
   - Add shortcut to Windows Startup folder
   - Dashboard starts automatically with Windows

### Stopping the Dashboard:

1. **In the command window:**
   - Press `Ctrl + C`
   - Confirm with `Y` if prompted
   - Window will close

2. **Or close the command window directly**

### Regular Maintenance:

1. **Weekly Network Scans:**
   - Run manual scans to discover new devices
   - Remove devices that are no longer on network

2. **Review Status History:**
   - Check which devices have connectivity issues
   - Monitor for unauthorized devices

3. **Database Cleanup (Monthly):**
   - Dashboard automatically cleans old logs
   - No manual maintenance required

---

## 🔒 Security & Privacy

### What Data is Stored:

✅ **Local Only:**
- All data stored in SQLite database on your computer
- No cloud storage or external data transmission
- Device IP addresses, names, and status history only

✅ **Network Safety:**
- Uses standard ping protocol (ICMP)
- No modification of network devices
- Read-only network monitoring

✅ **Privacy:**
- No personal information collected
- No internet data transmission
- No tracking or analytics

### Access Control:

- Dashboard runs on localhost (127.0.0.1:5000) only
- Not accessible from other computers by default
- No remote access without manual configuration
- Windows Firewall provides automatic protection

---

## 🆘 Troubleshooting Common Issues

### Issue 1: "Python is not installed"

**Solution:**
1. Download Python from python.org
2. Re-run installer with "Add to PATH" checked
3. Restart computer
4. Try installation again

### Issue 2: "Virtual environment creation failed"

**Solution:**
1. Run installer as Administrator
2. Check available disk space (need 500MB+)
3. Temporarily disable antivirus
4. Try manual installation method

### Issue 3: Dashboard won't start

**Symptoms:** Browser shows "This site can't be reached"

**Solution:**
1. Check if quick_start.bat window is still open
2. Look for "Dashboard is now running!" message
3. Try http://127.0.0.1:5000 instead
4. Check Windows Firewall settings

### Issue 4: No devices found during scan

**Possible Causes:**
- Wrong network range detected
- Firewall blocking ICMP
- Network devices don't respond to ping

**Solution:**
1. Check your PC's IP address: `ipconfig`
2. Manually enter correct network range
3. Temporarily disable Windows Firewall to test
4. Try scanning smaller IP ranges

### Issue 5: WebSocket connection failed

**Symptoms:** "Disconnected" indicator, no real-time updates

**Solution:**
1. Refresh browser page
2. Check browser console (F12) for errors
3. Try different browser (Chrome recommended)
4. Restart dashboard application

---

## 🎓 Next Steps

### Learning the Interface:

1. **Read the User Manual:**
   - Complete feature guide
   - Advanced configuration options
   - Tips and best practices

2. **Watch for Updates:**
   - Check with your system provider
   - Backup configuration before updates

### Getting Support:

1. **Documentation Priority:**
   - User Manual (comprehensive feature guide)
   - Troubleshooting Guide (detailed solutions)
   - System Requirements (compatibility info)

2. **Technical Support:**
   - Contact your system provider
   - Include error messages and system info
   - Describe steps that led to the issue

### Advanced Features (Optional):

1. **Install Nmap for Enhanced Scanning:**
   - Download from: https://nmap.org/download.html
   - Provides MAC addresses and vendor information
   - Enables advanced device detection

2. **Network Access (Advanced):**
   - Configure dashboard for multi-user access
   - Set up SSL certificates for secure access
   - Contact support for enterprise deployment

---

## ✅ Installation Complete!

**Congratulations!** Your Network Device Dashboard is now installed and configured.

### Quick Reference:

- **Start Dashboard:** Double-click `quick_start.bat`
- **Access Dashboard:** http://localhost:5000
- **Stop Dashboard:** Press Ctrl+C in command window
- **Get Help:** Check Documentation folder

### What You Can Do Now:

1. 🔍 **Discover Devices:** Run network scans to find all devices
2. 📊 **Monitor Status:** Real-time online/offline monitoring  
3. 🏷️ **Organize:** Group devices and add custom names
4. 📈 **Track History:** View device connectivity over time
5. 🔍 **Search:** Find devices by IP, name, or group

**Your network monitoring solution is ready!** 🌐✨

---

**Installation Date:** _______________  
**Installed Version:** 1.0.0  
**Installer:** ___________________  
**Support Contact:** _____________