from manim import *

class MyPlotSceneAnimated3D(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            z_range=[0, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"include_numbers": False}
        )

        # Add custom labels to the axes
        x_label = axes.get_x_axis_label(Tex("Price"), edge=RIGHT, direction=UP)
        y_label = axes.get_y_axis_label(Tex("Quality"), edge=UP, direction=RIGHT)
        z_label = axes.get_z_axis_label(Tex("Speed"), edge=OUT, direction=RIGHT)

        # Create a value tracker for the animation
        vt = ValueTracker(0)

        # Define the functions for the lines
        f1 = always_redraw(lambda: axes.plot(lambda x: (1/5) * x ** 2, color=BLUE, x_range=[0, vt.get_value()]))
        f2 = always_redraw(lambda: axes.plot(lambda x: (1/2) * x + 1, color=YELLOW, x_range=[0, vt.get_value()]))

        # Define the dots for the tracing points
        f1_dot = always_redraw(lambda: Dot3D(
            point=axes.c2p(vt.get_value(), (1/5) * vt.get_value() ** 2, 0),
            color=BLUE
        ))
        f2_dot = always_redraw(lambda: Dot3D(
            point=axes.c2p(vt.get_value(), (1/2) * vt.get_value() + 1, 0),
            color=YELLOW
        ))

        # Add the axes and labels to the scene
        self.add(axes, x_label, y_label, z_label)
        self.play(Create(f1), Create(f2))
        self.add(f1_dot, f2_dot)
        self.wait(1)

        # Calculate the intersection point
        intersection_x = (5 + 105**0.5) / 4
        intersection_y = (1/5) * intersection_x ** 2

        # Animate the ValueTracker to the intersection point
        self.play(vt.animate.set_value(intersection_x), run_time=3)

        # Add a red dot at the intersection point
        intersection_dot = Dot3D(point=axes.c2p(intersection_x, intersection_y, 0), color=RED)
        self.add(intersection_dot)

        # Fade out the blue and yellow dots
        self.play(FadeOut(f1_dot), FadeOut(f2_dot))

        # Add another value tracker for the z-axis line
        vt_z = ValueTracker(0)

        # Define the third line from the z-axis, starting from three ticks down (z = -3)
        f3 = always_redraw(lambda: axes.plot(lambda z: z + 3, color=GREEN, x_range=[-3, vt_z.get_value()]))

        # Define the dot for the tracing point on the third line
        f3_dot = always_redraw(lambda: Dot3D(
            point=axes.c2p(0, 0, vt_z.get_value()),
            color=GREEN
        ))

        # Zoom out the camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES, zoom=0.75)

        # Animate the ValueTracker for the z-axis line to the intersection point
        self.play(Create(f3))
        self.add(f3_dot)
        self.play(vt_z.animate.set_value(intersection_x - 3), run_time=3)

        # Add a purple dot at the intersection point
        intersection_dot_z = Dot3D(point=axes.c2p(0, 0, intersection_x), color=PURPLE)
        self.add(intersection_dot_z)

        # Fade out the green dot
        self.play(FadeOut(f3_dot))
        self.wait(2)

# To run the scene, use the following command in your terminal:
# manim -pql your_script.py MyPlotSceneAnimated3D
