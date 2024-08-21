from manim import *


class Pomu(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        text = Text('Pomu', font="poppins", color='#2956ED', slant="ITALIC", font_size=54).scale(2)
        circ = Circle(3, color='#797979', stroke_width=15 )
        circ.move_to(text.get_center())

        self.play(DrawBorderThenFill(circ),run_time=1.5)
        self.play(Write(text))



class MultipleBellCurves(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        axes = Axes(
            x_range=[-4, 4, 1], 
            y_range=[0, 0.5, 0.1],
            x_length=10, 
            y_length=6,
            axis_config={"color": BLUE}
        )
        
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # Red curve
        red_curve = axes.plot(
            lambda x: (1 / (0.8 * (2 * PI)**0.5)) * np.exp(-0.5 * ((x - 0) / 0.8)**2), 
            color=RED
        )

        # Blue curve
        blue_curve = axes.plot(
            lambda x: (1 / (1.0 * (2 * PI)**0.5)) * np.exp(-0.5 * ((x - 1.5) / 1.0)**2), 
            color=BLUE
        )

        # Green curve
        green_curve = axes.plot(
            lambda x: (1 / (0.6 * (2 * PI)**0.5)) * np.exp(-0.5 * ((x + 1.0) / 0.6)**2), 
            color=GREEN
        )

        # Brown curve
        brown_curve = axes.plot(
            lambda x: (1 / (1.2 * (2 * PI)**0.5)) * np.exp(-0.5 * ((x + 0.5) / 1.2)**2), 
            color=DARK_BROWN
        )

        self.play(Create(axes), Write(labels))
        self.play(Create(red_curve))
        self.play(Create(blue_curve))
        self.play(Create(green_curve))
        self.play(Create(brown_curve))
        self.wait(2)

# To run this code, save it in a file and execute it with manim.
# For example:
# $ manim -pql my_file.py MultipleBellCurves
