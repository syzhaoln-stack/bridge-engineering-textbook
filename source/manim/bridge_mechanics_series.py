from __future__ import annotations

import numpy as np
from manim import *


PAPER = "#F4F0E6"
INK = "#17313B"
MUTED = "#60737A"
CYAN = "#24A8B5"
CORAL = "#E36B5D"
AMBER = "#E7A93B"
GRID = "#CAD6D3"
FONT = "Microsoft YaHei"


def txt(s, size=28, color=INK, weight="NORMAL"):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def pin_support(point, color=MUTED):
    tri = Polygon(point + LEFT * .3, point + RIGHT * .3, point + UP * .42,
                  color=color, fill_color=color, fill_opacity=.12)
    ground = Line(point + LEFT * .42, point + RIGHT * .42, color=color)
    return VGroup(tri, ground)


class MiniLesson(Scene):
    def setup(self):
        self.camera.background_color = PAPER

    def open(self, no, question):
        k = txt(f"{no} · 先看一个变化", 18, AMBER, "BOLD").to_corner(UL, buff=.34)
        q = txt(question, 31, INK, "BOLD").next_to(k, DOWN, aligned_edge=LEFT, buff=.08)
        rule = Line(LEFT * 6.55, RIGHT * 6.55, color=GRID, stroke_width=2).next_to(q, DOWN, buff=.14)
        self.play(FadeIn(k), FadeIn(q), Create(rule), run_time=.8)
        return VGroup(k, q, rule)

    def finish(self, plain, formula=None):
        note = txt(plain, 25, INK, "BOLD").to_edge(DOWN, buff=.2)
        if note.width > 12.4:
            note.scale_to_fit_width(12.4)
        items = [FadeIn(note, shift=UP * .12)]
        if formula is not None:
            formula.next_to(note, UP, buff=.15)
            items.append(Write(formula))
        self.play(*items, run_time=1)
        self.wait(1.5)


class ScaleLaw(MiniLesson):
    def construct(self):
        self.open("04", "所有尺寸都放大两倍，桥也只是重两倍吗？")
        premise = txt("同材料 · 几何相似 · 只比较自重", 18, MUTED).to_edge(RIGHT, buff=.55).shift(UP*1.75)
        small = Rectangle(width=3, height=.45, fill_color=CYAN, fill_opacity=.28, stroke_color=CYAN).shift(LEFT * 3 + UP * .5)
        large = Rectangle(width=6, height=.9, fill_color=CYAN, fill_opacity=.28, stroke_color=CYAN).shift(RIGHT * 1.8 + UP * .35)
        ls = txt("尺度 1", 22, MUTED).next_to(small, UP)
        ll = txt("尺度 2", 22, AMBER, "BOLD").next_to(large, UP)
        self.play(FadeIn(small), FadeIn(ls), FadeIn(premise))
        self.play(TransformFromCopy(small, large), FadeIn(ll), run_time=1.2)
        demand1 = VGroup(*[Square(.18, fill_color=CORAL, fill_opacity=.8, stroke_width=0) for _ in range(1)])
        demand2 = VGroup(*[Square(.18, fill_color=CORAL, fill_opacity=.8, stroke_width=0) for _ in range(16)]).arrange_in_grid(4, 4, buff=.06)
        cap1 = VGroup(*[Circle(.09, fill_color=CYAN, fill_opacity=1, stroke_width=0) for _ in range(1)])
        cap2 = VGroup(*[Circle(.09, fill_color=CYAN, fill_opacity=1, stroke_width=0) for _ in range(8)]).arrange_in_grid(2, 4, buff=.06)
        labels = VGroup(txt("自重弯矩", 20, CORAL, "BOLD"), txt("截面能力", 20, CYAN, "BOLD")).arrange(DOWN, buff=.55).to_edge(LEFT, buff=.75).shift(DOWN * 1.15)
        reason = txt("质量 ×8，再乘力臂 ×2", 17, CORAL).next_to(labels[0], DOWN, aligned_edge=LEFT, buff=.14)
        demand1.next_to(labels[0], RIGHT, buff=.35)
        demand2.next_to(demand1, RIGHT, buff=2.15)
        cap1.next_to(labels[1], RIGHT, buff=.35)
        cap2.next_to(cap1, RIGHT, buff=2.15)
        ratios = VGroup(txt("×1", 18, MUTED).next_to(demand1, RIGHT), txt("×16", 21, CORAL, "BOLD").next_to(demand2, RIGHT),
                        txt("×1", 18, MUTED).next_to(cap1, RIGHT), txt("×8", 21, CYAN, "BOLD").next_to(cap2, RIGHT))
        self.play(FadeIn(labels), FadeIn(reason), FadeIn(demand1), FadeIn(cap1))
        self.play(LaggedStart(*[FadeIn(m, scale=.3) for m in demand2], lag_ratio=.025), LaggedStart(*[FadeIn(m, scale=.3) for m in cap2], lag_ratio=.04), FadeIn(ratios), run_time=1.5)
        self.finish("尺寸一起长大，需求会跑得比能力更快。",
                    MathTex(r"M_g\propto\lambda^4\qquad M_R\propto\lambda^3", color=INK).scale(.8))


