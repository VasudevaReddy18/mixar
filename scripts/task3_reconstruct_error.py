import os
import numpy as np
import matplotlib.pyplot as plt
from mesh_utils import (
    load_mesh,
    minmax_normalize,
    unit_sphere_normalize,
    quantize,
    dequantize,
    denormalize_minmax,
    denormalize_unit_sphere,
)

mesh_folder = "meshes"
out_plots = os.path.join("outputs", "plots")
os.makedirs(out_plots, exist_ok=True)

bins = 1024  

def mse(a, b):
    return np.mean((a - b) ** 2, axis=0)

def mae(a, b):
    return np.mean(np.abs(a - b), axis=0)

results = []

for fname in sorted(os.listdir(mesh_folder)):
    if not fname.lower().endswith(".obj"):
        continue

    print(f"Processing {fname}")
    mesh = load_mesh(os.path.join(mesh_folder, fname))
    verts = mesh.vertices.copy()

    # --- Min–Max pipeline ---
    norm_mm, vmin, vmax = minmax_normalize(verts)
    q_mm = quantize(norm_mm, n_bins=bins)
    deq_mm = dequantize(q_mm, n_bins=bins)
    recon_mm = denormalize_minmax(deq_mm, vmin, vmax)

    # --- Unit-Sphere pipeline ---
    norm_us, centroid, max_dist = unit_sphere_normalize(verts)
    mapped = (norm_us + 1) / 2
    q_us = quantize(mapped, n_bins=bins)
    deq_us = dequantize(q_us, n_bins=bins)
    deq_us = deq_us * 2 - 1
    recon_us = denormalize_unit_sphere(deq_us, centroid, max_dist)

    # --- Errors ---
    mse_mm = mse(verts, recon_mm)
    mse_us = mse(verts, recon_us)
    mae_mm = mae(verts, recon_mm)
    mae_us = mae(verts, recon_us)

    results.append((fname, mse_mm, mse_us, mae_mm, mae_us))

    axes = ["x", "y", "z"]
    plt.figure(figsize=(6, 4))
    plt.bar(np.arange(3) - 0.15, mse_mm, width=0.3, label="Min–Max")
    plt.bar(np.arange(3) + 0.15, mse_us, width=0.3, label="Unit-Sphere")
    plt.xticks(range(3), axes)
    plt.ylabel("MSE")
    plt.title(f"Reconstruction Error: {fname}")
    plt.legend()
    plt.tight_layout()
    plot_path = os.path.join(out_plots, fname.replace(".obj", "_mse.png"))
    plt.savefig(plot_path)
    plt.close()

import csv
with open(os.path.join("outputs", "error_summary.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "file",
        "mse_mm_x", "mse_mm_y", "mse_mm_z",
        "mse_us_x", "mse_us_y", "mse_us_z",
        "mae_mm_x", "mae_mm_y", "mae_mm_z",
        "mae_us_x", "mae_us_y", "mae_us_z"
    ])
    for fname, mse_mm, mse_us, mae_mm, mae_us in results:
        writer.writerow([fname] + mse_mm.tolist() + mse_us.tolist() + mae_mm.tolist() + mae_us.tolist())

print("Task 3 complete — plots in outputs/plots and CSV summary in outputs/error_summary.csv")
