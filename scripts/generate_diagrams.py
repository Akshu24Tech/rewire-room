import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Temp")

DEST = Path("assets")
DEST.mkdir(parents=True, exist_ok=True)

# Colors
BG_COLOR = "#070E18"
PANEL_BG = "#0D1928"
CARD_BG = "#122338"
ACCENT_CYAN = "#38BDF8"
ACCENT_BLUE = "#60A5FA"
ACCENT_GREEN = "#34D399"
ACCENT_PURPLE = "#A78BFA"
ACCENT_AMBER = "#FBBF24"
TEXT_WHITE = "#FFFFFF"
TEXT_GRAY = "#94A3B8"
BORDER_COLOR = "#1E3A5F"

def create_figure(title, subtitle):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=140)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 900)
    ax.axis("off")
    
    ax.text(80, 852, title, color=TEXT_WHITE, fontsize=24, fontweight="bold", family="sans-serif")
    ax.text(80, 824, subtitle, color=ACCENT_CYAN, fontsize=12, fontweight="medium", family="sans-serif")
    ax.plot([80, 1520], [808, 808], color=BORDER_COLOR, linewidth=1.5)
    return fig, ax

def draw_card(ax, x, y, w, h, title="", subtitle="", border_color=BORDER_COLOR, fill_color=PANEL_BG, corner_radius=12):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={corner_radius}",
        edgecolor=border_color,
        facecolor=fill_color,
        linewidth=1.5
    )
    ax.add_patch(box)
    if title:
        ax.text(x + 16, y + h - 26, title, color=TEXT_WHITE, fontsize=12, fontweight="bold", family="sans-serif")
    if subtitle:
        ax.text(x + 16, y + h - 46, subtitle, color=ACCENT_CYAN, fontsize=9.5, fontweight="medium", family="sans-serif")

def draw_bullet(ax, x, y, text, detail="", color=TEXT_GRAY, highlight=TEXT_WHITE):
    ax.text(x, y, "•", color=ACCENT_CYAN, fontsize=11, family="sans-serif")
    ax.text(x + 14, y, text, color=highlight, fontsize=10, fontweight="bold", family="sans-serif")
    if detail:
        ax.text(x + 14, y - 16, detail, color=color, fontsize=8.5, family="sans-serif")

def draw_arrow(ax, x1, y1, x2, y2, color=ACCENT_CYAN, label=""):
    ax.annotate(
        "",
        xy=(x2, y2), xycoords="data",
        xytext=(x1, y1), textcoords="data",
        arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color=color, lw=2, shrinkA=4, shrinkB=4)
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 8, label, color=color, fontsize=8.5, fontweight="bold", ha="center", family="sans-serif")

