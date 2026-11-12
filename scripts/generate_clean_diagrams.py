import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Temp")

DEST = Path("assets")
DEST.mkdir(parents=True, exist_ok=True)

# Clean Minimalist White Palette
BG_WHITE = "#FFFFFF"
CARD_WHITE = "#F8FAFC"
CARD_BORDER = "#E2E8F0"
CARD_BORDER_ACTIVE = "#38BDF8"

TEXT_PRIMARY = "#0F172A"      # Slate 900
TEXT_SECONDARY = "#475569"    # Slate 600
TEXT_MUTED = "#94A3B8"        # Slate 400

BLUE_ACCENT = "#0284C7"       # Sky 600
BLUE_BG = "#F0F9FF"           # Sky 50
PURPLE_ACCENT = "#7C3AED"     # Violet 600
PURPLE_BG = "#F5F3FF"         # Violet 50
GREEN_ACCENT = "#059669"      # Emerald 600
GREEN_BG = "#ECFDF5"          # Emerald 50
AMBER_ACCENT = "#D97706"      # Amber 600
AMBER_BG = "#FFFBEB"          # Amber 50

def create_canvas(title, subtitle):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=140)
    fig.patch.set_facecolor(BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 900)
    ax.axis("off")
    
    # Clean, modern header
    ax.text(90, 840, title, color=TEXT_PRIMARY, fontsize=24, fontweight="bold", family="sans-serif")
    ax.text(90, 812, subtitle, color=TEXT_SECONDARY, fontsize=12, fontweight="medium", family="sans-serif")
    ax.plot([90, 1510], [792, 792], color="#E2E8F0", linewidth=1.2)
    return fig, ax

def draw_pill(ax, x, y, w, h, bg_color, border_color):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=12",
        edgecolor=border_color,
        facecolor=bg_color,
        linewidth=1.2
    )
    ax.add_patch(box)

def draw_arrow(ax, x1, y1, x2, y2, color=BLUE_ACCENT):
    ax.annotate(
        "",
        xy=(x2, y2), xycoords="data",
        xytext=(x1, y1), textcoords="data",
        arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.7", color=color, lw=2, shrinkA=6, shrinkB=6)
    )

