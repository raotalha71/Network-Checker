import nmap
import socket
import subprocess
import threading
import time
from pythonping import ping
import ipaddress
import platform
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkScanner:
    def __init__(self):
        try:
            self.nm = nmap.PortScanner()
            self.nmap_available = True
        except Exception as e:
            logger.warning(f"Nmap not available: {e}")
            self.nm = None
            self.nmap_available = False
        self.local_network = self.get_local_network()
        
    def get_local_network(self):
        """Get the local network range"""
        try:
            # Get local IP address
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Convert to network
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
            return str(network)
        except Exception as e:
            logger.error(f"Error getting local network: {e}")
            return "192.168.1.0/24"  # Default fallback

    def ping_host(self, ip_address, timeout=2):
        """Ping a single host and return response time"""
        try:
            response = ping(ip_address, count=1, timeout=timeout)
            if response.success():
                return {
                    'ip': ip_address,
                    'status': 'online',
                    'response_time': response.rtt_avg_ms
                }
            else:
                return {
                    'ip': ip_address,
                    'status': 'offline',
                    'response_time': None
                }
        except Exception as e:
            logger.debug(f"Ping failed for {ip_address}: {e}")
            return {
                'ip': ip_address,
                'status': 'offline',
                'response_time': None
            }

    def get_hostname(self, ip_address):
        """Get hostname for an IP address"""
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except Exception:
            return None

    def scan_network_ping(self, network_range=None):
        """Fast network scan using ping"""
        if network_range is None:
            network_range = self.local_network
        
        logger.info(f"Starting ping scan of {network_range}")
        start_time = time.time()
        
        try:
            network = ipaddress.IPv4Network(network_range, strict=False)
            hosts = list(network.hosts())
            
            # Limit to reasonable size for ping scan
            if len(hosts) > 254:
                hosts = hosts[:254]
                
            online_devices = []
            
            # Use ThreadPoolExecutor for concurrent pings
            with ThreadPoolExecutor(max_workers=50) as executor:
                future_to_ip = {executor.submit(self.ping_host, str(ip)): str(ip) for ip in hosts}
                
                for future in as_completed(future_to_ip):
                    result = future.result()
                    if result['status'] == 'online':
                        # Get hostname
                        hostname = self.get_hostname(result['ip'])
                        device_info = {
                            'ip_address': result['ip'],
                            'hostname': hostname,
                            'status': result['status'],
                            'response_time': result['response_time'],
                            'mac_address': None,
                            'vendor': None,
                            'device_type': 'Unknown'
                        }
                        online_devices.append(device_info)
                        logger.info(f"Found device: {result['ip']} ({hostname})")
            
            duration = time.time() - start_time
            logger.info(f"Ping scan completed in {duration:.2f} seconds. Found {len(online_devices)} devices.")
            
            return {
                'devices': online_devices,
                'scan_type': 'ping',
                'network_range': network_range,
                'duration': duration,
                'devices_found': len(online_devices)
            }
            
        except Exception as e:
            logger.error(f"Error during ping scan: {e}")
            return {
                'devices': [],
                'scan_type': 'ping',
                'network_range': network_range,
                'duration': 0,
                'devices_found': 0
            }

    def scan_network_nmap(self, network_range=None, scan_type='-sn'):
        """Detailed network scan using nmap"""
        if not self.nmap_available or self.nm is None:
            logger.warning("Nmap not available, falling back to ping scan")
            return self.scan_network_ping(network_range)
            
        if network_range is None:
            network_range = self.local_network
            
        logger.info(f"Starting nmap scan of {network_range}")
        start_time = time.time()
        
        try:
            # Perform nmap scan
            self.nm.scan(hosts=network_range, arguments=scan_type)
            
            devices = []
            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    device_info = {
                        'ip_address': host,
                        'hostname': self.nm[host].hostname() or None,
                        'status': 'online',
                        'response_time': None,
                        'mac_address': None,
                        'vendor': None,
                        'device_type': 'Unknown'
                    }
                    
                    # Get MAC address and vendor if available
                    if 'mac' in self.nm[host]['addresses']:
                        device_info['mac_address'] = self.nm[host]['addresses']['mac']
                        device_info['vendor'] = self.nm[host]['vendor'].get(
                            self.nm[host]['addresses']['mac'], 'Unknown'
                        )
                    
                    # Try to determine device type based on hostname or other factors
                    if device_info['hostname']:
                        device_info['device_type'] = self.guess_device_type(device_info['hostname'])
                    
                    devices.append(device_info)
                    logger.info(f"Found device: {host} ({device_info['hostname']})")
            
            duration = time.time() - start_time
            logger.info(f"Nmap scan completed in {duration:.2f} seconds. Found {len(devices)} devices.")
            
            return {
                'devices': devices,
                'scan_type': 'nmap',
                'network_range': network_range,
                'duration': duration,
                'devices_found': len(devices)
            }
            
        except Exception as e:
            logger.error(f"Error during nmap scan: {e}")
            # Fallback to ping scan
            logger.info("Falling back to ping scan")
            return self.scan_network_ping(network_range)

    def guess_device_type(self, hostname):
        """Guess device type from hostname"""
        if not hostname:
            return 'Unknown'
            
        hostname_lower = hostname.lower()
        
        # Router patterns
        if any(pattern in hostname_lower for pattern in ['router', 'gateway', 'rt-', 'linksys', 'netgear', 'dlink']):
            return 'Router'
        
        # Printer patterns
        if any(pattern in hostname_lower for pattern in ['printer', 'print', 'hp-', 'canon', 'epson', 'brother']):
            return 'Printer'
        
        # Mobile device patterns
        if any(pattern in hostname_lower for pattern in ['iphone', 'android', 'mobile', 'phone']):
            return 'Mobile Device'
        
        # Computer patterns
        if any(pattern in hostname_lower for pattern in ['desktop', 'laptop', 'pc-', 'workstation']):
            return 'Computer'
        
        # Smart TV patterns
        if any(pattern in hostname_lower for pattern in ['tv', 'roku', 'chromecast', 'appletv']):
            return 'Smart TV'
        
        # IoT devices
        if any(pattern in hostname_lower for pattern in ['nest', 'alexa', 'echo', 'iot', 'smart']):
            return 'IoT Device'
        
        return 'Unknown'

    def scan_single_device(self, ip_address):
        """Scan a single device for detailed information"""
        try:
            # First, check if device is online
            ping_result = self.ping_host(ip_address)
            
            if ping_result['status'] == 'offline':
                return {
                    'ip_address': ip_address,
                    'status': 'offline',
                    'response_time': None
                }
            
            # Get basic info
            device_info = {
                'ip_address': ip_address,
                'hostname': self.get_hostname(ip_address),
                'status': ping_result['status'],
                'response_time': ping_result['response_time'],
                'mac_address': None,
                'vendor': None,
                'device_type': 'Unknown'
            }
            
            # Try to get more details with nmap (lightweight scan)
            if self.nmap_available and self.nm is not None:
                try:
                    self.nm.scan(hosts=ip_address, arguments='-sn')
                    if ip_address in self.nm.all_hosts():
                        host = self.nm[ip_address]
                        if 'mac' in host['addresses']:
                            device_info['mac_address'] = host['addresses']['mac']
                            device_info['vendor'] = host['vendor'].get(
                                host['addresses']['mac'], 'Unknown'
                            )
                except Exception as e:
                    logger.debug(f"Nmap scan failed for {ip_address}: {e}")
            
            # Guess device type
            if device_info['hostname']:
                device_info['device_type'] = self.guess_device_type(device_info['hostname'])
            
            return device_info
            
        except Exception as e:
            logger.error(f"Error scanning device {ip_address}: {e}")
            return {
                'ip_address': ip_address,
                'status': 'error',
                'response_time': None
            }

    def get_network_interfaces(self):
        """Get available network interfaces"""
        interfaces = []
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                # Parse Windows ipconfig output
                current_interface = None
                for line in result.stdout.split('\n'):
                    if 'adapter' in line.lower() and ':' in line:
                        current_interface = line.strip()
                    elif 'IPv4 Address' in line and current_interface:
                        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                        if ip_match:
                            ip = ip_match.group(1)
                            network = ipaddress.IPv4Network(f"{ip}/24", strict=False)
                            interfaces.append({
                                'name': current_interface,
                                'ip': ip,
                                'network': str(network)
                            })
            else:
                result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                # Parse Unix/Linux ifconfig output (simplified)
                pass
                
        except Exception as e:
            logger.error(f"Error getting network interfaces: {e}")
        
        return interfaces

class DeviceMonitor:
    """Background monitoring service for device status"""
    
    def __init__(self, database_manager):
        self.db = database_manager
        self.scanner = NetworkScanner()
        self.is_monitoring = False
        self.monitor_thread = None
        self.check_interval = 300  # 5 minutes
        
    def start_monitoring(self):
        """Start background monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("Device monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Device monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                self.check_all_devices()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)  # Short sleep before retry
    
    def check_all_devices(self):
        """Check status of all known devices"""
        devices = self.db.get_all_devices()
        
        logger.info(f"Checking status of {len(devices)} devices")
        
        for device in devices:
            if not self.is_monitoring:
                break
                
            try:
                result = self.scanner.ping_host(device['ip_address'], timeout=3)
                self.db.log_device_status(
                    device['id'],
                    result['status'],
                    result['response_time']
                )
            except Exception as e:
                logger.error(f"Error checking device {device['ip_address']}: {e}")
        
        logger.info("Device status check completed")