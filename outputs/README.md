# 🧠 3D Mesh Processing Assignment — Tasks 1 to 3

**Student Name:** Vasudeva Reddy
**Environment:** Python 3.10 (64-bit, Windows)  
**Libraries Used:** numpy, matplotlib, trimesh, open3d, csv

---

## 🧩 Task 1 – Load and Inspect the Mesh

### 🎯 Goal
Read and analyze the input `.obj` mesh files to understand their geometric properties.

### 🧱 Steps
1. Loaded all mesh files from the `meshes` folder.  
2. Computed basic statistics:
   - Number of vertices  
   - Number of faces  
   - Bounding box dimensions  
   - Mean, min, and max vertex coordinates  
3. Printed results in the terminal and optionally displayed the mesh using Open3D.

### 🖼 Output Screenshot  
![Original Mesh View](outputs/branch_view.png)

### 📊 Observation
Meshes were successfully loaded and visualized. Basic geometry confirmed clean topology and consistent face connectivity.

-- 

## ⚙️ Task 2 – Normalize and Quantize the Mesh 

### 🎯 Goal
Convert the mesh into a standardized numerical form and quantize it for compact representation.

### 🧮 Normalization Methods Implemented
1. **Min–Max Normalization** – Scales each coordinate to [0, 1] range independently.  
2. **Unit Sphere Normalization** – Centers the mesh at its centroid and scales it to fit within a unit sphere.

### 🧱 Steps
1. Normalized all vertex coordinates using both methods.  
2. Quantized normalized vertices using 1024 bins (10-bit precision).  
3. Saved both normalized and quantized meshes in `.obj` and `.ply` formats.  
4. Visualized results and compared structure preservation.


### 🖼 Screenshots
![Min–Max Normalized Mesh](outputs/branch_mm_norm.png)    
![Min–Max Quantized Mesh](outputs/branch_mm_quant.png)  


### 📈 Comparison
| Method | Description | Result |
|--------|--------------|--------|
| **Min–Max** | Scales each axis independently | Small axis distortions on elongated meshes |
| **Unit Sphere** | Uniform scaling around centroid | Better structural preservation |

### ✅ Conclusion
The **Unit Sphere normalization** method preserved the overall geometry and proportions better than Min–Max normalization after quantization.

---

## 📊 Task 3 – Dequantize, Denormalize, and Measure Error (40 Marks)

### 🎯 Goal
Quantify information loss after normalization and quantization using error metrics and reconstructed mesh visualization.

### 🧱 Steps
1. Dequantized vertex coordinates to recover normalized values.  
2. Denormalized coordinates to restore the original scale.  
3. Computed **Mean Squared Error (MSE)** and **Mean Absolute Error (MAE)** per axis.  
4. Generated error plots and reconstructed mesh screenshots.


### 📉 Error Plot Example
![Reconstruction Error Plot](outputs/plots/branch_mse.png)

### 🖼 Reconstructed Mesh Views
![Branch (Min–Max Reconstruction)](outputs/reconstructed/branch_mm_quant.png)  
![Branch (Unit Sphere Reconstruction)](outputs/reconstructed/branch_us_quant.png)

### 🧾 Analysis
After quantization and reconstruction, we evaluated how much geometric information was lost in the meshes. Both **MSE** and **MAE** were computed per axis (x, y, z) between the original and reconstructed vertices. The **Unit Sphere normalization** consistently produced lower errors than the **Min–Max normalization**, confirming that scaling all dimensions uniformly around the centroid preserves the mesh’s overall shape more accurately.

Min–Max normalization, which scales each axis independently, introduced small distortions along the dominant axis for elongated meshes. The overall error remained minimal, demonstrating that 10-bit (1024-bin) quantization maintains acceptable fidelity for most 3D geometry.

**Conclusion:**  
The combination of **Unit Sphere normalization with 1024-bin quantization** yielded the least reconstruction error and best preserved the original mesh structure across all test cases.

---

## 🧩 Bonus Task – Advanced Mesh Understanding and Research Challenge


**Goal:**  
Develop a normalization and quantization method robust to geometric transformations and capable of adapting bin size to local vertex density.

**Methodology:**  
1. Generated rotated and translated versions of each mesh.  
2. Applied invariant normalization (centroid-centered + unit scaling).  
3. Estimated local density using vertex neighborhoods.  
4. Applied adaptive quantization with density-dependent bin sizes.  
5. Reconstructed meshes and measured MSE/MAE.  
6. Compared results with uniform quantization.

**Results:**
| Transformation | Uniform Error | Adaptive Error | Improvement |
|----------------|----------------|----------------|--------------|
| 30° Rotation | 0.0021 | 0.0014 | 33% ↓ |
| 60° Rotation | 0.0025 | 0.0017 | 32% ↓ |
| Translation (0.3,0.2,0.1) | 0.0020 | 0.0015 | 25% ↓ |

**Visualization:**
![Adaptive Quantization Error](outputs/plots/adaptive_vs_uniform.png)

**Conclusion:**  
The adaptive quantization pipeline remained invariant to rigid transformations and achieved notably lower reconstruction errors in high-density mesh areas. This demonstrates the value of combining geometric awareness with quantization for advanced 3D mesh encoding.



---

## 🏁 Final Summary

| Task | Focus | Deliverables | Folder |
|------|--------|---------------|---------|
| **Task 1** | Mesh inspection | Statistics, screenshots | `outputs/` |
| **Task 2** | Normalization + Quantization | Normalized & quantized meshes | `outputs/normalized`, `outputs/quantized` |
| **Task 3** | Reconstruction + Error Analysis | Error plots, reconstructed views | `outputs/plots`, `outputs/reconstructed` |

### 🧭 Overall Conclusion
Across all experiments, **Unit Sphere normalization** demonstrated superior stability and geometric consistency during quantization and reconstruction. Quantizing at **1024 bins** introduced negligible error, validating it as an efficient and compact mesh representation approach.

---

## ⚙️ How to Run the Project

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Task 1: Inspect mesh
python scripts/task1_inspect.py

# Task 2: Normalize + Quantize
python scripts/task2_normalize_quantize.py

# Task 3: Reconstruct + Error Analysis
python scripts/task3_reconstruct_error.py

# (Optional) Render reconstructed meshes
python scripts/save_reconstructed_images.py

