# 教材 Manim 动画源码

## 环境

- Python 3.10–3.12
- Manim Community 0.18.1
- FFmpeg
- LaTeX（公式渲染）
- Windows 中文字体 `Microsoft YaHei`；其他系统可在源码顶部替换 `FONT`

## 渲染

在本目录运行：

```powershell
pip install -r requirements.txt
manim -qm bridge_math_basics.py ConcreteGuaranteeRate ConcreteToDesignValue ReliabilityFromOneToJoint InfluenceLineMovingLoad
manim -qm bridge_mechanics_series.py ScaleLaw ForcePath BeamDepth ArchPressureLine CableSag CableStayedBalance TemperatureSupports CantileverBalance WindSquare Resonance FEMDiscretization
```

`-qm` 输出 1280×720、30 fps。若只想快速预览，把它改成 `-ql`。

`scenes.md` 与 `mechanics_scenes.md` 记录问题、镜头、公式与教学边界。代码使用教学示意参数，不代替规范验算。
