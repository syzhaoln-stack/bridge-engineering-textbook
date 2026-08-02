from __future__ import annotations

import math

import numpy as np
from manim import *


PAPER = "#F4F0E6"
INK = "#17313B"
MUTED = "#60737A"
RESIST = "#24A8B5"
LOAD = "#E36B5D"
AMBER = "#E7A93B"
GRID = "#CAD6D3"
FONT = "Microsoft YaHei"


def cn(text: str, size: int = 30, color: str = INK, weight: str = "NORMAL") -> Text:
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def normal_pdf(x: float, mu: float, sigma: float) -> float:
    return math.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2 * math.pi))


class PaperScene(Scene):
    def setup(self):
        self.camera.background_color = PAPER

    def heading(self, question: str, kicker: str):
        k = cn(kicker, 19, AMBER, "BOLD").to_corner(UL, buff=0.38)
        q = cn(question, 32, INK, "BOLD").next_to(k, DOWN, aligned_edge=LEFT, buff=0.1)
        rule = Line(LEFT * 6.55, RIGHT * 6.55, color=GRID, stroke_width=2).next_to(q, DOWN, buff=0.16)
        self.play(FadeIn(k, shift=RIGHT * 0.15), FadeIn(q, shift=RIGHT * 0.15), Create(rule), run_time=1)
        return VGroup(k, q, rule)


class ConcreteGuaranteeRate(PaperScene):
    def construct(self):
        title = self.heading("同一批混凝土，为什么不能只压一个试块？", "01 · 从试块到保证率")

        specimen_group = VGroup()
        strengths = [56, 63, 58, 67, 61, 53]
        for i, value in enumerate(strengths):
            cube = RoundedRectangle(
                corner_radius=0.08, width=0.58, height=0.58,
                fill_color="#D8D1C4", fill_opacity=1, stroke_color=MUTED, stroke_width=1.5,
            )
            cube.add(cn(str(value), 17, INK, "BOLD").move_to(cube))
            specimen_group.add(cube)
        specimen_group.arrange(RIGHT, buff=0.22).move_to(UP * 0.95)

        press_top = RoundedRectangle(corner_radius=0.04, width=0.68, height=0.12,
                                     fill_color=INK, fill_opacity=1, stroke_width=0)
        press_bottom = press_top.copy()
        press = VGroup(press_top, press_bottom)
        press_top.move_to(specimen_group[0].get_top() + UP * 0.18)
        press_bottom.move_to(specimen_group[0].get_bottom() + DOWN * 0.18)
        label = cn("每个试块，都会给出一个不完全相同的数", 23, MUTED).next_to(specimen_group, DOWN, buff=0.42)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in specimen_group], lag_ratio=0.12), run_time=1.8)
        self.play(FadeIn(press), FadeIn(label), run_time=0.6)
        for i in range(3):
            target_x = specimen_group[i].get_x()
            self.play(press.animate.set_x(target_x), run_time=0.28)
            self.play(press_top.animate.shift(DOWN * 0.12), press_bottom.animate.shift(UP * 0.12), run_time=0.18)
            self.play(press_top.animate.shift(UP * 0.12), press_bottom.animate.shift(DOWN * 0.12), run_time=0.18)
        self.wait(0.5)

        axes = Axes(
            x_range=[40, 80, 5], y_range=[0, 0.07, 0.02],
            x_length=9.6, y_length=3.3,
            axis_config={"color": MUTED, "stroke_width": 2, "include_tip": False},
            x_axis_config={"numbers_to_include": [45, 50, 60, 70]},
            y_axis_config={"include_ticks": False},
        ).shift(DOWN * 0.45)
        x_lab = cn("立方体抗压强度 / MPa", 20, MUTED).next_to(axes.x_axis, DOWN, buff=0.23)
        curve = axes.plot(lambda x: normal_pdf(x, 60.5, 6.4), x_range=[40, 80], color=RESIST, stroke_width=4)
        dots = VGroup(*[
            Dot(axes.c2p(v, 0), radius=0.065, color=AMBER) for v in [53, 56, 58, 59, 61, 61, 62, 63, 65, 67, 69]
        ])
        self.play(FadeOut(VGroup(specimen_group, press, label)), FadeIn(axes), FadeIn(x_lab), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.18) for d in dots], lag_ratio=0.07), run_time=1.2)
        self.play(Create(curve), run_time=1.4)

        mu_x = 60.5
        fk_x = 50.0
        mean_line = DashedLine(axes.c2p(mu_x, 0), axes.c2p(mu_x, normal_pdf(mu_x, 60.5, 6.4)), color=MUTED)
        mean_lab = MathTex(r"\mu", color=MUTED).scale(0.8).next_to(mean_line, UP, buff=0.08)
        fk_line = DashedLine(axes.c2p(fk_x, 0), axes.c2p(fk_x, normal_pdf(fk_x, 60.5, 6.4)), color=AMBER)
        fk_lab = MathTex(r"f_{cu,k}", color=AMBER).scale(0.68).next_to(fk_line, UP, buff=0.08)
        area95 = axes.get_area(curve, x_range=[fk_x, 80], color=RESIST, opacity=0.25)
        area5 = axes.get_area(curve, x_range=[40, fk_x], color=LOAD, opacity=0.34)
        ninety = cn("95%", 27, RESIST, "BOLD").move_to(axes.c2p(63.0, 0.022))
        five = cn("5%", 20, LOAD, "BOLD").move_to(axes.c2p(46.5, 0.006))
        question = cn("C50 是“平均值 50”吗？", 27, INK, "BOLD").to_edge(RIGHT, buff=0.65).shift(UP * 1.85)
        self.play(FadeIn(question, shift=LEFT * 0.15), Create(mean_line), FadeIn(mean_lab), run_time=0.8)
        self.play(FadeIn(area95), FadeIn(area5), Create(fk_line), FadeIn(fk_lab), FadeIn(ninety), FadeIn(five), run_time=1.3)

        relation = MathTex(r"f_{cu,k}=\mu-1.645\sigma", color=INK).scale(0.82)
        relation.to_edge(RIGHT, buff=0.65).shift(UP * 1.25)
        answer = cn("C50：标准值为 50 MPa，不是平均值", 23, RESIST, "BOLD")
        answer.next_to(relation, DOWN, aligned_edge=RIGHT, buff=0.17)
        self.play(Write(relation), FadeTransform(question, answer), run_time=1.4)
        self.wait(0.8)

        closing = cn("多做试块，是为了看见离散。", 29, INK, "BOLD").to_edge(DOWN, buff=0.28)
        self.play(FadeOut(VGroup(question, answer, relation, dots)), FadeIn(closing, shift=UP * 0.12), run_time=0.9)
        self.wait(1.5)


