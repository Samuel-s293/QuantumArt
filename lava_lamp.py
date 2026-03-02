from flask import Flask, jsonify, render_template
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import colorsys

app = Flask(__name__)
backend = AerSimulator()

# Configuration
NUM_BLOBS = 30 

def get_quantum_batch(requested_quantity):
    """Generates quantum random floats in [0.0, 1.0]."""
    num_qubits = 12 
    quantum_circuit = QuantumCircuit(num_qubits, num_qubits)
    for qubit_index in range(num_qubits): 
        quantum_circuit.h(qubit_index)
    quantum_circuit.measure(range(num_qubits), range(num_qubits))
    
    compiled_circuit = transpile(quantum_circuit, backend)
    shots_required = max(requested_quantity, 128) 
    
    job_result = backend.run(compiled_circuit, shots=shots_required, memory=True).result()
    measured_bitstrings = job_result.get_memory()
    
    selected_bitstrings = measured_bitstrings[:requested_quantity]
    max_integer_value = (2**num_qubits) - 1
    
    return [int(bitstring, 2) / max_integer_value for bitstring in selected_bitstrings]

@app.route('/api/init_liquid')
def init_liquid():
    random_floats_required = NUM_BLOBS * 7
    quantum_random_floats = get_quantum_batch(random_floats_required)
    
    liquid_blobs = []
    float_index = 0
    
    for blob_id in range(NUM_BLOBS):
        normalized_x = 0.3 + (quantum_random_floats[float_index] * 0.4) 
        normalized_y = 0.3 + (quantum_random_floats[float_index+1] * 0.4)
        velocity_x = (quantum_random_floats[float_index+2] - 0.5) * 0.008
        velocity_y = (quantum_random_floats[float_index+3] - 0.5) * 0.008
        blob_radius = 60 + (quantum_random_floats[float_index+4] * 100)
        
        initial_hue = quantum_random_floats[float_index+5]
        initial_saturation = 0.6 + (quantum_random_floats[float_index+6] * 0.4)
        
        liquid_blobs.append({
            'id': blob_id,
            'x': normalized_x, 'y': normalized_y, 
            'vx': velocity_x, 'vy': velocity_y, 'radius': blob_radius,
            'hue': initial_hue, 
            'saturation': initial_saturation,
        })
        float_index += 7
        
    return jsonify({'blobs': liquid_blobs, 'entropy_used': random_floats_required})

@app.route('/api/stream_updates')
def stream_updates():
    """Streams target colors and destinations."""
    random_floats_required = NUM_BLOBS * 5
    quantum_random_floats = get_quantum_batch(random_floats_required)
    
    blob_updates = []
    float_index = 0
    
    for blob_id in range(NUM_BLOBS):
        blob_updates.append({
            'id': blob_id,
            'target_hue': quantum_random_floats[float_index],
            'target_sat': 0.6 + (quantum_random_floats[float_index+1] * 0.4),
            'lerp_speed': 0.005 + (quantum_random_floats[float_index+2] * 0.015),
            'target_x_norm': -0.1 + (quantum_random_floats[float_index+3] * 1.2),
            'target_y_norm': -0.1 + (quantum_random_floats[float_index+4] * 1.2)
        })
        float_index += 5
        
    return jsonify({'updates': blob_updates})

@app.route('/')
def index():
    # Serve main UI
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=True)