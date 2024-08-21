from manim import *

class Cube(Scene):
    def construct(self):
        # These are the 2-d screen directions and distances that the hypercube will grow into.
        # There is no higher dimensional object under the hood, it is only an illusion.
        # The hypercube will grow to as many dimensions as there are entries in this list.
        # In other words, the length of this list controls the length of the entire animation.
        # Add more if you want more steps/dimensions!
        directions = [
            RIGHT,
            DOWN,
            (2*RIGHT + UP) / 5,
            UR / 2,
            (LEFT + 3*UP) / 7
        ]
        # It was looking a bit small so I just used this to double all their lengths
        directions = [2 * d for d in directions]

        # Edges will be colored according to this list. Must be at least as long as
        # the directions list.
        colors = [
            RED,
            ORANGE,
            YELLOW,
            GREEN,
            BLUE,
            PURPLE
        ]

        # All vertices and edges will be contained within these two VGroups.
        # z_index is so the vertices will always appear in front of edges.
        # All vertices are ultimately copies of this first vertex.
        vertices = VGroup(Dot(radius=0.05).set_z_index(1))
        edges = VGroup()

        # This is probably an over-complicated way to have done this, but it spits out a Tex mobject saying
        # 3-dimensional or whatever which has the updater to always stay just above the hypercube.
        # I gave two substrings to Tex instead of just one so that it correctly transforms just the first string.
        def dimension_text_factory(n):
            if n == 1:
                return Tex(str(n), "\\text{-Input}").add_updater(lambda mob: mob.next_to(vertices, UP))
            else:
                return Tex(str(n), "\\text{-Inputs}").add_updater(lambda mob: mob.next_to(vertices, UP))
        dimension_text = dimension_text_factory(0).update()

        self.add(vertices, dimension_text)
        self.wait(0.5)

        final_dot_radius = 0.05
        final_dot = None

        # As you can see, the master loop is over the elements of the directions list
        for i, d in enumerate(directions):
            # A whole lot of animations need to happen at once, so I will put them all in a
            # list for now to be passed to a single AnimationGroup later.
            anims = []
            for e in edges:
                # Copies the existing edge and adds the new one to the edges VGroup.
                # Then it adds the animated motion of both edges to the anims list.
                # One goes one way, the other goes the other way. That way it all stays centered.
                new_e = e.copy()
                edges.add(new_e)
                anims.append(new_e.animate.shift(d / 2))
                anims.append(e.animate.shift(-d / 2))
            for v in vertices:
                # Copies the existing vertex and adds the new one to the vertices VGroup.
                # Then it adds the animated motion of both vertices to the anims list, same as the edges.
                # Initial tiny shift is because the Line will throw an error if the endpoints are equal.
                new_v = v.copy().shift(d * 0.001)
                vertices.add(new_v)
                anims.append(new_v.animate.shift(d / 2))
                anims.append(v.animate.shift(-d / 2))
                # Now we also must make the new edges between the old vertices and the new vertices.
                # always_redraw is a useful syntax for placing an updater on a new object.
                # It will always be redrawn every frame according to its definition until the updater is removed.
                # That way, the new edges will automatically span between the old and new vertices as they separate.
                between_edge = always_redraw(lambda v=v, new_v=new_v:
                                             Line(v.get_center(), new_v.get_center(), color=colors[i])
                                             )
                edges.add(between_edge)
            # Both these groups got new submobjects so we add them to the scene again to guarantee visibility
            self.add(vertices, edges)
            self.play(
                Transform(dimension_text, dimension_text_factory(i + 1), run_time=0.2),
                AnimationGroup(*anims, run_time=0.3)  # it all culminates in this line!
            )
            # Once this animation step is complete, we want to remove the updaters from the new edges
            # and turn them back into mundane Lines, so they do not get confused on the next step.
            for e in edges:
                e.clear_updaters()
            # And finally, a pause before the next step.
            self.wait(0.5)

            final_dot_radius += 0.1
            new_final_dot = Dot(radius=final_dot_radius).shift(4.5 * RIGHT)
            self.play(ReplacementTransform(edges.copy(), new_final_dot, run_time=0.5))
            
            if final_dot:
                self.remove(final_dot)
            final_dot = new_final_dot

        self.play(FadeOut(vertices), FadeOut(edges))

        final_text = Tex("Manufacturer")

        self.play(final_dot.animate.shift(4.5 * LEFT), FadeOut(dimension_text), FadeIn(final_text.shift(UP * 2.7)))
        self.play(FadeOut(final_dot), FadeOut(final_text))
