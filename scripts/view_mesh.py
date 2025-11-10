import open3d as o3d
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python scripts/view_mesh.py path/to/mesh.obj")
    sys.exit(1)

mesh_path = sys.argv[1]
if not os.path.exists(mesh_path):
    print("File not found:", mesh_path)
    sys.exit(1)

# Load mesh
mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()

# Try interactive window first
try:
    o3d.visualization.draw_geometries([mesh])
except Exception as e:
    print("Interactive window failed:", e)
    print("Saving a static render to outputs/view_render.png")

    # Save an image instead
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)
    vis.add_geometry(mesh)
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image("outputs/view_render.png")
    vis.destroy_window()
    print("Saved: outputs/view_render.png")
