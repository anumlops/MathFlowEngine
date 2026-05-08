# MathFlowEngine - Pedagogical Intelligence Schema

## Structured Teaching Schema for EVERY Concept

This is the core of the "Teacher Brain" - every concept gets stored with full pedagogical context.

---

```json
{
  "concept_id": "derivative",
  "display_name": "Derivative",
  "level": "advanced",
  
  "intuition": "How fast are you going RIGHT NOW? Not average, instant - like a speedometer!",
  
  "problem": "Average rate tells you 'over the whole trip I averaged 60mph' but we need 'at this EXACT moment, am I speeding?'",
  
  "emergence": "Average rate fails when we need instant measurement. The limit of average rate as time interval → 0 creates derivative.",
  
  "formalization": "f'(x) = lim(h→0) [f(x+h) - f(x)] / h",
  
  "visualization": [
    {"type": "secant_to_tangent", "description": "Secant line approaching tangent as h → 0"},
    {"type": "zooming", "description": "Zooming into a curve point"},
    {"type": "speedometer", "description": "Car speedometer showing instantaneous speed"}
  ],
  
  "misconceptions": [
    {"misconception": "derivative is a fraction", "correct": "It's a single rate value, dy/dx is notation showing ratio"},
    {"misconception": "derivative = slope", "correct": "derivative AT a point = slope of tangent; derivative function = slope at every point"},
    {"misconception": "limit = division", "correct": "Limit is approaching a value, not actual division"},
    {"misconception": "dy/dx can simplify to dy÷d", "correct": "d is notation for 'infinitesimal change', not a number"}
  ],
  
  "interactions": [
    {"change": "y=sin(x) → y=cos(x)", "understands": "phase shift, wave transformation, initial conditions"},
    {"change": "increase function", "understands": "derivative > 0 everywhere"},
    {"change": "decrease function", "understands": "derivative < 0 everywhere"}
  ]
}
```

---

## Concept Dependency Tree

```
LIMIT INTUITION
      ↓
RATE OF CHANGE (average)
      ↓
SLOPE OF CURVE
      ↓
INSTANTANEOUS RATE (= derivative)
      ↓
OPTIMIZATION (set derivative = 0, solve)
```

---

## Visual-Concept Mapping

| Concept | Best Visualization |
|---------|-------------------|
| derivative | secant → tangent animation |
| integral | area accumulation under curve |
| limit | zooming continuity |
| sine | rotating circle projection |
| exponential | growth factor animation |
| derivative proof | tangent slope on curve |

---

## Misconception Prediction Triggers

| Concept | Expected Misconception | Anti-teaching |
|---------|----------------------|---------------|
| derivative | "It's a fraction" | Show dy/dx as single notation, not division |
| limits | "It equals the value" | Show approaching but never reaching |
| negative exponents | "Makes things smaller" | Show 2^-3 = 1/8, visual scaling |
| sine waves | "sin = y" | Show sin as projection, full circle reference |

---

## Emerging Concepts (What Forces Discovery)

| Problem | Forces Concept |
|---------|---------------|
| "How fast right NOW?" | derivative |
| "Area under curve?" | integral |
| "Infinite sum finite?" | limits |
| "What's closest?" | optimization |
| "Repeated growth?" | exponential |

---

*Part of MathFlowEngine Pedagogical Intelligence System*