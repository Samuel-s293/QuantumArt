from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from PIL import Image, ImageFilter
import colorsys
import time

# --- Configuration ---
FINAL_WIDTH = 800
FINAL_HEIGHT = 600
FILENAME = "quantum_nebula.png"

# The size of our quantum anchor grid. 
# Smaller grid = larger, smoother clouds of color.
# Larger grid = more complex, tighter patches of color.
GRID_W = 4
GRID_H = 3
# ---------------------

def get_quantum_nums(amount):
    """Generates a batch of quantum random floats between 0.0 and 1.0."""
    print(f"Initializing quantum circuit to generate {amount} numbers...")
    num_qubits = 10
    qc = QuantumCircuit(num_qubits, num_qubits)
    
    for i in range(num_qubits):
        qc.h(i)
        
    qc.measure(range(num_qubits), range(num_qubits))
    
    backend = AerSimulator()
    job = backend.run(qc, shots=amount, memory=True)
    measurements = job.result().get_memory()
    
    # Convert binary strings to floats between 0.0 and 1.0
    quantum_floats = [int(bitstring, 2) / (2**num_qubits - 1) for bitstring in measurements]
    return quantum_floats

def generate_nebula():
    start_time = time.time()
    
    # We need 3 quantum numbers (Hue, Saturation, Value) for every pixel in our tiny grid
    total_anchors = GRID_W * GRID_H
    numbers_needed = total_anchors * 3
    q_entropy = get_quantum_nums(numbers_needed)
    
    print(f"Generating quantum anchor grid ({GRID_W}x{GRID_H})...")
    
    # 1. Create the tiny base image
    base_img = Image.new('RGB', (GRID_W, GRID_H))
    pixels = base_img.load()
    
    # 2. Assign vibrant quantum colors to the tiny grid
    idx = 0
    for x in range(GRID_W):
        for y in range(GRID_H):
            # Hue: Any color on the rainbow (0.0 to 1.0)
            hue = q_entropy[idx]
            
            # Saturation: Keep it between 0.7 and 1.0 so colors are fiercely bright, not washed out
            saturation = 0.7 + (q_entropy[idx+1] * 0.3)
            
            # Value (Brightness): Keep it between 0.8 and 1.0 so it glows brightly
            value = 0.8 + (q_entropy[idx+2] * 0.2)
            
            # Convert HSV to RGB
            r_float, g_float, b_float = colorsys.hsv_to_rgb(hue, saturation, value)
            pixels[x, y] = (int(r_float * 255), int(g_float * 255), int(b_float * 255))
            
            idx += 3

    print(f"Upscaling and smoothing to {FINAL_WIDTH}x{FINAL_HEIGHT}...")

    # 3. Upscale the image using Bicubic interpolation 
    # This forces the computer to calculate incredibly smooth gradients between our quantum pixels
    upscaled_img = base_img.resize(
        (FINAL_WIDTH, FINAL_HEIGHT), 
        resample=Image.Resampling.BICUBIC
    )
    
    # 4. Apply a Gaussian Blur to perfectly melt the colors together
    # A radius of 20 to 50 is usually perfect for a dreamy, nebulous look
    final_img = upscaled_img.filter(ImageFilter.GaussianBlur(radius=30))
    
    final_img.save(FILENAME)
    end_time = time.time()
    print(f"Success! Masterpiece saved to {FILENAME} in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    generate_nebula()