# ==============================================================================
# DIAGRAM 1: MINIMALIST ARCHITECTURE & FILE MAP
# ==============================================================================
def make_diagram_1():
    fig, ax = create_canvas(
        "Rewire Room: Architecture & Codebase Map",
        "Clean overview of the five core layers and files"
    )
    
    layers = [
        ("1. Skill Protocol", ".claude/skills/rewire/", BLUE_BG, BLUE_ACCENT, [
            "SKILL.md  (Chair rules & routing)",
            "roster.json  (7 council seats)",
            "safety.md  (Clinical screen)",
            "seats.md  (Tensions & weights)",
            "round-prompts.md  (Prompts)",
            "scoring.md  (Rep formulas)"
        ]),
        ("2. Sub-Agents", ".claude/agents/", PURPLE_BG, PURPLE_ACCENT, [
            "seat-kukushkin.md",
            "seat-huberman.md",
            "seat-yousef.md",
            "seat-grant.md",
            "seat-greene.md",
            "seat-galloway.md",
            "seat-evidence.md"
        ]),
        ("3. Verified Brains", "skills/.../brains/", GREEN_BG, GREEN_ACCENT, [
            "6 Persona Brains:",
            "  • _hot.md  (Worldview)",
            "  • frameworks.md  [Sxxx]",
            "  • positions.md",
            "1 Research Brain:",
            "  • claims.md  (Grades)",
            "  • studies.md  (Meta-RCTs)"
        ]),
        ("4. Scripts & Gates", "scripts/ & tests/", AMBER_BG, AMBER_ACCENT, [
            "check_quotes.py  (0 fails)",
            "ledger.py  (CLI tracking)",
            "textnorm.py  (Loose match)",
            "fetch_sources.py  (Corpus)",
            "builder.py  (Synthesis)",
            "tests/  (22 tests pass)"
        ]),
        ("5. Local Data", "sessions/ & ledger/", CARD_WHITE, TEXT_PRIMARY, [
            "sessions/YYYY-MM-DD-slug/",
            "  • brief.md",
            "  • round-1.md",
            "  • round-2.md",
            "  • evidence.md",
            "  • debrief.md",
            "ledger/reps.jsonl"
        ])
    ]
    
    card_w = 260
    card_h = 640
    start_x = 90
    gap = 25
    
    for i, (title, sub, bg, border, items) in enumerate(layers):
        x = start_x + i * (card_w + gap)
        y = 110
        draw_pill(ax, x, y, card_w, card_h, bg, border)
        
        # Header
        ax.text(x + 18, y + card_h - 38, title, color=border, fontsize=13, fontweight="bold", family="sans-serif")
        ax.text(x + 18, y + card_h - 60, sub, color=TEXT_SECONDARY, fontsize=9.5, family="sans-serif")
        ax.plot([x + 18, x + card_w - 18], [y + card_h - 75, y + card_h - 75], color=border, linewidth=1, alpha=0.3)
        
        # Items
        for j, item in enumerate(items):
            iy = y + card_h - 110 - j * 42
            ax.text(x + 18, iy, item, color=TEXT_PRIMARY, fontsize=9.5, fontweight="medium", family="sans-serif")
            
        # Arrows between cards
        if i < len(layers) - 1:
            draw_arrow(ax, x + card_w, 430, x + card_w + gap, 430, color=BLUE_ACCENT)
            
    plt.tight_layout()
    out = DEST / "diagram-1-full-architecture.png"
    plt.savefig(out, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated {out}")

# ==============================================================================
# DIAGRAM 2: MINIMALIST PHASE 1 DEBRIEF FLOWCHART
# ==============================================================================
def make_diagram_2():
    fig, ax = create_canvas(
        "Phase 1: Debrief & Evidence Audit Flowchart",
        "Simple 6-step loop: from raw moment to verified rep"
    )
    
    # 6 Steps in a clean 2x3 Grid
    steps = [
        ("Step 1: Intake & Safety", "references/safety.md", BLUE_BG, BLUE_ACCENT, [
            "• User shares real moment",
            "• Safety screen checks clinical flags",
            "• Safe social nerves: proceed"
        ]),
        ("Step 2: The Brief", "brief.md in sessions/", BLUE_BG, BLUE_ACCENT, [
            "• Where, who, and stakes",
            "• What wanted vs what actually did",
            "• Discomfort score (0 to 10)"
        ]),
        ("Step 3: Council Seating", "roster.json & seats.md", PURPLE_BG, PURPLE_ACCENT, [
            "• Seated: 3-4 ready experts",
            "• Weighted: 3 (broke), 2 (contributed)",
            "• Seated: Evidence Seat (research)"
        ]),
        ("Step 4: Parallel Diagnosis", "round-1.md (3 Cards)", PURPLE_BG, PURPLE_ACCENT, [
            "• Each seat diagnoses its layer",
            "• Verbatim quotes cited with [Sxxx]",
            "• Chair extracts cruxes & claims"
        ]),
        ("Step 5: Cross-Exam & Audit", "round-2.md + evidence.md", GREEN_BG, GREEN_ACCENT, [
            "• Experts debate cruxes & shift votes",
            "• Evidence seat audits claims",
            "• Grades: STRONG to UNSUPPORTED"
        ]),
        ("Step 6: Debrief & Ledger", "debrief.md & ledger.py", AMBER_BG, AMBER_ACCENT, [
            "• Primary layer selected",
            "• 1 observable rep + If-then plan",
            "• Logged to ledger + quote check (0 fails)"
        ])
    ]
    
    box_w = 420
    box_h = 240
    
    # Row 1 (Steps 1, 2, 3)
    row1_y = 480
    xs = [100, 590, 1080]
    for i in range(3):
        x = xs[i]
        title, sub, bg, col, lines = steps[i]
        draw_pill(ax, x, row1_y, box_w, box_h, bg, col)
        ax.text(x + 22, row1_y + box_h - 38, title, color=col, fontsize=14, fontweight="bold", family="sans-serif")
        ax.text(x + 22, row1_y + box_h - 60, sub, color=TEXT_SECONDARY, fontsize=10, family="sans-serif")
        ax.plot([x + 22, x + box_w - 22], [row1_y + box_h - 75, row1_y + box_h - 75], color=col, linewidth=1, alpha=0.3)
        for j, line in enumerate(lines):
            ax.text(x + 22, row1_y + box_h - 110 - j * 32, line, color=TEXT_PRIMARY, fontsize=10.5, family="sans-serif")
        if i < 2:
            draw_arrow(ax, x + box_w, row1_y + box_h // 2, xs[i+1], row1_y + box_h // 2, color=BLUE_ACCENT)

    # Down arrow from Step 3 to Step 4
    draw_arrow(ax, 1290, row1_y, 1290, 420, color=PURPLE_ACCENT)

    # Row 2 (Steps 6, 5, 4) in reverse order for smooth loop
    row2_y = 150
    xs_rev = [1080, 590, 100]
    rev_steps = [steps[3], steps[4], steps[5]]
    
    for i in range(3):
        x = xs_rev[i]
        title, sub, bg, col, lines = rev_steps[i]
        draw_pill(ax, x, row2_y, box_w, box_h, bg, col)
        ax.text(x + 22, row2_y + box_h - 38, title, color=col, fontsize=14, fontweight="bold", family="sans-serif")
        ax.text(x + 22, row2_y + box_h - 60, sub, color=TEXT_SECONDARY, fontsize=10, family="sans-serif")
        ax.plot([x + 22, x + box_w - 22], [row2_y + box_h - 75, row2_y + box_h - 75], color=col, linewidth=1, alpha=0.3)
        for j, line in enumerate(lines):
            ax.text(x + 22, row2_y + box_h - 110 - j * 32, line, color=TEXT_PRIMARY, fontsize=10.5, family="sans-serif")
        if i < 2:
            draw_arrow(ax, x, row2_y + box_h // 2, xs_rev[i+1] + box_w, row2_y + box_h // 2, color=GREEN_ACCENT)

    plt.tight_layout()
    out = DEST / "diagram-2-debrief-flowchart.png"
    plt.savefig(out, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated {out}")

# ==============================================================================
# DIAGRAM 3: MINIMALIST PHASE 2 & 3 PROGRESSION FLOWCHART
# ==============================================================================
def make_diagram_3():
    fig, ax = create_canvas(
        "Phase 2 & 3: Progression & Habit Compounding",
        "How reps, challenge ladders, and ledger tracking build lasting range"
    )

    # Top Row: The 3 Core Modes
    modes = [
        ("Mode: /rewire prep", "Before the moment", BLUE_BG, BLUE_ACCENT, [
            "• Walk in ready for interviews or talks",
            "• 1 somatic readiness tool (Huberman)",
            "• 1 cognitive focus anchor (Grant/Greene)"
        ]),
        ("Mode: /rewire reps", "The Challenge Ladder", PURPLE_BG, PURPLE_ACCENT, [
            "• 5 progressive rungs per situation type",
            "• Calibrated from 2/10 up to 8/10 discomfort",
            "• Unlocks next rung only when ready"
        ]),
        ("Mode: /rewire check-in", "Weekly Progress Review", GREEN_BG, GREEN_ACCENT, [
            "• Analyzes discomfort trends over time",
            "• Identifies easier vs flat vs stuck",
            "• Hands user 1 focus for the week"
        ])
    ]
    
    top_w = 420
    top_h = 220
    top_y = 510
    top_xs = [100, 590, 1080]
    
    for i in range(3):
        x = top_xs[i]
        title, sub, bg, col, lines = modes[i]
        draw_pill(ax, x, top_y, top_w, top_h, bg, col)
        ax.text(x + 22, top_y + top_h - 38, title, color=col, fontsize=14, fontweight="bold", family="sans-serif")
        ax.text(x + 22, top_y + top_h - 58, sub, color=TEXT_SECONDARY, fontsize=10, family="sans-serif")
        ax.plot([x + 22, x + top_w - 22], [top_y + top_h - 72, top_y + top_h - 72], color=col, linewidth=1, alpha=0.3)
        for j, line in enumerate(lines):
            ax.text(x + 22, top_y + top_h - 105 - j * 32, line, color=TEXT_PRIMARY, fontsize=10.5, family="sans-serif")

    # Bottom Area: The Compounding Habit Loop (5 Stages)
    draw_pill(ax, 100, 120, 1400, 310, CARD_WHITE, CARD_BORDER)
    ax.text(130, 395, "The Compounding Habit Loop", color=TEXT_PRIMARY, fontsize=15, fontweight="bold", family="sans-serif")
    ax.text(130, 372, "Closed-loop feedback connecting moments, execution, and discomfort scores", color=TEXT_SECONDARY, fontsize=10, family="sans-serif")

    loop_stages = [
        ("1. Real Freeze", "Hesitation in class,\nmeeting, or talk.", AMBER_BG, AMBER_ACCENT),
        ("2. Debrief & Rep", "Council assigns 1\ncalibrated small rep.", BLUE_BG, BLUE_ACCENT),
        ("3. Action Logged", "Saved to ledger with\nbefore score (e.g. 7).", PURPLE_BG, PURPLE_ACCENT),
        ("4. Execute in Life", "User does rep next\ntime cue happens.", GREEN_BG, GREEN_ACCENT),
        ("5. Rate & Expand", "Mark done; discomfort\ndrops (e.g. 7 → 4).", BLUE_BG, BLUE_ACCENT)
    ]
    
    step_w = 230
    step_h = 160
    step_y = 170
    step_start_x = 135
    step_gap = 48
    
    for i, (title, desc, bg, col) in enumerate(loop_stages):
        x = step_start_x + i * (step_w + step_gap)
        draw_pill(ax, x, step_y, step_w, step_h, bg, col)
        ax.text(x + 18, step_y + step_h - 36, title, color=col, fontsize=11.5, fontweight="bold", family="sans-serif")
        ax.plot([x + 18, x + step_w - 18], [step_y + step_h - 50, step_y + step_h - 50], color=col, linewidth=1, alpha=0.3)
        ax.text(x + 18, step_y + step_h - 85, desc, color=TEXT_PRIMARY, fontsize=9.5, family="sans-serif")
        if i < len(loop_stages) - 1:
            draw_arrow(ax, x + step_w, step_y + step_h // 2, x + step_w + step_gap, step_y + step_h // 2, color=BLUE_ACCENT)

    plt.tight_layout()
    out = DEST / "diagram-3-progression-flowchart.png"
    plt.savefig(out, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated {out}")

if __name__ == "__main__":
    make_diagram_1()
    make_diagram_2()
    make_diagram_3()

