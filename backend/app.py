from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from .signal_processor import SignalProcessor

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize signal processor with 100 receivers
signal_processor = SignalProcessor(size=100, initial_range=(20, 80))

@app.route('/api/status', methods=['GET'])
def status():
    """API status check"""
    return jsonify({
        'status': 'online',
        'message': 'Deep Space Dominator 3000 is operational',
        'receivers': signal_processor.size
    })

@app.route('/api/receivers', methods=['GET'])
def get_receivers():
    """Get all receiver data"""
    return jsonify({
        'receivers': signal_processor.get_receiver_data(),
        'size': signal_processor.size
    })

@app.route('/api/update', methods=['POST'])
def update_receiver():
    """Update a single receiver"""
    data = request.json
    index = data.get('index')
    value = data.get('value')
    
    if index is None or value is None:
        return jsonify({'error': 'Missing index or value'}), 400
    
    success = signal_processor.update(index, value)
    if success:
        return jsonify({
            'success': True,
            'message': f'Receiver {index} updated to {value}'
        })
    else:
        return jsonify({'error': 'Invalid index'}), 400

@app.route('/api/query', methods=['POST'])
def query_range():
    """Query statistics for a range"""
    data = request.json
    L = data.get('L')
    R = data.get('R')
    
    if L is None or R is None:
        return jsonify({'error': 'Missing range parameters'}), 400
    
    stats = signal_processor.query(L, R)
    if stats:
        return jsonify({
            'success': True,
            'range': f'[{L}, {R}]',
            'statistics': stats
        })
    else:
        return jsonify({'error': 'Invalid range'}), 400

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Run a simulation step"""
    data = request.json
    steps = data.get('steps', 1)
    
    results = []
    for _ in range(steps):
        # Random update
        idx, val = signal_processor.random_update()
        
        # Random query
        L, R, stats = signal_processor.random_query()
        
        results.append({
            'update': {'index': idx, 'value': val},
            'query': {'L': L, 'R': R, 'statistics': stats}
        })
    
    return jsonify({
        'success': True,
        'steps': results,
        'receivers': signal_processor.get_receiver_data(),
        'logs': signal_processor.signal_history[-10:]  # Last 10 logs
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get signal detection history"""
    return jsonify({
        'logs': signal_processor.signal_history
    })

@app.route('/api/heatmap', methods=['GET'])
def get_heatmap():
    """Get heatmap data"""
    heatmap = signal_processor.get_signal_heatmap()
    if heatmap is not None:
        return jsonify({
            'success': True,
            'heatmap': heatmap.tolist()
        })
    else:
        return jsonify({'error': 'Cannot generate heatmap'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
