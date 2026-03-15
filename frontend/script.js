// API Configuration
const API_BASE = 'http://localhost:5000/api';

// Chart instances
let autoSimInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    checkStatus();
    loadReceiverData();
    loadHistory();
    
    // Set up periodic updates
    setInterval(loadReceiverData, 2000);
    setInterval(loadHistory, 3000);
});

// Check API status
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        document.getElementById('status-badge').textContent = '● Online';
        document.getElementById('status-badge').style.color = '#00ff88';
    } catch (error) {
        document.getElementById('status-badge').textContent = '● Offline';
        document.getElementById('status-badge').style.color = '#ff4444';
        console.error('API offline:', error);
    }
}

// Load receiver data and update heatmap
async function loadReceiverData() {
    try {
        const response = await fetch(`${API_BASE}/receivers`);
        const data = await response.json();
        updateHeatmap(data.receivers);
    } catch (error) {
        console.error('Failed to load receiver data:', error);
    }
}

// Manual update
async function manualUpdate() {
    const index = document.getElementById('update-index').value;
    const value = document.getElementById('update-value').value;
    
    try {
        const response = await fetch(`${API_BASE}/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ index: parseInt(index), value: parseInt(value) })
        });
        
        const data = await response.json();
        if (data.success) {
            addLogEntry(`Manual update: ${data.message}`);
            loadReceiverData();
        }
    } catch (error) {
        console.error('Update failed:', error);
        addLogEntry('❌ Update failed');
    }
}

// Manual query
async function manualQuery() {
    const L = document.getElementById('query-start').value;
    const R = document.getElementById('query-end').value;
    
    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ L: parseInt(L), R: parseInt(R) })
        });
        
        const data = await response.json();
        if (data.success) {
            displayQueryResults(data.range, data.statistics);
            addLogEntry(`Query [${L}-${R}]: Min=${data.statistics.min}, Max=${data.statistics.max}, Mean=${data.statistics.mean}`);
        }
    } catch (error) {
        console.error('Query failed:', error);
        addLogEntry('❌ Query failed');
    }
}

// Display query results
function displayQueryResults(range, stats) {
    document.getElementById('range-display').textContent = range;
    document.getElementById('min-display').textContent = stats.min;
    document.getElementById('max-display').textContent = stats.max;
    document.getElementById('mean-display').textContent = stats.mean;
    document.getElementById('variance-display').textContent = stats.variance;
    
    // Check for cosmic signal
    if (stats.variance > 500) {
        document.getElementById('variance-display').style.color = '#ff4444';
        addLogEntry(`⚠ COSMIC SIGNAL DETECTED in range ${range}!`);
    } else {
        document.getElementById('variance-display').style.color = '#00d4ff';
    }
}

// Run simulation step
async function runSimulation() {
    try {
        const response = await fetch(`${API_BASE}/simulate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ steps: 1 })
        });
        
        const data = await response.json();
        if (data.success) {
            loadReceiverData();
            data.logs.forEach(log => addLogEntry(log));
            updateHeatmap(data.receivers);
        }
    } catch (error) {
        console.error('Simulation failed:', error);
    }
}

// Start auto simulation
function startAutoSim() {
    autoSimInterval = setInterval(runSimulation, 1000);
    document.getElementById('auto-btn').disabled = true;
    document.getElementById('stop-btn').disabled = false;
    addLogEntry('▶ Auto simulation started');
}

// Stop auto simulation
function stopAutoSim() {
    if (autoSimInterval) {
        clearInterval(autoSimInterval);
        autoSimInterval = null;
    }
    document.getElementById('auto-btn').disabled = false;
    document.getElementById('stop-btn').disabled = true;
    addLogEntry('⏸ Auto simulation stopped');
}

// Load event history
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/history`);
        const data = await response.json();
        
        const logContainer = document.getElementById('event-log');
        logContainer.innerHTML = '';
        
        data.logs.slice().reverse().forEach(log => {
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            
            if (log.includes('COSMIC')) {
                logEntry.style.color = '#ff4444';
                logEntry.style.fontWeight = 'bold';
            } else if (log.includes('significant')) {
                logEntry.style.color = '#ffaa00';
            }
            
            logEntry.textContent = log;
            logContainer.appendChild(logEntry);
        });
        
        logContainer.scrollTop = logContainer.scrollHeight;
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// Add a single log entry
function addLogEntry(message) {
    const logContainer = document.getElementById('event-log');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    
    const timestamp = new Date().toLocaleTimeString('en-US', { 
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    logEntry.textContent = `[${timestamp}] ${message}`;
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Update heatmap
function updateHeatmap(receivers) {
    const canvas = document.getElementById('heatmap-canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = 300;
    canvas.height = 300;
    
    const size = 10;
    const cellSize = canvas.width / size;
    
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const index = i * size + j;
            const value = receivers[index];
            
            const intensity = Math.min(value / 500, 1);
            const r = Math.floor(255 * intensity);
            const b = Math.floor(255 * (1 - intensity));
            const g = Math.floor(100 * (1 - Math.abs(intensity - 0.5) * 2));
            
            ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
            ctx.fillRect(j * cellSize, i * cellSize, cellSize - 1, cellSize - 1);
            
            ctx.strokeStyle = '#1a1f2f';
            ctx.strokeRect(j * cellSize, i * cellSize, cellSize, cellSize);
        }
    }
}
