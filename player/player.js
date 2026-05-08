/**
 * MathFlowEngine - Main Player
 * Interactive Video Player for Mathematical Concepts
 */

// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
    
    // ============================================
    // INITIALIZATION
    // ============================================
    
    console.log('MathFlowEngine Interactive Player Loading...');
    
    // Elements
    const canvas = document.getElementById('render-canvas');
    const ctx = canvas.getContext('2d');
    
    const slider = document.getElementById('r-slider');
    const sliderValue = document.getElementById('slider-value');
    
    const displayR = document.getElementById('display-r');
    const displayArea = document.getElementById('display-area');
    const displayC = document.getElementById('display-c');
    const displayD = document.getElementById('display-d');
    
    const canvasR = document.getElementById('canvas-r');
    
    const discoveryPanel = document.getElementById('discovery-panel');
    const discoveryText = document.getElementById('discovery-text');
    const discoveryFormula = document.getElementById('discovery-formula');
    
    const btnPlay = document.getElementById('btn-play');
    const btnReset = document.getElementById('btn-reset');
    const btnDiscover = document.getElementById('btn-discover');
    
    // ============================================
    // CONFIGURATION
    // ============================================
    
    const config = {
        variables: [
            { id: 'r', name: 'radius', min: 0.5, max: 5.0, default: 1.5, step: 0.1 }
        ],
        formulas: [
            { id: 'area', formula: 'Math.PI * r * r' },
            { id: 'circumference', formula: '2 * Math.PI * r' },
            { id: 'diameter', formula: '2 * r' }
        ],
        discoveries: [
            { 
                id: 'double', 
                condition: 'r >= 2.9 && r <= 3.1', 
                message: 'DISCOVERY: When radius DOUBLES, area QUADRUPLES!',
                formula: 'A₂ = 4 × A₁' 
            },
            { 
                id: 'triple', 
                condition: 'r >= 4.4 && r <= 4.6', 
                message: 'DISCOVERY: When radius TRIPLES, area becomes 9x!',
                formula: 'A₃ = 9 × A₁' 
            }
        ],
        visual: {
            centerX: canvas.width / 2,
            centerY: canvas.height / 2,
            scale: 50
        }
    };
    
    // Current state
    let currentR = config.variables[0].default;
    let isAnimating = false;
    
    // ============================================
    // MATH FUNCTIONS
    // ============================================
    
    function calculateFormulas(r) {
        return {
            area: Math.PI * r * r,
            circumference: 2 * Math.PI * r,
            diameter: 2 * r
        };
    }
    
    function checkDiscoveries(r) {
        const results = [];
        
        for (const d of config.discoveries) {
            try {
                // Simple condition check
                const cond = d.condition
                    .replace(/r/g, r)
                    .replace(/AND/g, '&&')
                    .replace(/<=/g, '<=');
                
                if (eval(cond)) {
                    results.push(d);
                }
            } catch (e) {}
        }
        
        return results;
    }
    
    // ============================================
    // RENDERING
    // ============================================
    
    function render() {
        // Clear canvas
        ctx.fillStyle = '#0d1117';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        const { centerX, centerY, scale } = config.visual;
        const radiusPx = currentR * scale;
        
        // Draw grid (subtle)
        drawGrid(centerX, centerY, scale);
        
        // Draw circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, radiusPx, 0, 2 * Math.PI);
        ctx.fillStyle = 'rgba(65, 105, 225, 0.4)';
        ctx.fill();
        ctx.strokeStyle = '#4169E1';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw radius line
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + radiusPx, centerY);
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw center point
        ctx.beginPath();
        ctx.arc(centerX, centerY, 4, 0, 2 * Math.PI);
        ctx.fillStyle = '#FFFFFF';
        ctx.fill();
    }
    
    function drawGrid(centerX, centerY, scale) {
        ctx.strokeStyle = '#21262d';
        ctx.lineWidth = 1;
        
        // Vertical lines
        for (let x = 0; x < centerX * 2; x += scale) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(centerX * 2 - x, 0);
            ctx.lineTo(centerX * 2 - x, canvas.height);
            ctx.stroke();
        }
        
        // Horizontal lines
        for (let y = 0; y < centerY * 2; y += scale) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(0, centerY * 2 - y);
            ctx.lineTo(canvas.width, centerY * 2 - y);
            ctx.stroke();
        }
    }
    
    // ============================================
    // DISPLAY UPDATE
    // ============================================
    
    function updateDisplay() {
        const values = calculateFormulas(currentR);
        
        // Update display panel
        displayR.textContent = values.area.toFixed(2);
        displayArea.textContent = values.area.toFixed(2);
        displayC.textContent = values.circumference.toFixed(2);
        displayD.textContent = values.diameter.toFixed(2);
        
        // Update canvas info
        canvasR.textContent = currentR.toFixed(2);
        
        sliderValue.textContent = currentR.toFixed(2);
        
        // Check discoveries
        const discoveries = checkDiscoveries(currentR);
        if (discoveries.length > 0) {
            discoveryPanel.classList.add('visible');
            discoveryText.textContent = discoveries[0].message;
            discoveryFormula.textContent = discoveries[0].formula;
        } else {
            discoveryPanel.classList.remove('visible');
        }
    }
    
    // ============================================
    // ANIMATION
    // ============================================
    
    function animateTo(targetR, duration = 2000) {
        if (isAnimating) return;
        
        isAnimating = true;
        btnPlay.textContent = '⏸';
        
        const startR = currentR;
        const startTime = performance.now();
        
        function animate(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Smooth easing
            const eased = progress < 0.5 
                ? 2 * progress * progress 
                : 1 - Math.pow(-2 * progress + 2, 2) / 2;
            
            currentR = startR + (targetR - startR) * eased;
            slider.value = currentR;
            
            render();
            updateDisplay();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                isAnimating = false;
                btnPlay.textContent = '▶ Play';
            }
        }
        
        requestAnimationFrame(animate);
    }
    
    // ============================================
    // EVENT HANDLERS
    // ============================================
    
    // Slider change
    slider.addEventListener('input', (e) => {
        currentR = parseFloat(e.target.value);
        render();
        updateDisplay();
    });
    
    // Play button
    btnPlay.addEventListener('click', () => {
        if (isAnimating) return;
        
        if (currentR >= 3) {
            animateTo(1.5);
        } else {
            animateTo(3.0);
        }
    });
    
    // Reset button
    btnReset.addEventListener('click', () => {
        currentR = 1.5;
        slider.value = 1.5;
        render();
        updateDisplay();
    });
    
    // Discover button
    btnDiscover.addEventListener('click', () => {
        animateTo(3.0, 2000);
    });
    
    // ============================================
    // INITIAL RENDER
    // ============================================
    
    render();
    updateDisplay();
    
    console.log('MathFlowEngine Interactive Player Ready!');
});