class ForcePath(MiniLesson):
    def construct(self):
        self.open("05", "一个车轮的重量，最后交给谁？")
        deck = Rectangle(width=8.6, height=.26, fill_color="#AFC0C1", fill_opacity=1, stroke_color=INK).shift(UP * 1.1)
        girders = VGroup(*[Rectangle(width=3.5, height=.18, fill_color=CYAN, fill_opacity=.45, stroke_color=CYAN) for _ in range(2)])
        girders.arrange(RIGHT, buff=1).next_to(deck, DOWN, buff=.15)
        bearings = VGroup(*[RoundedRectangle(corner_radius=.04, width=.48, height=.18, fill_color=AMBER, fill_opacity=1, stroke_width=0) for _ in range(2)])
        bearings.arrange(RIGHT, buff=5.6).next_to(girders, DOWN, buff=.16)
        piers = VGroup(*[Rectangle(width=.55, height=1.1, fill_color=MUTED, fill_opacity=.25, stroke_color=MUTED) for _ in range(2)])
        piers.arrange(RIGHT, buff=5.5).next_to(bearings, DOWN, buff=.02)
        foundations = VGroup(*[Rectangle(width=1.25, height=.24, fill_color=MUTED, fill_opacity=.35, stroke_color=MUTED) for _ in range(2)])
        foundations.arrange(RIGHT, buff=4.8).next_to(piers, DOWN, buff=0)
        wheel = Circle(.22, fill_color=INK, fill_opacity=1, stroke_width=0).move_to(deck.get_top() + UP * .23 + LEFT * 1.2)
        self.play(FadeIn(VGroup(deck, girders, bearings, piers, foundations, wheel)), run_time=1)
        points = [wheel.get_bottom(), deck.get_center() + LEFT * 1.2, girders[0].get_center(), bearings[0].get_center(), piers[0].get_center(), foundations[0].get_center()]
        labels = ["桥面板", "主梁", "支座", "桥墩", "基础"]
        for i in range(len(points) - 1):
            arrow = Arrow(points[i], points[i + 1], buff=.05, color=CORAL if i == 0 else CYAN, stroke_width=5)
            lab = txt(labels[i], 19, MUTED).next_to(points[i + 1], RIGHT, buff=.18)
            self.play(GrowArrow(arrow), FadeIn(lab), run_time=.45)
        self.finish("力走到地面，反力才把账结清。", MathTex(r"\sum R=\sum W", color=INK).scale(.85))


