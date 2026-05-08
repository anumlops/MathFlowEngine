"""
MathFlowEngine - Core Concepts Module
======================================
This module handles the conceptual relationships between mathematical ideas.

Key Principle: Every concept answers "Why?" not just "What?"
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class DifficultyLevel(Enum):
    INTRODUCTORY = 1
    BASIC = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


@dataclass
class Concept:
    """
    A mathematical concept with full pedagogical context.
    
    Attributes:
        id: Unique identifier
        name: Display name
        short_description: Brief description
        
        # The WHY - not just what it is, but why it exists
        problem_motivated_by: What problem led to this concept?
        intuition: How should a student think about this?
        
        # Relationships
        prerequisites: List of concepts needed first
        builds_upon: List of concepts this builds upon
        related_concepts: Related concepts
        
        # Visual representation
        default_visual: Type of visual ("circle", "graph", "numberline")
        
        # Variables that affect this concept
        variables: List of manipulable variables
        
        # Difficulty
        difficulty: Level of complexity
        
        # Formula (if applicable)
        formula_latex: LaTeX formula string
        formula_explanation: How to read the formula
    """
    id: str
    name: str
    short_description: str
    
    # The WHY
    problem_motivated_by: str = ""
    intuition: str = ""
    
    # Relationships - stored as strings to avoid circular imports
    prerequisites: List[str] = field(default_factory=list)
    builds_upon: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    
    # Visual
    default_visual: str = ""
    
    # Variables
    variables: List['MathVariable'] = field(default_factory=list)
    
    # Difficulty  
    difficulty: DifficultyLevel = DifficultyLevel.BASIC
    
    # Formula
    formula_latex: Optional[str] = None
    formula_explanation: Optional[str] = None


@dataclass
class MathVariable:
    """
    A variable that can be manipulated in a concept.
    
    Attributes:
        symbol: The variable symbol (r, x, theta)
        name: Human-readable name
        unit: Unit of measurement (cm, m/s) or None
        
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        default_value: Starting value
        
        affects: List of what this changes
    """
    symbol: str
    name: str
    unit: Optional[str] = None
    
    min_value: float = 0
    max_value: float = 100
    default_value: float = 1
    
    affects: List[str] = field(default_factory=list)


@dataclass
class ConceptualRelationship:
    """
    Represents how one concept relates to another.
    
    Attributes:
        from_concept: Starting concept ID
        to_concept: Ending concept ID
        relationship_type: Type ("prerequisite", "generalizes", "specializes", "extends")
        explanation: Why this relationship exists
        transformation: How to transform (formula substitution, limit, etc.)
    """
    from_concept: str
    to_concept: str
    relationship_type: str
    explanation: str
    transformation: Optional[str] = None


class ConceptGraph:
    """
    A graph structure representing relationships between concepts.
    
    This is the core of the "flow" - knowing what builds on what.
    
    Usage:
        graph = ConceptGraph()
        graph.add_concept(circle_area)
        sequence = graph.get_learning_sequence("circle_area")
    """
    
    def __init__(self):
        self.concepts: Dict[str, Concept] = {}
        self.relationships: List[ConceptualRelationship] = []
    
    def add_concept(self, concept: Concept):
        """Add a concept to the graph."""
        self.concepts[concept.id] = concept
    
    def add_relationship(self, rel: ConceptualRelationship):
        """Add a relationship between concepts."""
        self.relationships.append(rel)
    
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Get a concept by ID."""
        return self.concepts.get(concept_id)
    
    def get_prerequisites(self, concept_id: str) -> List[str]:
        """Get prerequisite concept IDs."""
        concept = self.concepts.get(concept_id)
        if not concept:
            return []
        return concept.prerequisites
    
    def get_learning_sequence(self, concept_id: str) -> List[str]:
        """
        Determine proper pedagogical sequence.
        Returns concept IDs in learning order.
        """
        sequence = []
        visited = set()
        
        def visit(concept_id: str):
            if concept_id in visited:
                return
            visited.add(concept_id)
            
            # First learn prerequisites
            for prereq in self.get_prerequisites(concept_id):
                visit(prereq)
            
            # Then add this concept
            if concept_id in self.concepts:
                sequence.append(concept_id)
        
        visit(concept_id)
        return sequence
    
    def get_related(self, concept_id: str) -> List[str]:
        """Get related concept IDs."""
        concept = self.concepts.get(concept_id)
        if not concept:
            return []
        return concept.related_concepts


