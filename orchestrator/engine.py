from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import math

from core.concepts import Concept, ConceptGraph, ConceptBuilder, DifficultyLevel, MathVariable
from visual.transform import VisualTransformEngine, VisualState, Animation, EasingFunction, PedagogicalSequence
from render.renderer import FrameRenderer, RendererConfig, render_animation, create_gif
from brain import (
    SandersonLessonDesigner, IntuitionBuilder, MisconceptionHandler,
    TeachingSequenceBuilder, TransformationEngine,
    TeachingPhase, AnimationTechnique, SandersonStep, VisualMetaphor
)


@dataclass
class TeachingStep:
    """A single teaching step."""
    step_number: int
    title: str
    explanation: str
    why_this_matters: str
    visual_element: str
    formula: Optional[str] = None
    questions: List[str] = field(default_factory=list)
    animation_data: Optional[Dict] = None


@dataclass
class Lesson:
    """A complete lesson."""
    concept_id: str
    title: str
    steps: List[TeachingStep] = field(default_factory=list)
    key_takeaway: str = ""
    formula: str = ""


class MathFlowEngine:
    """
    Main orchestrator for mathematical teaching.
    
    This is the core that:
    - Knows WHAT to teach (ConceptGraph)
    - Knows HOW to visualize it (VisualTransformEngine)
    - Knows WHEN to show what (PedagogicalSequence)
    - Knows HOW to render it (FrameRenderer)
    
    Usage:
        engine = MathFlowEngine()
        lesson = engine.build_lesson("circle_area")
        engine.teach(lesson)
    """
    
    def __init__(self):
        self.concept_graph = ConceptGraph()
        self.visual_engine = VisualTransformEngine()
        self.renderer = FrameRenderer()
        self.output_dir = "output"
        # The Brain - Sanderson's teaching methodology
        self.sanderson_designer = SandersonLessonDesigner()
        self.intuition_builder = IntuitionBuilder()
        self.misconception_handler = MisconceptionHandler()

    def build_sanderson_lesson(self, concept_id: str, concept_data: Dict) -> List[SandersonStep]:
        """
        Build a lesson following Grant Sanderson's methodology.

        This creates lessons with:
        1. Problem-first structure
        2. Animation-driven intuition
        3. Pattern discovery moments
        4. Just-in-time prerequisites
        5. Misconception handling

        Args:
            concept_id: The concept to teach
            concept_data: Dictionary with keys like:
                - problem_motivated_by
                - intuition
                - default_visual
                - formula_latex
                - formula_explanation
                - prerequisites

        Returns:
            List of SandersonSteps for the lesson
        """
        return self.sanderson_designer.design(concept_id, concept_data)
    
    def build_lesson(self, concept_id: str) -> Lesson:
        """Build a lesson for a concept."""
        
        if concept_id == "circle_area":
            return self._build_circle_area_lesson()
        elif concept_id == "derivative":
            return self._build_derivative_lesson()
        else:
            raise ValueError(f"Unknown concept: {concept_id}")
    
    def _build_circle_area_lesson(self) -> Lesson:
        """Build circle area lesson."""
        
        lesson = Lesson(
            concept_id="circle_area",
            title="Why is Area = pi*r^2?",
            key_takeaway=(
                "Area increases with the SQUARE of radius. "
                "Double radius = 4x area!"
            ),
            formula="A = pi*r^2"
        )
        
        lesson.steps.append(TeachingStep(
            step_number=1,
            title="The Mystery",
            explanation="Ancient mathematicians asked: How do we measure a circle's area?",
            why_this_matters="We can measure lines and polygons, but circles are curved.",
            visual_element="circle_mystery",
            questions=["How would you measure this?"]
        ))
        
        lesson.steps.append(TeachingStep(
            step_number=2,
            title="Start with Radius",
            explanation="One number: distance from center to edge.",
            why_this_matters="The radius describes the WHOLE circle!",
            visual_element="radius_line",
            formula="r = d/2",
            questions=["What if we change r?"]
        ))
        
        lesson.steps.append(TeachingStep(
            step_number=3,
            title="The Magic Pi",
            explanation="Every circle has C/d = approximately 3.14159",
            why_this_matters="Universal constant - same for ALL circles!",
            visual_element="circle_constant",
            formula="pi approx 3.14159"
        ))
        
        lesson.steps.append(TeachingStep(
            step_number=4,
            title="The SQUARE Matters!",
            explanation="Double radius = 4x area! This is WHY we say 'squared'.",
            why_this_matters="Doubling creates 4x, not 2x!",
            visual_element="expanding_circle",
            formula="A2 = 4 * A1",
            animation_data={"start": 1.5, "end": 3.0}
        ))
        
        return lesson
    
    def _build_derivative_lesson(self) -> Lesson:
        """Build derivative lesson for calculus chapter."""
        
        lesson = Lesson(
            concept_id="derivative",
            title="What is a Derivative?",
            key_takeaway=(
                "Derivative = instantaneous rate of change. "
                "Like a speedometer - shows speed RIGHT NOW."
            ),
            formula="f'(x) = dy/dx"
        )
        
        lesson.steps.append(TeachingStep(
            step_number=1,
            title="The Speed Problem",
            explanation="How fast are you going RIGHT NOW? Not average, instant!",
            why_this_matters="Average rate isn't enough - we need instant!",
            visual_element="speedometer"
        ))
        
        lesson.steps.append(TeachingStep(
            step_number=2,
            title="Average Rate First",
            explanation="Distance traveled divided by time = average speed.",
            why_this_matters="Start with something we can calculate.",
            visual_element="average_rate"
        ))
        
        lesson.steps.append(TeachingStep(
            step_number=3,
            title="The Magic Limit",
            explanation="As time interval approaches zero...",
            why_this_matters="We get instantaneous rate!",
            visual_element="secant_to_tangent"
        ))
        
        lesson.steps.append(TeachingStep(
            step_number=4,
            title="The Derivative!",
            explanation="The limit of average rate as h approaches 0.",
            why_this_matters="This IS calculus!",
            visual_element="tangent_line",
            formula="f'(x) = lim(h->0) [f(x+h) - f(x)] / h"
        ))
        
        return lesson
    
    def teach(self, lesson: Lesson):
        """Execute a lesson."""
        
        print("=" * 60)
        print(f"TEACHING: {lesson.title}")
        print("=" * 60)
        
        for step in lesson.steps:
            print(f"\nStep {step.step_number}: {step.title}")
            print(f"  EXPLAIN: {step.explanation}")
            print(f"  WHY: {step.why_this_matters}")
            if step.formula:
                print(f"  FORMULA: {step.formula}")
            
            if step.animation_data:
                self._render_step_animation(step)
        
        print("\n" + "=" * 60)
        print(f"KEY: {lesson.key_takeaway}")
        print(f"FORMULA: {lesson.formula}")
    
    def _render_step_animation(self, step: TeachingStep):
        """Render animation for a step."""
        
        data = step.animation_data
        print(f"\n  Rendering animation...")
        
        if "start" in data and "end" in data:
            anim = self.visual_engine.create_circle_expansion(
                start_radius=data["start"],
                end_radius=data["end"],
                duration=2.0
            )
            
            step_dir = f"{self.output_dir}/step_{step.step_number}"
            frames = render_animation(anim, step_dir)
            
            gif_path = f"{step_dir}/animation.gif"
            create_gif(frames, gif_path)
            
            print(f"    Saved to: {step_dir}")


