"""
Generate uml_final.png — PawPal+ class diagram.

Classes: Task, Pet, Owner, Scheduler
Relationships:
  Pet  <>──── Task   (composition, 1 to 0..*)
  Owner <>──── Pet   (composition, 1 to 0..*)
  Scheduler ──── Owner  (association, 1 to 1)
  Scheduler - - ▷ Task  (dependency via schedule list)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch


# ── Layout constants ──────────────────────────────────────────────────────────
HEADER_H   = 0.42   # height of the class-name row
ATTR_LINE  = 0.28   # height per attribute / method line
BOX_PAD    = 0.14   # internal padding (top/bottom of each section)
LINE_COLOR = "#2c3e50"
FILL_HEADER = "#2c3e50"
FILL_ATTR   = "#ecf0f1"
FILL_METHOD = "#dfe6e9"
TEXT_LIGHT  = "white"
TEXT_DARK   = "#2c3e50"
MONO        = {"fontfamily": "monospace", "fontsize": 8.4}


def section_height(lines: list[str]) -> float:
    return BOX_PAD * 2 + ATTR_LINE * len(lines)


def draw_class(ax, x: float, y_top: float, width: float,
               name: str, attrs: list[str], methods: list[str]) -> dict:
    """Draw a UML class box; return bounding box info."""

    h_header  = HEADER_H
    h_attrs   = section_height(attrs)
    h_methods = section_height(methods)
    total_h   = h_header + h_attrs + h_methods

    # ── header ────────────────────────────────────────────────────────────────
    header = mpatches.FancyBboxPatch(
        (x, y_top - h_header), width, h_header,
        boxstyle="square,pad=0", linewidth=1.2,
        edgecolor=LINE_COLOR, facecolor=FILL_HEADER, zorder=2
    )
    ax.add_patch(header)
    ax.text(x + width / 2, y_top - h_header / 2, f"«class»\n{name}",
            ha="center", va="center", color=TEXT_LIGHT,
            fontsize=9.5, fontweight="bold", zorder=3,
            linespacing=1.35)

    # ── attributes ────────────────────────────────────────────────────────────
    y_attr_top = y_top - h_header
    attr_box = mpatches.FancyBboxPatch(
        (x, y_attr_top - h_attrs), width, h_attrs,
        boxstyle="square,pad=0", linewidth=1.2,
        edgecolor=LINE_COLOR, facecolor=FILL_ATTR, zorder=2
    )
    ax.add_patch(attr_box)
    for i, line in enumerate(attrs):
        ty = y_attr_top - BOX_PAD - ATTR_LINE * i - ATTR_LINE / 2
        ax.text(x + 0.10, ty, line, va="center", color=TEXT_DARK, zorder=3, **MONO)

    # ── methods ───────────────────────────────────────────────────────────────
    y_method_top = y_attr_top - h_attrs
    method_box = mpatches.FancyBboxPatch(
        (x, y_method_top - h_methods), width, h_methods,
        boxstyle="square,pad=0", linewidth=1.2,
        edgecolor=LINE_COLOR, facecolor=FILL_METHOD, zorder=2
    )
    ax.add_patch(method_box)
    for i, line in enumerate(methods):
        ty = y_method_top - BOX_PAD - ATTR_LINE * i - ATTR_LINE / 2
        ax.text(x + 0.10, ty, line, va="center", color=TEXT_DARK, zorder=3, **MONO)

    return {
        "x": x, "y_top": y_top, "width": width, "total_h": total_h,
        "cx": x + width / 2,
        "y_bottom": y_top - total_h,
        "y_mid": y_top - total_h / 2,
        "right": x + width,
    }


def arrow(ax, x1, y1, x2, y2, style="solid", color=LINE_COLOR, label="", lw=1.4):
    """Draw an arrow between two points."""
    ls = "-" if style == "solid" else "--"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>", color=color, lw=lw,
            linestyle=ls,
            mutation_scale=12,
        ),
        zorder=1
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.06, label, ha="center", va="bottom",
                fontsize=7.5, color="#636e72", style="italic")


def diamond(ax, x, y, size=0.12, fill=LINE_COLOR):
    """Draw a filled diamond (composition)."""
    pts = [(x, y + size), (x + size * 0.55, y),
           (x, y - size), (x - size * 0.55, y)]
    diamond_patch = plt.Polygon(pts, closed=True, facecolor=fill,
                                edgecolor=LINE_COLOR, lw=1.2, zorder=4)
    ax.add_patch(diamond_patch)


# ── Figure setup ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(15, 9.5))
ax.set_xlim(0, 15)
ax.set_ylim(0, 9.5)
ax.axis("off")
fig.patch.set_facecolor("#f8f9fa")

# ── Class definitions ─────────────────────────────────────────────────────────

#  Task  (bottom-left)
task = draw_class(
    ax, x=0.4, y_top=8.8, width=3.8,
    name="Task",
    attrs=[
        "+ description : str",
        "+ duration    : int",
        "+ priority    : Literal[high|medium|low]",
        "+ frequency   : str",
        "+ time        : str  (HH:MM)",
        "+ pet_name    : str",
        "+ completed   : bool",
        "+ due_date    : date",
    ],
    methods=[
        "+ is_high_priority() → bool",
        "+ mark_complete() → None",
        "+ create_next_occurrence() → Task|None",
    ],
)

#  Pet  (top-left, to the right of Task)
pet = draw_class(
    ax, x=5.0, y_top=8.8, width=3.6,
    name="Pet",
    attrs=[
        "+ name    : str",
        "+ species : str",
        "+ tasks   : list[Task]",
    ],
    methods=[
        "+ add_task(task: Task) → None",
        "+ get_tasks() → list[Task]",
    ],
)

#  Owner  (top-right)
owner = draw_class(
    ax, x=9.4, y_top=8.8, width=3.8,
    name="Owner",
    attrs=[
        "+ name           : str",
        "+ available_time : int",
        "+ pets           : list[Pet]",
    ],
    methods=[
        "+ add_pet(pet: Pet) → None",
        "+ get_all_tasks() → list[Task]",
        "+ get_available_time() → int",
    ],
)

#  Scheduler  (bottom-right, centred under Owner)
sched = draw_class(
    ax, x=9.4, y_top=4.6, width=5.2,
    name="Scheduler",
    attrs=[
        "+ owner    : Owner",
        "+ schedule : list[Task]",
    ],
    methods=[
        "+ generate_schedule() → list[Task]",
        "+ sort_by_time() → list[Task]",
        "+ filter_tasks(completed, pet_name) → list[Task]",
        "+ detect_conflicts() → list[str]",
        "+ explain_schedule() → str",
        "+ mark_task_complete(task) → Task|None",
    ],
)


# ── Relationships ─────────────────────────────────────────────────────────────

# 1. Pet <>──0..* Task   (composition — Pet owns Tasks)
#    Diamond on Pet's left edge, arrow to Task's right edge
pet_lx = pet["x"]
pet_ly = pet["y_mid"]
task_rx = task["right"]
task_ry = task["y_mid"]

ax.annotate("", xy=(task_rx + 0.01, task_ry), xytext=(pet_lx - 0.12, pet_ly),
            arrowprops=dict(arrowstyle="-", color=LINE_COLOR, lw=1.4), zorder=1)
diamond(ax, pet_lx - 0.12, pet_ly, fill=LINE_COLOR)
ax.text(task_rx + 0.08, task_ry + 0.12, "0..*", fontsize=7.5,
        color="#636e72", style="italic")
ax.text(pet_lx - 0.06, pet_ly + 0.22, "1", fontsize=7.5,
        color="#636e72", style="italic")
ax.text((task_rx + pet_lx) / 2, task_ry - 0.22, "contains",
        ha="center", fontsize=7.5, color="#636e72", style="italic")

# 2. Owner <>──0..* Pet  (composition — Owner owns Pets)
owner_lx = owner["x"]
owner_ly = owner["y_mid"]
pet_rx   = pet["right"]
pet_ry   = pet["y_mid"]

ax.annotate("", xy=(pet_rx + 0.01, pet_ry), xytext=(owner_lx - 0.12, owner_ly),
            arrowprops=dict(arrowstyle="-", color=LINE_COLOR, lw=1.4), zorder=1)
diamond(ax, owner_lx - 0.12, owner_ly, fill=LINE_COLOR)
ax.text(pet_rx + 0.08, pet_ry + 0.12, "0..*", fontsize=7.5,
        color="#636e72", style="italic")
ax.text(owner_lx - 0.06, owner_ly + 0.22, "1", fontsize=7.5,
        color="#636e72", style="italic")
ax.text((pet_rx + owner_lx) / 2, pet_ry - 0.22, "contains",
        ha="center", fontsize=7.5, color="#636e72", style="italic")

# 3. Scheduler ──── Owner  (association — Scheduler holds ref to Owner)
sched_top_cx = sched["cx"]
sched_top_y  = sched["y_top"]
owner_bottom_cx = owner["cx"]
owner_bottom_y  = owner["y_bottom"]

ax.annotate("", xy=(owner_bottom_cx, owner_bottom_y),
            xytext=(sched_top_cx, sched_top_y),
            arrowprops=dict(arrowstyle="-|>", color="#2980b9", lw=1.6,
                            linestyle="-", mutation_scale=13), zorder=1)
ax.text((sched_top_cx + owner_bottom_cx) / 2 + 0.25,
        (sched_top_y + owner_bottom_y) / 2,
        "uses", fontsize=7.5, color="#2980b9", style="italic")

# 4. Scheduler - - ▷ Task  (dependency — schedule list holds Tasks)
sched_lx = sched["x"]
sched_ly = sched["y_mid"]
task_bottom_cx = task["cx"]
task_bottom_y  = task["y_bottom"]

ax.annotate("", xy=(task_bottom_cx, task_bottom_y),
            xytext=(sched_lx, sched_ly),
            arrowprops=dict(arrowstyle="-|>", color="#8e44ad", lw=1.4,
                            linestyle="--", mutation_scale=12), zorder=1)
ax.text(task_bottom_cx - 0.5, task_bottom_y - 0.28,
        "«schedules»", fontsize=7.5, color="#8e44ad", style="italic")


# ── Legend ────────────────────────────────────────────────────────────────────
lx, ly = 0.4, 1.55
ax.text(lx, ly, "Legend", fontsize=8.5, fontweight="bold", color=TEXT_DARK)
# composition
diamond(ax, lx + 0.13, ly - 0.30, size=0.09, fill=LINE_COLOR)
ax.annotate("", xy=(lx + 0.50, ly - 0.30), xytext=(lx + 0.22, ly - 0.30),
            arrowprops=dict(arrowstyle="-", color=LINE_COLOR, lw=1.2))
ax.text(lx + 0.56, ly - 0.30, "Composition (owns)", va="center", fontsize=7.8, color=TEXT_DARK)
# association
ax.annotate("", xy=(lx + 0.50, ly - 0.62), xytext=(lx + 0.04, ly - 0.62),
            arrowprops=dict(arrowstyle="-|>", color="#2980b9", lw=1.2, mutation_scale=11))
ax.text(lx + 0.56, ly - 0.62, "Association (uses)", va="center", fontsize=7.8, color=TEXT_DARK)
# dependency
ax.annotate("", xy=(lx + 0.50, ly - 0.94), xytext=(lx + 0.04, ly - 0.94),
            arrowprops=dict(arrowstyle="-|>", color="#8e44ad", lw=1.2,
                            linestyle="--", mutation_scale=11))
ax.text(lx + 0.56, ly - 0.94, "Dependency (schedules)", va="center", fontsize=7.8, color=TEXT_DARK)


# ── Title & footer ────────────────────────────────────────────────────────────
ax.text(7.5, 9.35, "PawPal+  —  Class Diagram (Final)",
        ha="center", va="center", fontsize=13, fontweight="bold", color=TEXT_DARK)
ax.text(7.5, 0.15, "Generated from pawpal_system.py  •  PawPal+ Module 2",
        ha="center", fontsize=7.5, color="#b2bec3")

plt.tight_layout(pad=0.3)
plt.savefig("uml_final.png", dpi=180, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Saved: uml_final.png")