class BeamDepth(MiniLesson):
    def construct(self):
        self.open("06", "材料不变，只把梁加深一倍，会发生什么？")
        premise = txt("同跨度 · 同荷载 · 同边界 · 同材料和宽度", 17, MUTED).to_edge(RIGHT, buff=.5).shift(UP*1.72)
        b1 = Rectangle(width=5.1, height=.35, fill_color=CYAN, fill_opacity=.35, stroke_color=CYAN).shift(UP * 1.05)
        b2 = Rectangle(width=5.1, height=.7, fill_color=CYAN, fill_opacity=.35, stroke_color=CYAN).shift(DOWN * .95)
        supports = VGroup(pin_support(b1.get_bottom() + LEFT * 2.3 + DOWN * .45), pin_support(b1.get_bottom() + RIGHT * 2.3 + DOWN * .45),
                          pin_support(b2.get_bottom() + LEFT * 2.3 + DOWN * .45), pin_support(b2.get_bottom() + RIGHT * 2.3 + DOWN * .45))
        load1 = Arrow(b1.get_top() + UP * .7, b1.get_top(), color=CORAL, buff=0)
        load2 = Arrow(b2.get_top() + UP * .7, b2.get_top(), color=CORAL, buff=0)
        labs = VGroup(txt("梁高 h", 20, MUTED).next_to(b1, LEFT), txt("梁高 2h", 20, AMBER, "BOLD").next_to(b2, LEFT))
        self.play(FadeIn(VGroup(b1, b2, supports, load1, load2, labs)), FadeIn(premise), run_time=1)
        curve1 = VMobject(color=CORAL, stroke_width=4).set_points_smoothly([[-2.55,.86,0],[0,.45,0],[2.55,.86,0]])
        curve2 = VMobject(color=CYAN, stroke_width=4).set_points_smoothly([[-2.55,-1.32,0],[0,-1.38,0],[2.55,-1.32,0]])
        self.play(Transform(b1.copy(), curve1), Transform(b2.copy(), curve2), run_time=1.5)
        compare = VGroup(txt("挠得多", 20, CORAL, "BOLD").next_to(curve1, RIGHT), txt("约为 1/8", 20, CYAN, "BOLD").next_to(curve2, RIGHT))
        self.play(FadeIn(compare))
        self.finish("同样材料，放得离中性轴更远，抗弯刚度增长很快。",
                    MathTex(r"I=\frac{bh^3}{12}\quad\Rightarrow\quad I(2h)=8I(h)", color=INK).scale(.72))


class ArchPressureLine(MiniLesson):
    def construct(self):
        self.open("07", "为什么拱的形状要追着压力线走？")
        arch = ParametricFunction(lambda t: [4.6*t, -1.55*t*t + .9, 0], t_range=[-1, 1], color=INK, stroke_width=12)
        deck = Line([-4.8,1.25,0],[4.8,1.25,0],color=MUTED,stroke_width=5)
        columns = VGroup(*[Line([x,1.25,0],[x,-1.55*(x/4.6)**2+.9,0],color=MUTED,stroke_width=2) for x in np.linspace(-3.8,3.8,7)])
        thrust = arch.copy().set_color(CYAN).set_stroke(width=4)
        loads = VGroup(*[Arrow([x,2.25,0],[x,1.25-1.55*(x/4.6)**2,0],buff=.05,color=CORAL,stroke_width=3) for x in np.linspace(-3.4,3.4,7)])
        self.play(Create(arch), Create(deck), LaggedStart(*[Create(c) for c in columns],lag_ratio=.05), LaggedStart(*[GrowArrow(a) for a in loads], lag_ratio=.08), Create(thrust), run_time=1.5)
        centered = txt("压力线贴近拱轴：弯曲很小", 21, CYAN, "BOLD").to_edge(RIGHT, buff=.65).shift(UP * 1.8)
        self.play(FadeIn(centered))
        shifted = ParametricFunction(lambda t: [4.6*t, -1.55*t*t + .9 + .32*(1-t*t)*t, 0], t_range=[-1,1], color=AMBER, stroke_width=4)
        self.play(Transform(thrust, shifted), loads[0].animate.set_opacity(.15), loads[1].animate.set_opacity(.15), run_time=1.3)
        changed = txt("荷载偏到一侧", 19, CORAL, "BOLD").to_edge(RIGHT, buff=.55).shift(UP*1.75)
        e_line = Line(arch.point_from_proportion(.68), shifted.point_from_proportion(.68), color=CORAL, stroke_width=5)
        e = MathTex("e", color=CORAL).scale(.7).next_to(e_line, RIGHT, buff=.08)
        self.play(Create(e_line), FadeIn(e), FadeIn(changed), FadeOut(centered))
        self.finish("压力线离开拱轴，轴力就带出弯矩。", MathTex(r"M=N\,e", color=INK).scale(.9))


