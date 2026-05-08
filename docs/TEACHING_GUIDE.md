# MathFlowEngine - Teaching Guide

## Quick Start

### Installation

```bash
pip install pillow
```

### Basic Usage

```python
from orchestrator import MathFlowEngine

# Create engine
engine = MathFlowEngine()

# Build and teach a lesson
lesson = engine.build_lesson("circle_area")
engine.teach(lesson)
```

## Concepts Available

### 1. Circle Area
- Teaches: Why area increases quadratically
- Key insight: Double radius = 4x area
- Formula: A = pi*r^2

### 2. Derivatives (Calculus)
- Teaches: Instantaneous rate of change
- Key insight: Derivative = speedometer
- Formula: f'(x) = dy/dx

## Interactive Playground

Open the HTML files in a browser:

```bash
python interactive/playground.py
```

This creates interactive HTML where students can drag sliders and discover math relationships themselves!

## Architecture

```
MathFlowEngine/
├── core/           # Concept graph & relationships
├── visual/         # Visual transformations  
├── render/         # Frame rendering
├── orchestrator/   # Teaching orchestration
├── interactive/    # Phase 2 playground
└── lessons/       # Pre-built lessons
```

## Pedagogical Approach

The engine follows evidence-based learning:

1. **Start with problem** - Not formula first
2. **Build intuition** - Visual understanding
3. **Show transformations** - What changes and why
4. **Let discover** - Students find patterns themselves

This is why students who learn this way truly understand math - they discovered it, not just memorized it.