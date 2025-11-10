import open3d as o3d
import os

mesh_path = "outputs/quantized/branch_mm_quant.obj"
save_path = "outputs/reconstructed/branch_mm_quant_open3d.png"

mesh = o3d.io.read_triangle_mesh(mesh_path)
mesh.compute_vertex_normals()

vis = o3d.visualization.Visualizer()
vis.create_window(window_name="Mesh Viewer", width=800, height=600, visible=True)
vis.add_geometry(mesh)
vis.run()  # open window for you to rotate manually if needed
vis.capture_screen_image(save_path, do_render=True)
vis.destroy_window()

print(f"✅ Saved image: {save_path}")
