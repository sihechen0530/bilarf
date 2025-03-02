from safetensors.torch import load_file
import torch
import numpy as np
from scipy.spatial.distance import cosine

# Function to load and flatten weights from a .safetensors file
def extract_flattened_weights(filepath):
    state_dict = load_file(filepath)  # Load safetensors
    weights = [tensor.flatten().numpy() for tensor in state_dict.values()]
    return np.concatenate(weights)  # Merge all weights into a single vector

# Load two model checkpoints
vec1 = extract_flattened_weights("/work/SuperResolutionData/sihe.chen/lognerf/GPLog/GX010416_TrueLog/checkpoints/025000/model.safetensors")
vec2 = extract_flattened_weights("/work/SuperResolutionData/sihe.chen/lognerf/GPLog/GX010416_sRGB/checkpoints/025000/model.safetensors")

# Compute cosine distance
cos_dist = cosine(vec1, vec2)
print(f"Cosine Distance: {cos_dist}")

