"""
MathFlowEngine - Visual Transform Engine
=====================================
Transforms mathematical concepts into visual animations.
Handles the "Show me WHY" part of the system.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Dict, Any
import math


@dataclass
class VisualState:
    """
    Represents a visual state of a mathematical concept.
    
    Attributes:
        concept_id: Which concept this represents
        variables: Dictionary of variable values {name: value}
    """
    concept_id: str
    variables: Dict[str, float]
    
    def get(self, key: str, default: float = 0.0) -> float:
        """Get a variable value."""
        return self.variables.get(key, default)


@dataclass
class VisualElement:
    """
    A single visual element that can be rendered.
    
    Attributes:
        element_type: Type ("circle", "line", "arrow", "text", "graph")
        
        Position
        x, y, z: Coordinates
        
        Size
        width, height, scale: Dimensions
        
        Style
        fill_color: Fill color (hex)
        stroke_color: Outline color (hex)
        stroke_width: Line thickness
        opacity: Transparency 0-1
        
        Text content (for text elements)
        text: String content
        font_size: Font size
        
        Line/arrow endpoints
        start_x, start_y, end_x, end_y: Coordinates
    """
    element_type: str
    
    # Position
    x: float = 0
    y: float = 0
    z: float = 0
    
    # Size
    width: float = 1
    height: float = 1
    scale: float = 1
    
    # Style
    fill_color: str = "#4169E1"
    stroke_color: str = "#FFFFFF"
    stroke_width: float = 2
    opacity: float = 1.0
    
    # Text
    text: str = ""
    font_size: float = 24
    
    # Lines
    start_x: float = 0
    start_y: float = 0
    end_x: float = 1
    end_y: float = 1
    
    def copy(self) -> 'VisualElement':
        """Create a copy of this element."""
        return VisualElement(
            element_type=self.element_type,
            x=self.x, y=self.y, z=self.z,
            width=self.width, height=self.height, scale=self.scale,
            fill_color=self.fill_color, stroke_color=self.stroke_color,
            stroke_width=self.stroke_width, opacity=self.opacity,
            text=self.text, font_size=self.font_size,
            start_x=self.start_x, start_y=self.start_y,
            end_x=self.end_x, end_y=self.end_y
        )


class EasingFunction:
    """
    Mathematical easing functions for smooth animations.
    
    These create natural-looking motion instead of linear movement.
    """
    
    @staticmethod
    def linear(t: float) -> float:
        """Constant speed."""
        return t
    
    @staticmethod
    def smooth(t: float) -> float:
        """Smooth ease in-out (manim's default).
        
        Formula: 3t² - 2t³
        """
        return 3 * t * t - 2 * t * t * t
    
    @staticmethod
    def ease_in(t: float) -> float:
        """Ease in - starts slow, speeds up."""
        return t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        """Ease out - starts fast, slows down."""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """Ease in-out."""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def there_and_back(t: float) -> float:
        """Go to target and back."""
        if t < 0.5:
            return 2 * t
        else:
            return 2 - 2 * t
    
    @staticmethod
    def exponential(t: float) -> float:
        """Exponential easing."""
        if t == 0:
            return 0
        return pow(2, 10 * (t - 1))


@dataclass
class Animation:
    """
    An animation that transforms between visual states.
    
    Attributes:
        name: Animation name
        from_state: Starting state
        to_state: Ending state
        duration: Duration in seconds
        fps: Frames per second
        easing: Easing function to use
        elements: List of visual elements
        animated_variables: Variables to animate
    """
    name: str
    from_state: VisualState
    to_state: VisualState
    
    duration: float = 2.0
    fps: int = 60
    
    easing: Callable[[float], float] = field(default_factory=lambda: EasingFunction.smooth)
    
    elements: List[VisualElement] = field(default_factory=list)
    animated_variables: List[str] = field(default_factory=list)
    
    def generate_frames(self) -> List[VisualState]:
        """
        Generate all frames for this animation.
        
        Returns:
            List of VisualState for each frame
        """
        num_frames = int(self.duration * self.fps)
        frames = []
        
        for i in range(num_frames + 1):
            t = i / num_frames
            eased_t = self.easing(t)
            
            # Interpolate variables
            interpolated_vars = {}
            for var_name in self.animated_variables:
                start_val = self.from_state.get(var_name)
                end_val = self.to_state.get(var_name)
                interpolated_vars[var_name] = start_val + (end_val - start_val) * eased_t
            
            state = VisualState(
                concept_id=self.to_state.concept_id,
                variables=interpolated_vars
            )
            frames.append(state)
        
        return frames
    
    def get_value_at_time(self, var_name: str, time: float) -> float:
        """
        Get the value of a variable at a specific time.
        
        Args:
            var_name: Variable name
            time: Time in seconds
            
        Returns:
            Interpolated value
        """
        start_val = self.from_state.get(var_name)
        end_val = self.to_state.get(var_name)
        eased_t = self.easing(time / self.duration)
        return start_val + (end_val - start_val) * eased_t


class VisualTransformEngine:
    """
    Core engine for transforming between visual states.
    
    This is where "WHY" becomes visual.
    
    Usage:
        engine = VisualTransformEngine()
        anim = engine.create_circle_expansion(1.5, 3.0)
        frames = anim.generate_frames()
    """
    
    def __init__(self):
        self.elements: Dict[str, VisualElement] = {}
        self.animations: List[Animation] = []
    
    def add_element(self, name: str, element: VisualElement):
        """Add a named element."""
        self.elements[name] = element
    
    def create_circle_expansion(
        self,
        start_radius: float,
        end_radius: float,
        center_x: float = 0,
        center_y: float = 0,
        duration: float = 3.0
    ) -> Animation:
        """
        Create a circle expansion animation.
        
        This demonstrates WHY area increases quadratically:
        - double radius = 4x area
        
        Args:
            start_radius: Starting radius
            end_radius: Ending radius
            center_x: X center position
            center_y: Y center position
            duration: Animation duration in seconds
            
        Returns:
            Animation object
        """
        
        from_state = VisualState(
            concept_id="circle_area",
            variables={
                "radius": start_radius, 
                "area": math.pi * start_radius**2
            }
        )
        
        to_state = VisualState(
            concept_id="circle_area",
            variables={
                "radius": end_radius, 
                "area": math.pi * end_radius**2
            }
        )
        
        # Create circle element
        circle = VisualElement(
            element_type="circle",
            x=center_x,
            y=center_y,
            width=start_radius * 2,
            height=start_radius * 2,
            stroke_color="#FFFFFF",
            stroke_width=2,
            fill_color="#4169E1",
            opacity=0.4
        )
        
        animation = Animation(
            name="circle_expansion",
            from_state=from_state,
            to_state=to_state,
            duration=duration,
            easing=EasingFunction.smooth,
            elements=[circle],
            animated_variables=["radius", "area"]
        )
        
        self.animations.append(animation)
        return animation
    
    def create_secant_to_tangent(
        self,
        function: Callable[[float], float],
        point_x: float,
        h_values: List[float],
        duration: float = 3.0
    ) -> Animation:
        """
        Create animation of secant approaching tangent.
        
        This shows limit concept visually:
        - secant line as h > 0
        - approaches tangent as h -> 0
        """
        
        def calc_slope(h: float) -> float:
            if h == 0:
                return 0
            return (function(point_x + h) - function(point_x)) / h

        from_state = VisualState(
            concept_id="derivative",
            variables={
                "h": h_values[0],
                "slope": calc_slope(h_values[0])
            }
        )

        to_state = VisualState(
            concept_id="derivative",
            variables={
                "h": h_values[-1],
                "slope": calc_slope(h_values[-1])
            }
        )

        animation = Animation(
            name="secant_to_tangent",
            from_state=from_state,
            to_state=to_state,
            duration=duration,
            animated_variables=["h", "slope"]
        )
        
        self.animations.append(animation)
        return animation
    
    def create_function_plot(
        self,
        func: Callable[[float], float],
        x_range: tuple,
        duration: float = 1.0
    ) -> Animation:
        """Create animation of a function being drawn."""
        
        from_state = VisualState(
            concept_id="function",
            variables={"progress": x_range[0]}
        )
        
        to_state = VisualState(
            concept_id="function",
            variables={"progress": x_range[1]}
        )
        
        animation = Animation(
            name="draw_function",
            from_state=from_state,
            to_state=to_state,
            duration=duration,
            animated_variables=["progress"]
        )
        
        self.animations.append(animation)
        return animation


class PedagogicalSequence:
    """
    Creates sequences of explanations that build understanding.
    
    This is key to the "WHY" approach:
    - Start with mystery, not formula
    
    Usage:
        pedagory = PedagogicalSequence(engine)
        steps = pedagory.create_circle_area_sequence()
    """
    
    def __init__(self, transform_engine: VisualTransformEngine):
        self.transform_engine = transform_engine
    
    def create_circle_area_sequence(self) -> List[Dict[str, Any]]:
        """
        Create pedagogical sequence for circle area.
        
        Step 1: Introduce radius
        Step 2: Show what pi means
        Step 3: Derive A = pi*r^2
        Step 4: Show what happens when r changes
        """
        sequence = []
        
        # Step 1: Show radius
        sequence.append({
            "step": 1,
            "title": "What is Radius?",
            "visual": "line_from_center",
            "why": "The radius is the single number that describes the circle.",
            "formula": "r = d/2",
            "action": "draw_line_from_center"
        })
        
        # Step 2: Show pi
        sequence.append({
            "step": 2,
            "title": "The Magic Number Pi",
            "visual": "circle_with_measurements",
            "why": "Every circle has the same ratio: circumference/diameter.",
            "formula": "pi approx 3.14159",
            "action": "measure_circumference"
        })
        
        # Step 3: Derive formula
        sequence.append({
            "step": 3,
            "title": "Why A = pi*r^2?",
            "visual": "circle_with_slices",
            "why": "Cut circle into slices, rearrange to rectangle.",
            "formula": "A = pi*r*r",
            "action": "cut_and_rearrange"
        })
        
        # Step 4: Show expansion
        sequence.append({
            "step": 4,
            "title": "What Happens When Radius Doubles?",
            "visual": "expanding_circle",
            "why": "Double radius = 4x area! This is WHY it's squared.",
            "formula": "A2 = 4 * A1",
            "action": "expand_circle",
            "animation": self.transform_engine.create_circle_expansion(
                start_radius=1.5,
                end_radius=3.0,
                duration=2.0
            )
        })
        
        return sequence


# Demo
def demo():
    """Demo the visual transform engine."""
    
    print("=" * 60)
    print("Visual Transform Engine - Demo")
    print("=" * 60)
    
    engine = VisualTransformEngine()
    
    # Create animation
    anim = engine.create_circle_expansion(
        start_radius=1.5,
        end_radius=3.0,
        duration=2.0
    )
    
    print(f"\nAnimation: {anim.name}")
    print(f"Duration: {anim.duration}s at {anim.fps}fps")
    print(f"Frames: {int(anim.duration * anim.fps)}")
    
    print("\nVariable values over time:")
    print("-" * 50)
    print(f"{'Time':<8} {'Radius':<12} {'Area':<12}")
    print("-" * 50)
    
    for t in [0.0, 0.5, 1.0, 1.5, 2.0]:
        r = anim.get_value_at_time("radius", t)
        a = anim.get_value_at_time("area", t)
        print(f"{t:<8.1f} {r:<12.2f} {a:<12.2f}")
    
    print("\nPedagogical sequence:")
    pedagory = PedagogicalSequence(engine)
    for step in pedagory.create_circle_area_sequence():
        print(f"  Step {step['step']}: {step['title']}")


if __name__ == "__main__":
    demo()