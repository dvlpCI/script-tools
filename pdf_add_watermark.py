#!/usr/bin/env python3
# 给 pdf 加水印
# $ cd /Users/lichaoqian/Documents/plans && python3 pdf_add_watermark.py 2>&1 | tail -3
from PIL import Image, ImageDraw, ImageFont
import os
import fitz  # PyMuPDF

def create_rotated_watermark_image(text, size=(200, 200)):
    """Create a watermark image with rotated text"""
    # Create transparent image
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to use system font
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 30)
    except:
        font = ImageFont.load_default()
    
    # Draw text in center
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Create a larger image to hold rotated text
    rot_img = Image.new('RGBA', (text_width + 40, text_height + 40), (255, 255, 255, 0))
    rot_draw = ImageDraw.Draw(rot_img)
    rot_draw.text((20, 20), text, fill=(210, 210, 210, 40), font=font)
    
    # Rotate 45 degrees
    rot_img = rot_img.rotate(45, expand=True)
    
    return rot_img

def add_watermark(input_pdf, output_pdf, watermark_text):
    """Add watermark to each page of PDF"""
    # Create watermark image
    watermark_img = create_rotated_watermark_image(watermark_text)
    
    # Save to temp file
    temp_img = '/tmp/watermark.png'
    watermark_img.save(temp_img)
    
    # Open PDF
    doc = fitz.open(input_pdf)
    
    for page_num, page in enumerate(doc):
        width = page.rect.width
        height = page.rect.height
        
        # Calculate positions for 5x10 grid
        x_spacing = width / 5
        y_spacing = height / 10
        
        for row in range(10):
            for col in range(5):
                x = col * x_spacing + x_spacing/2 - 50
                y = row * y_spacing + y_spacing/2 - 50
                
                # Load pixmap from file
                pix = fitz.Pixmap(temp_img)
                page.insert_image(fitz.Rect(x, y, x + pix.width, y + pix.height), pixmap=pix)
    
    doc.save(output_pdf)
    print(f"Watermarked {len(doc)} pages")
    
    # Clean up
    os.remove(temp_img)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='给 PDF 添加水印',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''示例:
  python3 pdf_add_watermark.py -i input.pdf -t "水印文字"
  python3 pdf_add_watermark.py -i input.pdf -o output.pdf -t "水印文字"
  python3 pdf_add_watermark.py --input=input.pdf --text="水印文字"'''
    )
    parser.add_argument('--input', '-i', required=True, help='输入 PDF 文件路径')
    parser.add_argument('--output', '-o', help='输出 PDF 文件路径（默认：输入文件名+加水印）')
    parser.add_argument('--text', '-t', required=True, help='水印文字')
    
    args = parser.parse_args()
    
    if not args.output:
        base, ext = os.path.splitext(args.input)
        args.output = f"{base}_水印{ext}"
    
    add_watermark(args.input, args.output, args.text)
    print(f"Watermarked PDF created: {args.output}")