# ==============================================================================
# DIAGRAM 1: FULL ARCHITECTURE & CODEBASE MAP
# ==============================================================================
def generate_diagram_1():
    fig, ax = create_figure(
        "Rewire Room: System Architecture & Codebase Map",
        "Layered structure connecting Claude Code skills, sub-agent manifests, verified brains, scripts, and sessions"
    )
    
    # Col 1: Orchestration
    draw_card(ax, 80, 80, 260, 695, "1. Orchestration Layer", ".claude/skills/rewire/", border_color=ACCENT_BLUE)
    draw_bullet(ax, 95, 705, "SKILL.md", "Chair protocol & mode routing", highlight=ACCENT_CYAN)
    draw_bullet(ax, 95, 650, "roster.json", "7 seats, dimensions, status registry")
    draw_bullet(ax, 95, 595, "references/", "Operating manuals & templates:")
    
    refs = [
        ("safety.md", "Clinical red-line filter"),
        ("seats.md", "Seat matrix & tensions"),
        ("round-prompts.md", "R1, R2, Audit, Prep, Ladder"),
        ("scoring.md", "Layer scoring & Rep test"),
        ("session-format.md", "Folder & markdown rules"),
        ("debrief-template.md", "Standard debrief schema"),
        ("prep-template.md", "Pre-moment action schema")
    ]
    for i, (fn, desc) in enumerate(refs):
        ax.text(110, 545 - i * 36, f"• {fn}", color=TEXT_WHITE, fontsize=9, fontweight="bold", family="sans-serif")
        ax.text(122, 531 - i * 36, desc, color=TEXT_GRAY, fontsize=8, family="sans-serif")

    # Col 2: Agents
    draw_card(ax, 370, 80, 250, 695, "2. Agent Manifests", ".claude/agents/", border_color=ACCENT_PURPLE)
    agents = [
        ("seat-kukushkin.md", "Identity and memory"),
        ("seat-huberman.md", "Nervous system and state"),
        ("seat-yousef.md", "Attention and energy"),
        ("seat-grant.md", "Growth and rethinking"),
        ("seat-greene.md", "Human nature and mastery"),
        ("seat-galloway.md", "Real-world stakes"),
        ("seat-evidence.md", "Empirical research auditor")
    ]
    for i, (ag, layer) in enumerate(agents):
        y_pos = 705 - i * 86
        draw_card(ax, 385, y_pos - 45, 220, 65, "", "", border_color=BORDER_COLOR, fill_color=CARD_BG, corner_radius=8)
        ax.text(400, y_pos - 10, ag, color=TEXT_WHITE, fontsize=9.5, fontweight="bold", family="sans-serif")
        ax.text(400, y_pos - 28, layer, color=ACCENT_PURPLE, fontsize=8.5, family="sans-serif")

    # Col 3: Brains
    draw_card(ax, 650, 80, 280, 695, "3. Verified Brains", "Corpus of 20-30+ Sources per Seat", border_color=ACCENT_GREEN)
    ax.text(665, 705, "Persona Brains (6 Expert Seats):", color=ACCENT_CYAN, fontsize=9.5, fontweight="bold", family="sans-serif")
    files_expert = [
        ("_hot.md", "Worldview, rules, frameworks, misfires"),
        ("frameworks.md", "Core named models with quotes [Sxxx]"),
        ("positions.md", "Positions on introversion & stakes"),
        ("principles.md", "Actionable heuristics & rules"),
        ("stories.md", "Biographical case studies"),
        ("voice.md", "Tone, pacing, signature phrases"),
        ("sources.md", "Full catalog of cited public sources")
    ]
    for i, (fn, desc) in enumerate(files_expert):
        y_pos = 675 - i * 36
        ax.text(665, y_pos, f"• {fn}", color=TEXT_WHITE, fontsize=9, fontweight="bold", family="sans-serif")
        ax.text(677, y_pos - 14, desc, color=TEXT_GRAY, fontsize=8, family="sans-serif")
    
    # Evidence Brain
    draw_card(ax, 665, 105, 250, 270, "The Evidence Brain (Research)", "31 Open-Access Systematic Reviews", border_color=ACCENT_GREEN, fill_color=CARD_BG, corner_radius=8)
    draw_bullet(ax, 678, 305, "claims.md", "Pre-graded claims (STRONG to UNSUPP)")
    draw_bullet(ax, 678, 252, "studies.md", "Extracted effect sizes, RCTs & metas")
    draw_bullet(ax, 678, 199, "sources.md", "Open-access reviews & trials")
    draw_bullet(ax, 678, 146, "_hot.md", "Rigorous grading standards & limits")

    # Col 4: Scripts & Verification
    draw_card(ax, 960, 80, 280, 695, "4. Verification & Engine", "scripts/ & tests/", border_color=ACCENT_AMBER)
    scripts = [
        ("check_quotes.py", "Verifies every quote [Sxxx] against brain.", "Fails CI if quote or ID is not verbatim."),
        ("ledger.py", "CLI to log, complete, & analyze reps.", "Calculates trends per situation type."),
        ("textnorm.py", "Loose text matching & token normalization.", "Handles whitespace and punctuation."),
        ("fetch_sources.py", "Corpus fetcher for /newseat.", "Downloads transcripts & books."),
        ("builder.py", "Sub-agent orchestrator for brain drafting.", "Coordinates 9 extraction agents."),
        ("tests/ (22 pass)", "Automated test suite verifying roster,", "ledger schemas, quotes, and CLI flags.")
    ]
    for i, (sc, d1, d2) in enumerate(scripts):
        y_pos = 705 - i * 100
        draw_card(ax, 975, y_pos - 60, 250, 75, "", "", border_color=BORDER_COLOR, fill_color=CARD_BG, corner_radius=8)
        ax.text(990, y_pos - 2, sc, color=ACCENT_AMBER, fontsize=10, fontweight="bold", family="sans-serif")
        ax.text(990, y_pos - 22, d1, color=TEXT_WHITE, fontsize=8.5, family="sans-serif")
        ax.text(990, y_pos - 40, d2, color=TEXT_GRAY, fontsize=8, family="sans-serif")

    # Col 5: Storage
    draw_card(ax, 1270, 80, 250, 695, "5. Storage & Privacy", "sessions/ & ledger/ (Gitignored)", border_color=ACCENT_CYAN)
    draw_bullet(ax, 1285, 705, "sessions/YYYY-MM-DD-slug/", "Isolated folder per debrief:", highlight=ACCENT_CYAN)
    sfiles = [
        ("brief.md", "Context, scores, seated council"),
        ("round-1.md", "Diagnosis cards verbatim"),
        ("round-2.md", "Cross-exam cards + cruxes"),
        ("evidence.md", "Claim audit & reps at risk"),
        ("debrief.md", "Final rep, if-then, minority view")
    ]
    for i, (sf, desc) in enumerate(sfiles):
        y_pos = 645 - i * 44
        ax.text(1295, y_pos, f"• {sf}", color=TEXT_WHITE, fontsize=9, fontweight="bold", family="sans-serif")
        ax.text(1307, y_pos - 15, desc, color=TEXT_GRAY, fontsize=8, family="sans-serif")

    draw_card(ax, 1285, 105, 220, 250, "ledger/reps.jsonl", "Personal Habit Database", border_color=BORDER_COLOR, fill_color=CARD_BG, corner_radius=8)
    draw_bullet(ax, 1298, 285, "reps.jsonl", "Tracks all active & completed reps")
    draw_bullet(ax, 1298, 230, "Metrics", "Discomfort before/after (0-10)")
    draw_bullet(ax, 1298, 175, "Trend lines", "Identifies easier, flat, or stuck")
    draw_bullet(ax, 1298, 125, "Privacy", "Zero telemetry; stays on disk")

    # Connectors
    draw_arrow(ax, 340, 715, 370, 715, color=ACCENT_BLUE)
    draw_arrow(ax, 620, 500, 650, 500, color=ACCENT_PURPLE)
    draw_arrow(ax, 930, 400, 960, 400, color=ACCENT_GREEN)
    draw_arrow(ax, 1240, 550, 1270, 550, color=ACCENT_AMBER)

    plt.tight_layout()
    out_file = DEST / "diagram-1-full-architecture.png"
    plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated {out_file}")

