# 🌐 Network Device Dashboard

**Professional network monitoring made simple!** A complete web-based solution for discovering, monitoring, and managing all devices on your network.

## ✨ Features

- 🔍 **Auto Network Discovery** - Finds all devices automatically
- ⚡ **Real-time Monitoring** - Live status updates via WebSocket
- 📱 **Modern Web Interface** - Responsive dashboard for any device
- 🏷️ **Device Organization** - Custom groups, names, and notes
- 📊 **Network Analytics** - Statistics, charts, and insights
- 📈 **Historical Tracking** - Monitor performance over time
- 🔍 **Advanced Search** - Quick filtering and device location
- 📤 **Data Export** - CSV exports for reporting

## 🚀 ONE-CLICK INSTALLATION

**The easiest way - No technical knowledge required!**

### For First-Time Setup:
```
🔴 Right-click "ONE_CLICK_SETUP_AND_RUN.bat" → "Run as administrator"
```

**That's it!** This will:
- ✅ Install Python automatically (if missing)
- ✅ Install all required components
- ✅ Start the dashboard
- ✅ Open in your browser

### For Daily Use:
```
🔵 Double-click "LAUNCH_DASHBOARD.bat"
```

## 🛠️ Manual Installation (Advanced Users)

1. **Install Python 3.8+** from [python.org](https://python.org/downloads)
2. **Run the installer:**
```bash
install_dependencies.bat
```

3. **Start the dashboard:**
```bash
quick_start.bat
```

4. Open your browser to `http://localhost:5000`

## Usage

1. **Initial Discovery**: The app will automatically scan your local network
2. **Device Management**: Click on devices to add custom names and group them
3. **Monitoring**: Watch real-time status updates on the dashboard
4. **History**: View historical status logs for troubleshooting

## Requirements

- Python 3.7+
- nmap (must be installed separately on your system)
- Network access for device discovery

## Note

Make sure nmap is installed on your system:
- Windows: Download from https://nmap.org/download.html
- Linux: `sudo apt-get install nmap`
- macOS: `brew install nmap`