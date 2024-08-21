from manim import * 

config.background_color = ('#2956ED')


# Some color palettes
blue_p = [PURE_BLUE, "#9507b5"]
green_p = [PURE_GREEN, "#02ad9c"]
purple_p = ["#620169", "#8b0994"]
red_p = [PURE_RED, "#a61c41"]

# Light effect
def create_glow(vmobject, rad=0.7, col=YELLOW):
    glow_group = VGroup()
    for idx in range(30, 60):
        new_circle = Circle(radius=rad*(1.002**(idx**2))/400, stroke_opacity=0, fill_color=col,
        fill_opacity=0.2-idx/350).move_to(vmobject)
        glow_group.add(new_circle)
    return glow_group

class MachineAnimation(MovingCameraScene):
    def construct(self):

        machine_rectangle = Rectangle(width=3, height=4, color=BLACK).set_fill(WHITE, 1).set_z_index(-1)

        # Create gears and position them
        gears = SVGMobject(file_name='gears.svg').set_color(BLACK)
        gear1 = gears[:2]
        gear2 = gears[2:]
        gear2.shift(DL*0.1+UP*0.1)
        gears.scale(0.8).shift(DOWN*0.4)

        #Pomu
        pomu = Tex('Pomu', font_size=28, color=BLACK).next_to(machine_rectangle, DOWN+LEFT, buff=0.2).align_to(machine_rectangle, LEFT).shift(UP*0.68 + RIGHT * 0.1 + DOWN*0.2)


        # Progress bar
        progress_rec = Rectangle(height=0.25, width=2.5, stroke_width=2.5, color = BLACK).next_to(machine_rectangle.get_top(), DOWN).set_z_index(10)
        fill_rec = Rectangle(height=0.25, width=0.01, stroke_width=0).next_to(progress_rec.get_left(), buff=0).set_fill(opacity=1).set_color(red_p)
        fill_rec_final = Rectangle(height=0.25, width=2.5, stroke_width=0).next_to(progress_rec.get_left(), buff=0).set_fill(opacity=1).set_color(red_p)

        # Lights
        dot1 = Dot(radius=DEFAULT_SMALL_DOT_RADIUS*2, fill_opacity=0.3, color=PURE_GREEN).set_stroke(width=1, color=BLACK)
        dot2 = Dot(radius=DEFAULT_SMALL_DOT_RADIUS*2, fill_opacity=0.3, color=PURE_GREEN).set_stroke(width=1, color=BLACK)
        dot3 = Dot(radius=DEFAULT_SMALL_DOT_RADIUS*2, fill_opacity=0.3, color=PURE_GREEN).set_stroke(width=1, color=BLACK)
        dots = VGroup(dot1, dot2, dot3).arrange(buff=0.6).next_to(progress_rec, DOWN, buff=0.45)

        glow1 = create_glow(dot1, rad=0.2, col=PURE_GREEN)
        glow2 = create_glow(dot2, rad=0.2, col=PURE_GREEN)
        glow3 = create_glow(dot3, rad=0.2, col=PURE_GREEN)

        # Graphs
        square = Square(1).set_color(BLACK).next_to(machine_rectangle.get_bottom(), UP, buff=0.2).shift(RIGHT*0.8).scale(0.98).set_z_index(5)

        X = np.array([0, 0.2, 0.4, 0.6, 0.8, 1])
        Y1 = np.array([0.2, 0.6, 0.4, 0.8, 0.5, 0.6])
        Y2 = np.array([0.8, 0.1, 0.75, 0.3, 0.6, 0.1])

        axis = Axes(x_range=[0,1,2], y_range=[0,1,2], x_length=square.width*0.95, y_length=square.height*0.95).move_to(square).shift(LEFT*0.08)

        plot1 = axis.plot_line_graph(X, Y1, line_color=ORANGE, add_vertex_dots=False, stroke_width=2).set_z_index(1).set_color(purple_p)['line_graph'].make_smooth()
        plot2 = axis.plot_line_graph(X, Y2, line_color=BLUE, add_vertex_dots=False, stroke_width=2).set_color(red_p)['line_graph'].make_smooth()

        CHUTE_COLOR1 = GRAY_A
        CHUTE_COLOR2 = GRAY_E

        # Chutes components
        chute1 = VGroup()

        rec1 = Rectangle(width=0.12, height=1).set_fill(WHITE, 1).set_stroke(width=0).next_to(machine_rectangle, LEFT, buff=0.02)
        rec2 = rec1.copy().set_color(DARK_GREY).next_to(rec1, LEFT, buff=0)
        
        # Assembling the chutes
        chute1.add(rec2.copy(), rec1.copy(), rec2.copy(), rec1.copy(), rec1.copy()).arrange(LEFT, buff=0).next_to(machine_rectangle, LEFT, buff=0.02)

        sector1 = AnnularSector(inner_radius=0.7, outer_radius=1.1, angle=-PI/2, start_angle=PI+PI/4, color=WHITE).next_to(chute1[-3], LEFT, buff=0).set_z_index(1)
        sector2 =  AnnularSector(inner_radius=1, outer_radius=1.1, angle=-PI/2, start_angle=PI+PI/4, color=WHITE).next_to(sector1.get_left(), RIGHT, buff=0).set_z_index(2)

        chute1.add(sector1, sector2)
        chute2 = chute1.copy().flip().next_to(machine_rectangle, buff=0.02).set_z_index(30)

        # SVGs for the different inputs
        clock = SVGMobject(file_name='clock.svg').set_color(WHITE).scale_to_fit_width(1)
        pin = SVGMobject(file_name='location_pin.svg').set_color(WHITE).scale_to_fit_width(0.8)
        tshirt = SVGMobject(file_name='tshirt.svg').set_color(WHITE).scale_to_fit_width(1.2)

        svgs = VGroup(clock, pin, tshirt).set_z_index(-5).arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.5)

        material = Tex('Material').set_color(WHITE)
        quantity = Tex('Quantity').set_color(WHITE)
        style = Tex('Style').set_color(WHITE)
        dollar = Text('$',font_size=96).set_color(WHITE)

        words = VGroup(dollar, material, quantity, style).arrange(DOWN, buff=1).to_edge(LEFT, buff=0.5)

        inputs = VGroup(dollar, style, tshirt, clock, quantity, pin, material).set_stroke(opacity=0).set_fill(opacity=0)

        # Manufacturer card
        rec_card = Rectangle(width=2, height=3, stroke_width=2).set_fill(WHITE, 1).set_z_index(20).set_stroke(color=GRAY_E)
        printful = Text('PRINTFUL', font='Arial', font_size=26, weight=BOLD).set_color(BLACK).set_z_index(25).next_to(rec_card.get_top(), DOWN, buff=0.2)


        logo = ImageMobject('logo').scale_to_fit_width(rec_card.width*0.7).set_z_index(25).move_to(rec_card).shift(UP*0.3)

        bullets = BulletedList('Fastest delivery', 'Lowest cost', 'Nearest location').set_color(BLACK).scale_to_fit_width(rec_card.width*0.8).next_to(logo, DOWN, buff=-0.1).set_z_index(25)

        card = Group(rec_card, printful, logo, bullets).scale(0.3).move_to(chute2)

        ### ANIMATIONS ###

        self.add(machine_rectangle, gears, pomu, progress_rec, fill_rec, dots, square, chute1, chute2)
        self.add(inputs)
        self.wait(0.5)

        # Inputs go in

        for n, i in enumerate(inputs):
            if n == 0:  # For the dollar sign specifically
                self.play(i.animate.set_fill(opacity=1), run_time=0.4)
                self.play(
                    i.animate(rate_func=rate_functions.ease_in_expo).move_to(chute1).scale(0.4), 
                    chute1.animate.move_to(chute1),
                    run_time=0.15
                    )
            else:
                self.play(i.animate.set_fill(opacity=1), run_time=0.4)
                self.play(
                    i.animate(rate_func=rate_functions.ease_in_expo).move_to(chute1).scale(0.4),
                    chute1.animate.move_to(chute1), 
                    run_time=0.15
                    )

            # Only remove the input after it's completely moved
            self.remove(i)
        
        # Machine processes information
        self.wait(0.5)
        self.play(
            LaggedStart(
                AnimationGroup(dot1.animate.set_fill(opacity=1), FadeIn(glow1), rate_func=lambda t: np.sin(5.5*PI*t)**2, run_time=3/3),
                AnimationGroup(dot2.animate.set_fill(opacity=1), FadeIn(glow2), rate_func=lambda t: np.sin(5.5*PI*t)**2, run_time=3/3),
                AnimationGroup(dot3.animate.set_fill(opacity=1), FadeIn(glow3), rate_func=lambda t: np.sin(5.5*PI*t)**2, run_time=3/3),
                lag_ratio=1,
                run_time=3
            ),
            ReplacementTransform(fill_rec, fill_rec_final, run_time=3, rate_func=linear),
            Rotating(gear1, radians=-TAU, run_time=3),
            Rotating(gear2, run_time=3),
            Create(plot1, run_time=3, rate_func=linear),
            Create(plot2, run_time=3, rate_func=linear),
        )
        # Card appears

        self.wait(0.1)
        self.add(card)
        self.play(
            card.animate.scale(5/3).next_to(chute2, buff=0.2),
            chute2.animate.move_to(chute2),
            run_time=1.0
        )
        chute2.set_z_index(0)
        self.wait(0.4)
        self.play(card.animate.center().scale(3), run_time=1.8)
        self.wait()



#Searching for the right manufacturer?

#Input your needs and leave the work up to us

#With pomu, your perfect fit is just a click away.