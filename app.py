from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import json
from datetime import datetime
import threading
import time
import logging

from database import DatabaseManager
from network_scanner import NetworkScanner, DeviceMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'network_dashboard_secret_key_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize components
db = DatabaseManager()
scanner = NetworkScanner()
monitor = DeviceMonitor(db)

# Global state
scanning_in_progress = False

@app.route('/')
def dashboard():
    """Main dashboard page"""
    stats = db.get_network_statistics()
    devices = db.get_all_devices()
    groups = db.get_device_groups()
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         devices=devices, 
                         groups=groups)

@app.route('/devices')
def devices():
    """Devices listing page"""
    search_query = request.args.get('search', '')
    group_filter = request.args.get('group', '')
    
    if search_query:
        devices_list = db.search_devices(search_query)
    else:
        devices_list = db.get_all_devices()
    
    # Filter by group if specified
    if group_filter:
        devices_list = [d for d in devices_list if str(d['group_id']) == group_filter]
    
    groups = db.get_device_groups()
    
    return render_template('devices.html', 
                         devices=devices_list, 
                         groups=groups,
                         search_query=search_query,
                         group_filter=group_filter)

@app.route('/device/<ip_address>')
def device_detail(ip_address):
    """Device detail page"""
    device = db.get_device_by_ip(ip_address)
    if not device:
        flash('Device not found', 'error')
        return redirect(url_for('devices'))
    
    # Get status history
    status_history = db.get_device_status_history(device['id'])
    groups = db.get_device_groups()
    
    return render_template('device_detail.html', 
                         device=device, 
                         status_history=status_history,
                         groups=groups)

@app.route('/groups')
def groups():
    """Device groups management page"""
    groups_list = db.get_device_groups()
    
    # Get device count for each group
    for group in groups_list:
        devices = db.get_all_devices()
        group['device_count'] = len([d for d in devices if d['group_id'] == group['id']])
    
    return render_template('groups.html', groups=groups_list)

@app.route('/scan')
def scan_page():
    """Network scan page"""
    return render_template('scan.html')

# API Routes
@app.route('/api/scan/start', methods=['POST'])
def start_scan():
    """Start network scan"""
    global scanning_in_progress
    
    if scanning_in_progress:
        return jsonify({'error': 'Scan already in progress'}), 400
    
    scan_type = request.json.get('scan_type', 'ping')
    network_range = request.json.get('network_range', None)
    
    # Start scan in background thread
    def run_scan():
        global scanning_in_progress
        scanning_in_progress = True
        
        try:
            socketio.emit('scan_status', {'status': 'started', 'message': f'Starting {scan_type} scan...'})
            
            if scan_type == 'nmap':
                result = scanner.scan_network_nmap(network_range)
            else:
                result = scanner.scan_network_ping(network_range)
            
            # Save devices to database
            devices_added = 0
            for device_info in result['devices']:
                device_id = db.add_device(
                    device_info['ip_address'],
                    device_info['hostname'],
                    device_info.get('mac_address'),
                    device_info.get('vendor'),
                    device_info.get('device_type')
                )
                
                # Log initial status
                db.log_device_status(
                    device_id,
                    device_info['status'],
                    device_info.get('response_time')
                )
                devices_added += 1
                
                # Emit progress update
                socketio.emit('scan_progress', {
                    'devices_found': devices_added,
                    'current_device': device_info['ip_address']
                })
            
            socketio.emit('scan_status', {
                'status': 'completed',
                'message': f'Scan completed! Found {devices_added} devices.',
                'devices_found': devices_added,
                'duration': result['duration']
            })
            
        except Exception as e:
            logger.error(f"Scan error: {e}")
            socketio.emit('scan_status', {
                'status': 'error',
                'message': f'Scan failed: {str(e)}'
            })
        finally:
            scanning_in_progress = False
    
    threading.Thread(target=run_scan, daemon=True).start()
    
    return jsonify({'message': 'Scan started'})

@app.route('/api/device/<int:device_id>/update', methods=['POST'])
def update_device(device_id):
    """Update device information"""
    data = request.json
    
    try:
        db.update_device(
            device_id,
            custom_name=data.get('custom_name'),
            notes=data.get('notes'),
            group_id=data.get('group_id')
        )
        return jsonify({'message': 'Device updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/device/<ip_address>/check', methods=['POST'])
def check_device_status(ip_address):
    """Check single device status"""
    try:
        device = db.get_device_by_ip(ip_address)
        if not device:
            return jsonify({'error': 'Device not found'}), 404
        
        # Scan device
        result = scanner.scan_single_device(ip_address)
        
        # Log status
        db.log_device_status(
            device['id'],
            result['status'],
            result.get('response_time')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/group/add', methods=['POST'])
def add_group():
    """Add new device group"""
    data = request.json
    
    try:
        group_id = db.add_device_group(
            data['name'],
            data.get('description'),
            data.get('color', '#007bff')
        )
        return jsonify({'message': 'Group added successfully', 'id': group_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get network statistics"""
    try:
        stats = db.get_network_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices/status')
def get_devices_status():
    """Get current status of all devices"""
    try:
        devices = db.get_all_devices()
        device_status = []
        
        for device in devices:
            # Get latest status
            recent_logs = db.get_device_status_history(device['id'], limit=1)
            latest_status = recent_logs[0] if recent_logs else None
            
            device_status.append({
                'id': device['id'],
                'ip_address': device['ip_address'],
                'hostname': device['hostname'],
                'custom_name': device['custom_name'],
                'is_active': bool(device['is_active']),
                'last_seen': device['last_seen'],
                'status': latest_status['status'] if latest_status else 'unknown',
                'response_time': latest_status['response_time'] if latest_status else None
            })
        
        return jsonify(device_status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connection_response', {'message': 'Connected to network dashboard'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')

@socketio.on('request_device_status')
def handle_device_status_request():
    """Send current device status to client"""
    try:
        devices = db.get_all_devices()
        emit('device_status_update', {'devices': [dict(d) for d in devices]})
    except Exception as e:
        logger.error(f"Error sending device status: {e}")

# Background tasks
def status_update_broadcaster():
    """Broadcast status updates to connected clients"""
    while True:
        try:
            if not scanning_in_progress:  # Don't broadcast during scans
                stats = db.get_network_statistics()
                socketio.emit('stats_update', stats)
            time.sleep(30)  # Update every 30 seconds
        except Exception as e:
            logger.error(f"Error broadcasting updates: {e}")
            time.sleep(60)

# Initialize background tasks
def init_background_tasks():
    """Initialize background monitoring and updates"""
    # Start device monitoring
    monitor.start_monitoring()
    
    # Start status broadcaster
    broadcaster_thread = threading.Thread(target=status_update_broadcaster, daemon=True)
    broadcaster_thread.start()
    
    logger.info("Background tasks initialized")

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

if __name__ == '__main__':
    # Initialize background tasks
    init_background_tasks()
    
    # Run the application
    logger.info("Starting Network Device Dashboard")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)