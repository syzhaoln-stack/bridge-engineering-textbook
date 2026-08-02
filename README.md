# 我所理解的桥梁工程

从力学出发，重新理解桥梁。教材以文字为主，配合参数化可视化、三维模型、有限元实验、Manim 动画和判断闪卡。

在线阅读：<https://syzhaoln-stack.github.io/bridge-engineering-textbook/>

## 目录

- `source/`：Quarto 源码、交互程序、图像与动画源文件。
- `docs/`：已经构建好的网页版本，也是 GitHub Pages 的发布目录。

## 本地构建

安装 Quarto 后，在仓库根目录运行：

```powershell
quarto render source --to html
```

构建结果写入 `docs/`。

本仓库不包含课堂原始录音、完整转写、过程审核包和内部覆盖率台账。
