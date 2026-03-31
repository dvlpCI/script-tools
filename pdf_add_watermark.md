# PDF 水印脚本使用教程

## 脚本功能

`pdf_add_watermark.py` 用于给 PDF 文件添加水印，主要特点：

- 生成带 45 度旋转的半透明文字水印
- 将水印以 5×10 网格形式平铺到每一页
- 水印文字颜色为浅灰色 (#D2D2D2)，透明度 40%
- 使用 PingFang 系统字体（macOS 默认）

## 依赖安装

```bash
pip install PyMuPDF Pillow
```

## 使用方式

### 基本用法

```bash
# 完整参数（具名参数）
python3 pdf_add_watermark.py --input input.pdf --output output.pdf --text "水印文字"

# 简短参数
python3 pdf_add_watermark.py -i input.pdf -o output.pdf -t "水印文字"

# 省略输出路径（自动生成：输入文件名_水印.pdf）
python3 pdf_add_watermark.py -i input.pdf -t "水印文字"
```

### 查看帮助

```bash
python3 pdf_add_watermark.py -h
```

输出：

```
usage: pdf_add_watermark.py [-h] --input INPUT [-o OUTPUT] --text TEXT

给 PDF 添加水印

选项:
  --input INPUT, -i INPUT  输入 PDF 文件路径
  --output OUTPUT, -o OUTPUT  输出 PDF 文件路径（默认：输入文件名+加水印）
  --text TEXT, -t TEXT    水印文字

示例:
  python3 pdf_add_watermark.py -i input.pdf -t "水印文字"
  python3 pdf_add_watermark.py -i input.pdf -o output.pdf -t "水印文字"
  python3 pdf_add_watermark.py --input=input.pdf --text="水印文字"
```

## 参数说明

| 参数 | 简短形式 | 必填 | 说明 | 示例 |
|------|----------|------|------|------|
| `--input` | `-i` | 是 | 输入 PDF 文件路径 | `/Users/xxx/input.pdf` |
| `--output` | `-o` | 否 | 输出 PDF 文件路径，默认自动生成 | `/Users/xxx/output.pdf` |
| `--text` | `-t` | 是 | 水印文字内容 | `Li Chaoqian` |

## 自定义水印样式

修改脚本中的相关参数：

```python
# 水印字体大小（第 17 行）
font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 30)  # 30 为字号

# 水印颜色和透明度（第 29 行）
rot_draw.text((20, 20), text, fill=(210, 210, 210, 40), font=font)
# fill 参数: (R, G, B, A)，A 越小越透明（0=完全透明，255=完全不透明）

# 旋转角度（第 32 行）
rot_img = rot_img.rotate(45, expand=True)  # 45 为旋转角度

# 网格密度（第 53-54 行）
x_spacing = width / 5   # 每行 5 个水印
y_spacing = height / 10 # 每列 10 个水印
```

## 注意事项

1. 确保输入 PDF 路径存在且可读
2. 确保输出目录有写入权限
3. 水印图片临时保存在 `/tmp/watermark.png`，处理完成后自动删除
4. 脚本会自动处理多页 PDF，每一页都会添加水印
