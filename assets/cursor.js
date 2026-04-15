document.addEventListener("DOMContentLoaded", () => {
    // 1. Create the leading glowing dot
    const dot = document.createElement("div");
    dot.id = "custom-cursor-dot";
    document.body.appendChild(dot);

    // 2. Create the Canvas for the tracing line
    const canvas = document.createElement("canvas");
    canvas.id = "cursor-canvas";
    document.body.appendChild(canvas);
    
    let ctx = canvas.getContext('2d');
    
    // Resize canvas
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();
    
    // State
    let mouse = { x: window.innerWidth/2, y: window.innerHeight/2 };
    
    // Create an array to hold the history of positions for the trail
    const trail = [];
    const maxTrailLength = 40; // Number of segments in the line
    
    document.addEventListener("mousemove", (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        
        // Snap the main dot exactly to mouse pointer
        dot.style.transform = `translate3d(${mouse.x - 5}px, ${mouse.y - 5}px, 0)`;
        
        // Hover state logic
        const isClickable = e.target.closest('a') || e.target.closest('button') || e.target.closest('.card-3d') || e.target.closest('.Select-control');
        if (isClickable) dot.classList.add("cursor-hover");
        else dot.classList.remove("cursor-hover");
    });

    // Animation loop to draw the trail line
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Push current mouse pos to trail
        trail.push({ x: mouse.x, y: mouse.y });
        
        // Keep trail size limited
        if (trail.length > maxTrailLength) {
            trail.shift();
        }
        
        // Draw the trail using segmented paths to allow fading thickness/alpha
        if (trail.length > 1) {
            ctx.lineJoin = 'round';
            ctx.lineCap = 'round';
            
            for (let i = 0; i < trail.length - 1; i++) {
                ctx.beginPath();
                ctx.moveTo(trail[i].x, trail[i].y);
                
                const nextPoint = trail[i+1];
                const age = i / trail.length;
                
                ctx.strokeStyle = '#ff5722'; 
                ctx.lineWidth = Math.max(0.5, age * 3); // Max width 3px at the head
                ctx.globalAlpha = Math.max(0, age * 0.8);
                
                const xc = (trail[i].x + nextPoint.x) / 2;
                const yc = (trail[i].y + nextPoint.y) / 2;
                ctx.quadraticCurveTo(trail[i].x, trail[i].y, xc, yc);
                
                ctx.stroke();
            }
            ctx.globalAlpha = 1; // reset
        }
        
        // Optional: If mouse stops moving, we want the tail to catch up and disappear
        // So we pop the tail if the head didn't move much
        if (trail.length > 0) {
            const last = trail[trail.length - 1];
            if (mouse.x === last.x && mouse.y === last.y) {
                // If the mouse hasn't changed, pull the tail forward
                trail.shift();
            }
        }

        requestAnimationFrame(animate);
    }
    
    animate();

    // Hide everything when leaving window
    document.addEventListener("mouseout", () => {
        dot.style.opacity = 0;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        trail.length = 0; // clear trail immediately
    });
    
    document.addEventListener("mouseover", () => {
        dot.style.opacity = 1;
    });
});
