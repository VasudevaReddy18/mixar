import numpy as np
import trimesh
import matplotlib.pyplot as plt
import os
from sklearn.neighbors import NearestNeighbors

INPUT_MESH = "meshes/branch.obj"   
OUTPUT_DIR = "outputs/adaptive_quant/"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("outputs/plots", exist_ok=True)

def rotation_matrix(axis, angle):
    """Generate a 3D rotation matrix given an axis and angle (radians)."""
    axis = axis / np.linalg.norm(axis)
    a = np.cos(angle / 2.0)
    b, c, d = -axis * np.sin(angle / 2.0)
    return np.array([
        [a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c)],
        [2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b)],
        [2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c]
    ])


def normalize_invariant(vertices):
    """Center mesh at origin and scale to unit sphere (rotation/translation invariant)."""
    centroid = np.mean(vertices, axis=0)
    centered = vertices - centroid
    scale = np.max(np.linalg.norm(centered, axis=1))
    normalized = centered / scale
    return normalized, centroid, scale


def adaptive_quantize(vertices, base_bins=1024):
    """Apply adaptive quantization: finer bins in dense areas."""
    nbrs = NearestNeighbors(n_neighbors=8).fit(vertices)
    distances, _ = nbrs.kneighbors(vertices)
    local_density = np.mean(distances, axis=1)
    bins = np.clip(base_bins / (local_density / np.mean(local_density)), 256, 2048)
    q_vertices = np.round(vertices * bins[:, None]) / bins[:, None]
    return q_vertices


def mse(a, b):
    """Mean Squared Error."""
    return np.mean((a - b) ** 2)

print("[INFO] Loading mesh:", INPUT_MESH)
mesh = trimesh.load(INPUT_MESH, process=False)
original_vertices = np.array(mesh.vertices)

transforms = [
    ("rot_30", rotation_matrix(np.array([1, 0, 0]), np.radians(30))),
    ("rot_60", rotation_matrix(np.array([0, 1, 0]), np.radians(60))),
]

translations = [
    ("trans_shift", np.array([0.3, 0.2, 0.1])),
]

results = []

for name, transform in transforms + translations:
    print(f"\n[INFO] Processing transformation: {name}")

    if "rot" in name:
        rotated = original_vertices.dot(transform.T)
    else:
        rotated = original_vertices + transform

    normed, centroid, scale = normalize_invariant(rotated)
    uniform_q = np.round(normed * 1024) / 1024
    adaptive_q = adaptive_quantize(normed)

    uniform_recon = (uniform_q * scale) + centroid
    adaptive_recon = (adaptive_q * scale) + centroid

    err_uniform = mse(rotated, uniform_recon)
    err_adaptive = mse(rotated, adaptive_recon)

    results.append((name, err_uniform, err_adaptive))

    adaptive_mesh = mesh.copy()
    adaptive_mesh.vertices = adaptive_recon
    adaptive_mesh.export(os.path.join(OUTPUT_DIR, f"{name}_adaptive.obj"))

names = [r[0] for r in results]
uniform_errors = [r[1] for r in results]
adaptive_errors = [r[2] for r in results]

plt.figure(figsize=(6, 4))
x = np.arange(len(names))
plt.bar(x - 0.15, uniform_errors, width=0.3, label='Uniform')
plt.bar(x + 0.15, adaptive_errors, width=0.3, label='Adaptive')
plt.xticks(x, names)
plt.ylabel("MSE")
plt.title("Adaptive vs Uniform Quantization Error")
plt.legend()
plt.tight_layout()
plot_path = "outputs/plots/adaptive_vs_uniform.png"
plt.savefig(plot_path, dpi=200)
plt.close()

print("\n[RESULTS]")
for name, u, a in results:
    print(f"{name:15s} | Uniform: {u:.6f} | Adaptive: {a:.6f}")

print(f"\n✅ Plot saved to {plot_path}")
print("Adaptive quantized meshes saved")