class ConceptBuilder:
    """
    Builder for creating concepts with pedagogical context.
    
    Usage:
        builder = ConceptBuilder()
        graph = builder.build_circle_area_concept()
    """
    
    def __init__(self, graph: ConceptGraph):
        self.graph = graph
    
    def build_circle_area(self) -> Concept:
        """Create the circle area concept."""
        return Concept(
            id="circle_area",
            name="Circle Area",
            short_description="Area enclosed by a circle",
            
            problem_motivated_by=(
                "Ancient civilizations needed to measure land, crops, and materials. "
                "While rectangles and triangles were easy, circles (wheels, lakes, columns) "
                "had no simple formula. The mystery: 'What is the area of a circle?'"
            ),
            intuition=(
                "Think of a circle as a pizza. Spin it fast and the cheese stretches outward. "
                "The area fills every direction equally from the center."
            ),
            
            default_visual="expanding_circle",
            formula_latex=r"A = \pi r^2",
            formula_explanation=(
                "Area = pi times radius times radius. "
                "The radius tells how far the 'pizza' stretches."
            ),
            difficulty=DifficultyLevel.INTERMEDIATE,
            
            variables=[
                MathVariable(
                    symbol="r",
                    name="radius",
                    unit="cm",
                    min_value=0.1,
                    max_value=10,
                    default_value=1.5,
                    affects=["area", "circumference"]
                ),
            ],
            
            prerequisites=[],
            related_concepts=["radius", "pi", "circumference"]
        )
    
    def build_radius(self) -> Concept:
        """Create the radius concept."""
        return Concept(
            id="radius",
            name="Radius",
            short_description="Distance from center to edge",
            
            problem_motivated_by=(
                "How do we describe 'how big' a circle is? "
                "One number: the distance from center to edge."
            ),
            intuition=(
                "Imagine a pizza slice from center to crust. "
                "That's the radius."
            ),
            
            default_visual="line_from_center",
            formula_latex=r"r = d/2",
            formula_explanation="Radius is half the diameter.",
            difficulty=DifficultyLevel.INTRODUCTORY,
            
            variables=[
                MathVariable(
                    symbol="r",
                    name="radius",
                    unit="cm",
                    min_value=0,
                    max_value=10,
                    default_value=1.5,
                    affects=["area", "circumference", "diameter"]
                ),
            ],
            
            prerequisites=[],
            related_concepts=["diameter", "circle_area"]
        )
    
    def build_pi(self) -> Concept:
        """Create the pi concept."""
        return Concept(
            id="pi",
            name="Pi",
            short_description="The circle constant",
            
            problem_motivated_by=(
                "Every circle, no matter the size, has the same ratio: "
                "circumference divided by diameter = 3.14159... "
                "This constant appears everywhere circles exist."
            ),
            intuition=(
                "If you measure around any circle and divide by across, "
                "you always get approximately 3.14. It's universal!"
            ),
            
            default_visual="circle_constant",
            formula_latex=r"\pi \approx 3.14159",
            formula_explanation=(
                "Pi is approximately 3.14 or 22/7. "
                "It's irrational - never ends!"
            ),
            difficulty=DifficultyLevel.INTERMEDIATE,
            
            variables=[],
            
            prerequisites=["radius"],
            related_concepts=["circumference", "circle_area"]
        )
    
    def build_derivative(self) -> Concept:
        """Create derivative concept (for calculus chapter)."""
        return Concept(
            id="derivative",
            name="Derivative",
            short_description="Instantaneous rate of change",
            
            problem_motivated_by=(
                "How do we measure how fast something is changing "
                "at an EXACT moment? Not the average, but RIGHT NOW?"
            ),
            intuition=(
                "Think of a car's speedometer. It shows how fast "
                "you're going at THIS second, not your average for the trip."
            ),
            
            default_visual="tangent_line",
            formula_latex=r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            formula_explanation=(
                "The derivative is the limit of average rate "
                "as the distance approaches zero."
            ),
            difficulty=DifficultyLevel.ADVANCED,
            
            variables=[
                MathVariable(
                    symbol="x",
                    name="input",
                    unit=None,
                    min_value=-10,
                    max_value=10,
                    default_value=0,
                    affects=["slope", "rate"]
                ),
            ],
            
            prerequisites=["limit", "function"],
            related_concepts=["integral", "chain_rule", "power_rule"]
        )
    
    def build_all_core_concepts(self) -> ConceptGraph:
        """Build foundational concepts for circle area."""
        radius = self.build_radius()
        pi = self.build_pi()
        circle_area = self.build_circle_area()
        
        self.graph.add_concept(radius)
        self.graph.add_concept(pi)
        self.graph.add_concept(circle_area)
        
        # Set relationships
        circle_area.prerequisites = ["radius", "pi"]
        
        return self.graph


# Demo
def demo():
    """Demonstrate the concept system."""
    print("=" * 60)
    print("MathFlowEngine - Core Concepts Demo")
    print("=" * 60)
    
    # Build concepts
    graph = ConceptGraph()
    builder = ConceptBuilder(graph)
    builder.build_all_core_concepts()
    
    # Get circle area
    circle = graph.get_concept("circle_area")
    
    print(f"\nConcept: {circle.name}")
    print(f"Formula: {circle.formula_latex}")
    print(f"\nWHY does this exist?")
    print(f"  {circle.problem_motivated_by}")
    print(f"\nINTUITION:")
    print(f"  {circle.intuition}")
    print(f"\nVariables: {len(circle.variables)}")
    for var in circle.variables:
        print(f"  {var.symbol} ({var.name}): affects {var.affects}")
    
    print(f"\nLearning sequence:")
    sequence = graph.get_learning_sequence("circle_area")
    for i, cid in enumerate(sequence, 1):
        c = graph.get_concept(cid)
        print(f"  {i}. {c.name}")


if __name__ == "__main__":
    demo()