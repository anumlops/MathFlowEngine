"""
MathFlowEngine - The Brain Module
=================================
Based on Grant Sanderson's (3Blue1Brown) teaching methodology.

This module encapsulates the pedagogical intelligence that makes
mathematical concepts click for learners.

Core Principles (from Sanderson):
1. Intuition FIRST, formalization SECOND
2. Problem-First: Compelling question before explanation
3. Transformation over Static: Animation reveals structure
4. One core idea per lesson
5. Prerequisites just-in-time, not front-loaded
6. Pattern discovery before formula
7. Multiple visual representations
8. Make abstract concrete through animation
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
from enum import Enum
from abc import ABC, abstractmethod


class TeachingPhase(Enum):
    """The 5 phases of a Sanderson-style lesson."""
    PROBLEM = "problem"           # Open with compelling question
    INTUITION = "intuition"       # Animation reveals pattern
    PATTERN = "pattern"           # Pause, let pattern crystallize
    FORMALIZATION = "formalization"  # Brief notation after intuition
    RESOLUTION = "resolution"     # Original problem solved


class AnimationTechnique(Enum):
    """Animation techniques from manim/Sanderson."""
    TRANSFORM = "transform"       # Concept A morphs into B
    ZOOM = "zoom"                 # Reveal structure at multiple scales
    PAN = "pan"                   # Camera movement to direct attention
    HIGHLIGHT = "highlight"       # Point lights draw attention
    REVEAL = "reveal"             # Progressive disclosure
    SUPERIMPOSE = "superimpose"   # Overlay comparisons


class VisualRepresentation(Enum):
    """Types of visual representations."""
    GEOMETRIC = "geometric"       # Shapes, diagrams
    GRAPH = "graph"               # Plots, functions
    NUMBER_LINE = "number_line"    # Real number visualization
    PHYSICAL = "physical"         # Physical metaphors
    ABSTRACT = "abstract"         # Pure mathematical


@dataclass
class SandersonStep:
    """
    A single teaching step following Sanderson's template.

    Structure:
    1. Phase: Which phase of the lesson
    2. Visual: What animation reveals this
    3. Discovery: What the learner should notice
    4. Formal: When to introduce notation
    """
    phase: TeachingPhase
    title: str

    # What animation reveals this step
    animation_technique: AnimationTechnique
    visual_description: str  # "Zoom into curve showing tangent approach"
    metaphor: str  # "Like zooming into a map"

    # What learner should discover
    discovery_prompt: str  # "What do you notice as h gets smaller?"
    expected_discovery: str  # "The secant line approaches the tangent"

    # How to introduce formal notation (if any)
    formal_notation: Optional[str] = None
    formal_explanation: Optional[str] = None

    # Duration guidance
    pause_duration: float = 2.0  # Seconds to pause for pattern to crystallize

    # Prerequisites for this step (just-in-time)
    prerequisite_concepts: List[str] = field(default_factory=list)

    # Misconception handling
    anticipated_misconception: Optional[str] = None
    misconception_correction: Optional[str] = None


@dataclass
class VisualMetaphor:
    """
    A concrete visual metaphor for an abstract concept.

    Example: "Vectors are like arrows pointing somewhere"
    """
    concept_id: str
    metaphor: str
    visual_representation: VisualRepresentation
    animation_behavior: str  # How this metaphor animates
    limitations: Optional[str] = None  # When metaphor breaks down


class SandersonLessonDesigner:
    """
    Designs lessons following Grant Sanderson's methodology.

    Usage:
        designer = SandersonLessonDesigner()
        lesson_design = designer.design("derivative")
    """

    # The core teaching template
    LESSON_TEMPLATE = [
        TeachingPhase.PROBLEM,
        TeachingPhase.INTUITION,
        TeachingPhase.PATTERN,
        TeachingPhase.FORMALIZATION,
        TeachingPhase.RESOLUTION
    ]

    def __init__(self):
        self.visual_metaphors: Dict[str, List[VisualMetaphor]] = {}

    def design(self, concept_id: str, concept_data: Dict) -> List[SandersonStep]:
        """
        Design a lesson following Sanderson's template.

        Args:
            concept_id: The concept to teach
            concept_data: Contains intuition, problem, formula, etc.

        Returns:
            List of SandersonSteps following the teaching template
        """
        steps = []

        # Phase 1: PROBLEM - Open with compelling question
        problem_steps = self._design_problem_phase(concept_id, concept_data)
        steps.extend(problem_steps)

        # Phase 2: INTUITION - Animation reveals pattern
        intuition_steps = self._design_intuition_phase(concept_id, concept_data)
        steps.extend(intuition_steps)

        # Phase 3: PATTERN - Pause and let pattern crystallize
        pattern_steps = self._design_pattern_phase(concept_id, concept_data)
        steps.extend(pattern_steps)

        # Phase 4: FORMALIZATION - Brief notation after intuition
        formal_steps = self._design_formalization_phase(concept_id, concept_data)
        steps.extend(formal_steps)

        # Phase 5: RESOLUTION - Original problem solved
        resolution_steps = self._design_resolution_phase(concept_id, concept_data)
        steps.extend(resolution_steps)

        return steps

    def _design_problem_phase(self, concept_id: str, data: Dict) -> List[SandersonStep]:
        """Phase 1: Open with compelling question/mystery."""
        problem = data.get("problem_motivated_by", "")

        # Transform problem into visual question
        visual_question = self._problem_to_visual(problem)

        return [SandersonStep(
            phase=TeachingPhase.PROBLEM,
            title="The Mystery",
            animation_technique=AnimationTechnique.REVEAL,
            visual_description=visual_question,
            metaphor="A compelling question that makes you want to know",
            discovery_prompt="What do you wonder about?",
            expected_discovery="Curiosity about the problem",
            prerequisite_concepts=[]
        )]

    def _design_intuition_phase(self, concept_id: str, data: Dict) -> List[SandersonStep]:
        """Phase 2: Animation reveals pattern (THE CORE)."""
        intuition = data.get("intuition", "")
        visual = data.get("default_visual", "")

        steps = []

        # Find or create visual metaphor
        metaphor = self._get_visual_metaphor(concept_id, intuition)

        # Primary intuition animation
        steps.append(SandersonStep(
            phase=TeachingPhase.INTUITION,
            title="Building Intuition",
            animation_technique=AnimationTechnique.TRANSFORM,
            visual_description=f"Animation showing: {intuition}",
            metaphor=metaphor.metaphor if metaphor else intuition,
            discovery_prompt="What do you notice happening?",
            expected_discovery="Pattern emerges through transformation",
            prerequisite_concepts=data.get("prerequisites", [])
        ))

        # Secondary animation: show from different angle
        if data.get("alternative_visual"):
            steps.append(SandersonStep(
                phase=TeachingPhase.INTUITION,
                title="Another View",
                animation_technique=AnimationTechnique.ZOOM,
                visual_description=f"Zoom to reveal: {data['alternative_visual']}",
                metaphor="Same concept, different perspective",
                discovery_prompt="How does this view compare?",
                expected_discovery="Understanding deepens through multiple views",
                prerequisite_concepts=[]
            ))

        return steps

    def _design_pattern_phase(self, concept_id: str, data: Dict) -> List[SandersonStep]:
        """Phase 3: Pause, let pattern crystallize."""

        # This is the "What do you notice?" moment
        return [SandersonStep(
            phase=TeachingPhase.PATTERN,
            title="Pattern Discovery",
            animation_technique=AnimationTechnique.HIGHLIGHT,
            visual_description="Highlight the key pattern that emerged",
            metaphor="The 'aha!' moment",
            discovery_prompt="What pattern do you see?",
            expected_discovery=data.get("key_insight", ""),
            pause_duration=3.0,  # Longer pause here
            prerequisite_concepts=[]
        )]

    def _design_formalization_phase(self, concept_id: str, data: Dict) -> List[SandersonStep]:
        """Phase 4: Brief notation after intuition."""

        return [SandersonStep(
            phase=TeachingPhase.FORMALIZATION,
            title="The Formal Way",
            animation_technique=AnimationTechnique.SUPERIMPOSE,
            visual_description=f"Show formula appearing: {data.get('formula_latex', '')}",
            metaphor="Notation now makes sense",
            discovery_prompt="How does this formula relate to what you saw?",
            expected_discovery="Formula feels earned, not arbitrary",
            formal_notation=data.get("formula_latex"),
            formal_explanation=data.get("formula_explanation"),
            prerequisite_concepts=[]
        )]

    def _design_resolution_phase(self, concept_id: str, data: Dict) -> List[SandersonStep]:
        """Phase 5: Original problem solved with new understanding."""

        return [SandersonStep(
            phase=TeachingPhase.RESOLUTION,
            title="Now We Understand",
            animation_technique=AnimationTechnique.TRANSFORM,
            visual_description="Solve original problem using new understanding",
            metaphor="The circle is complete",
            discovery_prompt="Can you explain why this works?",
            expected_discovery="Deep understanding achieved",
            prerequisite_concepts=[]
        )]

    def _problem_to_visual(self, problem: str) -> str:
        """Transform a text problem into a visual description."""
        # Simple transformation - could be enhanced with LLM
        return f"Visual representation of: {problem[:100]}..."

    def _get_visual_metaphor(self, concept_id: str, intuition: str) -> Optional[VisualMetaphor]:
        """Get or create a visual metaphor for a concept."""
        if concept_id in self.visual_metaphors:
            return self.visual_metaphors[concept_id][0]
        return None

    def register_metaphor(self, metaphor: VisualMetaphor):
        """Register a visual metaphor for later use."""
        if metaphor.concept_id not in self.visual_metaphors:
            self.visual_metaphors[metaphor.concept_id] = []
        self.visual_metaphors[metaphor.concept_id].append(metaphor)


class IntuitionBuilder:
    """
    Builds intuition for concepts using Sanderson's approach.

    Key principle: "Get intuition first, then definition"
    """

    # Metaphor library for common concepts
    METAPHORS = {
        # CALCULUS
        "derivative": VisualMetaphor(
            concept_id="derivative",
            metaphor="Like a car's speedometer - shows speed RIGHT NOW",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Needle moving as speed changes",
            limitations="Doesn't show acceleration directly"
        ),
        "limit": VisualMetaphor(
            concept_id="limit",
            metaphor="Approaching a destination but never quite arriving",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Object getting closer but never touching",
            limitations="Some limits are reached"
        ),
        "integral": VisualMetaphor(
            concept_id="integral",
            metaphor="Adding up infinitely thin slices of area",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Rectangles stacking up under curve",
            limitations="Can be negative when curve is below axis"
        ),
        "continuity": VisualMetaphor(
            concept_id="continuity",
            metaphor="Drawing without lifting your pen",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Pen traces smoothly across paper",
            limitations="Has holes or jumps = not continuous"
        ),
        "chain_rule": VisualMetaphor(
            concept_id="chain_rule",
            metaphor="Nesting dolls - each affects the next",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="One doll opening reveals another inside",
            limitations="Complex nested functions get confusing"
        ),
        "antiderivative": VisualMetaphor(
            concept_id="antiderivative",
            metaphor="Rewinding a speedometer to find the original distance",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Running time backwards, accumulating distance",
            limitations="Plus constant - we don't know starting point"
        ),

        # LINEAR ALGEBRA
        "vector": VisualMetaphor(
            concept_id="vector",
            metaphor="An arrow with direction and length - where to go",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Arrow pointing somewhere, can be stretched",
            limitations="High dimensions are hard to visualize"
        ),
        "basis": VisualMetaphor(
            concept_id="basis",
            metaphor="The building blocks that define your coordinate system",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Unit arrows at right angles, everything measured from them",
            limitations="Different bases give different coordinates for same vector"
        ),
        "linear_transformation": VisualMetaphor(
            concept_id="linear_transformation",
            metaphor="A special machine that warps space but keeps lines straight",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Grid of parallel lines stays parallel after transformation",
            limitations="Only works for linear (straight-line) operations"
        ),
        "matrix": VisualMetaphor(
            concept_id="matrix",
            metaphor="A machine that transforms space - inputs become outputs",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Space stretching, rotating, flipping",
            limitations="Not all transformations are linear"
        ),
        "eigenvalue": VisualMetaphor(
            concept_id="eigenvalue",
            metaphor="Axes that don't rotate under transformation - they just stretch",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Blue line stays blue, red stays red, only stretches",
            limitations="Complex eigenvalues have no real eigenvectors"
        ),
        "determinant": VisualMetaphor(
            concept_id="determinant",
            metaphor="How much a transformation stretches or flips space",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Area of unit square becomes determinant area, sign = flip",
            limitations="Zero determinant = squishes to flat line"
        ),
        "dot_product": VisualMetaphor(
            concept_id="dot_product",
            metaphor="How aligned are two arrows? Points same direction = high",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Two arrows, project one onto other, measure overlap",
            limitations="Measures alignment, not perpendicularity"
        ),
        "cross_product": VisualMetaphor(
            concept_id="cross_product",
            metaphor="Creates a NEW arrow perpendicular to both inputs",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Two arrows spinning, right-hand rule points result",
            limitations="Only exists in 3D, not 2D"
        ),

        # ALGEBRA & FUNCTIONS
        "function": VisualMetaphor(
            concept_id="function",
            metaphor="A machine - you put in a number, get out exactly one number",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Input enters one end, transformed output exits other",
            limitations="Each input must have exactly one output"
        ),
        "exponential": VisualMetaphor(
            concept_id="exponential",
            metaphor="Growth that accelerates - more you have, faster you grow",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Curve bending upward steeper and steeper",
            limitations="Can grow or decay depending on base"
        ),
        "logarithm": VisualMetaphor(
            concept_id="logarithm",
            metaphor="The EXPONENT needed to get your number - undoing exponentiation",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="As exponential grows, logarithm grows slower",
            limitations="Only works for positive numbers"
        ),
        "quadratic": VisualMetaphor(
            concept_id="quadratic",
            metaphor="A parabola - like a U-shape that opens up or down",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Arc bending symmetrically around vertex",
            limitations="Only symmetrical U-shapes, not all curves"
        ),
        "polynomial": VisualMetaphor(
            concept_id="polynomial",
            metaphor="Wavy hills and valleys made by combining x powers",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Higher degree = more turns and wiggles",
            limitations="Always smooth curves, no sharp corners"
        ),
        "asymptote": VisualMetaphor(
            concept_id="asymptote",
            metaphor="A line the curve approaches but never touches",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Curve getting closer and closer to line but staying away",
            limitations="Some curves cross their asymptotes"
        ),

        # GEOMETRY
        "circle_area": VisualMetaphor(
            concept_id="circle_area",
            metaphor="A pizza spinning and stretching outward from center",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Circle expanding, area filling every direction",
            limitations="Large circles still behave the same way"
        ),
        "pythagorean": VisualMetaphor(
            concept_id="pythagorean",
            metaphor="The two smaller squares always equal the big one",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Squares on triangle sides rearranging to match hypotenuse",
            limitations="Only works for RIGHT triangles"
        ),
        "sine": VisualMetaphor(
            concept_id="sine",
            metaphor="Shadow length of a spinning circle's point",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Point rotating on circle, vertical shadow tracing wave",
            limitations="Requires understanding circle as reference"
        ),
        "cosine": VisualMetaphor(
            concept_id="cosine",
            metaphor="Horizontal shadow of a spinning circle's point",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Point rotating, horizontal shadow tracing cosine wave",
            limitations="Just shifted sine wave"
        ),
        "tangent": VisualMetaphor(
            concept_id="tangent",
            metaphor="A line that touches the circle at exactly one point",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Line just grazing curve, not crossing through",
            limitations="At different points, different tangent lines"
        ),
        "radians": VisualMetaphor(
            concept_id="radians",
            metaphor="Distance around the circle measured in radius lengths",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Arc length = radius length, angles measured by arc",
            limitations="Not as intuitive as degrees"
        ),

        # TRIGONOMETRY
        "unit_circle": VisualMetaphor(
            concept_id="unit_circle",
            metaphor="A clock face where coordinates tell you trig values",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Point moving around circle, (cos θ, sin θ) always shown",
            limitations="Radius = 1, so scaled differently than general circles"
        ),
        "trig_identity": VisualMetaphor(
            concept_id="trig_identity",
            metaphor="Pythagoras living on the unit circle - sin² + cos² = 1",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Triangle inside unit circle, identity visualized",
            limitations="Only true for sin and cos on unit circle"
        ),
        "phase_shift": VisualMetaphor(
            concept_id="phase_shift",
            metaphor="Shifting the wave left or right - same wave, different start",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Sine wave sliding horizontally, peak moves",
            limitations="Only shifts horizontally, not vertically"
        ),

        # CALCULUS APPLICATIONS
        "optimization": VisualMetaphor(
            concept_id="optimization",
            metaphor="Finding the highest peak or lowest valley on a landscape",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Ball rolling to bottom of valley or top of hill",
            limitations="Local vs global maxima/minima"
        ),
        "related_rates": VisualMetaphor(
            concept_id="related_rates",
            metaphor="Connected wheels turning - one spin affects the others",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Gears connected, rotation of one spins others proportionally",
            limitations="Must identify relationship between variables"
        ),
        "taylor_series": VisualMetaphor(
            concept_id="taylor_series",
            metaphor="Zooms into a curve and approximates it with a polynomial",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Magnifying glass on curve, polynomial matching perfectly at point",
            limitations="Only accurate near the center point"
        ),
        "lhopitals_rule": VisualMetaphor(
            concept_id="lhopitals_rule",
            metaphor="When 0/0 or ∞/∞, take another look - derivatives might reveal truth",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Indeterminate form being differentiated to find limit",
            limitations="Only works for 0/0 or ∞/∞ cases"
        ),

        # PROBABILITY & STATISTICS
        "expected_value": VisualMetaphor(
            concept_id="expected_value",
            metaphor="The average you'd get if you repeated forever",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Many trials averaging out to expected value",
            limitations="Rare events can still happen despite low probability"
        ),
        "variance": VisualMetaphor(
            concept_id="variance",
            metaphor="How spread out from the average - bigger = more scattered",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Data points spreading from center, showing spread",
            limitations="Sensitive to outliers"
        ),
        "normal_distribution": VisualMetaphor(
            concept_id="normal_distribution",
            metaphor="The bell curve - most things cluster around average",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Bell-shaped curve, data piling at mean",
            limitations="Not all data follows normal distribution"
        ),
        "bayes_theorem": VisualMetaphor(
            concept_id="bayes_theorem",
            metaphor="Updating beliefs with new evidence - revising probability",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Prior probability updating to posterior with new data",
            limitations="Depends heavily on prior probability choice"
        ),

        # DISCRETE MATH
        "recursion": VisualMetaphor(
            concept_id="recursion",
            metaphor="Russian nesting dolls - each contains a smaller version of itself",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Doll opening to reveal smaller doll inside",
            limitations="Can be infinite if not careful"
        ),
        "combinatorics": VisualMetaphor(
            concept_id="combinatorics",
            metaphor="Counting ways to arrange or choose - combinations vs permutations",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Arrangements being counted systematically",
            limitations="Factorials grow extremely fast"
        ),
        "graph_theory": VisualMetaphor(
            concept_id="graph_theory",
            metaphor="Friendship network - dots (people) connected by lines (friendships)",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Nodes and edges forming network",
            limitations="Abstracts away edge weights and types"
        ),

        # MULTIVARIABLE
        "partial_derivative": VisualMetaphor(
            concept_id="partial_derivative",
            metaphor="Slicing through 3D terrain - what's the steepest direction?",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Plane cutting through surface, slope measured in one direction",
            limitations="Ignores changes in other directions"
        ),
        "gradient": VisualMetaphor(
            concept_id="gradient",
            metaphor="The direction of steepest ascent on a mountain",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Arrow pointing uphill in direction of maximum slope",
            limitations="Only shows direction, not magnitude clearly"
        ),
        "divergence": VisualMetaphor(
            concept_id="divergence",
            metaphor="Spraying water - outward flow from a point",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Arrows pointing outward from center",
            limitations="Positive = outward, negative = inward"
        ),
        "curl": VisualMetaphor(
            concept_id="curl",
            metaphor="Twisting water - rotation at a point",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Arrows swirling around like a vortex",
            limitations="Measures rotation, not overall flow"
        ),

        # DIFFERENTIAL EQUATIONS
        "differential_equation": VisualMetaphor(
            concept_id="differential_equation",
            metaphor="Describing how things change - the change itself is the equation",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Slope field showing direction of solution at each point",
            limitations="Often can't solve exactly, only numerically"
        ),
        "initial_condition": VisualMetaphor(
            concept_id="initial_condition",
            metaphor="Where you start determines where you'll end up",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Solution curve starting from specific point",
            limitations="Different starting points = different curves"
        )
    }

    @classmethod
    def get_metaphor(cls, concept_id: str) -> Optional[VisualMetaphor]:
        """Get a pre-built metaphor for a concept."""
        return cls.METAPHORS.get(concept_id)

    @classmethod
    def build_intuition(cls, concept_id: str) -> Dict:
        """
        Build complete intuition context for a concept.

        Returns:
            Dictionary with: metaphor, animation_plan, key_insights
        """
        metaphor = cls.get_metaphor(concept_id)

        if not metaphor:
            return {
                "metaphor": None,
                "animation_plan": [],
                "key_insights": []
            }

        # Build animation plan based on metaphor
        animation_plan = cls._build_animation_plan(metaphor)

        return {
            "metaphor": metaphor,
            "animation_plan": animation_plan,
            "key_insights": cls._extract_insights(metaphor)
        }

    @classmethod
    def _build_animation_plan(cls, metaphor: VisualMetaphor) -> List[Dict]:
        """Build animation sequence from metaphor."""
        return [
            {"type": "introduce", "description": f"Show: {metaphor.metaphor}"},
            {"type": "animate", "description": metaphor.animation_behavior},
            {"type": "transform", "description": "Show concept morphing"},
            {"type": "pause", "duration": 2.0, "prompt": "What do you notice?"}
        ]

    @classmethod
    def _extract_insights(cls, metaphor: VisualMetaphor) -> List[str]:
        """Extract key insights from metaphor."""
        insights = [metaphor.metaphor]
        if metaphor.limitations:
            insights.append(f"But: {metaphor.limitations}")
        return insights


class MisconceptionHandler:
    """
    Handles misconceptions following Sanderson's approach.

    Key principle: Show what goes wrong when misconception is held.
    """

    MISCONCEPTIONS = {
        # CALCULUS
        "derivative": [
            {
                "misconception": "Derivative is a fraction",
                "correction": "dy/dx is notation showing ratio, not actual division",
                "animation": "Show d as notation, not a number"
            },
            {
                "misconception": "Derivative equals slope",
                "correction": "Derivative AT a point = slope; derivative function = slope everywhere",
                "animation": "Show point where slope = derivative value"
            }
        ],
        "limit": [
            {
                "misconception": "Limit equals the value",
                "correction": "Limit is approaching, not arriving",
                "animation": "Show approaching but never reaching"
            },
            {
                "misconception": "0/0 = 0",
                "correction": "0/0 is indeterminate - could be anything",
                "animation": "Show different functions giving different limits"
            }
        ],
        "integral": [
            {
                "misconception": "Integral always gives positive area",
                "correction": "Below x-axis gives negative area",
                "animation": "Show parts below axis subtracting"
            },
            {
                "misconception": "Integration is the opposite of differentiation",
                "correction": "It's the inverse, but with +C (we don't know starting point)",
                "animation": "Show many curves with same derivative"
            }
        ],
        "chain_rule": [
            {
                "misconception": "Just multiply derivatives",
                "correction": "Must multiply outer derivative by inner derivative",
                "animation": "Show nesting, derivative of each layer"
            }
        ],
        "taylor_series": [
            {
                "misconception": "Infinite series converges to exact value",
                "correction": "Only converges in radius of convergence",
                "animation": "Show diverging at edges"
            }
        ],

        # LINEAR ALGEBRA
        "matrix": [
            {
                "misconception": "Matrix is a grid of numbers",
                "correction": "Matrix is a transformation machine",
                "animation": "Show grid becoming transformation"
            },
            {
                "misconception": "Matrix multiplication is commutative",
                "correction": "AB ≠ BA in general",
                "animation": "Show transformation order matters"
            }
        ],
        "eigenvalue": [
            {
                "misconception": "Eigenvalues are always real numbers",
                "correction": "Can be complex for rotation-heavy transformations",
                "animation": "Show rotation without real eigenvectors"
            },
            {
                "misconception": "Eigenvalue tells you where vector goes",
                "correction": "Eigenvalue tells you how much vector stretches",
                "animation": "Show eigenvector staying on its line"
            }
        ],
        "determinant": [
            {
                "misconception": "Larger determinant = larger transformation",
                "correction": "Determinant = area scaling factor (can be negative)",
                "animation": "Show flip giving negative determinant"
            },
            {
                "misconception": "Determinant tells the shape",
                "correction": "Determinant only tells volume/area scaling",
                "animation": "Show different shapes with same determinant"
            }
        ],
        "dot_product": [
            {
                "misconception": "Dot product gives a vector",
                "correction": "Dot product gives a SCALAR (number)",
                "animation": "Show two arrows producing single number"
            },
            {
                "misconception": "Higher dot product = better",
                "correction": "Sign matters: positive = aligned, negative = opposite",
                "animation": "Show aligned vs opposite arrows"
            }
        ],
        "basis": [
            {
                "misconception": "The standard basis is the only basis",
                "correction": "Many bases exist, each gives different coordinates",
                "animation": "Show same vector in different bases"
            }
        ],

        # ALGEBRA & FUNCTIONS
        "exponential": [
            {
                "misconception": "Exponential grows slower than polynomial",
                "correction": "Exponential eventually outgrows ANY polynomial",
                "animation": "Show exponential catching and passing polynomial"
            }
        ],
        "logarithm": [
            {
                "misconception": "log(x) + log(y) = log(x+y)",
                "correction": "log(x) + log(y) = log(xy)",
                "animation": "Show log rules with numbers"
            },
            {
                "misconception": "Log of negative number exists",
                "correction": "Log only defined for positive numbers",
                "animation": "Show calculator error for log(-1)"
            }
        ],
        "quadratic": [
            {
                "misconception": "x² = 9 has one solution (x = 3)",
                "correction": "Two solutions: x = 3 and x = -3",
                "animation": "Show parabola crossing x-axis twice"
            }
        ],

        # TRIGONOMETRY
        "sine": [
            {
                "misconception": "sin(x) = y",
                "correction": "sin is a function, y = sin(x) is the graph",
                "animation": "Show full circle projection context"
            },
            {
                "misconception": "sin(30) = cos(30)",
                "correction": "sin(30) = 0.5, cos(30) = √3/2",
                "animation": "Show 30° in first quadrant, values differ"
            }
        ],
        "cosine": [
            {
                "misconception": "Cosine is just shifted sine",
                "correction": "Yes! cos(x) = sin(x + π/2) - but understanding WHY matters",
                "animation": "Show cosine as rotated sine"
            }
        ],
        "tangent": [
            {
                "misconception": "Tangent line touches but doesn't cross",
                "correction": "That's one definition, but tangent can cross in some cases",
                "animation": "Show different tangent behaviors"
            }
        ],
        "radians": [
            {
                "misconception": "Radians are just converted degrees",
                "correction": "Radians are natural - ratio of arc length to radius",
                "animation": "Show arc length = radius × angle in radians"
            }
        ],

        # PROBABILITY
        "expected_value": [
            {
                "misconception": "Expected value is what you'll get",
                "correction": "It's the average, not what you actually get",
                "animation": "Show many trials with varied outcomes"
            }
        ],
        "variance": [
            {
                "misconception": "Variance is the spread",
                "correction": "Variance is spread² (units squared) - use std dev for spread",
                "animation": "Show units squaring effect"
            }
        ],
        "bayes_theorem": [
            {
                "misconception": "P(A|B) = P(B|A)",
                "correction": "Only equal if P(A) = P(B)",
                "animation": "Show different priors giving different results"
            }
        ],

        # MULTIVARIABLE
        "gradient": [
            {
                "misconception": "Gradient points to the maximum",
                "correction": "Gradient points in direction of steepest ASCENT",
                "animation": "Show ball rolling uphill in gradient direction"
            },
            {
                "misconception": "Gradient is zero at maximum",
                "correction": "Gradient is zero AT extremum, not around it",
                "animation": "Show flat spot at peak"
            }
        ],
        "curl": [
            {
                "misconception": "Curl measures rotation speed",
                "correction": "Curl measures tendency to rotate at a POINT",
                "animation": "Show local spinning in vector field"
            }
        ],

        # DISCRETE MATH
        "recursion": [
            {
                "misconception": "Recursion goes on forever",
                "correction": "Must have base case to stop",
                "animation": "Show dolls eventually reaching smallest"
            }
        ],
        "combinatorics": [
            {
                "misconception": "nCr = nPr",
                "correction": "nCr = nPr / r! - order doesn't matter in combinations",
                "animation": "Show permutations vs combinations"
            }
        ],

        # GENERAL
        "negative_exponents": [
            {
                "misconception": "Makes things smaller",
                "correction": "2^-3 = 1/8, can be larger than 2^2",
                "animation": "Show scaling down visually"
            }
        ],
        "function": [
            {
                "misconception": "x² = y² means x = y",
                "correction": "Could be x = y or x = -y",
                "animation": "Show both positive and negative roots"
            }
        ]
    }

    @classmethod
    def get_misconceptions(cls, concept_id: str) -> List[Dict]:
        """Get anticipated misconceptions for a concept."""
        return cls.MISCONCEPTIONS.get(concept_id, [])

    @classmethod
    def design_misconception_correction(cls, concept_id: str) -> List[SandersonStep]:
        """Design steps that address misconceptions."""
        misconceptions = cls.get_misconceptions(concept_id)
        steps = []

        for m in misconceptions:
            steps.append(SandersonStep(
                phase=TeachingPhase.INTUITION,
                title=f"Common Misconception: {m['misconception']}",
                animation_technique=AnimationTechnique.TRANSFORM,
                visual_description=m["animation"],
                metaphor=m["misconception"],
                discovery_prompt="What's wrong here?",
                expected_discovery=m["correction"],
                anticipated_misconception=m["misconception"],
                misconception_correction=m["correction"],
                pause_duration=3.0
            ))

        return steps


class TeachingSequenceBuilder:
    """
    Builds proper teaching sequences following Sanderson's principles.

    Key principle: Prerequisites just-in-time, not front-loaded.
    """

    @staticmethod
    def build_sequence(concept_id: str, graph: 'ConceptGraph') -> List[str]:
        """
        Build learning sequence using just-in-time prerequisite introduction.

        Unlike traditional approaches that front-load prerequisites,
        this introduces them when context reveals need.

        Returns:
            Ordered list of concept IDs
        """
        sequence = []
        introduced = set()

        def visit(cid: str, depth: int = 0):
            if cid in introduced:
                return

            prerequisites = graph.get_prerequisites(cid)

            # Only introduce prerequisites if context makes them relevant
            # (This is the "just-in-time" principle)
            for prereq in prerequisites:
                if prereq not in introduced:
                    # Check if this concept truly needs the prerequisite
                    # to understand the current problem
                    visit(prereq, depth + 1)

            introduced.add(cid)
            sequence.append(cid)

        visit(concept_id)
        return sequence

    @staticmethod
    def create_discovery_moments(concept_id: str) -> List[str]:
        """
        Identify moments where learner should have discovery.

        These are the "What do you notice?" moments.
        """
        discovery_points = []

        # For each phase, identify discovery opportunity
        if concept_id == "derivative":
            discovery_points = [
                "As h gets smaller, the secant line approaches...",
                "The two points get closer together...",
                "The slope stabilizes to a single value..."
            ]
        elif concept_id == "limit":
            discovery_points = [
                "The value gets closer but never reaches...",
                "The gap shrinks to nearly zero..."
            ]
        elif concept_id == "circle_area":
            discovery_points = [
                "The pieces fit together to form a rectangle...",
                "Height = r, width = pi*r (half circumference)..."
            ]

        return discovery_points


class TransformationEngine:
    """
    Core engine for creating transformations like Sanderson.

    Key technique: Show concept A morphing into B.
    """

    TRANSFORMATIONS = {
        # CALCULUS
        "secant_to_tangent": {
            "from": "Two points on curve with secant line",
            "to": "One point with tangent line",
            "how": "Animate one point approaching the other, line rotating to tangent",
            "insight": "Derivative = slope of tangent line"
        },
        "rectangle_to_approximation": {
            "from": "Rectangles approximating area under curve",
            "to": "Smooth curve",
            "how": "Increase number of rectangles, width shrinks",
            "insight": "Integral = limit of Riemann sums"
        },
        "piecewise_to_smooth": {
            "from": "Many small line segments",
            "to": "Smooth curve",
            "how": "Connect segments smoothly, show transition",
            "insight": "Limits create smooth functions"
        },
        "slope_field_to_solution": {
            "from": "Arrow field showing direction at each point",
            "to": "Solution curve following the arrows",
            "how": "Draw curve tangent to all arrows",
            "insight": "Differential equations define solution families"
        },

        # LINEAR ALGEBRA
        "grid_to_transformation": {
            "from": "Square grid with basis vectors",
            "to": "Transformed parallelogram grid",
            "how": "Apply matrix to each grid point, show stretching",
            "insight": "Matrix = transformation machine"
        },
        "vector_to_basis": {
            "from": "Single vector in space",
            "to": "Decomposition into basis vectors with coefficients",
            "how": "Show vector as combination of basis arrows",
            "insight": "Vectors = linear combination of basis"
        },
        "rotation_matrix": {
            "from": "Original shape at angle 0",
            "to": "Shape rotated by theta",
            "how": "Apply rotation matrix, basis vectors spinning",
            "insight": "Rotation matrix encodes angular transformation"
        },
        "eigenvector_unchanged": {
            "from": "Vector on its own line",
            "to": "Same line after transformation, only stretched",
            "how": "Show vector staying on line, only changing length",
            "insight": "Eigenvectors don't change direction under transformation"
        },
        "determinant_area": {
            "from": "Unit square with area 1",
            "to": "Parallelogram with area = determinant",
            "how": "Transform unit square, measure resulting area",
            "insight": "Determinant = area scaling factor"
        },
        "null_space": {
            "from": "All vectors in space",
            "to": "Only vectors that collapse to zero",
            "how": "Show vectors landing at origin after transformation",
            "insight": "Null space = vectors destroyed by transformation"
        },

        # TRIGONOMETRY
        "circle_to_sine": {
            "from": "Point rotating around unit circle",
            "to": "Sine wave traced over time",
            "how": "Point on circle, vertical projection drawing wave",
            "insight": "Sine = vertical projection of unit circle"
        },
        "circle_to_cosine": {
            "from": "Point rotating around unit circle",
            "to": "Cosine wave traced over time",
            "how": "Point on circle, horizontal projection drawing wave",
            "insight": "Cosine = horizontal projection of unit circle"
        },
        "triangle_to_sin": {
            "from": "Right triangle inside circle",
            "to": "sin(θ) = opposite/hypotenuse",
            "how": "Show angle, label sides, calculate ratio",
            "insight": "Sine = opposite/hypotenuse in right triangle"
        },
        "sine_to_phase_shift": {
            "from": "sin(x) wave",
            "to": "sin(x + φ) wave shifted left",
            "how": "Shift wave horizontally, show phase change",
            "insight": "Phase shift = horizontal translation"
        },

        # ALGEBRA
        "factor_to_zeros": {
            "from": "Factored polynomial (x-a)(x-b)",
            "to": "Graph crossing x-axis at a and b",
            "how": "Show roots becoming x-intercepts",
            "insight": "Zeros of polynomial = x-intercepts"
        },
        "completing_square": {
            "from": "ax² + bx incomplete square",
            "to": "a(x + h)² + k complete square",
            "how": "Show rectangle pieces rearranging into square",
            "insight": "Completing square reveals vertex form"
        },
        "exponential_catching_polynomial": {
            "from": "Polynomial outgrowing exponential",
            "to": "Exponential eventually surpassing polynomial",
            "how": "Show both graphs, exponential catching and passing",
            "insight": "Exponential outgrows any polynomial eventually"
        },

        # GEOMETRY
        "circle_to_pi": {
            "from": "Circle with radius",
            "to": "Pi visualized as circumference/diameter ratio",
            "how": "Measure around and across, show ratio = π",
            "insight": "Pi = universal constant for all circles"
        },
        "pizza_slices_to_rectangle": {
            "from": "Circle cut into equal slices",
            "to": "Rectangle formed by rearranging slices",
            "how": "Cut circle, alternate slices, form rectangle",
            "insight": "Circle area = πr × r = πr²"
        },
        "right_triangle_to_hypotenuse": {
            "from": "Two smaller squares on legs",
            "to": "One large square on hypotenuse",
            "how": "Rearrange pieces from small squares into big",
            "insight": "a² + b² = c² (Pythagorean theorem)"
        },

        # PROBABILITY
        "trials_to_expected_value": {
            "from": "Many random trials with different outcomes",
            "to": "Outcomes averaging to expected value",
            "how": "Run many trials, show average converging",
            "insight": "Expected value = theoretical average"
        },
        "bell_curve_from_data": {
            "from": "Individual data points scattered",
            "to": "Smooth bell curve formed",
            "how": "Add more points, histogram smoothing",
            "insight": "Normal distribution emerges from many small factors"
        },

        # MULTIVARIABLE
        "surface_to_gradient": {
            "from": "3D surface showing height",
            "to": "Gradient arrows pointing uphill",
            "how": "At each point, show arrow in steepest direction",
            "insight": "Gradient = steepest ascent vector field"
        },
        "vector_field_to_divergence": {
            "from": "Vector field with arrows",
            "to": "Spraying (+) or absorbing (-) regions highlighted",
            "how": "Show arrows expanding or contracting at points",
            "insight": "Divergence = net outflow at a point"
        },
        "vector_field_to_curl": {
            "from": "Vector field with arrows",
            "to": "Spinning/swirling regions highlighted",
            "how": "Show arrows rotating around points",
            "insight": "Curl = tendency to rotate at a point"
        }
    }

    @classmethod
    def get_transformation(cls, name: str) -> Optional[Dict]:
        """Get a pre-defined transformation."""
        return cls.TRANSFORMATIONS.get(name)

    @classmethod
    def create_custom_transformation(cls, from_state: str, to_state: str) -> Dict:
        """Create a custom transformation."""
        return {
            "from": from_state,
            "to": to_state,
            "how": "Animate morphing from to state",
            "insight": "Relationship revealed through transformation"
        }


# Demo function
def demo():
    """Demonstrate Sanderson's brain in action."""
    print("=" * 60)
    print("MathFlowEngine Brain - Sanderson's Methodology")
    print("=" * 60)

    # Design a derivative lesson
    designer = SandersonLessonDesigner()

    concept_data = {
        "problem_motivated_by": "How fast are you going RIGHT NOW?",
        "intuition": "Like a speedometer - shows speed at THIS moment",
        "default_visual": "secant_to_tangent",
        "formula_latex": r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
        "formula_explanation": "Limit of average rate as interval approaches zero",
        "prerequisites": ["function", "average_rate"]
    }

    print("\n--- Designing Derivative Lesson ---\n")
    steps = designer.design("derivative", concept_data)

    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step.title}")
        print(f"  Phase: {step.phase.value}")
        print(f"  Animation: {step.animation_technique.value}")
        print(f"  Visual: {step.visual_description}")
        print(f"  Discovery: {step.discovery_prompt}")
        if step.formal_notation:
            print(f"  Formula: {step.formal_notation}")
        print()

    print("\n--- Intuition Builder ---\n")
    for concept in ["derivative", "limit", "matrix"]:
        metaphor = IntuitionBuilder.get_metaphor(concept)
        if metaphor:
            print(f"{concept}: {metaphor.metaphor}")

    print("\n--- Misconception Handler ---\n")
    for misconception in MisconceptionHandler.get_misconceptions("derivative"):
        print(f"Misconception: {misconception['misconception']}")
        print(f"Correction: {misconception['correction']}\n")


if __name__ == "__main__":
    demo()