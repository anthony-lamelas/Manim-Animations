from manim import *

class MyPlotSceneAnimated(Scene):
    def construct(self):

        # Create a value tracker that updates the scene with an x-value
        vt = ValueTracker(0)

        # Declare x and y axes
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1])

        # Declare the two functions but always update their upper end to the ValueTracker
        f1 = always_redraw(lambda: ax.plot(lambda x: (1/5) * x ** 2, color=BLUE, x_range=[0, vt.get_value()]))
        f2 = always_redraw(lambda: ax.plot(lambda x: (1/2) * x + 1, color=YELLOW, x_range=[0, vt.get_value()]))

        # Declare two dots to trace the two functions, also pointed to the ValueTracker
        f1_dot = always_redraw(lambda: Dot(
                    point=ax.c2p(vt.get_value(), f1.underlying_function(vt.get_value())),
                    color=BLUE
                )
            )

        f2_dot = always_redraw(lambda: Dot(
                    point=ax.c2p(vt.get_value(), f2.underlying_function(vt.get_value())),
                    color=YELLOW
                )
            )

        # Animate the axis being drawn
        self.play(Write(ax))
        self.wait()

        # Add the functions and trace dots
        self.add(f1, f2, f1_dot, f2_dot)

        # Calculate the intersection point
        intersection_x = (5 + 105**0.5) / 4
        intersection_y = (1/5) * intersection_x ** 2  # or (1/2) * intersection_x + 1

        # Animate the ValueTracker to the intersection point
        self.play(vt.animate.set_value(intersection_x), run_time=3)

        # Add a red dot at the intersection point
        intersection_dot = Dot(point=ax.c2p(intersection_x, intersection_y), color=RED)
        self.add(intersection_dot)
        
        # Fade out the blue and yellow dots
        self.play(FadeOut(f1_dot), FadeOut(f2_dot))
        self.wait()
