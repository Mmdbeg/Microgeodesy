# Network Adjustment (Beta Version)

This is a **beta version** of a network adjustment software developed by **Mohammad Hossein Beglari**, a geodesy student at **KNTU University (Faculty of Geodesy and Geomatics)**.

The project aims to perform **geodetic network adjustments** using parametric models. Currently, the 2D network adjustment is partially implemented, and 3D adjustment is planned as the next step.

---

## File Overview

Each file handles a specific part of the network adjustment process:

1. **distance_cor.py**  
   Performs distance correction considering **pressure, humidity, and light fraction**.

2. **V_cor.py**  
   Performs **vertical angles correction** (light fraction).

3. **2d_projection_correction.py**  
   Projects all distances to a **common height** to avoid radial errors.

4. **triangle_checker.py**  
   Creates all possible triangles and checks their **misclosure errors**.

5. **zero_change.py**  
   Adjusts all horizontal angles to a **single azimuth**, necessary for network adjustment.

6. **2d.py**  
   Performs a **parametric model adjustment** for 2D networks (**work in progress**).

7. **Next step**  
   Implement **parametric model adjustment** for 3D networks (**planned next**).

---

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/your-repo.git
