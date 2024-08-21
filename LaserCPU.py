from manim import *
from collections import deque

class CPU(VGroup):
    # Custom class to create the CPU. In retrospect I could have just done this in the scene.
    def __init__(self, **kwargs):
        # Create the inner square of the CPU
        inner_square = Square(side_length=2.1, fill_opacity=1, fill_color=BLACK, **kwargs)
        
        # Create the outer square with rounded corners, removing the inner square
        outer_square = Difference(
            RoundedRectangle(corner_radius=0.4, height=2.75, width=2.75),
            inner_square,
            fill_opacity=1,
            fill_color=BLACK,
            **kwargs
        )
        
        # Create a single top wire
        top_wire = Line(
            outer_square.get_edge_center(UP),
            outer_square.get_edge_center(UP) + 0.5 * UP,
            **kwargs
        )
        
        # Create a group of wires arranged horizontally
        top_wires = VGroup(*[top_wire.copy() for _ in range(5)]).arrange(RIGHT, buff=0.45).move_to(top_wire)
        
        # Create a group of wires arranged in four directions (top, right, bottom, left)
        all_wires = VGroup(*[top_wires.copy().rotate(i * 90 * DEGREES, about_point=ORIGIN) for i in range(4)])
        
        # Create the text "CPU" and scale it
        CPU_text = Text("Pomu").scale(0.9)
        
        # Combine all parts of the CPU
        parts = [all_wires, outer_square, inner_square, CPU_text]
        
        # Set the z-index for each part to ensure proper layering
        for i, mob in enumerate(parts):
            mob.set_z_index(i + 1)
        
        # Initialize the VGroup with all the parts
        super().__init__(*parts, **kwargs)

class Laser(Line):
    # Custom class to create the lasers. This time it actually makes sense because there are several lasers in the scene.
    def __init__(self, direction=RIGHT, length=2, color=RED, **kwargs):
        # Initialize the laser line with gradient opacity
        super().__init__(
            start=ORIGIN,
            end=direction * length,
            stroke_color=color,
            stroke_opacity=[0, 1, 1, 0],
            **kwargs
        )
        # Set the z-index to ensure the laser is below other elements
        self.set_z_index(-1)

class LaserCPU(Scene):
    def construct(self):
        # Create and scale the CPU
        CPU_mob = CPU(stroke_width=3).scale(0.75)
        self.add(CPU_mob)

        # Create input and output text labels and position them
        input_text = Text("Inputs").scale(1).to_edge(LEFT).shift(UP * 2.3)
        output_text = Text("Manufacturer").scale(1).to_edge(RIGHT).shift(UP * 2.3)

        # Display the input and output text labels
        self.play(
            Write(VGroup(input_text, output_text)),
            run_time=1.5
        )

        # Define laser colors for animation.
        laser_colors = [RED_E, YELLOW_E, GREEN_E, BLUE_E, PURPLE_E]
        
        # Animate lasers through the CPU wires from left to right, matching heights with wires
        for i in range(len(laser_colors)):
            wire_y = CPU_mob[0][1][i % len(laser_colors)].get_y()
            laser = Laser(color=laser_colors[i]).shift(LEFT * 10 + UP * wire_y)
            self.play(
                laser.animate(run_time=0.3).shift(RIGHT * 9),  # Set uniform run_time for all lasers
                Succession(
                    CPU_mob[1].animate(run_time=0.2).set(fill_color=laser_colors[0:i+1]),
                )
            )
            self.remove(laser)
        
        # Animate lasers from left to right, but this time from top coil to bottom coil
        for i in range(len(laser_colors)):
            wire_y = CPU_mob[0][1][i % len(laser_colors)].get_y()
            laser = Laser(color=laser_colors[i]).shift(LEFT * 10 + UP * wire_y)
            self.play(
                laser.animate(run_time=0.3).shift(RIGHT * 9),  # Set uniform run_time for all lasers
                Succession(
                    CPU_mob[1].animate(run_time=0.2).set(fill_color=laser_colors[0:i+1]),
                )
            )
            self.remove(laser)
        
        # Animate the CPU changing colors in a loop while it is thinking
        color_deque = deque(laser_colors)
        for i in range(2 * len(laser_colors)):  # Reduced the number of iterations
            color_deque.rotate(-1)
            self.play(
                CPU_mob[1].animate(run_time=0.07).set(fill_color=list(color_deque)),
            )

        # Create the output logo and position it
        output_logo = SVGMobject("result_logo.svg").scale(0.6).move_to(RIGHT * output_text.get_x())
        
        # Create a copy of the outer square to stay behind so that the rainbow one can be transformed into the output logo
        finished_outer_square = CPU_mob[1].copy().set(fill_color=BLACK).set_z_index(1.9)
        
        # Transform the outer square into the output logo
        self.play(
            Transform(CPU_mob[1], output_logo)
        )

        self.wait(2)
