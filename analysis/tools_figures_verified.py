# Regenerates Table II tool figures from the VERIFIED dataset (2026-07-13).
# Source of truth: tab:gdpr_tools_comparison in bare_jrnl_new_sample4.tex,
# rebuilt after row-by-row verification of all 15 citations against Crossref
# and the papers' own abstracts. Replaces the earlier fabricated dataset.
#
# DAPRECO KB is a regulation-wide formalisation and is excluded from the
# per-article coverage figure (noted in the figure caption in the .tex).

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

tools = [
    # label,           family,          articles,               D  S  I  A   LoI
    ("CCV",            "Semantic Web",  "5,6",                  0, 1, 1, 1, "PT"),
    ("Agarwal+18",     "Semantic Web",  "4,8,9,12,13,14,17,32", 1, 0, 1, 0, "P"),
    ("SPECIAL-K",      "Semantic Web",  "5,6,7",                0, 1, 1, 1, "PT"),
    ("Basin+18",       "Formal/legal",  "5,17",                 0, 0, 0, 1, "PoC"),
    ("DERECHA",        "NLP/ML",        "8,28,32,33,34,35,36,40,42,43,63,82,83,84,93", 0, 0, 0, 1, "P"),
    ("Regorous",       "Formal/legal",  "4,6,8",                1, 0, 1, 1, "P"),
    ("Piao+21",        "Blockchain",    "16,17",                0, 0, 0, 1, "PoC"),
    ("GDPRov",         "Semantic Web",  "7,15,16,17,33",        0, 0, 1, 0, "PoC"),
    ("BPR4GDPR",       "Platform",      "15,17,20,25",          1, 1, 0, 1, "P"),
    ("DAPRECO KB",     "Formal/legal",  None,                   1, 0, 1, 0, "P"),  # regulation-wide
    ("Truong+20",      "Blockchain",    "5,13,14,15,16,17,18,20", 0, 1, 0, 1, "P"),
    ("SPECIAL-PL",     "Semantic Web",  "6,7,9,10,13,14,15,17,18,21,22,30,32", 1, 1, 1, 1, "P"),
    ("Kammuller+18",   "Formal/legal",  "25,32",                0, 0, 0, 0, "PoC"),
    ("Polisis",        "NLP/ML",        "12,13,14",             0, 1, 0, 1, "PT"),
    ("DEFeND",         "Platform",      "4,5,6,7,8,13,14,15,19,23,24,25,32,33,34,35,36", 0, 0, 1, 1, "PT"),
]

df = pd.DataFrame(
    tools,
    columns=["Tool", "Family", "Articles", "Dynamicity", "Scalability",
             "Interoperability", "Automaticity", "LoI"],
)

FAMILY_LABELS = {
    "Semantic Web": "Semantic Web",
    "Formal/legal": "Formal methods &\nlegal rule languages",
    "Blockchain": "Blockchain",
    "NLP/ML": "NLP/ML",
    "Platform": "Integrated platforms",
}
FAMILY_COLORS = {
    "Semantic Web": "#4472C4",
    "Formal/legal": "#C0504D",
    "Blockchain": "#9BBB59",
    "NLP/ML": "#8064A2",
    "Platform": "#F79646",
}

# ---- Figure A: technology families -------------------------------------
fam_counts = df["Family"].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
labels = [FAMILY_LABELS[f] for f in fam_counts.index]
colors = [FAMILY_COLORS[f] for f in fam_counts.index]
bars = ax.barh(labels, fam_counts.values, color=colors, height=0.55, edgecolor="white")
for bar, val in zip(bars, fam_counts.values):
    ax.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height() / 2,
            str(val), va="center", fontsize=22, fontweight="bold")
