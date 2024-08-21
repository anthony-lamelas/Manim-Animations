from manim import *

class Tute1(ThreeDScene):
    def construct(self):
        # Create the 3D axes
        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6,
        )

        # 2D Graph on 3D Axes
        graph = axes.plot(lambda x: (1/5) * x ** 2, color=YELLOW, x_range=[-2, 6])

        # Parametric Curve (defined correctly)
        graph2 = axes.plot(lambda x: (1/2) * x + 1, color=BLUE, x_range=[-2, 6])

        # Add the objects to the scene
        self.add(axes, graph, graph2)
        self.wait()

        # Initial camera orientation (phi = 60, theta = -45)
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.wait(2)

        # Move camera to a different orientation to show 3D perspective
        self.move_camera(phi=30 * DEGREES, theta=45 * DEGREES, run_time=3)
        self.wait(2)

        # Optional: Animate the graphs or apply other visual effects

        
        '''
        self.play(  # Example animation: change color
            graph2.animate.set_stroke(width=5),  # Example animation: change stroke width
            run_time=2
        )


'''
