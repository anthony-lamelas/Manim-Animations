from manim import *
import numpy as np

class ThreeDDots(ThreeDScene):
    def construct(self):
        # Set up the 3D axes (we'll hide the z-axis initially)
        axes = ThreeDAxes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            z_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": False}
        )
        
        # Hide the z-axis initially
        axes.z_axis.set_opacity(0)

        # Add axis labels for the 2D view
        x_label = axes.get_x_axis_label(Tex("Price"), edge=RIGHT, direction=UP)
        y_label = axes.get_y_axis_label(Tex("Quality"), edge=UP, direction=RIGHT)
        self.add(axes, x_label, y_label)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # Define the target point
        target_point = np.array([2, 2, 2])

        # Generate 2 initial dots
        initial_dots = VGroup()
        for _ in range(2):
            random_point = np.random.uniform(0, 5, size=2)
            dot = Dot(point=axes.c2p(random_point[0], random_point[1], 0))
            initial_dots.add(dot)
        
        self.add(initial_dots)

        # Animate the dots moving
        self.play(
            AnimationGroup(
                *[dot.animate.move_to(axes.c2p(*target_point)) for dot in initial_dots],
                lag_ratio=0.1
            ),
            run_time=3
        )

        # Transition to 3D view and add more dots
        self.play(axes.z_axis.animate.set_opacity(1), run_time=1)
        self.move_camera(phi=70 * DEGREES, theta=140 * DEGREES, gamma=30 * DEGREES, run_time=3)

        # Generate and add the remaining random dots
        num_dots = 8
        dots = VGroup()
        for _ in range(num_dots):
            random_point = np.random.uniform(0, 5, size=3)
            dot = Dot3D(point=axes.c2p(*random_point))
            dots.add(dot)
        
        self.add(dots)

        # Animate the new dots converging to the target point
        self.play(
            AnimationGroup(
                *[dot.animate.move_to(axes.c2p(*target_point)) for dot in dots],
                lag_ratio=0.1
            ),
            run_time=3
        )

        # Keep the final frame for a moment
        self.wait(1)

# To run the scene, use the following command in your terminal:
# manim -pql <name_of_this_file>.py ThreeDDots
