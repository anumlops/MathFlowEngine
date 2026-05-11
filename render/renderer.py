"""
MathFlowEngine - Frame Renderer
============================
Renders visual states to actual images.
Handles the "pixel to screen" part of the engine.
"""

from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import math
import os
from typing import Dict, List, Any, Optional

from visual.transform import VisualElement, VisualState, Animation


@dataclass
class RendererConfig:
    """
    Configuration for rendering.
    
    Attributes:
        width: Canvas width in pixels
        height: Canvas height in pixels
        background_color: Background color (hex)
        fps: Frames per second for animations
        scale: Pixels per unit for coordinates
    """
    width: int = 800
    height: int = 600
    background_color: str = "#0d1117"
    fps: int = 60
    scale: int = 80


class FrameRenderer:
    """
    Renders frames from visual state data.
    
    This is the final layer - converts to pixels.
    
    Usage:
        renderer = FrameRenderer()
        img = renderer.render_frame(state, elements)
        img.save("frame.png")
    """
    
    def __init__(self, config: Optional[RendererConfig] = None):
        self.config = config or RendererConfig()
    
    def create_canvas(self) -> Image.Image:
        """Create a new canvas."""
        return Image.new(
            'RGB',
            (self.config.width, self.config.height),
            self.config.background_color
        )
    
    def draw_circle(
        self,
        draw: ImageDraw.Draw,
        x: float,
        y: float,
        radius: float,
        fill: str = None,
        stroke: str = None,
        stroke_width: int = 2
    ):
        """
        Draw a circle at given position.
        
        Args:
            draw: PIL ImageDraw object
            x: X coordinate (in units, not pixels)
            y: Y coordinate (in units, not pixels)
            radius: Radius in units
            fill: Fill color (hex)
            stroke: Stroke color (hex)
            stroke_width: Line thickness
        """
        # Scale coordinates
        center_x = self.config.width // 2 + x * self.config.scale
        center_y = self.config.height // 2 + y * self.config.scale
        scaled_radius = radius * self.config.scale
        
        bbox = [
            center_x - scaled_radius,
            center_y - scaled_radius,
            center_x + scaled_radius,
            center_y + scaled_radius
        ]
        
        if fill:
            draw.ellipse(bbox, fill=fill)
        if stroke:
            draw.ellipse(bbox, outline=stroke, width=stroke_width)
    
    def draw_line(
        self,
        draw: ImageDraw.Draw,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = "#FFFFFF",
        width: int = 2
    ):
        """Draw a line between two points."""
        start_x = self.config.width // 2 + x1 * self.config.scale
        start_y = self.config.height // 2 + y1 * self.config.scale
        end_x = self.config.width // 2 + x2 * self.config.scale
        end_y = self.config.height // 2 + y2 * self.config.scale
        
        draw.line(
            [(start_x, start_y), (end_x, end_y)],
            fill=color,
            width=width
        )
    
    def draw_text(
        self,
        draw: ImageDraw.Draw,
        text: str,
        x: float,
        y: float,
        color: str = "#FFFFFF",
        font_size: int = 24
    ):
        """Draw text at position."""
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        pos_x = int(x * self.config.scale if x < 10 else x)
        pos_y = int(y * self.config.scale if y < 10 else y)
        
        draw.text((pos_x, pos_y), text, fill=color, font=font)
    
    def draw_bar(
        self,
        draw: ImageDraw.Draw,
        x: float,
        y: float,
        width: float,
        height: float,
        fill: str,
        max_width: float = None
    ):
        """Draw a progress bar."""
        if max_width:
            ratio = width / max_width
            width = ratio * max_width
        
        pos_x = int(x * self.config.scale if x < 10 else x)
        pos_y = int(y * self.config.scale if y < 10 else y)
        bar_w = int(width * self.config.scale if width < 10 else width)
        bar_h = int(height * self.config.scale if height < 10 else height)
        
        draw.rectangle(
            [pos_x, pos_y, pos_x + bar_w, pos_y + bar_h],
            fill=fill
        )
    
    def render_frame(
        self,
        state: VisualState,
        elements: List[VisualElement],
        title: str = "",
        subtitle: str = ""
    ) -> Image.Image:
        """
        Render a complete frame.
        
        Args:
            state: Visual state with variables
            elements: List of visual elements
            title: Frame title
            subtitle: Frame subtitle
            
        Returns:
            PIL Image object
        """
        img = self.create_canvas()
        draw = ImageDraw.Draw(img)
        
        # Draw elements
        for element in elements:
            if element.element_type == "circle":
                self.draw_circle(
                    draw,
                    element.x, element.y,
                    element.width / 2,  # radius
                    element.fill_color,
                    element.stroke_color,
                    int(element.stroke_width)
                )
            
            elif element.element_type == "line":
                self.draw_line(
                    draw,
                    element.start_x, element.start_y,
                    element.end_x, element.end_y,
                    element.stroke_color,
                    int(element.stroke_width)
                )
        
        # Draw title
        if title:
            self.draw_text(draw, title, 30, 30)
        
        if subtitle:
            self.draw_text(draw, subtitle, 30, 70, "#AAAAAA")
        
        # Draw variable values
        y_offset = 120
        for var_name, value in state.variables.items():
            text = f"{var_name} = {value:.4f}"
            self.draw_text(draw, text, 30, y_offset, "#87CEEB")
            y_offset += 30
        
        return img


