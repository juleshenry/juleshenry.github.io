document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    canvas.id = 'dot-matrix';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    let width, height;
    let dots = [];
    const spacing = 30;

    function init() {
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;

        dots = [];
        for (let x = 0; x < width; x += spacing) {
            for (let y = 0; y < height; y += spacing) {
                dots.push({
                    x,
                    y,
                    baseX: x,
                    baseY: y,
                    size: 1,
                    alpha: Math.random() * 0.5 + 0.1
                });
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        
        const time = Date.now() * 0.001;

        dots.forEach(dot => {
            // Subtle breathing effect
            const offset = Math.sin(time + (dot.x * 0.01) + (dot.y * 0.01)) * 0.5;
            const currentAlpha = Math.max(0.05, dot.alpha + offset * 0.1);
            
            ctx.fillStyle = `rgba(179, 27, 27, ${currentAlpha})`;
            ctx.beginPath();
            ctx.arc(dot.x, dot.y, dot.size + offset * 0.2, 0, Math.PI * 2);
            ctx.fill();
        });

        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', init);
    init();
    animate();

    // Mouse interaction for the "eclectic genius" vibe
    window.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX;
        const mouseY = e.clientY;

        dots.forEach(dot => {
            const dx = mouseX - dot.x;
            const dy = mouseY - dot.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 100) {
                dot.size = 1.5;
                // Shift dots slightly away from mouse
                const force = (100 - dist) / 100;
                dot.x = dot.baseX - dx * force * 0.1;
                dot.y = dot.baseY - dy * force * 0.1;
            } else {
                dot.size = 1;
                dot.x += (dot.baseX - dot.x) * 0.1;
                dot.y += (dot.baseY - dot.y) * 0.1;
            }
        });
    });
});
