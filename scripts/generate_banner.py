from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT = 1400, 750
AVATAR_SIZE = 160

# Solid RGB canvas - dark midnight navy (#070e18)
canvas = Image.new("RGB", (WIDTH, HEIGHT), (7, 14, 24))
draw = ImageDraw.Draw(canvas)

# Radial navy lighting glow at top center
for r in range(WIDTH, 0, -10):
    factor = 1.0 - (r / WIDTH)
    # subtle blend towards (14, 28, 48)
    r_val = int(7 + 10 * factor)
    g_val = int(14 + 18 * factor)
    b_val = int(24 + 30 * factor)
    bbox = [700 - r, 200 - int(r * 0.5), 700 + r, 200 + int(r * 0.5)]
    draw.ellipse(bbox, fill=(r_val, g_val, b_val))

# Subtle vertical grid lines
for x in range(0, WIDTH, 60):
    draw.line([(x, 0), (x, HEIGHT)], fill=(18, 32, 52), width=1)

# Load fonts
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 34)
    font_sub = ImageFont.truetype("arial.ttf", 15)
    font_code = ImageFont.truetype("consola.ttf", 15)
    font_badge = ImageFont.truetype("arialbd.ttf", 13)
    font_status = ImageFont.truetype("arialbd.ttf", 12)
    font_btn = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font_bold = font_sub = font_code = font_badge = font_status = font_btn = ImageFont.load_default()

# Exact face crops for each person
advisors = [
    {"name": "Scott Galloway", "file": "assets/avatars/galloway.jpg", "crop": (0.05, 0.01, 0.95, 0.36)},
    {"name": "Robert Greene", "file": "assets/avatars/greene.jpg", "crop": (0.12, 0.06, 0.88, 0.52)},
    {"name": "Andrew Huberman", "file": "assets/avatars/huberman.jpg", "crop": (0.10, 0.03, 0.90, 0.65)},
    {"name": "Sahar Yousef", "file": "assets/avatars/yousef.jpg", "crop": (0.05, 0.02, 0.95, 0.92)},
    {"name": "Adam Grant", "file": "assets/avatars/grant.jpg", "crop": (0.15, 0.05, 0.85, 0.44)},
    {"name": "Nikolay Kukushkin", "file": "assets/avatars/kukushkin.jpg", "crop": (0.10, 0.08, 0.90, 0.58)},
]

# Arc geometry for 6 avatars - sitting along the curve
n = len(advisors)
arc_coords = []
for i in range(n):
    t = -1.0 + 2.0 * i / (n - 1)
    x = int(700 + t * 510)
    y = int(225 - 45 * (1.0 - t ** 2))
    arc_coords.append((x, y))