class ConcreteToDesignValue(PaperScene):
    def construct(self):
        self.heading("试块压出的 50 MPa，能直接拿去算桥吗？", "01B · 从材料试验到构件设计")
        cube = RoundedRectangle(corner_radius=.08, width=1.25, height=1.25,
                                fill_color="#D8D1C4", fill_opacity=1, stroke_color=MUTED, stroke_width=2)
        cube.shift(LEFT * 4 + UP * .25)
        cube_lab = VGroup(cn("立方体试块", 20, MUTED), MathTex(r"f_{cu,k}", color=INK).scale(.72)).arrange(DOWN, buff=.1).next_to(cube, DOWN)
        member = Rectangle(width=1.1, height=2.4, fill_color="#AFC0C1", fill_opacity=.65, stroke_color=INK).shift(UP * .25)
        member_lab = VGroup(cn("构件受压状态", 20, MUTED), MathTex(r"f_{ck}", color=INK).scale(.72)).arrange(DOWN, buff=.1).next_to(member, DOWN)
        design = VGroup(
            Rectangle(width=2.2, height=.34, fill_color=RESIST, fill_opacity=.42, stroke_color=RESIST),
            Line(LEFT*.85, DOWN*.65, color=INK), Line(RIGHT*.85, DOWN*.65, color=INK)
        ).shift(RIGHT * 4 + UP * .25)
        design_lab = VGroup(cn("进入设计", 20, MUTED), MathTex(r"f_d", color=INK).scale(.72)).arrange(DOWN, buff=.1).next_to(design, DOWN)
        a1 = Arrow(cube.get_right(), member.get_left(), color=AMBER, buff=.25, stroke_width=5)
        a2 = Arrow(member.get_right(), design.get_left(), color=AMBER, buff=.25, stroke_width=5)
        self.play(FadeIn(cube), FadeIn(cube_lab))
        self.play(GrowArrow(a1), FadeIn(member), FadeIn(member_lab), run_time=1)
        self.play(GrowArrow(a2), FadeIn(design), FadeIn(design_lab), run_time=1)
        route = cn("试块标准值 → 构件受力状态 → 设计值", 24, RESIST, "BOLD").to_edge(UP, buff=1.45)
        formula = MathTex(r"f_d=\frac{f_k}{\gamma_M}", color=INK).scale(.88).to_edge(DOWN, buff=.72)
        scope = cn("抽象关系；具体换算与取值查所采用的标准", 18, MUTED).next_to(formula, DOWN, buff=.12)
        self.play(FadeIn(route), Write(formula), FadeIn(scope), run_time=1.2)
        closing = cn("试块给证据，不直接替构件作决定。", 27, INK, "BOLD").to_edge(DOWN, buff=.12)
        self.play(FadeOut(VGroup(formula, scope)), FadeIn(closing), run_time=.8)
        self.wait(1.4)