# ==============================================================================
# DIAGRAM 2: PHASE 1 DEBRIEF & EVIDENCE AUDIT FLOWCHART
# ==============================================================================
def generate_diagram_2():
    fig, ax = create_figure(
        "Phase 1: The Core Debrief & Evidence Audit Loop",
        "Step-by-step execution flowchart: from raw social freeze to calibrated rep and verified progress"
    )

    # Top Row: Steps 0 to 3
    # Step 0
    draw_card(ax, 80, 630, 320, 145, "Step 0: Intake & Safety Screen", "references/safety.md", border_color=ACCENT_AMBER)
    ax.text(95, 692, "User inputs real moment (/rewire debrief ...)", color=TEXT_WHITE, fontsize=9.5, family="sans-serif")
    ax.text(95, 672, "Clinical red-line filter (panic, trauma, depression):", color=TEXT_GRAY, fontsize=8.5, family="sans-serif")
    ax.text(95, 652, "• Red flags? STOP: compassionate crisis referral.", color="#F87171", fontsize=8.5, fontweight="bold", family="sans-serif")
    ax.text(95, 636, "• Everyday social nerves? PROCEED.", color=ACCENT_GREEN, fontsize=8.5, fontweight="bold", family="sans-serif")

    draw_arrow(ax, 400, 702, 455, 702, color=ACCENT_CYAN)

    # Step 1
    draw_card(ax, 455, 630, 325, 145, "Step 1: The Brief Formulation", "brief.md in sessions/YYYY-MM-DD-<slug>/", border_color=ACCENT_BLUE)
    ax.text(470, 692, "1. The Moment (where, who, stakes)", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(470, 672, "2. Wanted vs Actually Did (the freeze point)", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(470, 652, "3. Discomfort Rating (before/during/after 0-10)", color=ACCENT_CYAN, fontsize=9, family="sans-serif")
    ax.text(470, 634, "4. Past History (ledger.py list --type <tag>)", color=TEXT_GRAY, fontsize=8.5, family="sans-serif")

    draw_arrow(ax, 780, 702, 835, 702, color=ACCENT_CYAN)

    # Step 2
    draw_card(ax, 835, 630, 335, 145, "Step 2: Council Selection", "roster.json & references/seats.md", border_color=ACCENT_PURPLE)
    ax.text(850, 692, "• Picks 3-4 ready seats tailored to the freeze:", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(865, 672, "Weights: 3 (broke), 2 (contributed), 1 (outside view)", color=TEXT_GRAY, fontsize=8.5, family="sans-serif")
    ax.text(850, 652, "• Tensions: pairs natural opposites (e.g. Grant vs Greene)", color=ACCENT_PURPLE, fontsize=8.5, family="sans-serif")
    ax.text(850, 634, "• Evidence Seat: always seated (auditor, not persona)", color=ACCENT_GREEN, fontsize=8.5, fontweight="bold", family="sans-serif")

    draw_arrow(ax, 1170, 702, 1225, 702, color=ACCENT_CYAN)

    # Step 3
    draw_card(ax, 1225, 630, 295, 145, "Step 3: Session Workspace", "sessions/YYYY-MM-DD-<slug>/", border_color=ACCENT_CYAN)
    ax.text(1240, 692, "• Initializes private session folder", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(1240, 672, "• Writes brief.md with council roster", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(1240, 652, "• Prepares parallel agent dispatch", color=TEXT_GRAY, fontsize=8.5, family="sans-serif")
    ax.text(1240, 634, "• Ignored by Git (stays local)", color=ACCENT_CYAN, fontsize=8.5, family="sans-serif")

    # Down arrow to Round 1
    draw_arrow(ax, 1370, 630, 1370, 560, color=ACCENT_CYAN)

    # Step 4: Round 1 (Parallel Diagnosis)
    draw_card(ax, 80, 385, 1440, 175, "Step 4: Round 1 Parallel Diagnosis (round-1.md)", "Every seated expert analyzes brief from their own layer simultaneously", border_color=ACCENT_BLUE)
    
    # 3 Sample Card Boxes inside
    draw_card(ax, 100, 400, 390, 115, "Huberman (Nervous system)", "Layer Score: 1/5 | Confidence: high", border_color=BORDER_COLOR, fill_color=CARD_BG, corner_radius=6)
    ax.text(112, 455, "What broke: Sympathetic freeze & vocal tightening.", color=TEXT_WHITE, fontsize=8.5, family="sans-serif")
    ax.text(112, 435, "Verbatim quote: \"it's very hard to control...\" [S030]", color=ACCENT_CYAN, fontsize=8, family="sans-serif")
    ax.text(112, 415, "Rep: Physiological sigh on question call.", color=TEXT_GRAY, fontsize=8, family="sans-serif")

    draw_card(ax, 510, 400, 390, 115, "Grant (Growth & rethinking)", "Layer Score: 2/5 | Confidence: high", border_color=BORDER_COLOR, fill_color=CARD_BG, corner_radius=6)
    ax.text(522, 455, "What broke: Perfectionism trap, waiting for certainty.", color=TEXT_WHITE, fontsize=8.5, family="sans-serif")
    ax.text(522, 435, "Verbatim quote: \"becoming a creature of discomfort\" [S001]", color=ACCENT_CYAN, fontsize=8, family="sans-serif")
    ax.text(522, 415, "Rep: Ask unpolished starter within 5 seconds.", color=TEXT_GRAY, fontsize=8, family="sans-serif")

    draw_card(ax, 920, 400, 390, 115, "Greene (Human nature)", "Layer Score: 2/5 | Confidence: med", border_color=BORDER_COLOR, fill_color=CARD_BG, corner_radius=6)
    ax.text(932, 455, "What broke: Internal self-absorbed anxiety spiral.", color=TEXT_WHITE, fontsize=8.5, family="sans-serif")
    ax.text(932, 435, "Verbatim quote: \"you want to be outer directed...\" [S004]", color=ACCENT_CYAN, fontsize=8, family="sans-serif")
    ax.text(932, 415, "Rep: Observe 3 peers before speaking.", color=TEXT_GRAY, fontsize=8, family="sans-serif")

    ax.text(1330, 465, "Chair Notes:\n• Identifies cruxes\n• Unanimity check\n• Extracts claims C1..Cn", color=ACCENT_AMBER, fontsize=9, fontweight="bold", family="sans-serif")

    # Down arrow to Round 2 & Audit
    draw_arrow(ax, 800, 385, 800, 335, color=ACCENT_CYAN)

    # Step 5: Round 2 & Audit
    draw_card(ax, 80, 170, 680, 165, "Step 5A: Round 2 Cross-Exam (round-2.md)", "Experts debate cruxes, challenge assumptions, and concede points", border_color=ACCENT_PURPLE)
    ax.text(95, 260, "• I Disagree Most With: challenges another seat's lens", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(95, 240, "• I Concede: acknowledges stronger counter-arguments", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(95, 220, "• Crux Resolution: council tests whether state or mindset leads", color=ACCENT_PURPLE, fontsize=9, family="sans-serif")
    ax.text(95, 200, "• Position Shifts: seats can move their vote (e.g. Greene to Huberman)", color=ACCENT_CYAN, fontsize=9, family="sans-serif")
    ax.text(95, 180, "• Primary Layer Support: weighted tally decides the leverage layer", color=TEXT_GRAY, fontsize=8.5, family="sans-serif")

    draw_card(ax, 780, 170, 740, 165, "Step 5B: Evidence Audit (evidence.md)", "The Evidence seat audits every factual claim against its 31-paper research corpus", border_color=ACCENT_GREEN)
    ax.text(795, 260, "• Rigorous Grading: STRONG | MIXED | WEAK | UNSUPPORTED | NOT IN BRAIN", color=ACCENT_GREEN, fontsize=9, fontweight="bold", family="sans-serif")
    ax.text(795, 240, "• Audits C1..Cn: checks physiological sigh, reappraisal, liking gap, if-then plans", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(795, 220, "• Reps at Risk: flags reps relying on unproven biological mechanisms", color=ACCENT_AMBER, fontsize=9, family="sans-serif")
    ax.text(795, 200, "• Safer Framing: preserves low-risk behavioral experiment while dropping hype", color=TEXT_WHITE, fontsize=9, family="sans-serif")
    ax.text(795, 180, "• Independence: holds research line; never argues advice or personality", color=TEXT_GRAY, fontsize=8.5, family="sans-serif")

    # Down arrow to Debrief & Verify
    draw_arrow(ax, 800, 170, 800, 120, color=ACCENT_CYAN)

    # Step 6 & 7: Synthesis, Ledger, Verification
    draw_card(ax, 80, 15, 1440, 105, "Step 6 & 7: The Debrief, Ledger Log & Verification Gate", "Final synthesis in debrief.md, recorded in ledger/reps.jsonl, gated by check_quotes.py", border_color=ACCENT_CYAN)
    
    pillars = [
        ("1. Primary Layer Decided", "Weighted consensus + evidence check", ACCENT_CYAN),
        ("2. One Calibrated Rep", "Passes 5-point rep test (small, soon, safe)", ACCENT_CYAN),
        ("3. If-Then Plan", "\"When [cue], I will [the rep]\"", ACCENT_CYAN),
        ("4. Ledger Entry Logged", "python scripts/ledger.py add --type class ...", ACCENT_AMBER),
        ("5. Quote Gate (0 Failures)", "check_quotes.py validates every quote verbatim", ACCENT_GREEN)
    ]
    for i, (p_title, p_sub, p_col) in enumerate(pillars):
        px = 100 + i * 285
        ax.text(px, 50, p_title, color=p_col, fontsize=9.5, fontweight="bold", family="sans-serif")
        ax.text(px, 30, p_sub, color=TEXT_GRAY, fontsize=8.5, family="sans-serif")

    plt.tight_layout()
    out_file = DEST / "diagram-2-debrief-flowchart.png"
    plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated {out_file}")

# ==============================================================================
# DIAGRAM 3: PROGRESSION, REPS & COMPOUNDING FLOWCHART
# ==============================================================================
def generate_diagram_3():
    fig, ax = create_figure(
        "Phase 2 & 3: Challenge Ladders, Habit Compounding & Future Extensions",
        "How Rewire Room turns single debriefs into compounding confidence, progressive ladders, and long-term range"
    )

    # Top Row: 3 Modes
    # Col A: Prep
    draw_card(ax, 80, 480, 440, 295, "Mode: Prep (/rewire prep <moment>)", "Walk into high-stakes situations ready", border_color=ACCENT_BLUE)
    draw_bullet(ax, 100, 680, "Trigger", "Before an interview, big presentation, or difficult meeting")
    draw_bullet(ax, 100, 625, "1 Fast Round", "Seated seats provide forward-looking anchors (not diagnosis)")
    draw_bullet(ax, 100, 570, "State Readiness Tool", "1 somatic lever for the minutes before (e.g. cyclic sighing)")
    draw_bullet(ax, 100, 515, "Intentional Anchor", "1 focus cue to hold during the interaction")
    
    # Col B: Reps
    draw_card(ax, 580, 480, 440, 295, "Mode: Reps (/rewire reps <type>)", "Progressive 5-Rung Exposure Ladder", border_color=ACCENT_PURPLE)
    draw_bullet(ax, 600, 680, "Calibrated to Ledger", "Reads hardest completed rung; never jumps > 1 level")
    draw_bullet(ax, 600, 625, "Single-Seat Consult", "Drafted by Adam Grant (stretch) or Yousef/Greene")
    draw_bullet(ax, 600, 570, "Rungs 1 to 5", "From a 2/10 discomfort stretch up to an 8/10 challenge")
    draw_bullet(ax, 600, 515, "Measurable Proof", "Observable action with clear unlock criteria")

    # Col C: Check-In
    draw_card(ax, 1080, 480, 440, 295, "Mode: Check-In (/rewire check-in)", "Honest Weekly Progress Read", border_color=ACCENT_GREEN)
    draw_bullet(ax, 1100, 680, "Statistical Trend", "python scripts/ledger.py stats --json")
    draw_bullet(ax, 1100, 625, "What is Getting Easier", "Tags showing statistically declining discomfort")
    draw_bullet(ax, 1100, 570, "What is Stuck / Dodged", "High skip rates or reps open > 2 weeks")
    draw_bullet(ax, 1100, 515, "One Weekly Focus", "Hands user exactly 1 priority for the coming week")

    # Middle Row: Compounding Loop
    draw_card(ax, 80, 220, 1440, 230, "The Compounding Habit Loop (ledger/reps.jsonl)", "How behavioral reps permanently rewire neural pathways", border_color=ACCENT_CYAN)
    
    stages = [
        ("1. Real Life Freeze", "User encounters friction in\nclass, meeting, or interview.", ACCENT_AMBER),
        ("2. /rewire debrief", "Council identifies broken layer\n& assigns 1 calibrated rep.", ACCENT_BLUE),
        ("3. Rep Logged", "Stored in ledger/reps.jsonl\nwith initial discomfort score.", ACCENT_PURPLE),
        ("4. Execute Next Time", "User does the rep when cue\nhits in their next real moment.", ACCENT_GREEN),
        ("5. Mark Done & Rate", "python scripts/ledger.py done\n--after <score> --note \"...\"", ACCENT_CYAN),
        ("6. Range Expands", "Discomfort drops 7 → 4;\nnext challenge rung unlocks.", TEXT_WHITE)
    ]
    for i, (title, desc, col) in enumerate(stages):
        x = 95 + i * 238
        draw_card(ax, x, 235, 218, 145, "", "", border_color=col, fill_color=CARD_BG, corner_radius=8)
        ax.text(x + 12, 350, title, color=col, fontsize=10, fontweight="bold", family="sans-serif")
        ax.text(x + 12, 305, desc, color=TEXT_GRAY, fontsize=8.5, family="sans-serif")
        if i < len(stages) - 1:
            draw_arrow(ax, x + 218, 305, x + 238, 305, color=ACCENT_CYAN)

    # Bottom Row: Roadmap
    draw_card(ax, 80, 25, 1440, 165, "Phase 3 & Future Extensions (Roadmap)", "Upcoming capabilities and ecosystem integrations", border_color=BORDER_COLOR)
    
    exts = [
        ("Web Visual Council", "localhost:4730 visual interface to watch\n3D seats debate in real time.", ACCENT_CYAN),
        ("Personal Seat Builder", "Build a custom seat modeled on user's\npersonal journals, values, and essays.", ACCENT_BLUE),
        ("Mode: Decide", "3-round strategic debate for high-stakes\ncareer, project, and life decisions.", ACCENT_PURPLE),
        ("Ledger Web Dashboard", "Interactive visual charting of discomfort\ndrops over months of compounding.", ACCENT_GREEN)
    ]
    for i, (title, desc, col) in enumerate(exts):
        x = 95 + i * 360
        draw_card(ax, x, 40, 340, 95, "", "", border_color=BORDER_COLOR, fill_color=CARD_BG, corner_radius=8)
        ax.text(x + 14, 105, title, color=col, fontsize=10, fontweight="bold", family="sans-serif")
        ax.text(x + 14, 68, desc, color=TEXT_GRAY, fontsize=8.5, family="sans-serif")

    plt.tight_layout()
    out_file = DEST / "diagram-3-progression-flowchart.png"
    plt.savefig(out_file, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated {out_file}")

if __name__ == "__main__":
    generate_diagram_1()
    generate_diagram_2()
    generate_diagram_3()
