import os
import numpy as np
from mesh_utils import (
    load_mesh,
    minmax_normalize,
    unit_sphere_normalize,
    quantize,
    save_vertices_as_obj,
)

mesh_folder = "meshes"
out_norm = os.path.join("outputs", "normalized")
out_quant = os.path.join("outputs", "quantized")
os.makedirs(out_norm, exist_ok=True)
os.makedirs(out_quant, exist_ok=True)

bins = 1024

for fname in sorted(os.listdir(mesh_folder)):
    if not fname.lower().endswith(".obj"):
        continue

    path = os.path.join(mesh_folder, fname)
    mesh = load_mesh(path)
    verts = mesh.vertices.copy()
    faces = mesh.faces.copy()

    print(f"Processing: {fname}")

    norm_mm, vmin, vmax = minmax_normalize(verts)
    q_mm = quantize(norm_mm, n_bins=bins)
    deq_mm = q_mm.astype(np.float64) / (bins - 1)
    recon_mm = deq_mm * (vmax - vmin) + vmin

    save_vertices_as_obj(norm_mm, faces, os.path.join(out_norm, fname.replace(".obj", "_mm_norm.obj")))
    save_vertices_as_obj(recon_mm, faces, os.path.join(out_quant, fname.replace(".obj", "_mm_quant.obj")))

    norm_us, centroid, max_dist = unit_sphere_normalize(verts)
    mapped = (norm_us + 1.0) / 2.0  # map [-1,1] → [0,1] for quantization
    q_us = quantize(mapped, n_bins=bins)
    deq_us = q_us.astype(np.float64) / (bins - 1)
    deq_us = deq_us * 2.0 - 1.0     # map back [0,1] → [-1,1]
    recon_us = deq_us * max_dist + centroid

    save_vertices_as_obj(norm_us, faces, os.path.join(out_norm, fname.replace(".obj", "_us_norm.obj")))
    save_vertices_as_obj(recon_us, faces, os.path.join(out_quant, fname.replace(".obj", "_us_quant.obj")))

print("Task 2 complete — check 'outputs/normalized' and 'outputs/quantized'")
