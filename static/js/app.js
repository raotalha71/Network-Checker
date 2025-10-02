// Network Dashboard JavaScript Application
class NetworkDashboard {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.deviceUpdateInterval = null;
        
        this.init();
    }
    
    init() {
        // Initialize Socket.IO connection
        this.initSocket();
        
        // Initialize UI components
        this.initUI();
        
        // Start periodic updates
        this.startPeriodicUpdates();
        
        console.log('Network Dashboard initialized');
    }
    
    initSocket() {
        // Only initialize if Socket.IO is available
        if (typeof io !== 'undefined') {
            this.socket = io();
            
            this.socket.on('connect', () => {
                this.isConnected = true;
                this.updateConnectionStatus(true);
                console.log('Connected to server');
            });
            
            this.socket.on('disconnect', () => {
                this.isConnected = false;
                this.updateConnectionStatus(false);
                console.log('Disconnected from server');
            });
            
            this.socket.on('stats_update', (data) => {
                this.updateDashboardStats(data);
            });
            
            this.socket.on('device_status_update', (data) => {
                this.updateDeviceStatus(data.devices);
            });
            
            this.socket.on('scan_status', (data) => {
                if (window.updateScanStatus) {
                    window.updateScanStatus(data);
                }
            });
            
            this.socket.on('scan_progress', (data) => {
                if (window.updateScanProgress) {
                    window.updateScanProgress(data);
                }
            });
        } else {
            console.warn('Socket.IO not available, real-time features disabled');
        }
    }
    
    initUI() {
        // Initialize tooltips
        this.initTooltips();
        
        // Initialize network range validation
        this.initNetworkRangeValidation();
        
        // Initialize device row interactions
        this.initDeviceRows();
    }
    
    initTooltips() {
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }
    
    initNetworkRangeValidation() {
        const networkRangeInput = document.getElementById('networkRange');
        if (networkRangeInput) {
            networkRangeInput.addEventListener('input', (e) => {
                this.validateNetworkRange(e.target);
            });
        }
    }
    
    initDeviceRows() {
        // Add hover effects and click handlers to device rows
        const deviceRows = document.querySelectorAll('.device-row');
        deviceRows.forEach(row => {
            const isActive = row.querySelector('.status-indicator').textContent.includes('Online');
            row.classList.add(isActive ? 'device-online' : 'device-offline');
        });
    }
    
    validateNetworkRange(input) {
        const value = input.value.trim();
        if (!value) {
            input.classList.remove('network-range-valid', 'network-range-invalid');
            return;
        }
        
        // Simple CIDR validation
        const cidrPattern = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;
        if (cidrPattern.test(value)) {
            const [ip, mask] = value.split('/');
            const ipParts = ip.split('.').map(Number);
            const maskNum = parseInt(mask);
            
            const isValidIP = ipParts.every(part => part >= 0 && part <= 255);
            const isValidMask = maskNum >= 0 && maskNum <= 32;
            
            if (isValidIP && isValidMask) {
                input.classList.remove('network-range-invalid');
                input.classList.add('network-range-valid');
                return;
            }
        }
        
        input.classList.remove('network-range-valid');
        input.classList.add('network-range-invalid');
    }
    
    updateConnectionStatus(isConnected) {
        const statusElement = document.getElementById('connectionStatus');
        if (statusElement) {
            if (isConnected) {
                statusElement.className = 'badge bg-success connected';
                statusElement.innerHTML = '<i class="bi bi-wifi"></i> Connected';
            } else {
                statusElement.className = 'badge bg-danger disconnected';
                statusElement.innerHTML = '<i class="bi bi-wifi-off"></i> Disconnected';
            }
        }
    }
    
    updateDashboardStats(stats) {
        // Update statistics cards
        const activeElement = document.getElementById('activeDevices');
        const offlineElement = document.getElementById('offlineDevices');
        
        if (activeElement) activeElement.textContent = stats.active_devices;
        if (offlineElement) offlineElement.textContent = stats.offline_devices;
        
        // Update recent changes if on dashboard
        if (stats.recent_changes && window.updateRecentChanges) {
            window.updateRecentChanges(stats.recent_changes);
        }
    }
    
    updateDeviceStatus(devices) {
        // Update device status indicators in tables
        devices.forEach(device => {
            const row = document.querySelector(`[data-device-id="${device.id}"]`);
            if (row) {
                const statusBadge = row.querySelector('.status-indicator');
                if (statusBadge) {
                    if (device.is_active) {
                        statusBadge.className = 'status-indicator badge bg-success';
                        statusBadge.innerHTML = '<i class="bi bi-check-circle"></i> Online';
                        row.classList.remove('device-offline');
                        row.classList.add('device-online');
                    } else {
                        statusBadge.className = 'status-indicator badge bg-danger';
                        statusBadge.innerHTML = '<i class="bi bi-x-circle"></i> Offline';
                        row.classList.remove('device-online');
                        row.classList.add('device-offline');
                    }
                }
                
                // Update last seen
                const lastSeenCell = row.cells[row.cells.length - 2]; // Assuming last seen is second to last
                if (lastSeenCell && device.last_seen) {
                    const timeElement = lastSeenCell.querySelector('small');
                    if (timeElement && window.moment) {
                        timeElement.textContent = moment(device.last_seen).fromNow();
                    }
                }
            }
        });
    }
    
    startPeriodicUpdates() {
        // Update device status every 30 seconds if not using websockets
        if (!this.socket) {
            this.deviceUpdateInterval = setInterval(() => {
                this.refreshDeviceStatus();
            }, 30000);
        }
    }
    
    refreshDeviceStatus() {
        fetch('/api/devices/status')
            .then(response => response.json())
            .then(devices => {
                this.updateDeviceStatus(devices);
            })
            .catch(error => {
                console.error('Error refreshing device status:', error);
            });
    }
    
    // Utility methods
    showToast(message, type = 'info', duration = 5000) {
        const toastContainer = this.getOrCreateToastContainer();
        
        const bgClass = this.getToastBgClass(type);
        const iconClass = this.getToastIconClass(type);
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white ${bgClass} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconClass}"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        if (typeof bootstrap !== 'undefined') {
            const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: duration });
            bsToast.show();
            
            toast.addEventListener('hidden.bs.toast', () => {
                toastContainer.removeChild(toast);
            });
        } else {
            // Fallback without Bootstrap
            setTimeout(() => {
                if (toastContainer.contains(toast)) {
                    toastContainer.removeChild(toast);
                }
            }, duration);
        }
    }
    
    getOrCreateToastContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }
    
    getToastBgClass(type) {
        switch (type) {
            case 'success': return 'bg-success';
            case 'error': return 'bg-danger';
            case 'warning': return 'bg-warning';
            default: return 'bg-info';
        }
    }
    
    getToastIconClass(type) {
        switch (type) {
            case 'success': return 'bi-check-circle';
            case 'error': return 'bi-x-circle';
            case 'warning': return 'bi-exclamation-triangle';
            default: return 'bi-info-circle';
        }
    }
    
    // API helper methods
    async apiRequest(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, finalOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    // Device management methods
    async checkDeviceStatus(ipAddress) {
        try {
            const result = await this.apiRequest(`/api/device/${ipAddress}/check`, {
                method: 'POST'
            });
            
            this.showToast(
                `Device ${ipAddress} is ${result.status}`,
                result.status === 'online' ? 'success' : 'warning'
            );
            
            return result;
        } catch (error) {
            this.showToast(`Error checking device ${ipAddress}: ${error.message}`, 'error');
            throw error;
        }
    }
    
    async updateDevice(deviceId, data) {
        try {
            const result = await this.apiRequest(`/api/device/${deviceId}/update`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            this.showToast('Device updated successfully', 'success');
            return result;
        } catch (error) {
            this.showToast(`Error updating device: ${error.message}`, 'error');
            throw error;
        }
    }
    
    async addGroup(groupData) {
        try {
            const result = await this.apiRequest('/api/group/add', {
                method: 'POST',
                body: JSON.stringify(groupData)
            });
            
            this.showToast('Group added successfully', 'success');
            return result;
        } catch (error) {
            this.showToast(`Error adding group: ${error.message}`, 'error');
            throw error;
        }
    }
    
    // Cleanup
    destroy() {
        if (this.socket) {
            this.socket.disconnect();
        }
        
        if (this.deviceUpdateInterval) {
            clearInterval(this.deviceUpdateInterval);
        }
    }
}

// Global dashboard instance
let dashboard = null;

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    dashboard = new NetworkDashboard();
    
    // Make dashboard available globally for backward compatibility
    window.dashboard = dashboard;
    window.showToast = (message, type, duration) => dashboard.showToast(message, type, duration);
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (dashboard) {
        dashboard.destroy();
    }
});

// Global utility functions for backward compatibility
window.checkDeviceStatus = function(ipAddress) {
    if (dashboard) {
        const button = event.target.closest('button');
        const icon = button.querySelector('i');
        
        // Show loading
        icon.className = 'bi bi-arrow-repeat';
        button.disabled = true;
        
        dashboard.checkDeviceStatus(ipAddress)
            .finally(() => {
                // Reset button
                icon.className = 'bi bi-arrow-clockwise';
                button.disabled = false;
            });
    }
};

window.refreshStats = function() {
    if (dashboard) {
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                dashboard.updateDashboardStats(data);
            })
            .catch(error => {
                console.error('Error refreshing stats:', error);
                dashboard.showToast('Error refreshing statistics', 'error');
            });
    }
};