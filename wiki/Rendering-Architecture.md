# Rendering Architecture & Cetacean Physics

Unlike sprite-based animation systems, `git-tulkun` uses **pure mathematical procedurals**. Every frame is synthesized on the fly in Rust.

---

## 1. Spine Spline and Signed Distance Fields (SDFs)

The torso is represented as a flexible central spline containing up to 186 nodes. Appendages (opercular flippers, primary scythe wings, *kuru* neural whips, pelvic paddles, and caudal flukes) are anchored to the spine and evaluated using signed distance chains.

---

## 2. Cylindrical Normal Lighting

For each pixel $(x, y)$ inside the body or appendages, a 3D cylindrical surface normal vector is calculated:

$$\vec{n} = \left(n_x, n_y, \sqrt{\max\left(0, 1 - n_x^2 - n_y^2\right)}\right)$$

This normal is dotted with an ocean key light vector:

$$\vec{L} = [-0.30, -0.62, 0.72]$$

The resulting intensity is dithered using a $4\times4$ Bayer matrix to achieve authentic 90s-era retro pixel shading.

---

## 3. Cetacean S-Wave Swimming Loop

The swimming animation loops over **48 frames at 15 FPS (3.2 seconds)**:

$$\Delta y(u, t) = A_{\text{head}} \cdot \sin(\omega t) \cdot (1 - u)^{1.3} + A_{\text{tail}} \cdot \sin(2.35\pi u - \omega t) \cdot u^{0.92}$$

- $u \in [0, 1]$ represents normalized distance along the spine from rostrum to fluke.
- The head maintains steady posture with subtle vertical heave, while a traveling wave accelerates down the tail stock to drive the propulsion flukes.
- Pectoral flippers scull with natural hydrodynamic phase lag.
