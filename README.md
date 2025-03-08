# Ray Tracing Project

**Authors:** Abid Jeem, Liz Matthews, Geoff Matthews

## Overview

This repository contains a basic **ray tracer** in Python. It supports:

- **Spheres, Planes, Cubes, Ellipsoids, Torus**  
- **Recursive Ray Tracing** (reflections and refractions)  
- **3D Noise Materials** (clouds, wood, marble, etc.)  
- **2D Image Texturing** for spheres and planes  
- **Sky Plane** or background with a texture  
- **Fog/Atmospheric** effects

<details>
<summary>Final Render Example</summary>

![Final Scene](docs/final_scene.png)

*Replace this sample with your own final rendered image.*
</details>

---

## Features

1. **Recursive Reflection & Refraction**
   - Objects can have a `reflection_factor` (0.0 to 1.0).
   - Transparency (trans) and refraction index for glass/water-like materials.
   - Fresnel approximations, partial reflection/refraction.

2. **Multiple Lights**
   - Directional or Point Lights
   - Basic shadow checks (hard shadows).

3. **Progressive Rendering**
   - Renders from coarse to fine resolution.
   - Cancel early by closing the PyGame window.

4. **Modular Objects & Materials**
   - **Objects** each implement `intersect(...)` and `getNormal(...)`.
   - **Materials** can be plain color, 3D noise, or 2D textures.

---

## File Structure

```bash
.
├── rayTracer.py            # Main RayTracer class & getColorR(...) with recursive rays
├── render.py               # ProgressiveRenderer, step-by-step pixel rendering
├── modules/
│   ├── raytracing/
│   │   ├── scene.py        # Scene class (camera, lights, objects)
│   │   ├── objects.py      # Definitions: Sphere, Plane, Cube, Ellipsoid, Torus, ...
│   │   ├── lights.py       # PointLight, DirectionLight
│   │   ├── materials.py    # Material, Material2D, Material3D, reflection/trans params
│   │   ├── camera.py       # Camera setup (fwd, up, fov, distance, getRay(...))
│   │   └── ray.py          # Ray data structure
│   └── utils/
│       ├── vector.py       # Vector math (normalize, lerp, etc.)
│       ├── noise.py        # NoiseMachine for 2D/3D perlin-like noise
│       └── definitions.py  # EPSILON, constants
├── docs/
│   └── final_scene.png     # Example final rendered image
└── README.md               # This file

# My Ray Tracer

Here is the final rendered image:

![Final Render](/images/Abid_RayTracing_Final.png)