class CableSag(MiniLesson):
    def construct(self):
        self.open("08", "同样跨度与荷载，索垂得深一点会怎样？")
        premise = txt("两端等高 · 荷载沿水平投影均布 · 抛物线近似", 17, MUTED).to_edge(RIGHT, buff=.5).shift(UP*1.72)
        towers = VGroup(Line([-5,-1.5,0],[-5,1.7,0],color=INK,stroke_width=8), Line([5,-1.5,0],[5,1.7,0],color=INK,stroke_width=8))
        shallow = ParametricFunction(lambda t: [10*t-5, 1.5-1.0*(1-(2*t-1)**2),0], t_range=[0,1], color=CYAN, stroke_width=5)
        deep = ParametricFunction(lambda t: [10*t-5, 1.5-2.0*(1-(2*t-1)**2),0], t_range=[0,1], color=CYAN, stroke_width=5)
        arrows = VGroup(*[Arrow([x,2.25,0],[x,1.65,0],color=CORAL,buff=0,stroke_width=3) for x in np.linspace(-4,4,9)])
        h1 = Arrow([-5,1.5,0],[-3.2,1.5,0],color=AMBER,buff=0,stroke_width=6)
        lab = txt("鞍座处水平分力 H 较大", 19, AMBER, "BOLD").next_to(h1, DOWN)
        self.play(FadeIn(towers), Create(shallow), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.04), GrowArrow(h1), FadeIn(lab), FadeIn(premise), run_time=1.5)
        h2 = Arrow([-5,1.5,0],[-4.05,1.5,0],color=AMBER,buff=0,stroke_width=6)
        lab2 = txt("垂度增大，水平拉力减小", 20, CYAN, "BOLD").move_to(lab)
        self.play(Transform(shallow, deep), Transform(h1, h2), FadeTransform(lab, lab2), run_time=1.5)
        self.finish("索形不是画出来的轮廓，是荷载与拉力的平衡。", MathTex(r"H=\frac{qL^2}{8f}", color=INK).scale(.9))


