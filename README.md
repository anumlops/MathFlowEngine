# MathFlowEngine
## A Concept-Driven Mathematical Education System

**Created:** May 8, 2026  
**Version:** 1.0 (MVP)

---

## Project Overview

MathFlowEngine is an AI-powered teaching system that teaches mathematics by showing **WHY**, not just **WHAT**. Built on the philosophy that mathematics should flow like water — where every concept naturally evolves from the previous one without abrupt jumps.

---

## Core Philosophy

> "Mathematics should be taught like flowing water — where every concept naturally evolves from the previous one without abrupt jumps."

The system has two philosophical pillars:

### 1. Concept Flow Engine (Phase 1 - MVP)
An AI teaching orchestration system that converts educational content into logically flowing visual explanations using:
- Pedagogical sequencing
- Visual reasoning
- Manim-style animations
- Conversational teaching
- Generated explanatory videos

### 2. Interactive Mathematical Playground (Phase 2+)
A live experimentation layer where students can manipulate variables, equations, and visual states to discover:
- Why formulas behave the way they do
- Why certain mathematical choices work
- Why changing core components breaks/changes the system

---

## Key Differences from Normal EdTech

| Normal Teaching | MathFlowEngine |
|---------------|--------------|
| "Here is the formula, memorize it" | "Why does this exist? What problem led to it?" |
| Formula first | Problem first, then intuition, then formula |
| Passive watching | Active discovery through interaction |
| Static textbook | Dynamic visual transformations |

---

## Research Foundation

Built on evidence-based learning principles (from psychology_math_study_methods_analysis.md):

- **Active Recall** - Students must actively retrieve, not passively re-read
- **Spaced Practice** - Distribute learning over time, not cramming
- **Interleaving** - Mix different problem types, not blocked practice
- **Concrete Examples** - Anchor understanding in real scenarios
- **Dual Coding** - Combine verbal + visual for deeper memory

The research strongly validates the engine's approach - students construct understanding, not passively receive it.

---

## What We Built

### 1. Core Concept Graph (`core/concepts.py`)

Understanding mathematical relationships between concepts:

```python
Concept(
    id="circle_area",
    name="Circle Area",
    
    # WHY - not just what it is
    problem_motivated_by="...",
    intuition="Think of a circle as a pizza...",
    
    # Relationships
    prerequisites=["radius", "pi"],
    builds_upon=[...],
    
    # Variables that can be manipulated
    variables=[MathVariable(symbol="r", name="radius", ...)],
    
    # Formula with explanation
    formula_latex=r"A = \pi r^2",
    formula_explanation="..."
)
```

**Concepts implemented:**
- Circle Area (A = πr²)
- Radius (r = d/2)
- Pi (π ≈ 3.14159)
- Derivatives (f'(x))

---

### 2. Visual Transform Engine (`visual/transform.py`)

Transforms mathematical concepts into visual animations:

```python
# Example: Circle expansion showing quadratic growth
animation = engine.create_circle_expansion(
    start_radius=1.5,
    end_radius=3.0,
    duration=2.0
)
# Result: r: 1.5 -> 3.0, Area: 7.07 -> 28.27 (4x increase!)
```

**Key Features:**
- Easing functions (smooth, linear, ease_in, ease_out, etc.)
- State interpolation between mathematical states
- Visual elements (circles, lines, text, graphs)
- Pedagogical sequences for teaching

---

### 3. Frame Renderer (`render/renderer.py`)

Converts visual states to actual images:

```python
renderer = FrameRenderer()
img = renderer.render_frame(state, elements, title, subtitle)
img.save("frame.png")

# Or generate GIF
create_gif(frames, "animation.gif")
```

**Capabilities:**
- 60 FPS animation generation
- PNG frame sequences
- Animated GIF export
- Interactive HTML generation

---

### 4. Teaching Orchestrator (`orchestrator/engine.py`)

Main teaching orchestration:

```python
engine = MathFlowEngine()
lesson = engine.build_lesson("circle_area")
engine.teach(lesson)
```

**Lessons built:**
- Circle Area (Why is A = πr²?)
- Derivatives (What is a derivative?)

Each lesson has 4-5 steps with:
- The Mystery (problem first)
- Building intuition
- The formula discovery
- Interactive application

---

### 5. Interactive Playground (`interactive/playground.py`)

Phase 2 - Discovery learning:

```python
playground = CirclePlayground()
playground.set_value("radius", 3.0)
results = playground.evaluate()
# Area automatically recalculates
```

**Features:**
- Sliders for manipulation
- Observations (calculated values)
- Discovery tracking (auto-detects patterns)
- Interactive HTML generation

---

## Files Created

```
MathFlowEngine/
├── README.md                 (this file)
├── requirements.txt          # pillow, numpy
├── docs/
│   └── TEACHING_GUIDE.md    # Quick start guide
├── core/
│   ├── __init__.py
│   └── concepts.py         # Concept & ConceptGraph
├── visual/
│   ├── __init__.py
│   └── transform.py        # VisualTransformEngine
├── render/
│   └── renderer.py       # FrameRenderer
├── orchestrator/
│   └── engine.py         # MathFlowEngine
└── interactive/
    └── playground.py    # InteractivePlayground
```

---

## Demonstrations Created

### 1. Circle Expansion Animation
- **Location:** `animation_frames/circle_expansion.gif`
- **Shows:** Circle expanding from r=1.5 to r=3.0
- **Key insight:** Area increases 4x (quadratic relationship)

### 2. Math Flow Engine Teaching
- **Location:** `math_flow_engine/output/step_5/animation.gif`
- **Shows:** Full 5-step lesson sequence
- **Key insight:** Visual + discovery approach

### 3. Interactive HTML Playground
- **Location:** `math_flow_engine/interactive_playground.html`
- **Allows:** Student drag sliders to discover relationships auto-magically

---

## Teaching Approach (For Teachers)

### Day 1: Hook + Problem
- Ask real-world question
- Let students discuss

### Day 2: Build Intuition
- Show visual transformations
- Ask "What do you notice?"

### Day 3: Formalize
- Introduce notation
- Connect to their discoveries

### Day 4: Pattern Discovery
- Let them calculate
- Guide to pattern

### Day 5: Application
- Real problems
- Connect to real life (speedometer!)

---

## Research Document Analyzed

We analyzed `psychology_math_study_methods_analysis.md` which confirmed our approach:

| Research Finding | Our Implementation |
|-----------------|-------------------|
| Active Recall | Discovery tracker - students find patterns |
| Spaced Practice | Day-by-day sequence |
| Interleaving | Multiple concepts together |
| Concrete Examples | Circle animation |
| Dual Coding | GIF + HTML both |

---

## Usage

```python
# Basic
from orchestrator import MathFlowEngine

engine = MathFlowEngine()
lesson = engine.build_lesson("circle_area")
engine.teach(lesson)

# Interactive
from interactive import CirclePlayground
playground = CirclePlayground()
playground.set_value("radius", 2.0)
print(playground.evaluate())
# {"Area": 12.57, "Circumference": 12.57}
```

---

## Future Enhancements

Possible additions:
- More concepts (limits, integrals, series)
- Spaced repetition scheduling
- Error analysis
- Student progress tracking
- Voiceover generation
- Multi-language support

---

## Credits

Built with guidance from:
- Evidence-based learning research
- 3Blue1Brown's teaching philosophy
- Manim community

---

**Philosophy:** Let students discover, don't just tell them.

---

*Last Updated: May 8, 2026 23:30 UTC*