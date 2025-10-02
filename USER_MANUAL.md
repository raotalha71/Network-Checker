# Network Device Dashboard - User Manual

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Device Management](#device-management)
4. [Network Scanning](#network-scanning)
5. [Device Groups](#device-groups)
6. [Monitoring & History](#monitoring--history)
7. [Advanced Features](#advanced-features)
8. [Tips & Best Practices](#tips--best-practices)

---

## 🚀 Getting Started

### Starting the Dashboard

1. **Launch the Application:**
   - Double-click `quick_start.bat`
   - Wait for the startup message
   - Open browser to: http://localhost:5000

2. **First Time Setup:**
   - Dashboard starts with empty database
   - Run initial network scan to discover devices
   - Set up device groups for organization

### Interface Overview

The dashboard has 5 main sections:

| Section | Purpose | Key Features |
|---------|---------|--------------|
| **Dashboard** | Overview & statistics | Device counts, charts, recent activity |
| **Devices** | Device management | Search, edit, detailed view |
| **Groups** | Organization | Create groups, assign colors |
| **Scan** | Network discovery | Manual scans, progress tracking |
| **Device Detail** | Individual device info | History, actions, statistics |

---

## 📊 Dashboard Overview

### Main Dashboard Page

When you open http://localhost:5000, you'll see:

#### Statistics Cards

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Total       │ │ Online      │ │ Offline     │ │ Groups      │
│ Devices: 12 │ │ Devices: 9  │ │ Devices: 3  │ │ Total: 4    │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

- **Total Devices:** All discovered devices in database
- **Online:** Currently responding to ping
- **Offline:** Not responding (may be powered off)
- **Groups:** Number of device categories created

#### Device Groups Chart

- **Pie Chart:** Visual breakdown of devices by group
- **Interactive:** Hover for details, click to filter
- **Color-Coded:** Each group has unique color
- **Updates:** Real-time updates as groups change

#### Recent Status Changes

```
Device Name          Status     Time
Main Router         Online     2 minutes ago
John's Laptop       Offline    5 minutes ago
Office Printer      Online     12 minutes ago
```

- **Last 10 Changes:** Most recent device status updates
- **Real-Time:** Updates automatically via WebSocket
- **Click Device:** Jump to device detail page

#### Device Overview Table

- **Quick List:** All devices with status indicators
- **Status Dots:** 🟢 Online, 🔴 Offline, 🟡 Unknown
- **Click Row:** View device details
- **Auto-Refresh:** Updates every 30 seconds

### Connection Status

Look for the WebSocket indicator:
- 🟢 **Connected:** Real-time updates active
- 🔴 **Disconnected:** Refresh page to reconnect

---

## 🖥️ Device Management

### Devices Page (/devices)

#### Device List Table

| Column | Description | Example |
|--------|-------------|---------|
| **Status** | Online/Offline indicator | 🟢 Online |
| **IP Address** | Device network address | 192.168.1.100 |
| **Hostname** | Computer name | OFFICE-PC |
| **Custom Name** | Your assigned name | "Reception Computer" |
| **Type** | Device category | Computer, Router, Printer |
| **MAC Address** | Hardware identifier | AA:BB:CC:DD:EE:FF |
| **Vendor** | Hardware manufacturer | Intel, Apple, TP-Link |
| **Group** | Assigned category | Office Equipment |

#### Search & Filter

**Search Bar:**
- Search by IP address: `192.168.1.100`
- Search by hostname: `OFFICE-PC`
- Search by custom name: `Reception`
- Real-time filtering as you type

**Group Filter:**
- Dropdown shows all groups
- Filter to show only specific group
- Shows device count per group
- "All Groups" shows everything

#### Adding/Editing Devices

**Manual Device Addition:**
1. Click "Add Device" button
2. Enter IP address
3. Dashboard pings to verify
4. Fill in device details
5. Assign to group
6. Save

**Editing Existing Devices:**
1. Click "Edit" button next to device
2. Modify any field:
   - Custom Name
   - Device Type
   - Group Assignment
   - Notes
3. Click "Save Changes"

**Bulk Operations:**
- Select multiple devices (checkboxes)
- Assign to group simultaneously
- Delete multiple devices
- Export selected devices

### Device Detail Page (/device/IP_ADDRESS)

Click any device to see comprehensive information:

#### Device Information Cards

**Basic Information:**
```
IP Address: 192.168.1.100     [Copy] [Ping Now]
Hostname: OFFICE-PC
MAC Address: AA:BB:CC:DD:EE:FF
Vendor: Intel Corporate
```

**Custom Information:**
```
Custom Name: Reception Computer
Device Type: Desktop Computer
Group: Office Equipment
Notes: Main reception desk computer, Windows 11
```

**Network Status:**
```
Current Status: 🟢 Online
Last Seen: 2 minutes ago
First Discovered: October 1, 2025 9:30 AM
Response Time: 1.5ms (Average: 2.1ms)
```

#### Quick Actions

**Network Tests:**
- **Ping Now:** Test connectivity immediately
- **Traceroute:** Show network path to device
- **Port Scan:** Check open ports (if nmap installed)

**Management:**
- **Edit Device:** Modify device information
- **Copy IP:** Copy IP address to clipboard
- **Open in Browser:** Navigate to device web interface
- **Delete Device:** Remove from database

#### Status History

**Timeline View:**
```
October 2, 2025
├─ 14:30 - Online (Response: 1.2ms)
├─ 14:25 - Online (Response: 1.8ms)
├─ 14:20 - Offline (No response)
├─ 14:15 - Online (Response: 1.5ms)
└─ 14:10 - Online (Response: 2.1ms)
```

**History Features:**
- **Filter by Date:** View specific date ranges
- **Export History:** Download as CSV
- **Response Time Graph:** Visual performance chart
- **Uptime Statistics:** Percentage online over time

#### Uptime Statistics

**Current Period (24 hours):**
- Uptime: 95.2% (22h 51m online)
- Downtime: 4.8% (1h 9m offline)
- Average Response: 1.8ms
- Longest Uptime: 8h 23m
- Longest Downtime: 45m

**Historical Trends:**
- 7-day average: 94.1%
- 30-day average: 96.8%
- Best day: 100% (October 1)
- Worst day: 78.3% (September 28)

---

## 🔍 Network Scanning

### Scan Page (/scan)

#### Scan Configuration

**Network Range:**
- **Auto-Detected:** Dashboard detects your network
- **Examples:** 
  - `192.168.1.0/24` (home network)
  - `10.0.0.0/24` (office network)
  - `172.16.1.0/24` (corporate network)
- **Custom Range:** Enter specific IP ranges
- **Validation:** Checks for valid network format

**Scan Types:**

| Type | Speed | Information | Requirements |
|------|-------|-------------|--------------|
| **Ping Scan** | Fast (15-30 sec) | IP, Hostname, Status | None (default) |
| **Nmap Scan** | Slower (1-3 min) | + MAC, Vendor, OS | Nmap installed |

#### Running a Scan

**Step-by-Step Process:**

1. **Start Scan:**
   ```
   Network Range: 192.168.1.0/24 ✓
   Scan Type: Ping Scan
   [Start Scan] [Stop Scan]
   ```

2. **Live Progress:**
   ```
   Scanning Network: 192.168.1.0/24
   Progress: [████████████░░░░] 75%
   Current IP: 192.168.1.189
   Elapsed Time: 12.4 seconds
   Devices Found: 6
   ```

3. **Real-Time Results:**
   ```
   ✅ 192.168.1.1 (gateway.local) - Router
   ✅ 192.168.1.25 (OFFICE-PC) - Computer  
   ✅ 192.168.1.50 (printer) - Network Device
   ✅ 192.168.1.75 (iPhone-12) - Mobile Device
   ✅ 192.168.1.100 (laptop) - Computer
   ✅ 192.168.1.125 (smart-tv) - Media Device
   ```

4. **Scan Complete:**
   ```
   ✅ Scan Complete!
   Network: 192.168.1.0/24
   Duration: 18.7 seconds
   Total IPs Scanned: 254
   Devices Found: 6
   New Devices: 2
   Known Devices: 4
   ```

#### Scan History

**Previous Scans:**
```
Date/Time           Network Range    Duration  Devices Found
Oct 2, 2025 14:30  192.168.1.0/24   18.7s     6 devices
Oct 2, 2025 09:15  192.168.1.0/24   22.1s     5 devices  
Oct 1, 2025 16:45  192.168.1.0/24   19.3s     4 devices
```

**Scan Comparison:**
- **New Devices:** Highlighted in green
- **Missing Devices:** Shows previously found but now offline
- **Performance Trends:** Average scan times and device counts

#### Advanced Scan Options

**Custom IP Ranges:**
- Single IP: `192.168.1.100`
- IP Range: `192.168.1.100-120`
- Multiple Networks: `192.168.1.0/24,10.0.0.0/24`

**Scan Scheduling (Future Feature):**
- Daily scans at specific times
- Automatic device discovery
- Email notifications for new devices

---

## 📂 Device Groups

### Groups Page (/groups)

#### Managing Groups

**Default Groups:**
- **Network Equipment:** Routers, switches, access points
- **Computers:** Desktops, laptops, servers
- **Mobile Devices:** Phones, tablets
- **Printers:** Network printers, scanners
- **IoT Devices:** Smart home gadgets

#### Creating Groups

**Add New Group:**
1. Click "Add Group" button
2. **Group Name:** Enter descriptive name
3. **Description:** Optional details about group purpose
4. **Color:** Choose from predefined colors:
   - Blue (#007bff) - Network equipment
   - Green (#28a745) - Computers
   - Red (#dc3545) - Critical devices
   - Yellow (#ffc107) - IoT devices
   - Purple (#6f42c1) - Media devices
5. Click "Save Group"

**Group Color System:**
- Colors appear throughout interface
- Device badges, charts, and lists
- Consistent visual identification
- Customizable for your needs

#### Group Management

**Edit Group:**
- Change name, description, or color
- Reassign devices to different groups
- View all devices in group

**Delete Group:**
- Devices become "Ungrouped"
- Can reassign before deletion
- Confirms before permanent removal

**Group Statistics:**
```
Network Equipment (Blue)
├─ 3 devices total
├─ 2 online, 1 offline
├─ Average uptime: 99.2%
└─ Last scan: 5 minutes ago
```

#### Device Assignment

**Methods to Assign Devices:**

1. **From Device List:**
   - Edit device → Select group → Save

2. **From Group Page:**
   - Click group → "Assign Devices"
   - Select from available devices

3. **Bulk Assignment:**
   - Select multiple devices
   - Choose group from dropdown
   - Apply to all selected

**Group-Based Views:**
- Filter devices by group
- Group statistics in dashboard
- Color-coded device indicators

---

## 📈 Monitoring & History

### Real-Time Monitoring

#### Background Monitoring

**Automatic Status Checks:**
- **Frequency:** Every 5 minutes
- **Method:** ICMP ping to each device
- **Response:** Records online/offline status
- **Logging:** All changes saved to database

**Status Change Notifications:**
- **WebSocket Updates:** Instant browser notifications
- **Dashboard Updates:** Status cards refresh automatically
- **Device List:** Status indicators update in real-time
- **Toast Messages:** "Device X went offline" notifications

#### Monitoring Dashboard

**Live Status Overview:**
- Total devices online/offline
- Recent status changes
- Group-based statistics
- Network health indicators

**Status Indicators:**
- 🟢 **Online:** Device responding to ping
- 🔴 **Offline:** Device not responding
- 🟡 **Unknown:** Never been scanned
- ⚫ **Disabled:** Monitoring disabled for device

### Historical Analysis

#### Device History

**Individual Device Tracking:**
- Complete timeline of status changes
- Response time measurements
- Uptime/downtime statistics
- Performance trends over time

**History Visualization:**
```
Uptime Chart (Last 24 Hours):
Online  ████████████████████████░░░░  95%
        |    |    |    |    |    |
        00:00 04:00 08:00 12:00 16:00 20:00

Downtime Events:
├─ 14:30-14:45 (15 min) - Power outage
├─ 08:15-08:18 (3 min) - Network restart
└─ 02:00-02:05 (5 min) - Scheduled maintenance
```

#### Network-Wide Analysis

**Trend Reports:**
- Device discovery over time
- Network stability metrics
- Peak usage patterns
- Problem device identification

**Performance Metrics:**
- Average response times
- Network scan durations
- Database query performance
- WebSocket connection stability

#### Data Export

**Export Options:**
- **CSV Format:** Spreadsheet compatible
- **JSON Format:** API integration
- **Date Ranges:** Custom time periods
- **Device Selection:** Specific devices or groups

**Export Examples:**
```csv
Timestamp,Device_IP,Device_Name,Status,Response_Time
2025-10-02 14:30:00,192.168.1.1,Main Router,Online,1.2
2025-10-02 14:30:00,192.168.1.100,Office PC,Online,2.1
2025-10-02 14:30:00,192.168.1.200,Printer,Offline,NULL
```

---

## 🔧 Advanced Features

### Enhanced Scanning with Nmap

#### Installing Nmap

**Benefits of Nmap:**
- MAC address detection
- Vendor identification  
- Operating system detection
- Port scanning capabilities
- Service identification

**Installation Steps:**
1. Download from: https://nmap.org/download.html
2. Run installer with default settings
3. Restart dashboard application
4. You'll see: "Nmap available - enhanced scanning enabled"

#### Enhanced Device Information

**With Nmap Installed:**
```
Device: 192.168.1.100
├─ IP: 192.168.1.100
├─ Hostname: OFFICE-PC
├─ MAC: AA:BB:CC:DD:EE:FF
├─ Vendor: Intel Corporate
├─ OS: Microsoft Windows 10
├─ Open Ports: 80, 443, 3389
└─ Services: HTTP, HTTPS, RDP
```

**Nmap Scan Types:**
- **Host Discovery:** Fast ping sweep
- **Port Scan:** Check for open services
- **OS Detection:** Identify operating systems
- **Service Scan:** Determine running services

### Custom Network Ranges

#### Manual Network Configuration

**Custom Range Examples:**
```
Single Subnet: 192.168.50.0/24
Multiple Subnets: 192.168.1.0/24,192.168.2.0/24
IP Range: 10.0.0.100-200
Single IPs: 192.168.1.1,192.168.1.100,192.168.1.200
```

**Use Cases:**
- Scan specific VLANs
- Monitor critical devices only
- Skip unused IP ranges
- Focus on problem areas

### API Integration

#### REST API Endpoints

**Device Management:**
```
GET /api/devices - List all devices
GET /api/device/{id} - Get device details
POST /api/device/{id}/update - Update device
DELETE /api/device/{id} - Delete device
```

**Network Scanning:**
```
POST /api/scan/start - Start network scan
GET /api/scan/status - Get scan progress
GET /api/scan/history - List previous scans
```

**Statistics:**
```
GET /api/stats - Network statistics
GET /api/stats/groups - Group statistics
GET /api/stats/history - Historical data
```

#### WebSocket Events

**Real-Time Events:**
```javascript
// Device status changes
socket.on('device_status', (data) => {
    console.log(`Device ${data.ip} is now ${data.status}`);
});

// Scan progress updates
socket.on('scan_progress', (data) => {
    console.log(`Scan progress: ${data.progress}%`);
});

// Network statistics updates
socket.on('stats_update', (data) => {
    console.log(`${data.online} devices online`);
});
```

### Database Management

#### Manual Database Operations

**Database Location:**
- File: `network_devices.db`
- Format: SQLite 3
- Size: ~1MB per 1000 devices

**Backup Database:**
```cmd
copy network_devices.db network_devices_backup.db
```

**Restore Database:**
```cmd
copy network_devices_backup.db network_devices.db
```

**Database Tables:**
- `devices` - Device information
- `status_logs` - Historical status data
- `device_groups` - Group definitions
- `scan_history` - Scan records

---

## 💡 Tips & Best Practices

### Network Scanning Best Practices

#### Optimal Scan Frequency

**Manual Scans:**
- **Daily:** For active networks with new devices
- **Weekly:** For stable office environments
- **Monthly:** For static server networks

**Background Monitoring:**
- Default: Every 5 minutes
- High-activity networks: Every 2-3 minutes
- Stable networks: Every 10-15 minutes

#### Scan Timing

**Best Times to Scan:**
- **Morning:** Catch devices powering on
- **Evening:** Detect personal devices joining network
- **Weekends:** Find unused devices to remove

**Avoid Scanning During:**
- Critical business operations
- Network maintenance windows
- High-traffic periods

### Device Organization

#### Naming Conventions

**Effective Device Names:**
```
Good Examples:
├─ "Reception-PC-01" (clear location and purpose)
├─ "Print-Color-2nd-Floor" (device type and location)
├─ "Router-Main-Gateway" (role and importance)
└─ "Security-Camera-Front-Door" (type and position)

Poor Examples:
├─ "Device1" (not descriptive)
├─ "Computer" (too generic)
├─ "Thing" (meaningless)
└─ "192.168.1.100" (just IP address)
```

**Naming Strategy:**
1. **Purpose:** What is it used for?
2. **Location:** Where is it physically?
3. **User:** Who primarily uses it?
4. **Type:** What kind of device?

#### Group Organization

**Recommended Group Structure:**

**By Location:**
- First Floor
- Second Floor  
- Server Room
- Remote Office

**By Function:**
- Critical Infrastructure
- End User Devices
- Guest Network
- IoT Devices

**By Department:**
- IT Equipment
- Accounting
- Sales
- Reception

### Performance Optimization

#### For Large Networks (100+ devices)

**Scan Strategy:**
- Split large networks into smaller subnets
- Schedule scans during off-peak hours
- Use nmap for more efficient scanning
- Consider parallel scanning

**Database Optimization:**
- Regular cleanup of old logs (automatic)
- Monitor database size growth
- Consider archiving historical data

**Resource Management:**
- Monitor memory usage during scans
- Close unused browser tabs
- Restart dashboard weekly for maintenance

### Security Considerations

#### Network Safety

**Safe Practices:**
✅ **Read-Only:** Dashboard only reads network information
✅ **Standard Protocols:** Uses ICMP ping (industry standard)
✅ **Local Storage:** All data stays on your computer
✅ **No Modification:** Never changes device settings

**Security Features:**
✅ **Localhost Only:** Not accessible from other computers
✅ **No External Communication:** No internet data transmission
✅ **Encrypted Storage:** SQLite database with local encryption
✅ **Access Control:** Windows user permissions apply

#### Corporate Environment

**IT Policy Compliance:**
- Check with IT department before installation
- Review network scanning policies
- Understand firewall implications
- Document monitoring activities

**Best Practices:**
- Use service accounts for dedicated monitoring
- Log all network scanning activities
- Coordinate with network administrators
- Maintain change management records

### Troubleshooting Prevention

#### Proactive Monitoring

**Health Checks:**
- Monitor dashboard responsiveness
- Check WebSocket connectivity status
- Verify database size and performance
- Review scan success rates

**Early Warning Signs:**
- Increased scan duration
- WebSocket connection drops
- Database query slowdowns
- Memory usage growth

#### Maintenance Schedule

**Daily:**
- Check connection status indicator
- Review recent status changes
- Verify critical device availability

**Weekly:**
- Run comprehensive network scan
- Review device group assignments
- Check for unauthorized devices

**Monthly:**
- Export historical data
- Review network performance trends
- Update device documentation
- Clean up obsolete devices

### Integration with Other Tools

#### Complementary Tools

**Network Monitoring:**
- Use with existing network monitoring systems
- Export data to network management platforms
- Integrate with helpdesk ticketing systems

**Documentation:**
- Export device lists to network documentation
- Maintain network diagrams with device info
- Create asset inventory reports

**Security:**
- Cross-reference with security scanning tools
- Compare with authorized device lists
- Monitor for unauthorized network access

---

## 🎯 Common Use Cases

### Small Business Office

**Typical Setup:**
- 20-50 devices (computers, printers, phones)
- Single network segment (192.168.1.0/24)
- Mixed Windows/Mac environment
- Wireless and wired devices

**Recommended Approach:**
1. Daily morning scans to catch new devices
2. Group devices by department or function
3. Monitor critical devices (server, router, main printer)
4. Weekly review for unauthorized devices

### Home Network

**Typical Setup:**
- 10-20 devices (computers, phones, smart home)
- Home router with DHCP
- Mix of always-on and intermittent devices
- IoT devices (smart TVs, thermostats, cameras)

**Recommended Approach:**
1. Weekly scans to discover new smart devices
2. Group by device type (computers, mobile, smart home)
3. Monitor internet-connected devices for security
4. Track which devices use most bandwidth

### IT Department

**Typical Setup:**
- 100+ devices across multiple subnets
- Servers, workstations, network equipment
- Mixed operating systems and device types
- Critical infrastructure requiring monitoring

**Recommended Approach:**
1. Scheduled scans of each subnet
2. Group by criticality and function
3. Export data to existing monitoring systems
4. Use for asset inventory and compliance

---

## 📞 Getting Help

### Built-in Help

**Documentation:**
- This User Manual (comprehensive guide)
- Installation Guide (setup instructions)
- Troubleshooting Guide (problem solutions)
- System Requirements (compatibility info)

**Interface Help:**
- Tooltips on buttons and fields
- Status indicators with explanations
- Error messages with suggested solutions
- Progress indicators during operations

### Support Resources

**Self-Service:**
1. Check Troubleshooting Guide first
2. Review System Requirements
3. Verify network connectivity
4. Check browser console for errors (F12)

**Technical Support:**
- Contact your system provider
- Include error messages and screenshots
- Describe steps that led to the issue
- Provide system information (Windows version, Python version)

**Community Resources:**
- User forums and discussion groups
- Knowledge base articles
- Video tutorials and guides
- Best practices documentation

---

## 🎉 Congratulations!

You now have comprehensive knowledge of the Network Device Dashboard. This powerful tool will help you:

- 🔍 **Discover** all devices on your network
- 📊 **Monitor** device status in real-time  
- 🏷️ **Organize** devices into logical groups
- 📈 **Track** connectivity history and trends
- 🔧 **Manage** your network infrastructure effectively

**Start exploring your network today!** 🌐✨

---

**Manual Version:** 1.0.0  
**Last Updated:** October 2, 2025  
**Compatible with:** Dashboard v1.0.0