class CableStayedBalance(MiniLesson):
    def construct(self):
        self.open("09", "斜拉桥只压一侧，谁先失去平衡？")
        tower = Line([0,-1.8,0],[0,2.1,0],color=INK,stroke_width=10)
        deck = Line([-5,-1.15,0],[5,-1.15,0],color=INK,stroke_width=7)
        foundation = VGroup(Rectangle(width=1.25,height=.28,fill_color=MUTED,fill_opacity=.35,stroke_color=MUTED).move_to([0,-1.98,0]),
                            Line([-.8,-2.15,0],[.8,-2.15,0],color=MUTED))
        schematic = txt("单塔局部受力示意",17,MUTED).to_edge(RIGHT,buff=.55).shift(UP*1.72)
        cables = VGroup(*[Line([0,1.65-i*.25,0],[s*(1.5+i*.8),-1.15,0],color=CYAN,stroke_width=3) for s in (-1,1) for i in range(4)])
        bars_l = VGroup(*[Rectangle(width=.18,height=.65,fill_color=CYAN,fill_opacity=.8,stroke_width=0) for _ in range(4)]).arrange(RIGHT,buff=.1).move_to([-3.4,1.55,0])
        bars_r = bars_l.copy().move_to([3.4,1.55,0])
        self.play(FadeIn(tower), Create(deck), FadeIn(foundation), FadeIn(schematic), LaggedStart(*[Create(c) for c in cables],lag_ratio=.05), FadeIn(bars_l), FadeIn(bars_r), run_time=1.5)
        balanced = txt("两侧索力接近，塔以受压为主",20,CYAN,"BOLD").to_edge(DOWN,buff=.3)
        self.play(FadeIn(balanced))
        loads = VGroup(*[Arrow([x,.1,0],[x,-1.0,0],color=CORAL,buff=0,stroke_width=4) for x in (1.2,2.2,3.2,4.2)])
        taller = VGroup(*[Rectangle(width=.18,height=h,fill_color=CORAL,fill_opacity=.85,stroke_width=0) for h in (.85,1.0,1.15,1.3)]).arrange(RIGHT,buff=.1).move_to(bars_r)
        bent = ParametricFunction(lambda t:[.22*t*t, -1.8+3.9*t,0],t_range=[0,1],color=AMBER,stroke_width=10)
        self.play(LaggedStart(*[GrowArrow(a) for a in loads],lag_ratio=.08), Transform(bars_r,taller), Transform(tower,bent), FadeOut(balanced), run_time=1.6)
        self.finish("偏载先造成索力差，索力差再把弯矩送进塔。", MathTex(r"T_R-T_L\neq0",color=INK).scale(.82))


class TemperatureSupports(MiniLesson):
    def construct(self):
        self.open("10", "桥热胀时，支座为什么要允许它走一点？")
        beam = Rectangle(width=7.5,height=.35,fill_color=CYAN,fill_opacity=.35,stroke_color=CYAN).shift(UP*.45)
        fixed = pin_support(beam.get_bottom()+LEFT*3.2+DOWN*.42)
        roller = VGroup(pin_support(beam.get_bottom()+RIGHT*3.2+DOWN*.42), Circle(.08,color=MUTED,fill_opacity=1).shift(beam.get_bottom()+RIGHT*3.35+DOWN*.52))
        sun = Circle(.35,color=AMBER,fill_color=AMBER,fill_opacity=.8).to_corner(UR,buff=.7).shift(DOWN*.8)
        self.play(FadeIn(beam),FadeIn(fixed),FadeIn(roller),FadeIn(sun))
        move = Arrow(beam.get_right()+DOWN*.55,beam.get_right()+RIGHT*.75+DOWN*.55,color=AMBER,buff=0,stroke_width=5)
        self.play(beam.animate.stretch(1.16,0,about_edge=LEFT),roller.animate.shift(RIGHT*1.2),GrowArrow(move),run_time=1.5)
        free = txt("一端能走：长度变化释放出来",20,CYAN,"BOLD").to_edge(DOWN,buff=.35)
        free_formula = MathTex(r"\Delta L_{free}=\alpha L\Delta T",color=INK).scale(.78).next_to(free,UP,buff=.12)
        self.play(FadeIn(free), Write(free_formula))
        lock = pin_support(beam.get_bottom()+RIGHT*4.4+DOWN*.42,color=CORAL)
        arrows = VGroup(Arrow(beam.get_right()+RIGHT*.6,beam.get_right(),color=CORAL,buff=0),Arrow(beam.get_left()+LEFT*.6,beam.get_left(),color=CORAL,buff=0))
        self.play(FadeOut(roller),FadeIn(lock),FadeIn(arrows),FadeOut(free),FadeOut(free_formula),run_time=1)
        self.finish("理想完全约束时，自由伸长被压缩内力接住。", MathTex(r"N\approx EA\alpha\Delta T",color=INK).scale(.82))


