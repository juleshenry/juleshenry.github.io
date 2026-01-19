---
layout: post
title: "Announcing Three.js Support"
date: 2026-01-19
---

# Interactive 3D Graphics Come to the Blog

I'm excited to announce that this blog now supports interactive 3D graphics using [Three.js](https://threejs.org/)! 

Three.js is a powerful JavaScript library that makes WebGL accessible and easy to use. With it, I can now embed interactive 3D visualizations directly into blog posts to better illustrate complex concepts in mathematics, physics, computer science, and more.

## Demo: Rotating Torus

Here's a simple demo to show what's possible. This is a real-time 3D scene rendered in your browser:

<div id="torus-demo" class="three-canvas" style="width: 100%; height: 500px; margin: 2em 0; border-radius: 8px; overflow: hidden;"></div>

<script src="/javascripts/three-demos.js"></script>

Pretty cool, right? The torus rotates smoothly, and the sphere in the center gently pulses. All of this is being computed and rendered in real-time using your GPU.

## Why Three.js?

Adding 3D visualization capabilities opens up exciting possibilities for future posts:

- **Mathematical Visualizations**: Visualizing complex surfaces, transformations, and geometric concepts
- **Physics Simulations**: Demonstrating particle systems, fluid dynamics, and other physical phenomena  
- **Algorithm Demonstrations**: Showing how 3D algorithms work in real-time
- **Interactive Exploration**: Allowing readers to interact with and explore concepts hands-on

## Technical Details

The implementation uses:

- **Three.js v0.162.0** - The core 3D library loaded via CDN
- **WebGL** - Hardware-accelerated 3D graphics in the browser
- **Responsive Design** - Scenes automatically resize with the page
- **Custom Scripts** - Reusable demo functions for different visualizations

The demo above creates a torus knot with physically-based materials (PBR), multiple light sources, and atmospheric fog effects. The animation runs at 60fps and is fully GPU-accelerated.

## What's Next?

I'm planning to use Three.js in upcoming posts about:

- Quantum computing visualizations (Bloch spheres, quantum gates)
- 3D mathematical surfaces and transformations
- Computer graphics algorithms
- Physics simulations and numerical methods

Stay tuned for more interactive content!

## Source Code

The rotating torus demo is quite simple. Here's the core of how it works:

```javascript
// Create torus geometry
const torusGeometry = new THREE.TorusGeometry(1.2, 0.4, 16, 100);
const torusMaterial = new THREE.MeshStandardMaterial({
  color: 0x6366f1,
  metalness: 0.7,
  roughness: 0.3,
});
const torus = new THREE.Mesh(torusGeometry, torusMaterial);

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  torus.rotation.x += 0.005;
  torus.rotation.y += 0.008;
  renderer.render(scene, camera);
}
```

The full source code for all Three.js demos is available in `/javascripts/three-demos.js`.

---

I'm excited about the new possibilities this brings to the blog. If you have suggestions for visualizations you'd like to see, feel free to reach out!