ax.set_xlabel("Number of Tools", fontsize=24)
ax.set_xlim(0, fam_counts.max() + 1.2)
ax.tick_params(axis="both", labelsize=20)
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig("tools_tech_families.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close()
print("saved tools_tech_families.png")

# ---- Figure B: article coverage (DAPRECO excluded) ----------------------
from collections import Counter

art_counter = Counter()
for _, row in df.iterrows():
    if row["Articles"] is None:
        continue
    for a in row["Articles"].split(","):
        art_counter[int(a)] += 1

# Fold every singleton-count article (cited by exactly one tool) into one
# "Other" bucket so the chart isn't dominated by a long flat tail. Strict
# count-based rule -- no curated exceptions -- so it's a clean, defensible
# cutoff rather than a subjective "these two are interesting enough" call.
FOLD_SET = {a for a, c in art_counter.items() if c == 1}


def _format_ranges(nums):
    """Compact range notation, e.g. [10,19,21,22,23,24] -> '10, 19, 21-24'."""
    nums = sorted(nums)
    ranges = []
    start = prev = nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        ranges.append((start, prev))
        start = prev = n
    ranges.append((start, prev))
    return ", ".join(f"{a}" if a == b else f"{a}-{b}" for a, b in ranges)

arts = sorted(a for a in art_counter if a not in FOLD_SET)
counts = [art_counter[a] for a in arts]
labels = [str(a) for a in arts]

folded_arts = sorted(a for a in art_counter if a in FOLD_SET)
labels.append("")  # invisible spacer so the last real tick and "Other*" don't collide
counts.append(0)
labels.append("Other*")
counts.append(1)  # each folded article is itself cited by exactly 1 tool

fig, ax = plt.subplots(figsize=(15.5, 6))
bar_colors = ["#4472C4"] * (len(labels) - 2) + ["none", "#B0B0B0"]
bars = ax.bar(labels, counts, color=bar_colors, edgecolor="white", width=0.75)
ax.margins(x=0.01)
for bar, val, lab in zip(bars, counts, labels):
    if lab == "":
        continue
    text = f"n={len(folded_arts)}" if lab == "Other*" else str(val)
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.12,
            text, ha="center", va="bottom", fontsize=20, fontweight="bold")
ax.set_xlabel("GDPR Article", fontsize=24)
ax.set_ylabel("Number of Tools", fontsize=24)
ax.tick_params(axis="both", labelsize=20)
ax.set_ylim(0, max(counts) + 1.5)
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

fold_note = f"*Other = Art. {_format_ranges(folded_arts)} (each cited by 1 tool)"
ax.text(0.995, 0.97, fold_note, transform=ax.transAxes, ha="right", va="top",
        fontsize=13, style="italic", color="#444444")

plt.tight_layout()
plt.savefig("tools_article_coverage.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close()
print("saved tools_article_coverage.png")
print("folded into 'Other*':", _format_ranges(folded_arts))
print('LaTeX caption snippet: "Other" aggregates articles cited by exactly one tool '
      f"(Art. {_format_ranges(folded_arts)}).")

# ---- Figure C: capability heatmap ---------------------------------------
cap_cols = ["Dynamicity", "Scalability", "Interoperability", "Automaticity"]
cap = df.set_index("Tool")[cap_cols]
fig, ax = plt.subplots(figsize=(8, 10))
ax.imshow(cap.values, cmap=matplotlib.colors.ListedColormap(["#f2f2f2", "#4472C4"]),
          aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(cap_cols)))
ax.set_xticklabels(cap_cols, fontsize=14, rotation=30, ha="right")
ax.set_yticks(range(len(cap.index)))
ax.set_yticklabels(cap.index, fontsize=14)
for i in range(cap.shape[0]):
    for j in range(cap.shape[1]):
        ax.text(j, i, "✓" if cap.values[i, j] else "",
                ha="center", va="center", color="white", fontsize=16, fontweight="bold")
ax.set_xticks(np.arange(-0.5, len(cap_cols)), minor=True)
ax.set_yticks(np.arange(-0.5, len(cap.index)), minor=True)
ax.grid(which="minor", color="white", linewidth=1.5)
ax.tick_params(which="minor", length=0)
plt.tight_layout()
plt.savefig("tools_capability_heatmap.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close()
print("saved tools_capability_heatmap.png")

# ---- Figure D: LoI distribution ------------------------------------------
loi_order = ["PoC", "P", "PT", "FM"]
loi_counts = df["LoI"].value_counts().reindex(loi_order, fill_value=0)
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(["Proof of\nConcept", "Prototype", "Pilot\nTested", "Full\nMaturity"],
              loi_counts.values, color=["#C0504D", "#F79646", "#9BBB59", "#4472C4"],
              edgecolor="white")
for bar, val in zip(bars, loi_counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.12,
            str(val), ha="center", va="bottom", fontsize=22, fontweight="bold")
ax.set_ylabel("Number of Tools", fontsize=22)
ax.tick_params(axis="both", labelsize=18)
ax.set_ylim(0, loi_counts.max() + 1.5)
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig("tools_loi.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close()
print("saved tools_loi.png")

# ---- Summary stats for prose ---------------------------------------------
print("\n--- verified stats for §VII prose ---")
print("families:", dict(df["Family"].value_counts()))
print("articles:", dict(sorted(art_counter.items())))
print("capabilities:", {c: int(df[c].sum()) for c in cap_cols})
print("LoI:", dict(loi_counts))
n_all4 = ((df[cap_cols].sum(axis=1) == 4)).sum()
n_zero = ((df[cap_cols].sum(axis=1) == 0)).sum()
print("all-4 tools:", df[df[cap_cols].sum(axis=1) == 4]["Tool"].tolist())
print("zero-cap tools:", df[df[cap_cols].sum(axis=1) == 0]["Tool"].tolist())