class CantileverBalance(MiniLesson):
    def construct(self):
        self.open("11", "平衡悬臂为什么要成对长？")
        pier = Rectangle(width=.65,height=2.5,fill_color=MUTED,fill_opacity=.25,stroke_color=MUTED).shift(DOWN*.75)
        cap = Rectangle(width=1.3,height=.3,fill_color=INK,fill_opacity=1,stroke_width=0).next_to(pier,UP,buff=0)
        self.play(FadeIn(pier),FadeIn(cap))
        left=[]; right=[]
        for i in range(4):
            l=Rectangle(width=1.0,height=.34,fill_color=CYAN,fill_opacity=.5,stroke_color=CYAN).move_to([-1.15-i,cap.get_y()+.32,0])
            r=l.copy().set_x(1.15+i)
            left.append(l);right.append(r)
            self.play(FadeIn(l,shift=RIGHT*.2),FadeIn(r,shift=LEFT*.2),run_time=.35)
        balance=txt("两边成对：墩顶弯矩互相抵消",20,CYAN,"BOLD").to_edge(DOWN,buff=.3)
        self.play(FadeIn(balance))
        extra=Rectangle(width=1.0,height=.34,fill_color=CORAL,fill_opacity=.8,stroke_color=CORAL).move_to([5.15,cap.get_y()+.32,0])
        moment=CurvedArrow([-.2,.3,0],[.65,.45,0],radius=-.45,color=CORAL,stroke_width=5)
        self.play(FadeIn(extra,shift=LEFT*.2),Create(moment),FadeOut(balance),run_time=1)
        self.finish("多出的不是一块重量，而是重量乘上离墩的距离。",MathTex(r"M_{unb}=\sum P_i x_i",color=INK).scale(.86))


class WindSquare(MiniLesson):
    def construct(self):
        self.open("12", "风速加倍，风力为什么不是加倍？")
        premise=txt("空气密度、迎风面积与阻力系数暂时不变",17,MUTED).to_edge(RIGHT,buff=.5).shift(UP*1.72)
        deck=RoundedRectangle(corner_radius=.12,width=6.8,height=.65,fill_color=INK,fill_opacity=.85,stroke_width=0).shift(DOWN*.2)
        arrow1=Arrow([-5.7,.2,0],[-3.8,.2,0],color=CYAN,stroke_width=7)
        bar1=Rectangle(width=.7,height=.7,fill_color=CORAL,fill_opacity=.75,stroke_width=0).move_to([4.2,1.0,0])
        labels=VGroup(txt("风速 V",20,CYAN,"BOLD").next_to(arrow1,UP),txt("风力 1",20,CORAL,"BOLD").next_to(bar1,UP))
        self.play(FadeIn(deck),GrowArrow(arrow1),FadeIn(bar1),FadeIn(labels),FadeIn(premise))
        arrow2=Arrow([-5.7,.2,0],[-1.9,.2,0],color=AMBER,stroke_width=9)
        bar4=Rectangle(width=.7,height=2.8,fill_color=CORAL,fill_opacity=.8,stroke_width=0).move_to([4.2,-.05,0])
        l2=txt("风速 2V",20,AMBER,"BOLD").move_to(labels[0])
        l4=txt("风力 4",20,CORAL,"BOLD").next_to(bar4,UP)
        self.play(Transform(arrow1,arrow2),Transform(bar1,bar4),FadeTransform(labels[0],l2),FadeTransform(labels[1],l4),run_time=1.5)
        self.finish("速度只加一倍，动压已经乘了四。",MathTex(r"F=\tfrac12\rho C_D A V^2",color=INK).scale(.82))


