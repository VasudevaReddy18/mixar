import os
from mesh_utils import load_mesh, stats

mesh_folder = os.path.join(os.getcwd(), "meshes")

for fname in sorted(os.listdir(mesh_folder)):
    if not fname.lower().endswith(".obj"):
        continue
    path = os.path.join(mesh_folder, fname)
    mesh = load_mesh(path)
    s = stats(mesh.vertices)
    print(f"File: {fname}")
    print("  Vertices:", s['n_vertices'])
    print("  Min:", s['min'])
    print("  Max:", s['max'])
    print("  Mean:", s['mean'])
    print("  Std:", s['std'])
    print("-"*50)