class ReliabilityFromOneToJoint(ThreeDScene):
    def construct(self):
        self.camera.background_color = PAPER
        kicker = cn("02 · 从一维到联合分布", 19, AMBER, "BOLD").to_corner(UL, buff=0.38)
        question = cn("平均抗力更大，为什么仍可能失效？", 32, INK, "BOLD").next_to(kicker, DOWN, aligned_edge=LEFT, buff=0.1)
        self.add_fixed_in_frame_mobjects(kicker, question)
        self.play(FadeIn(kicker), FadeIn(question), run_time=0.8)

        axes = Axes(
            x_range=[20, 110, 10], y_range=[0, 0.065, 0.02],
            x_length=10.3, y_length=3.6,
            axis_config={"color": MUTED, "include_tip": False},
            x_axis_config={"numbers_to_include": [40, 60, 80, 100]},
            y_axis_config={"include_ticks": False},
        ).shift(DOWN * 0.75)
        xlab = cn("同一条数轴", 19, MUTED).next_to(axes.x_axis, DOWN, buff=0.22)
        s_curve = axes.plot(lambda x: normal_pdf(x, 53, 8.5), x_range=[20, 100], color=LOAD, stroke_width=4)
        r_curve = axes.plot(lambda x: normal_pdf(x, 77, 9.5), x_range=[35, 110], color=RESIST, stroke_width=4)
        s_lab = cn("荷载 S", 23, LOAD, "BOLD").move_to(axes.c2p(46, 0.052))
        r_lab = cn("抗力 R", 23, RESIST, "BOLD").move_to(axes.c2p(85, 0.048))
        self.add_fixed_in_frame_mobjects(axes, xlab, s_curve, r_curve, s_lab, r_lab)
        self.play(FadeIn(axes), FadeIn(xlab), Create(s_curve), Create(r_curve), FadeIn(s_lab), FadeIn(r_lab), run_time=1.8)

        s_shift = axes.plot(lambda x: normal_pdf(x, 60, 8.5), x_range=[25, 105], color=LOAD, stroke_width=4)
        r_shift = axes.plot(lambda x: normal_pdf(x, 70, 9.5), x_range=[30, 108], color=RESIST, stroke_width=4)
        first_change = cn("先只让荷载向大处偏。", 25, LOAD, "BOLD").to_edge(DOWN, buff=0.25)
        warning = cn("再让抗力向小处偏：两件事赶到同一次。", 25, INK, "BOLD").to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(first_change)
        self.play(Transform(s_curve, s_shift), s_lab.animate.shift(RIGHT * 0.75), FadeIn(first_change), run_time=1.2)
        self.wait(.45)
        self.add_fixed_in_frame_mobjects(warning)
        self.play(Transform(r_curve, r_shift), r_lab.animate.shift(LEFT * 0.75), FadeTransform(first_change, warning), run_time=1.2)
        self.wait(0.8)

        all2d = VGroup(axes, xlab, s_curve, r_curve, s_lab, r_lab, warning)
        plane = Axes(
            x_range=[25, 105, 20], y_range=[25, 105, 20],
            x_length=7.2, y_length=5.0,
            axis_config={"color": MUTED, "include_tip": True},
        ).shift(DOWN * 0.45)
        px = MathTex("S", color=LOAD).scale(0.8).next_to(plane.x_axis, RIGHT, buff=0.1)
        py = MathTex("R", color=RESIST).scale(0.8).next_to(plane.y_axis, UP, buff=0.1)
        boundary = Line(plane.c2p(25, 25), plane.c2p(105, 105), color=AMBER, stroke_width=4)
        rng = np.random.default_rng(19)
        samples = rng.multivariate_normal([60, 70], [[8.5**2, 0], [0, 9.5**2]], 64)
        dots = VGroup()
        for s, r in samples:
            if 25 <= s <= 105 and 25 <= r <= 105:
                dots.add(Dot(plane.c2p(s, r), radius=0.032, color=LOAD if r < s else RESIST, fill_opacity=0.72))
        safe = cn("可承受  R ≥ S", 22, RESIST, "BOLD").move_to(plane.c2p(45, 87))
        fail = cn("失效  R < S", 22, LOAD, "BOLD").move_to(plane.c2p(84, 43))
        pair_note = cn("每一个点，都是同一次出现的荷载与抗力", 22, MUTED).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(plane, px, py, boundary, dots, safe, fail, pair_note)
        self.play(FadeOut(all2d), FadeIn(plane), FadeIn(px), FadeIn(py), Create(boundary), run_time=1)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.015), FadeIn(safe), FadeIn(fail), FadeIn(pair_note), run_time=1.8)
        self.wait(1)

        self.play(FadeOut(VGroup(plane, px, py, boundary, dots, safe, fail, pair_note)), run_time=0.8)
        axes3 = ThreeDAxes(
            x_range=[25, 105, 20], y_range=[25, 105, 20], z_range=[0, 1.2, 0.4],
            x_length=7.0, y_length=5.0, z_length=2.8,
            axis_config={"color": MUTED, "stroke_width": 2},
        )

        def height(s, r):
            return math.exp(-0.5 * (((s - 60) / 8.5) ** 2 + ((r - 70) / 9.5) ** 2))

        def fail_joint(s, t):
            r = 25 + t * (s - 25)
            return axes3.c2p(s, r, height(s, r))

        def safe_joint(s, t):
            r = s + t * (105 - s)
            return axes3.c2p(s, r, height(s, r))

        fail_surface = Surface(
            fail_joint, u_range=[25, 105], v_range=[0, 1], resolution=(16, 10),
            fill_opacity=0.82, checkerboard_colors=[LOAD, "#F09886"], stroke_color="#F9E2DC", stroke_width=0.22,
        )
        safe_surface = Surface(
            safe_joint, u_range=[25, 105], v_range=[0, 1], resolution=(16, 10),
            fill_opacity=0.78, checkerboard_colors=[RESIST, "#62C5C8"], stroke_color="#E8F1EE", stroke_width=0.22,
        )
        diagonal = ParametricFunction(lambda t: axes3.c2p(t, t, 0.025), t_range=[25, 105], color=AMBER, stroke_width=5)
        boundary_peak = (60 / 8.5**2 + 70 / 9.5**2) / (1 / 8.5**2 + 1 / 9.5**2)
        mpf_point = Dot3D(axes3.c2p(boundary_peak, boundary_peak, height(boundary_peak, boundary_peak)), radius=0.09, color=AMBER)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.82)
        self.play(Create(axes3), FadeIn(safe_surface), FadeIn(fail_surface), Create(diagonal), FadeIn(mpf_point), run_time=2.2)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(3.2)
        self.stop_ambient_camera_rotation()

        formula = MathTex(r"g=R-S\qquad P_f=P(g<0)", color=INK).scale(0.92).to_edge(DOWN, buff=0.28)
        mpf = cn("失效边界上密度较高的位置", 20, AMBER, "BOLD").to_edge(RIGHT, buff=0.55).shift(DOWN * 0.2)
        closing = cn("可靠度问的不是“会不会”，而是留给失效侧的概率有多大。", 24, INK, "BOLD").to_edge(UP, buff=1.25)
        self.add_fixed_in_frame_mobjects(formula, mpf, closing)
        self.play(Write(formula), FadeIn(mpf), FadeIn(closing), run_time=1.5)
        self.wait(2)