class Resonance(MiniLesson):
    def construct(self):
        self.open("13", "外力不大，桥为什么仍可能越振越大？")
        pivot=Dot([0,1.55,0],radius=.07,color=INK)
        rope=Line([0,1.55,0],[0,-.15,0],color=INK,stroke_width=4)
        bob=Circle(.22,fill_color=AMBER,fill_opacity=1,stroke_color=INK).move_to([0,-.15,0])
        swing=VGroup(rope,bob)
        push=Arrow([-.95,-.15,0],[-.35,-.15,0],color=CORAL,buff=0,stroke_width=5)
        rhythm=txt("每次都在它回来时推一下",20,CORAL,"BOLD").next_to(swing,RIGHT,buff=.65)
        self.play(FadeIn(pivot),FadeIn(swing),GrowArrow(push),FadeIn(rhythm))
        for angle in (.22,-.44,.44,-.44,.44):
            self.play(swing.animate.rotate(angle,about_point=pivot.get_center()),run_time=.28,rate_func=smooth)
        self.play(FadeOut(VGroup(pivot,swing,push,rhythm)),run_time=.6)
        axes=Axes(x_range=[0,2,0.5],y_range=[0,7,1],x_length=7.8,y_length=3.6,axis_config={"color":MUTED,"include_tip":False}).shift(DOWN*.45)
        curve=axes.plot(lambda r:1/np.sqrt((1-r*r)**2+(2*.08*r)**2),x_range=[0,2],color=CYAN,stroke_width=4)
        labx=MathTex(r"r=f/f_n",color=INK).scale(.7).next_to(axes.x_axis,DOWN)
        laby=txt("放大",18,MUTED).next_to(axes.y_axis,LEFT)
        self.play(FadeIn(axes),FadeIn(labx),FadeIn(laby),Create(curve),run_time=1.5)
        dot=Dot(axes.c2p(.15,1/np.sqrt((1-.15**2)**2+(2*.08*.15)**2)),color=AMBER)
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot,curve),run_time=3,rate_func=linear)
        peak=DashedLine(axes.c2p(1,0),axes.c2p(1,6.3),color=CORAL)
        text=txt("频率接近：每一推都赶上了节奏",20,CORAL,"BOLD").to_edge(RIGHT,buff=.5).shift(UP*1.7)
        self.play(Create(peak),FadeIn(text))
        self.finish("共振看的是节奏是否接近；阻尼决定峰有多高。",MathTex(r"r=\frac{f}{f_n}\approx1",color=INK).scale(.86))


class FEMDiscretization(MiniLesson):
    def construct(self):
        self.open("14", "有限元为什么要把桥拆小？")
        exact=ParametricFunction(lambda t:[8*t-4,-1.4*(1-(2*t-1)**2)+.8,0],t_range=[0,1],color=MUTED,stroke_width=3)
        self.play(Create(exact))
        label=txt("连续结构",20,MUTED).next_to(exact,UP)
        self.play(FadeIn(label))
        meshes=[]
        for n,color in [(2,CORAL),(4,AMBER),(12,CYAN)]:
            pts=[]
            for i in range(n+1):
                t=i/n;pts.append([8*t-4,-1.4*(1-(2*t-1)**2)+.8,0])
            mesh=VMobject(color=color,stroke_width=6 if n<12 else 4).set_points_as_corners(pts)
            nodes=VGroup(*[Dot(p,radius=.07 if n<12 else .04,color=color) for p in pts])
            meshes.append(VGroup(mesh,nodes))
        count=txt("2 个单元",20,CORAL,"BOLD").to_edge(RIGHT,buff=.7).shift(UP*1.7)
        self.play(FadeIn(meshes[0]),FadeIn(count))
        count2=txt("4 个单元",20,AMBER,"BOLD").move_to(count)
        count3=txt("12 个单元：更接近，但仍要校核",18,CYAN,"BOLD").to_edge(RIGHT,buff=.45).shift(UP*1.7)
        self.play(ReplacementTransform(meshes[0],meshes[1]),FadeTransform(count,count2),run_time=1)
        self.play(ReplacementTransform(meshes[1],meshes[2]),FadeTransform(count2,count3),run_time=1.2)
        symbols=txt("K：刚度　u：节点位移　F：节点力",17,MUTED).to_edge(RIGHT,buff=.55).shift(DOWN*1.65)
        self.play(FadeIn(symbols))
        self.finish("网格是把连续问题变成有限个未知量；更多不自动等于更对。",MathTex(r"K\,u=F",color=INK).scale(.92))
