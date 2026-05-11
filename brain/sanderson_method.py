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
            metaphor="Adding up infinitely small pieces",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Rectangles filling area under curve",
            limitations="Can be negative too"
        ),
        "vector": VisualMetaphor(
            concept_id="vector",
            metaphor="An arrow with direction and length",
            visual_representation=VisualRepresentation.GEOMETRIC,
            animation_behavior="Arrow pointing somewhere",
            limitations="High dimensions are hard to visualize"
        ),
        "matrix": VisualMetaphor(
            concept_id="matrix",
            metaphor="A machine that transforms space",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Space stretching and rotating",
            limitations="Not all transformations are linear"
        ),
        "circle_area": VisualMetaphor(
            concept_id="circle_area",
            metaphor="A pizza spinning and stretching",
            visual_representation=VisualRepresentation.PHYSICAL,
            animation_behavior="Circle expanding outward from center",
            limitations="Large circles still behave the same"
        ),
        "eigenvalue": VisualMetaphor(
            concept_id="eigenvalue",
            metaphor="Axes that don't rotate under transformation",
            visual_representation=VisualRepresentation.GRAPH,
            animation_behavior="Blue line stays blue, red stays red",
            limitations="Complex eigenvalues have no real eigenvectors"
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
            }
        ],
        "negative_exponents": [
            {
                "misconception": "Makes things smaller",
                "correction": "2^-3 = 1/8, can be larger than 2^2",
                "animation": "Show scaling down visually"
            }
        ],
        "sine": [
            {
                "misconception": "sin(x) = y",
                "correction": "sin is a function, y = sin(x) is the graph",
                "animation": "Show full circle projection context"
            }
        ],
        "matrices": [
            {
                "misconception": "Matrix is a grid of numbers",
                "correction": "Matrix is a transformation machine",
                "animation": "Show grid becoming transformation"
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
        "secant_to_tangent": {
            "from": "Two points on curve",
            "to": "One point with tangent line",
            "how": "Animate one point approaching the other",
            "insight": "Derivative = slope of tangent"
        },
        "rectangle_to_approximation": {
            "from": "Rectangles approximating area",
            "to": "Smooth curve",
            "how": "Increase number of rectangles",
            "insight": "Integral = limit of Riemann sums"
        },
        "vector_to_basis": {
            "from": "Single vector",
            "to": "Basis vectors with coordinates",
            "how": "Show decomposition into basis",
            "insight": "Vectors = linear combination of basis"
        },
        "circle_to_pi": {
            "from": "Circle with radius",
            "to": "Pi visualized as ratio",
            "how": "Show circumference / diameter",
            "insight": "Pi is universal constant"
        },
        "grid_to_transformation": {
            "from": "Square grid",
            "to": "Transformed parallelogram grid",
            "how": "Apply matrix to each point",
            "insight": "Matrix = transformation"
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