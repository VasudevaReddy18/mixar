import numpy as np
import trimesh

def load_mesh(path):
    mesh = trimesh.load(path, process=False)
    if mesh.faces is None:
        raise ValueError(f"No faces found in mesh: {path}")
    return mesh

def stats(vertices):
    return {
        "n_vertices": int(vertices.shape[0]),
        "min": vertices.min(axis=0).tolist(),
        "max": vertices.max(axis=0).tolist(),
        "mean": vertices.mean(axis=0).tolist(),
        "std": vertices.std(axis=0).tolist()
    }

def minmax_normalize(vertices):
    vmin = vertices.min(axis=0)
    vmax = vertices.max(axis=0)
    denom = vmax - vmin
    denom[denom == 0] = 1.0
    normalized = (vertices - vmin) / denom
    return normalized, vmin, vmax

def unit_sphere_normalize(vertices):
    centroid = vertices.mean(axis=0)
    centered = vertices - centroid
    max_dist = np.linalg.norm(centered, axis=1).max()
    if max_dist == 0:
        max_dist = 1.0
    normalized = centered / max_dist
    return normalized, centroid, max_dist

def quantize(normalized, n_bins=1024):
    q = np.floor(normalized * (n_bins - 1)).astype(np.int64)
    return q

def dequantize(q, n_bins=1024):
    return q.astype(np.float64) / (n_bins - 1)

def denormalize_minmax(deq, vmin, vmax):
    return deq * (vmax - vmin) + vmin

def denormalize_unit_sphere(deq, centroid, max_dist):
    return deq * max_dist + centroid

def save_vertices_as_obj(vertices, triangles, path):
    mesh = trimesh.Trimesh(vertices=vertices, faces=triangles, process=False)
    mesh.export(path)
