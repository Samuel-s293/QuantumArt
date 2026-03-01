from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from PIL import Image, ImageDraw

def get_quantum_nums(amount):
    """Generates a batch of true quantum random numbers between 0 and 1023."""
    print(f"Initialising quantum circuit to generate {amount} numbers...")
    
    # Create a circuit with 10 qubits and 10 classical bits
    qc = QuantumCircuit(10, 10)
    
    # Apply a Hadamard gate to put all 10 qubits into superposition
    for i in range(10):
        qc.h(i)
        
    # Measure the qubits
    qc.measure(range(10), range(10))
    
    # Run the simulation
    simulator = AerSimulator()
    # 'memory=True' tells Qiskit to remember every individual shot, not just the averages
    job = simulator.run(qc, shots=amount, memory=True)
    measurements = job.result().get_memory()
    
    # Convert the binary strings (e.g., '1011001110') to integers
    quantum_numbers = [int(bitstring, 2) for bitstring in measurements]
    return quantum_numbers
