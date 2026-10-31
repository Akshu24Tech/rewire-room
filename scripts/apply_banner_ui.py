from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = Path("C:/Users/techl/.gemini/antigravity/brain/cc5cb8ef-f618-4b3e-ad98-24a3e4e1d8e3/council_of_advisors_pixar_3d_1793456095525.jpg")
OUT = Path("e:/Ghost OS/projects/rewire-room/assets/rewire-room-hero-pixar.png")

im = Image.open(SRC).convert("RGBA")
W, H = im.size
draw = ImageDraw.Draw(im)

# Load fonts
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 26)
    font_sub = ImageFont.truetype("arial.ttf", 13)
    font_code = ImageFont.truetype("consola.ttf", 13)
    font_badge = ImageFont.truetype("arialbd.ttf", 11)
    font_status = ImageFont.truetype("arialbd.ttf", 11)
    font_btn = ImageFont.truetype("arial.ttf", 12)
except Exception:
    font_bold = font_sub = font_code = font_badge = font_status = font_btn = ImageFont.load_default()

# 6 Advisors x-centers and badge positions
advisors = [
    {"name": "Scott Galloway", "x": 150, "y": 575},
    {"name": "Robert Greene", "x": 380, "y": 555},
    {"name": "Andrew Huberman", "x": 595, "y": 548},
    {"name": "Sahar Yousef", "x": 800, "y": 548},
    {"name": "Adam Grant", "x": 1010, "y": 555},
    {"name": "Nikolay Kukushkin", "x": 1225, "y": 575},
]

# Draw name badges on the table rim under each person
for adv in advisors:
    badge_text = adv["name"]
    bbox = font_badge.getbbox(badge_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx = adv["x"] - tw // 2 - 12
    by = adv["y"]
    bw = tw + 24
    bh = th + 10
    
    # Translucent dark pill badge matching Roast Room
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2, fill=(10, 18, 30, 230), outline=(255, 255, 255, 35), width=1)
    draw.text((bx + 12, by + 4), badge_text, font=font_badge, fill=(203, 213, 225, 255))

# Center Console Content
cx = W // 2

# 1. Status: • THE ROOM IS OPEN
status_text = "THE ROOM IS OPEN"
sb = font_status.getbbox(status_text)
stw = sb[2] - sb[0]
sy = 590
# Cyan dot
draw.ellipse([cx - stw // 2 - 14, sy + 3, cx - stw // 2 - 7, sy + 10], fill=(56, 189, 248, 255))
draw.text((cx - stw // 2, sy), status_text, font=font_status, fill=(56, 189, 248, 255))

# 2. Headline: Bring a freeze to the Rewire Room
head_text = "Bring a freeze to the Rewire Room"
hb = font_bold.getbbox(head_text)
htw = hb[2] - hb[0]
draw.text((cx - htw // 2, 612), head_text, font=font_bold, fill=(255, 255, 255, 255))

# 3. Subtitle: In Claude Code, type the line below with what happened. The council argues it out live.
sub_text = "In Claude Code, type the line below with what happened. The council argues it out live."
subb = font_sub.getbbox(sub_text)
sttw = subb[2] - subb[0]
draw.text((cx - sttw // 2, 648), sub_text, font=font_sub, fill=(148, 163, 184, 255))

# 4. Command Box: /rewire debrief I stayed quiet in class ...
cmd_text = "/rewire debrief I stayed quiet in class ..."
cb = font_code.getbbox(cmd_text)
cw = cb[2] - cb[0]
ch = cb[3] - cb[1]
cmd_box = [cx - cw // 2 - 20, 674, cx + cw // 2 + 20, 674 + ch + 14]
draw.rounded_rectangle(cmd_box, radius=14, fill=(3, 7, 15, 240), outline=(255, 255, 255, 30), width=1)
draw.text((cx - cw // 2, 680), cmd_text, font=font_code, fill=(56, 189, 248, 255))

# 5. Buttons: [ What to debrief ] [ Watch a past council ]
btn1_text = "What to debrief"
btn2_text = "Watch a past council"
b1 = font_btn.getbbox(btn1_text)
b2 = font_btn.getbbox(btn2_text)
w1 = b1[2] - b1[0] + 28
w2 = b2[2] - b2[0] + 28
gap = 12
total_btn_w = w1 + w2 + gap
start_btn_x = cx - total_btn_w // 2

# Button 1
draw.rounded_rectangle([start_btn_x, 715, start_btn_x + w1, 745], radius=15, fill=(15, 25, 40, 200), outline=(255, 255, 255, 35), width=1)
draw.text((start_btn_x + 14, 722), btn1_text, font=font_btn, fill=(203, 213, 225, 255))

# Button 2
draw.rounded_rectangle([start_btn_x + w1 + gap, 715, start_btn_x + total_btn_w, 745], radius=15, fill=(15, 25, 40, 200), outline=(255, 255, 255, 35), width=1)
draw.text((start_btn_x + w1 + gap + 14, 722), btn2_text, font=font_btn, fill=(203, 213, 225, 255))

# Save
im.convert("RGB").save(OUT, "PNG")
print(f"Generated {OUT} ({OUT.stat().st_size} bytes)")

