/**
 * MathFlowEngine - Math Calculation Engine
 * Handles all mathematical computations for the player
 */

class MathEngine {
    constructor() {
        this.variables = {};
        this.formulas = {};
    }
    
    /**
     * Load configuration
     */
    loadConfig(config) {
        this.config = config;
        
        // Initialize variables
        config.variables.forEach(v => {
            this.variables[v.id] = {
                ...v,
                value: v.default
            };
        });
        
        // Initialize formulas
        config.formulas.forEach(f => {
            this.formulas[f.id] = f;
        });
    }
    
    /**
     * Set a variable value
     */
    setVariable(name, value) {
        if (this.variables[name]) {
            this.variables[name].value = value;
        }
    }
    
    /**
     * Get variable value
     */
    getVariable(name) {
        return this.variables[name]?.value || 0;
    }
    
    /**
     * Calculate all formulas
     */
    calculateAll() {
        const results = {};
        
        // Create context with variable values
        const context = {};
        for (const [key, v] of Object.entries(this.variables)) {
            context[key] = v.value;
        }
        
        // Evaluate each formula
        for (const [id, formula] of Object.entries(this.formulas)) {
            results[id] = this.evaluate(formula.formula, context);
        }
        
        return results;
    }
    
    /**
     * Evaluate a formula string
     */
    evaluate(formulaStr, context) {
        try {
            // Replace variables in formula
            let expr = formulaStr;
            for (const [key, value] of Object.entries(context)) {
                expr = expr.replace(new RegExp(`\\b${key}\\b`, 'g'), value);
            }
            
            // Safe evaluation using Function
            const result = new Function(`return ${expr}`)();
            return result;
        } catch (e) {
            console.error('Formula evaluation error:', e);
            return 0;
        }
    }
    
    /**
     * Check for discoveries
     */
    checkDiscoveries(results) {
        const discoveries = [];
        
        if (!this.config?.discoveries) return discoveries;
        
        for (const discovery of this.config.discoveries) {
            if (this.matchCondition(discovery.condition, results)) {
                discoveries.push({
                    id: discovery.id,
                    message: discovery.message,
                    formula: discovery.formula
                });
            }
        }
        
        return discoveries;
    }
    
    /**
     * Match a discovery condition
     */
    matchCondition(condition, results) {
        try {
            // Parse condition like "r >= 2.9 AND r <= 3.1"
            let expr = condition;
            for (const [key, value] of Object.entries(results)) {
                expr = expr.replace(new RegExp(`\\b${key}\\b`, 'g'), value);
            }
            
            return new Function(`return ${expr}`)();
        } catch (e) {
            return false;
        }
    }
    
    /**
     * Format number for display
     */
    format(num, decimals = 2) {
        return num.toFixed(decimals);
    }
}

/**
 * Animation Controller
 */
class AnimationController {
    constructor(renderer) {
        this.renderer = renderer;
        this.isPlaying = false;
        this.animationId = null;
        this.startTime = 0;
        this.duration = 3000;
        this.startValue = 1.5;
        this.endValue = 3.0;
    }
    
    /**
     * Animate from start to end value
     */
    animate(from, to, duration = 3000) {
        this.startValue = from;
        this.endValue = to;
        this.duration = duration;
        this.isPlaying = true;
        this.startTime = performance.now();
        
        const animateFrame = (currentTime) => {
            const elapsed = currentTime - this.startTime;
            const progress = Math.min(elapsed / this.duration, 1);
            
            // Ease function (smooth)
            const eased = this.easeInOut(progress);
            const currentValue = this.startValue + (this.endValue - this.startValue) * eased;
            
            // Update renderer
            this.renderer.setVariable('r', currentValue);
            this.renderer.render();
            
            if (progress < 1) {
                this.animationId = requestAnimationFrame(animateFrame);
            } else {
                this.isPlaying = false;
            }
        };
        
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        this.animationId = requestAnimationFrame(animateFrame);
    }
    
    /**
     * Ease in-out function
     */
    easeInOut(t) {
        return t < 0.5 
            ? 2 * t * t 
            : 1 - Math.pow(-2 * t + 2, 2) / 2;
    }
    
    /**
     * Stop animation
     */
    stop() {
        this.isPlaying = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }
}

// Export for global use
window.MathEngine = MathEngine;
window.AnimationController = AnimationController;