import os
import math
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
W, H = 840, 360
FPS = 15
TOTAL_FRAMES = 60

# Palette (VS Code / GitHub Dark Modern)
BG_COLOR = (13, 17, 23)        # #0d1117
TITLEBAR_BG = (22, 27, 34)     # #161b22
BORDER_COLOR = (48, 54, 61)    # #30363d
LINE_NUM_COLOR = (110, 118, 129) # #6e7681

# Font setup
font_mono = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 15)
font_mono_bold = ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf', 15)
font_ui = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 12)

# Full code lines to display and animate
CODE_SCRIPT = [
    [("class ", "#ff7b72"), ("SilasVista", "#79c0ff"), ("(AutonomousAgent):", "#e6edf3")],
    [("    \"\"\"AI Engineer & Agent Architecture\"\"\"", "#8b949e")],
    [("    def ", "#ff7b72"), ("__init__", "#d2a8ff"), ("(self):", "#e6edf3")],
    [("        self.role = ", "#e6edf3"), ("\"AI / Agents / RAG\"", "#a5d6ff")],
    [("        self.focus = [", "#e6edf3"), ("\"Tool Use\"", "#a5d6ff"), (", ", "#e6edf3"), ("\"Memory\"", "#a5d6ff"), (", ", "#e6edf3"), ("\"Orchestration\"", "#a5d6ff"), ("]", "#e6edf3")],
    [("        self.products = [", "#e6edf3"), ("\"Windup\"", "#a5d6ff"), (", ", "#e6edf3"), ("\"Verso\"", "#a5d6ff"), (", ", "#e6edf3"), ("\"UniGate\"", "#a5d6ff"), ("]", "#e6edf3")],
    [("    async def ", "#ff7b72"), ("run_workflow", "#d2a8ff"), ("(self, query):", "#e6edf3")],
    [("        context = await self.rag_pipeline.retrieve(query)", "#7ee787")],
    [("        return await self.orchestrate(context)", "#7ee787")],
]

# Flatten characters for typing animation
all_chars = []
for row_idx, tokens in enumerate(CODE_SCRIPT):
    for text, color in tokens:
        for char in text:
            all_chars.append((row_idx, char, color))

total_chars = len(all_chars)

frames = []

for frame_idx in range(TOTAL_FRAMES):
    # Create image
    img = Image.new('RGB', (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 1. Window Outline and Border
    draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=10, outline=BORDER_COLOR, width=1)

    # 2. Window Header (macOS / Modern Editor style)
    draw.rounded_rectangle([0, 0, W - 1, 38], radius=10, fill=TITLEBAR_BG)
    # Square bottom of titlebar
    draw.rectangle([0, 25, W - 1, 38], fill=TITLEBAR_BG)
    draw.line([0, 38, W - 1, 38], fill=BORDER_COLOR, width=1)

    # Window traffic light buttons
    draw.ellipse([16, 13, 28, 25], fill=(255, 95, 86))   # Red
    draw.ellipse([36, 13, 48, 25], fill=(255, 189, 46))  # Yellow
    draw.ellipse([56, 13, 68, 25], fill=(39, 201, 63))   # Green

    # Window Title
    title = "silas_agent.py — Visual Studio Code"
    bbox = draw.textbbox((0, 0), title, font=font_ui)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 12), title, fill=(139, 148, 158), font=font_ui)

    # 3. Sidebar status indicator / breadcrumbs
    tab_text = "silas_agent.py"
    draw.rectangle([100, 44, 230, 68], fill=(22, 27, 34))
    draw.line([100, 44, 230, 44], fill=(0, 106, 255), width=2) # active tab blue line
    draw.text((115, 50), tab_text, fill=(230, 237, 243), font=font_ui)

    # 4. Typing Progress calculation
    # First 42 frames: typing
    # Last 18 frames: pause and cursor blink
    if frame_idx < 42:
        progress = frame_idx / 42.0
        active_char_count = int(progress * total_chars)
    else:
        active_char_count = total_chars

    # 5. Render visible code
    start_y = 85
    line_height = 24
    left_x = 75

    # Draw line numbers
    for i in range(len(CODE_SCRIPT)):
        ln_str = str(i + 1).rjust(2)
        draw.text((32, start_y + i * line_height), ln_str, fill=LINE_NUM_COLOR, font=font_mono)

    # Render typed text
    cur_x = left_x
    cur_row = 0
    chars_drawn = 0

    cursor_pos = (left_x, start_y)

    for r_idx, ch, col in all_chars:
        if chars_drawn >= active_char_count:
            break
        if r_idx != cur_row:
            cur_row = r_idx
            cur_x = left_x

        y = start_y + cur_row * line_height
        draw.text((cur_x, y), ch, fill=col, font=font_mono)
        ch_w = draw.textlength(ch, font=font_mono)
        cur_x += ch_w
        cursor_pos = (cur_x, y)
        chars_drawn += 1

    # 6. Cursor blinking
    show_cursor = (frame_idx % 8) < 4
    if show_cursor:
        cx, cy = cursor_pos
        draw.rectangle([cx + 1, cy, cx + 9, cy + 18], fill=(0, 217, 255))

    # 7. Subtle bottom status bar
    draw.rectangle([0, H - 24, W - 1, H - 1], fill=(22, 27, 34))
    draw.line([0, H - 24, W - 1, H - 24], fill=BORDER_COLOR, width=1)
    status_text = "Python 3.12  •  UTF-8  •  Spaces: 4  •  Silas Vista / Agent Core"
    draw.text((20, H - 19), status_text, fill=(110, 118, 129), font=font_ui)

    # Pulse / status dot in status bar
    dot_color = (0, 217, 255) if (frame_idx % 10 < 5) else (39, 201, 63)
    draw.ellipse([W - 140, H - 16, W - 132, H - 8], fill=dot_color)
    draw.text((W - 124, H - 19), "Agent Ready", fill=(139, 148, 158), font=font_ui)

    frames.append(img)

# Save animated GIF
output_path = os.path.join("assets", "silas_coding.gif")
frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=True
)

file_size_kb = os.path.getsize(output_path) / 1024
print(f"Generated {output_path} successfully! Size: {file_size_kb:.2f} KB, Frames: {len(frames)}")