class InfluenceLineMovingLoad(PaperScene):
    def construct(self):
        title = self.heading("同一辆车，为什么会有不同的“最不利位置”？", "03 · 影响线")
        beam_y = 0.65
        left_x, right_x = -5.0, 5.0
        beam = Line([left_x, beam_y, 0], [right_x, beam_y, 0], color=INK, stroke_width=7)
        support_l = VGroup(Polygon([-5.25, 0.15, 0], [-4.75, 0.15, 0], [-5.0, 0.58, 0], color=MUTED, fill_opacity=0.18),
                           Line([-5.4, 0.1, 0], [-4.6, 0.1, 0], color=MUTED))
        support_r = support_l.copy().shift(RIGHT * 10)
        car = VGroup(
            RoundedRectangle(corner_radius=0.08, width=0.9, height=0.38, fill_color=AMBER, fill_opacity=1, stroke_color=INK),
            Circle(radius=0.1, fill_color=INK, fill_opacity=1, stroke_width=0).shift(LEFT * 0.28 + DOWN * 0.22),
            Circle(radius=0.1, fill_color=INK, fill_opacity=1, stroke_width=0).shift(RIGHT * 0.28 + DOWN * 0.22),
        ).move_to([left_x, beam_y + 0.43, 0])
        self.play(Create(beam), FadeIn(support_l), FadeIn(support_r), FadeIn(car), run_time=1.2)

        axes = Axes(
            x_range=[0, 1, 0.25], y_range=[0, 1.15, 0.25], x_length=10, y_length=2.25,
            axis_config={"color": GRID, "include_tip": False, "include_ticks": False},
        ).shift(DOWN * 1.85)
        car_position = cn("车的位置", 18, MUTED).next_to(axes.x_axis, DOWN, buff=.1)
        observed = cn("正在看的结果", 18, MUTED).next_to(axes.y_axis, LEFT, buff=.1).rotate(PI/2)
        tracker = ValueTracker(0)
        car.add_updater(lambda m: m.move_to([left_x + 10 * tracker.get_value(), beam_y + 0.43, 0]))
        response_arrow = always_redraw(lambda: Arrow(
            [right_x, beam_y - 0.05, 0],
            [right_x, beam_y - 0.05 + 0.75 * tracker.get_value(), 0],
            color=RESIST, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.18,
        ))
        target = cn("现在守着：右支座反力", 22, RESIST, "BOLD").to_edge(RIGHT, buff=0.55).shift(UP * 1.8)
        rline = axes.plot(lambda x: x, x_range=[0, 1], color=RESIST, stroke_width=4)
        trace = always_redraw(lambda: axes.plot(lambda x: x, x_range=[0, max(0.001, tracker.get_value())], color=RESIST, stroke_width=4))
        self.play(FadeIn(axes), FadeIn(car_position), FadeIn(observed), FadeIn(target), FadeIn(response_arrow), FadeIn(trace), run_time=0.8)
        self.play(tracker.animate.set_value(1), run_time=4.3, rate_func=linear)
        self.play(FadeOut(trace), FadeIn(rline), run_time=0.4)
        self.wait(0.6)

        tracker.set_value(0)
        target2 = cn("换一个目标：跨中弯矩", 22, LOAD, "BOLD").move_to(target)
        triangle = axes.plot(lambda x: 2 * x if x <= 0.5 else 2 * (1 - x), x_range=[0, 1], color=LOAD, stroke_width=4)
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(tracker.get_value(), 2 * tracker.get_value() if tracker.get_value() <= 0.5 else 2 * (1 - tracker.get_value())),
            radius=0.06, color=AMBER,
        ))
        self.play(FadeOut(response_arrow), FadeTransform(target, target2), rline.animate.set_stroke(opacity=0.16), FadeIn(moving_dot), run_time=0.9)
        self.play(Create(triangle), tracker.animate.set_value(1), run_time=4.6, rate_func=linear)
        self.wait(0.6)

        self.play(tracker.animate.set_value(0.5), run_time=1.2)
        peak_line = DashedLine([0, beam_y, 0], axes.c2p(0.5, 1), color=AMBER, stroke_width=3)
        formula = MathTex(r"E=P\,y(x)", color=INK).scale(0.92).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.7)
        symbols = cn("P：车重　y：图上读数　E：正在看的结果", 17, MUTED).next_to(formula, DOWN, buff=.12)
        self.play(Create(peak_line), Write(formula), FadeIn(symbols), run_time=1)
        self.wait(0.8)

        closing = cn("别急着问车停在哪里。先说清楚，你替谁守着。", 28, INK, "BOLD").to_edge(DOWN, buff=0.18)
        term = cn("影响线：固定一个效应，让单位荷载沿桥移动。", 20, MUTED).next_to(closing, UP, buff=0.12)
        self.play(FadeIn(closing, shift=UP * 0.12), FadeIn(term), run_time=1)
        self.wait(2)