def demo():
    """Demo."""

    print("=" * 60)
    print("MathFlowEngine Demo")
    print("=" * 60)

    engine = MathFlowEngine()

    print("\n--- Circle Area Lesson ---")
    lesson = engine.build_lesson("circle_area")
    engine.teach(lesson)

    print("\n--- Derivative Lesson ---")
    lesson = engine.build_lesson("derivative")
    engine.teach(lesson)

    # New: Demonstrate Sanderson's Brain
    print("\n" + "=" * 60)
    print("SANDERSON'S BRAIN - Mathematical Pedagogy Engine")
    print("=" * 60)

    # Design a lesson using Sanderson's methodology
    concept_data = {
        "problem_motivated_by": "How do we measure how fast something is changing at an EXACT moment?",
        "intuition": "Think of a car's speedometer - it shows speed RIGHT NOW, not average",
        "default_visual": "secant_to_tangent",
        "formula_latex": r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
        "formula_explanation": "The limit of average rate as the interval approaches zero",
        "prerequisites": ["function", "average_rate"]
    }

    print("\n--- Derivative Lesson (Sanderson Style) ---\n")
    steps = engine.build_sanderson_lesson("derivative", concept_data)

    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step.title}")
        print(f"  Phase: {step.phase.value.upper()}")
        print(f"  Animation: {step.animation_technique.value}")
        print(f"  Visual: {step.visual_description}")
        print(f"  Discovery Prompt: \"{step.discovery_prompt}\"")
        if step.formal_notation:
            print(f"  Formula: {step.formal_notation}")
        if step.misconception_correction:
            print(f"  ✗ Misconception: {step.anticipated_misconception}")
            print(f"  ✓ Correction: {step.misconception_correction}")
        print()

    # Show intuition metaphors
    print("\n--- Intuition Metaphors Library ---\n")
    for concept in ["derivative", "limit", "circle_area", "matrix"]:
        result = IntuitionBuilder.build_intuition(concept)
        if result["metaphor"]:
            print(f"{concept.upper()}:")
            print(f"  Metaphor: {result['metaphor'].metaphor}")
            print(f"  Animation: {result['metaphor'].animation_behavior}")
            if result['metaphor'].limitations:
                print(f"  Limitation: {result['metaphor'].limitations}")
            print()

    # Show transformations
    print("\n--- Transformation Library (Sanderson's Core Technique) ---\n")
    for name in ["secant_to_tangent", "grid_to_transformation", "circle_to_pi"]:
        t = TransformationEngine.get_transformation(name)
        if t:
            print(f"{name.upper()}:")
            print(f"  From: {t['from']}")
            print(f"  To: {t['to']}")
            print(f"  Insight: {t['insight']}")
            print()


if __name__ == "__main__":
    demo()