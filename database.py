import sqlite3
import datetime
from contextlib import contextmanager

DATABASE = 'network_devices.db'

class DatabaseManager:
    def __init__(self, db_path=DATABASE):
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_database(self):
        """Initialize the database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Device groups table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS device_groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    color TEXT DEFAULT '#007bff',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Devices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT UNIQUE NOT NULL,
                    hostname TEXT,
                    mac_address TEXT,
                    vendor TEXT,
                    device_type TEXT,
                    custom_name TEXT,
                    notes TEXT,
                    group_id INTEGER,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (group_id) REFERENCES device_groups (id)
                )
            ''')
            
            # Status logs table for historical tracking
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS status_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    response_time REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (device_id) REFERENCES devices (id)
                )
            ''')
            
            # Network scan history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_type TEXT NOT NULL,
                    network_range TEXT,
                    devices_found INTEGER DEFAULT 0,
                    duration REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            # Insert default device group if not exists
            cursor.execute("SELECT COUNT(*) FROM device_groups WHERE name = 'Default'")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO device_groups (name, description, color)
                    VALUES ('Default', 'Default group for uncategorized devices', '#6c757d')
                """)
                conn.commit()

    def add_device(self, ip_address, hostname=None, mac_address=None, vendor=None, device_type=None):
        """Add a new device or update existing one"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if device exists
            cursor.execute("SELECT id FROM devices WHERE ip_address = ?", (ip_address,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing device
                cursor.execute("""
                    UPDATE devices 
                    SET hostname = COALESCE(?, hostname),
                        mac_address = COALESCE(?, mac_address),
                        vendor = COALESCE(?, vendor),
                        device_type = COALESCE(?, device_type),
                        last_seen = CURRENT_TIMESTAMP,
                        is_active = 1
                    WHERE ip_address = ?
                """, (hostname, mac_address, vendor, device_type, ip_address))
                device_id = existing[0]
            else:
                # Get default group ID
                cursor.execute("SELECT id FROM device_groups WHERE name = 'Default'")
                default_group = cursor.fetchone()[0]
                
                # Insert new device
                cursor.execute("""
                    INSERT INTO devices (ip_address, hostname, mac_address, vendor, device_type, group_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (ip_address, hostname, mac_address, vendor, device_type, default_group))
                device_id = cursor.lastrowid
            
            conn.commit()
            return device_id

    def log_device_status(self, device_id, status, response_time=None):
        """Log device status check result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO status_logs (device_id, status, response_time)
                VALUES (?, ?, ?)
            """, (device_id, status, response_time))
            
            # Update device's last_seen if online
            if status == 'online':
                cursor.execute("""
                    UPDATE devices SET last_seen = CURRENT_TIMESTAMP, is_active = 1
                    WHERE id = ?
                """, (device_id,))
            else:
                cursor.execute("""
                    UPDATE devices SET is_active = 0 WHERE id = ?
                """, (device_id,))
            
            conn.commit()

    def get_all_devices(self):
        """Get all devices with their group information"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.*, g.name as group_name, g.color as group_color
                FROM devices d
                LEFT JOIN device_groups g ON d.group_id = g.id
                ORDER BY d.ip_address
            """)
            return [dict(row) for row in cursor.fetchall()]

    def search_devices(self, query):
        """Search devices by IP, hostname, or custom name"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT d.*, g.name as group_name, g.color as group_color
                FROM devices d
                LEFT JOIN device_groups g ON d.group_id = g.id
                WHERE d.ip_address LIKE ? OR d.hostname LIKE ? OR d.custom_name LIKE ?
                ORDER BY d.ip_address
            """, (search_pattern, search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]

    def get_device_by_ip(self, ip_address):
        """Get device by IP address"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.*, g.name as group_name, g.color as group_color
                FROM devices d
                LEFT JOIN device_groups g ON d.group_id = g.id
                WHERE d.ip_address = ?
            """, (ip_address,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_device(self, device_id, custom_name=None, notes=None, group_id=None):
        """Update device custom information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE devices 
                SET custom_name = COALESCE(?, custom_name),
                    notes = COALESCE(?, notes),
                    group_id = COALESCE(?, group_id)
                WHERE id = ?
            """, (custom_name, notes, group_id, device_id))
            conn.commit()

    def get_device_groups(self):
        """Get all device groups"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM device_groups ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def add_device_group(self, name, description=None, color='#007bff'):
        """Add a new device group"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO device_groups (name, description, color)
                VALUES (?, ?, ?)
            """, (name, description, color))
            conn.commit()
            return cursor.lastrowid

    def get_device_status_history(self, device_id, limit=50):
        """Get status history for a device"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM status_logs 
                WHERE device_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (device_id, limit))
            return [dict(row) for row in cursor.fetchall()]

    def get_network_statistics(self):
        """Get network statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total devices
            cursor.execute("SELECT COUNT(*) as total FROM devices")
            total_devices = cursor.fetchone()[0]
            
            # Active devices
            cursor.execute("SELECT COUNT(*) as active FROM devices WHERE is_active = 1")
            active_devices = cursor.fetchone()[0]
            
            # Devices by group
            cursor.execute("""
                SELECT g.name, COUNT(d.id) as count, g.color
                FROM device_groups g
                LEFT JOIN devices d ON g.id = d.group_id
                GROUP BY g.id, g.name, g.color
                ORDER BY count DESC
            """)
            devices_by_group = [
                {'name': row[0], 'count': row[1], 'color': row[2]}
                for row in cursor.fetchall()
            ]
            
            # Recent status changes
            cursor.execute("""
                SELECT d.ip_address, d.hostname, d.custom_name, sl.status, sl.timestamp
                FROM status_logs sl
                JOIN devices d ON sl.device_id = d.id
                ORDER BY sl.timestamp DESC
                LIMIT 10
            """)
            recent_changes = [
                {
                    'ip_address': row[0],
                    'hostname': row[1],
                    'custom_name': row[2],
                    'status': row[3],
                    'timestamp': row[4]
                }
                for row in cursor.fetchall()
            ]
            
            return {
                'total_devices': total_devices,
                'active_devices': active_devices,
                'offline_devices': total_devices - active_devices,
                'devices_by_group': devices_by_group,
                'recent_changes': recent_changes
            }

    def cleanup_old_logs(self, days=30):
        """Clean up old status logs"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
            cursor.execute("""
                DELETE FROM status_logs 
                WHERE timestamp < ? AND id NOT IN (
                    SELECT MAX(id) FROM status_logs GROUP BY device_id
                )
            """, (cutoff_date,))
            deleted = cursor.rowcount
            conn.commit()
            return deleted