def make_circle_avatar(img_path, crop_box, size):
    try:
        raw = Image.open(img_path).convert("RGB")
        w, h = raw.size
        left = int(crop_box[0] * w)
        top = int(crop_box[1] * h)
        right = int(crop_box[2] * w)
        bottom = int(crop_box[3] * h)
        cropped = raw.crop((left, top, right, bottom))
        
        cw, ch = cropped.size
        min_side = min(cw, ch)
        cropped = cropped.crop(((cw - min_side) // 2, (ch - min_side) // 2, (cw + min_side) // 2, (ch + min_side) // 2))
        cropped = cropped.resize((size, size), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (size, size), 0)
        draw_m = ImageDraw.Draw(mask)
        draw_m.ellipse((0, 0, size - 1, size - 1), fill=255)
        
        avatar = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        avatar.paste(cropped, (0, 0), mask)
        
        border_draw = ImageDraw.Draw(avatar)
        border_draw.ellipse((0, 0, size - 1, size - 1), outline=(56, 189, 248, 160), width=3)
        return avatar
    except Exception as e:
        print(f"Error making avatar {img_path}: {e}")
        return None

# Draw avatars and badges
for (x, y), adv in zip(arc_coords, advisors):
    av = make_circle_avatar(adv["file"], adv["crop"], AVATAR_SIZE)
    if av:
        # Rim glow
        glow_size = AVATAR_SIZE + 20
        glow = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse((0, 0, glow_size - 1, glow_size - 1), fill=(56, 189, 248, 30))
        glow = glow.filter(ImageFilter.GaussianBlur(6))
        canvas.paste(glow, (x - glow_size // 2, y - glow_size // 2), glow)
        
        canvas.paste(av, (x - AVATAR_SIZE // 2, y - AVATAR_SIZE // 2), av)
        
    # Name pill badge below avatar
    badge_text = adv["name"]
    bbox = font_badge.getbbox(badge_text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    bx = x - tw // 2 - 14
    by = y + AVATAR_SIZE // 2 + 10
    bw = tw + 28
    bh = th + 12
    
    # Dark pill badge with subtle border
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2, fill=(10, 19, 32), outline=(45, 65, 95), width=1)
    draw.text((bx + 14, by + 5), badge_text, font=font_badge, fill=(226, 232, 240))

# Curved Council Desk (foreground ellipse)
table_box = [-220, 370, 1620, 1220]
draw.ellipse(table_box, fill=(8, 17, 30), outline=(56, 189, 248), width=2)

# Subtle inner highlight arc
inner_box = [-200, 380, 1600, 1200]
draw.ellipse(inner_box, outline=(25, 45, 75), width=1)

# Center console content
center_x = 700

# 1. Status: • THE ROOM IS OPEN
status_text = "THE ROOM IS OPEN"
sb = font_status.getbbox(status_text)
stw = sb[2] - sb[0]
sy = 445
# Glowing cyan dot
draw.ellipse([center_x - stw // 2 - 16, sy + 3, center_x - stw // 2 - 8, sy + 11], fill=(56, 189, 248))
draw.text((center_x - stw // 2, sy), status_text, font=font_status, fill=(56, 189, 248))

# 2. Headline: Bring a freeze to the Rewire Room
head_text = "Bring a freeze to the Rewire Room"
hb = font_bold.getbbox(head_text)
htw = hb[2] - hb[0]
draw.text((center_x - htw // 2, 480), head_text, font=font_bold, fill=(255, 255, 255))

# 3. Subtitle
sub_text = "In Claude Code, type the line below with what happened. The council argues it out live."
subb = font_sub.getbbox(sub_text)
sttw = subb[2] - subb[0]
draw.text((center_x - sttw // 2, 532), sub_text, font=font_sub, fill=(148, 163, 184))

# 4. Command Box: /rewire debrief I stayed quiet in class ...
cmd_text = "/rewire debrief I stayed quiet in class ..."
cb = font_code.getbbox(cmd_text)
cw = cb[2] - cb[0]
ch = cb[3] - cb[1]
cmd_box = [center_x - cw // 2 - 24, 572, center_x + cw // 2 + 24, 572 + ch + 18]
draw.rounded_rectangle(cmd_box, radius=18, fill=(3, 7, 14), outline=(40, 60, 90), width=1)
draw.text((center_x - cw // 2, 581), cmd_text, font=font_code, fill=(56, 189, 248))

# 5. Buttons (translucent dark pills with clean borders)
btn1_text = "What to debrief"
btn2_text = "Watch a past council"
b1 = font_btn.getbbox(btn1_text)
b2 = font_btn.getbbox(btn2_text)
w1 = b1[2] - b1[0] + 34
w2 = b2[2] - b2[0] + 34
gap = 14
total_btn_w = w1 + w2 + gap
start_btn_x = center_x - total_btn_w // 2

# Button 1
draw.rounded_rectangle([start_btn_x, 632, start_btn_x + w1, 668], radius=18, fill=(15, 26, 42), outline=(45, 68, 100), width=1)
draw.text((start_btn_x + 17, 642), btn1_text, font=font_btn, fill=(203, 213, 225))

# Button 2
draw.rounded_rectangle([start_btn_x + w1 + gap, 632, start_btn_x + total_btn_w, 668], radius=18, fill=(15, 26, 42), outline=(45, 68, 100), width=1)
draw.text((start_btn_x + w1 + gap + 17, 642), btn2_text, font=font_btn, fill=(203, 213, 225))

# Save output
out_path = Path("assets/rewire-room-hero-real.png")
canvas.save(out_path, "PNG")
print(f"Generated {out_path} ({out_path.stat().st_size} bytes)")
