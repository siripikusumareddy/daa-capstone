import math

class SegmentTree:
    """
    Segment Tree implementation for range queries and point updates
    Supports: Min, Max, Sum, Sum of Squares (for variance calculation)
    """
    
    def __init__(self, data):
        self.n = len(data)
        self.data = data.copy()
        
        # Size of segment tree (4*n is safe)
        self.min_tree = [0] * (4 * self.n)
        self.max_tree = [0] * (4 * self.n)
        self.sum_tree = [0] * (4 * self.n)
        self.sum_sq_tree = [0] * (4 * self.n)
        
        self._build(1, 0, self.n - 1)
    
    def _build(self, node, left, right):
        """Build the segment tree"""
        if left == right:
            self.min_tree[node] = self.data[left]
            self.max_tree[node] = self.data[left]
            self.sum_tree[node] = self.data[left]
            self.sum_sq_tree[node] = self.data[left] * self.data[left]
            return
        
        mid = (left + right) // 2
        self._build(node * 2, left, mid)
        self._build(node * 2 + 1, mid + 1, right)
        
        self._merge(node)
    
    def _merge(self, node):
        """Merge children results"""
        self.min_tree[node] = min(self.min_tree[node * 2], self.min_tree[node * 2 + 1])
        self.max_tree[node] = max(self.max_tree[node * 2], self.max_tree[node * 2 + 1])
        self.sum_tree[node] = self.sum_tree[node * 2] + self.sum_tree[node * 2 + 1]
        self.sum_sq_tree[node] = self.sum_sq_tree[node * 2] + self.sum_sq_tree[node * 2 + 1]
    
    def update(self, index, new_value):
        """Update value at index"""
        self._update(1, 0, self.n - 1, index, new_value)
        self.data[index] = new_value
    
    def _update(self, node, left, right, index, new_value):
        """Internal update function"""
        if left == right:
            self.min_tree[node] = new_value
            self.max_tree[node] = new_value
            self.sum_tree[node] = new_value
            self.sum_sq_tree[node] = new_value * new_value
            return
        
        mid = (left + right) // 2
        if index <= mid:
            self._update(node * 2, left, mid, index, new_value)
        else:
            self._update(node * 2 + 1, mid + 1, right, index, new_value)
        
        self._merge(node)
    
    def query(self, ql, qr):
        """Query range [ql, qr] - returns (min, max, sum, sum_sq)"""
        result = self._query(1, 0, self.n - 1, ql, qr)
        return result
    
    def _query(self, node, left, right, ql, qr):
        """Internal query function"""
        if ql <= left and right <= qr:
            return (self.min_tree[node], 
                   self.max_tree[node], 
                   self.sum_tree[node], 
                   self.sum_sq_tree[node])
        
        mid = (left + right) // 2
        
        if qr <= mid:
            return self._query(node * 2, left, mid, ql, qr)
        elif ql > mid:
            return self._query(node * 2 + 1, mid + 1, right, ql, qr)
        else:
            left_res = self._query(node * 2, left, mid, ql, qr)
            right_res = self._query(node * 2 + 1, mid + 1, right, ql, qr)
            
            return (min(left_res[0], right_res[0]),
                   max(left_res[1], right_res[1]),
                   left_res[2] + right_res[2],
                   left_res[3] + right_res[3])
    
    def get_statistics(self, ql, qr):
        """Get min, max, mean, variance for range [ql, qr]"""
        _min, _max, _sum, _sum_sq = self.query(ql, qr)
        count = qr - ql + 1
        mean = _sum / count
        
        # Variance = E[X²] - (E[X])²
        variance = (_sum_sq / count) - (mean * mean)
        
        return {
            'min': _min,
            'max': _max,
            'mean': round(mean, 2),
            'variance': round(variance, 2)
        }
