# backend/signal_processor.py
import random
import numpy as np
from datetime import datetime
import sys
import os

# Fix import for both running as script and as module
try:
    from backend.segnment_tree import SegmentTree
except ImportError:
    try:
        from segnment_tree import SegmentTree
    except ImportError:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from backend.segnment_tree import SegmentTree

class SignalProcessor:
    def __init__(self, size=100, initial_range=(0, 100)):
        self.size = size
        # Initialize with random cosmic signal data
        self.receivers = [random.randint(initial_range[0], initial_range[1]) 
                         for _ in range(size)]
        self.segment_tree = SegmentTree(self.receivers)
        self.signal_history = []
        self.detection_threshold = 500
        
    def update(self, index, value):
        """Update receiver intensity"""
        if 0 <= index < self.size:
            old_value = self.receivers[index]
            self.receivers[index] = value
            self.segment_tree.update(index, value)
            
            # Log significant changes
            if abs(value - old_value) > 50:
                self._log_event(f"Significant change at receiver {index}: {old_value} → {value}")
            
            return True
        return False
    
    def query(self, L, R):
        """Query statistics for range [L, R]"""
        if 0 <= L <= R < self.size:
            stats = self.segment_tree.get_statistics(L, R)
            
            # Check for cosmic signal detection
            if stats['variance'] > self.detection_threshold:
                self._log_event(f"⚠ COSMIC SIGNAL DETECTED in receivers [{L}-{R}]!")
            
            return stats
        return None
    
    def random_update(self):
        """Simulate random cosmic noise updates"""
        index = random.randint(0, self.size - 1)
        # Cosmic signals can cause sudden spikes
        if random.random() < 0.1:  # 10% chance of cosmic event
            new_value = random.randint(500, 1000)  # High intensity spike
        else:
            new_value = random.randint(0, 100)  # Normal background noise
        
        self.update(index, new_value)
        return index, new_value
    
    def random_query(self):
        """Generate random query range"""
        L = random.randint(0, self.size - 10)
        R = random.randint(L, min(L + 20, self.size - 1))
        return L, R, self.query(L, R)
    
    def _log_event(self, message):
        """Log significant events"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}"
        self.signal_history.append(log_entry)
        # Keep only last 100 logs
        if len(self.signal_history) > 100:
            self.signal_history.pop(0)
        print(log_entry)  # Also print to console
    
    def get_receiver_data(self):
        """Get current receiver intensities"""
        return self.receivers.copy()
    
    def get_signal_heatmap(self):
        """Generate heatmap data for visualization"""
        # Check if size is a perfect square
        grid_size = int(np.sqrt(self.size))
        if grid_size * grid_size == self.size:
            # For newer numpy versions
            return np.array(self.receivers).reshape(grid_size, grid_size)
        else:
            # If not perfect square, return a reshaped array with padding
            # or return None with a message
            print(f"Warning: Size {self.size} is not a perfect square for heatmap")
            return None
