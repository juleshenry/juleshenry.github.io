// Three.js Rotating Torus Demo
function initTorusDemo(containerId) {
  const container = document.getElementById(containerId);
  if (!container) {
    console.error('Container not found:', containerId);
    return;
  }

  // Scene setup
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0f172a);
  scene.fog = new THREE.Fog(0x0f172a, 5, 15);

  // Camera setup
  const width = container.clientWidth;
  const height = container.clientHeight || 500;
  const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
  camera.position.z = 5;

  // Renderer setup
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.appendChild(renderer.domElement);

  // Create torus geometry
  const torusGeometry = new THREE.TorusGeometry(1.2, 0.4, 16, 100);
  const torusMaterial = new THREE.MeshStandardMaterial({
    color: 0x6366f1, // Indigo
    metalness: 0.7,
    roughness: 0.3,
  });
  const torus = new THREE.Mesh(torusGeometry, torusMaterial);
  scene.add(torus);

  // Create sphere in the center
  const sphereGeometry = new THREE.SphereGeometry(0.3, 32, 32);
  const sphereMaterial = new THREE.MeshStandardMaterial({
    color: 0xec4899, // Pink
    metalness: 0.5,
    roughness: 0.2,
  });
  const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
  scene.add(sphere);

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight1 = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight1.position.set(5, 5, 5);
  scene.add(directionalLight1);

  const directionalLight2 = new THREE.DirectionalLight(0x6366f1, 0.5);
  directionalLight2.position.set(-5, -5, -5);
  scene.add(directionalLight2);

  // Animation loop
  function animate() {
    requestAnimationFrame(animate);

    // Rotate the torus
    torus.rotation.x += 0.005;
    torus.rotation.y += 0.008;

    // Gentle pulse for the sphere
    const time = Date.now() * 0.001;
    sphere.scale.setScalar(1 + Math.sin(time * 2) * 0.1);

    renderer.render(scene, camera);
  }

  // Handle window resize
  function onWindowResize() {
    const newWidth = container.clientWidth;
    const newHeight = container.clientHeight || 500;
    
    camera.aspect = newWidth / newHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(newWidth, newHeight);
  }

  window.addEventListener('resize', onWindowResize);

  // Start animation
  animate();

  // Cleanup function
  return function cleanup() {
    window.removeEventListener('resize', onWindowResize);
    container.removeChild(renderer.domElement);
    renderer.dispose();
  };
}

// Auto-initialize all three-canvas elements when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  const canvases = document.querySelectorAll('.three-canvas');
  canvases.forEach(function(canvas) {
    if (canvas.id) {
      initTorusDemo(canvas.id);
    }
  });
});
