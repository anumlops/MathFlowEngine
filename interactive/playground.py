"""
MathFlowEngine - Interactive Playground
==================================
Allows students to manipulate variables and discover relationships.
This is where "discovery learning" happens.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Callable, Optional
import math
import os


@dataclass
class InteractiveWidget:
    """
    A widget students can interact with.
    
    Attributes:
        id: Unique identifier
        name: Display name
        widget_type: Type ("slider", "button", "toggle")
        
        min_value, max_value, current_value: For sliders
        affects: What this changes
    """
    id: str
    name: str
    widget_type: str = "slider"
    
    min_value: float = 0
    max_value: float = 10
    current_value: float = 1
    
    affects: List[str] = field(default_factory=list)


@dataclass
class Observation:
    """Something to observe (calculated value)."""
    name: str
    formula: str
    calculate: Callable[[Dict], float]
    current_value: float = 0


class InteractivePlayground:
    """
    Interactive playground where students discover math.
    
    Phase 2 of MathFlowEngine - Live experimentation.
    
    Usage:
        playground = CirclePlayground()
        playground.set_value("radius", 3.0)
        results = playground.evaluate()
    """
    
    def __init__(self):
        self.widgets: Dict[str, InteractiveWidget] = {}
        self.observations: Dict[str, Observation] = {}
        self.history: List[Dict] = []
    
    def add_widget(self, widget: InteractiveWidget):
        """Add a widget."""
        self.widgets[widget.id] = widget
    
    def add_observation(self, obs: Observation):
        """Add something to observe."""
        self.observations[obs.name] = obs
    
    def set_value(self, widget_id: str, value: float):
        """Set widget value."""
        if widget_id in self.widgets:
            self.widgets[widget_id].current_value = value
    
    def get_values(self) -> Dict[str, float]:
        """Get all widget values."""
        return {w: self.widgets[w].current_value for w in self.widgets}
    
    def evaluate(self) -> Dict[str, float]:
        """Calculate all observations."""
        widget_values = {w: self.widgets[w].current_value for w in self.widgets}
        
        results = {}
        for obs in self.observations.values():
            obs.current_value = obs.calculate(widget_values)
            results[obs.name] = obs.current_value
        
        return results
    
    def create_html(self, title: str, filename: str):
        """Create interactive HTML page."""
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #0d1117;
            color: #e6edf3;
            padding: 20px;
            max-width: 700px;
            margin: 0 auto;
        }}
        h1 {{ color: #58a6ff; }}
        .widget {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}
        .slider {{
            width: 100%;
            height: 20px;
            accent-color: #58a6ff;
        }}
        .value {{
            font-size: 24px;
            color: #7ee787;
            font-weight: bold;
        }}
        .formula {{
            font-family: monospace;
            color: #8b949e;
            background: #21262d;
            padding: 10px;
            border-radius: 4px;
        }}
        .discovery {{
            background: #1f3a2f;
            border: 1px solid #238636;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Change the sliders and observe what happens!</p>
    
    <div class="widget">
        <label>Radius: <span id="r_value" class="value">1.50</span> cm</label>
        <input type="range" id="r_slider" class="slider" 
               min="0.5" max="5" step="0.1" value="1.5">
    </div>
    
    <div class="widget">
        <div class="formula">Area = pi * r^2</div>
        <div>Area: <span id="a_value" class="value">7.07</span> cm2</div>
    </div>
    
    <div id="discoveries"></div>
    
    <script>
        const slider = document.getElementById('r_slider');
        
        function checkDiscovery(r) {{
            const base = 1.5;
            const ratio = r / base;
            
            const div = document.getElementById('discoveries');
            
            if (Math.abs(ratio - 2) < 0.1) {{
                div.innerHTML = '<div class="discovery"><strong>DISCOVERY!</strong><br>When radius DOUBLES, area QUADRUPLES! This is why we say "squared"!</div>';
            }} else if (Math.abs(ratio - 3) < 0.1) {{
                div.innerHTML = '<div class="discovery"><strong>DISCOVERY!</strong><br>When radius TRIPLES, area becomes 9x!</div>';
            }} else {{
                div.innerHTML = '';
            }}
        }}
        
        slider.addEventListener('input', function() {{
            const r = parseFloat(this.value);
            const a = Math.PI * r * r;
            
            document.getElementById('r_value').textContent = r.toFixed(2);
            document.getElementById('a_value').textContent = a.toFixed(2);
            
            checkDiscovery(r);
        }});
    </script>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Interactive HTML: {filename}")


class CirclePlayground(InteractivePlayground):
    """Interactive playground for circle area."""
    
    def __init__(self):
        super().__init__()
        self._setup()
    
    def _setup(self):
        """Set up the playground."""
        
        self.add_widget(InteractiveWidget(
            id="radius",
            name="Radius",
            widget_type="slider",
            min_value=0.5,
            max_value=5.0,
            current_value=1.5,
            affects=["area", "circumference"]
        ))
        
        self.add_observation(Observation(
            name="Area",
            formula="A = pi * r^2",
            calculation=lambda v: math.pi * v.get("radius", 1)**2
        ))
        
        self.add_observation(Observation(
            name="Circumference",
            formula="C = 2 * pi * r",
            calculation=lambda v: 2 * math.pi * v.get("radius", 1)
        ))


class DerivativePlayground(InteractivePlayground):
    """Interactive playground for derivatives."""
    
    def __init__(self):
        super().__init__()
        self._setup()
    
    def _setup(self):
        """Set up derivative playground."""
        
        # Input value
        self.add_widget(InteractiveWidget(
            id="x",
            name="Input (x)",
            widget_type="slider",
            min_value=-5,
            max_value=5,
            current_value=2,
            affects=["derivative"]
        ))
        
        # Function choice
        self.add_widget(InteractiveWidget(
            id="function",
            name="Function",
            widget_type="slider",
            min_value=1,
            max_value=3,
            current_value=1,
            affects=["derivative"]
        ))
        
        # Observations - will be calculated dynamically


class DiscoveryTracker:
    """
    Tracks discoveries students make.
    
    Usage:
        tracker = DiscoveryTracker()
        finding = tracker.check({"r": 3}, {"r": 1.5, "Area": 7.07}, {"r": 3, "Area": 28.27})
    """
    
    def __init__(self):
        self.findings: List[str] = []
        self.discoveries_log: List[Dict] = []
    
    def check(
        self,
        before: Dict[str, float],
        after: Dict[str, float]
    ) -> Optional[str]:
        """Check if a discovery was made."""
        
        # Check radius doubling = area quadrupling
        r_before = before.get("radius", 1)
        r_after = after.get("radius", 1)
        
        A_before = before.get("Area", 0)
        A_after = after.get("Area", 0)
        
        if r_before > 0 and r_after > 0:
            r_ratio = r_after / r_before
            A_ratio = A_after / A_before
            
            # Radius doubled -> Area quadrupled
            if abs(r_ratio - 2) < 0.1 and abs(A_ratio - 4) < 0.3:
                finding = ("DISCOVERY: When radius DOUBLES, area QUADRUPLES! "
                        "This is why we say 'r squared' - it grows by square!")
                self.record(finding)
                return finding
            
            # Radius tripled -> Area 9x
            if abs(r_ratio - 3) < 0.1 and abs(A_ratio - 9) < 0.5:
                finding = "DISCOVERY: When radius TRIPLES, area becomes 9x!"
                self.record(finding)
                return finding
        
        return None
    
    def record(self, finding: str):
        """Record a new finding."""
        if finding not in self.findings:
            self.findings.append(finding)
            print(f"\n*** NEW DISCOVERY ***")
            print(finding)
    
    def get_findings(self) -> List[str]:
        """Get all discoveries."""
        return self.findings


def demo():
    """Demo the interactive system."""
    
    print("=" * 60)
    print("Interactive Playground - Demo")
    print("=" * 60)
    
    # Circle playground
    playground = CirclePlayground()
    
    print("\nWIDGETS:")
    for w in playground.widgets.values():
        print(f"  {w.name}: {w.min_value} to {w.max_value}")
    
    print("\nOBSERVATIONS:")
    for o in playground.observations.values():
        print(f"  {o.name}: {o.formula}")
    
    print("\nEXPLORING VALUES:")
    print("-" * 40)
    
    for r in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
        playground.set_value("radius", r)
        results = playground.evaluate()
        print(f"r = {r:.1f} -> Area = {results['Area']:.2f}")
    
    # Discovery tracking
    print("\nDISCOVERY TRACKING:")
    print("=" * 40)
    
    tracker = DiscoveryTracker()
    
    tracker.check(
        {"radius": 1.5, "Area": 7.07},
        {"radius": 3.0, "Area": 28.27}
    )
    
    print("\nFindings:", tracker.get_findings())
    
    # Create HTML
    print("\nCreating interactive HTML...")
    playground.create_html(
        "Circle Area - Interactive",
        "interactive_circle.html"
    )


if __name__ == "__main__":
    demo()