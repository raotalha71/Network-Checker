# Network Device Inventory & Status Dashboard

A Flask-based web application for discovering, monitoring, and managing network devices on your local network.

## Features

- **Network Discovery**: Automatically discover devices using ping and nmap
- **Real-time Monitoring**: Live status updates for all discovered devices  
- **Device Management**: Group devices, add custom names and notes
- **Historical Logs**: Track device status changes over time
- **Search & Filter**: Easy device search and filtering capabilities
- **Web Dashboard**: Clean, responsive web interface

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
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