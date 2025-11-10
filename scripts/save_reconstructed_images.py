# scripts/save_reconstructed_images.py
import os
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

recon_folder = "outputs/quantized"
img_folder = "outputs/reconstructed"
os.makedirs(img_folder, exist_ok=True)

files = [f for f in os.listdir(recon_folder) if f.lower().endswith((".obj", ".ply"))]

for fname in files:
    path = os.path.join(recon_folder, fname)
    mesh = trimesh.load(path, process=False)
    verts = mesh.vertices
    faces = mesh.faces

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2],
                    linewidth=0.2, antialiased=True, color='lightblue')

    ax.set_title(fname)
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    plt.tight_layout()

    out_path = os.path.join(img_folder, fname.replace(".obj", ".png").replace(".ply", ".png"))
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"✅ Saved Matplotlib render: {out_path}")

print("All reconstructed mesh snapshots saved in outputs/reconstructed/")