def render_animation(
    animation: Animation,
    output_dir: str,
    config: RendererConfig = None
) -> List[str]:
    """
    Render an animation to frames.
    
    Args:
        animation: Animation to render
        output_dir: Output directory
        config: Renderer configuration
        
    Returns:
        List of saved filenames
    """
    if config is None:
        config = RendererConfig()
    
    renderer = FrameRenderer(config)
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    frames = animation.generate_frames()
    filename_list = []
    
    for i, state in enumerate(frames):
        # Get current radius from state
        radius = state.get("radius", 1)
        
        # Create title and subtitle
        title = "Circle Area: Why r^2?"
        subtitle = f"r = {radius:.2f}, A = {state.get('area', 0):.2f}"
        
        # Create circle element (updated for each frame)
        elements = [
            VisualElement(
                element_type="circle",
                x=0, y=0,
                width=radius * 2,
                height=radius * 2,
                fill_color="#4169E1",
                stroke_color="#FFFFFF",
                stroke_width=2
            )
        ]
        
        # Render frame
        img = renderer.render_frame(state, elements, title, subtitle)
        
        # Save
        filename = os.path.join(output_dir, f"frame_{i:04d}.png")
        img.save(filename)
        filename_list.append(filename)
        
        if i % 10 == 0:
            print(f"  Frame {i}: r={radius:.2f}, A={state.get('area', 0):.2f}")
    
    return filename_list


def create_gif(
    frame_files: List[str],
    output_path: str,
    duration: int = 50
):
    """
    Create an animated GIF from frame files.
    
    Args:
        frame_files: List of frame filenames
        output_path: Output GIF path
        duration: Frame duration in milliseconds
    """
    frames = []
    
    for filename in sorted(frame_files):
        img = Image.open(filename)
        frames.append(img)
    
    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )
        print(f"GIF saved: {output_path}")


def render_interactive_html(
    animation: Animation,
    output_path: str
):
    """
    Render as interactive HTML for browser.
    
    Args:
        animation: Animation to embed
        output_path: Output HTML path
    """
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>MathFlow - Interactive</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            background: #0d1117;
            color: #e6edf3;
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
        }}
        .widget {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}
        h1 {{ color: #58a6ff; }}
    </style>
</head>
<body>
    <h1>Circle Area - Interactive</h1>
    <p>Drag the slider to change radius and observe area!</p>
    
    <div class="widget">
        <label>Radius: <span id="r_value">1.50</span> cm</label>
        <input type="range" id="slider" min="0.5" max="5" step="0.1" value="1.5">
    </div>
    
    <div class="widget">
        <div>Area = pi * r^2</div>
        <div>Area: <span id="a_value">7.07</span> cm2</div>
    </div>
    
    <script>
        const slider = document.getElementById('slider');
        const r_val = document.getElementById('r_value');
        const a_val = document.getElementById('a_value');
        
        slider.addEventListener('input', function() {{
            const r = parseFloat(this.value);
            const a = Math.PI * r * r;
            r_val.textContent = r.toFixed(2);
            a_val.textContent = a.toFixed(2);
        }});
    </script>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML saved: {output_path}")


# Demo
def demo():
    """Demo the renderer."""
    
    print("=" * 60)
    print("Frame Renderer - Demo")
    print("=" * 60)
    
    # Create animation
    from visual.transform import VisualTransformEngine
    
    engine = VisualTransformEngine()
    animation = engine.create_circle_expansion(
        start_radius=1.5,
        end_radius=3.0,
        duration=2.0
    )
    
    print(f"Rendering: {animation.name}")
    print(f"Frames: {int(animation.duration * animation.fps)}")
    
    # Render
    output_dir = r"output\frames"
    frames = render_animation(animation, output_dir)
    
    print(f"\nRendered {len(frames)} frames")
    
    # Create GIF
    gif_path = os.path.join(output_dir, "animation.gif")
    create_gif(frames, gif_path)


if __name__ == "__main__":
    demo()