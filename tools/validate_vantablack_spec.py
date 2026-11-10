#!/usr/bin/env python3
"""Validate the design contract and repository Markdown links, not font binaries."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def validate():
    data = json.loads((ROOT / "docs/vantablack-gothic/system.json").read_text(encoding="utf-8"))
    errors = []
    metrics = data["metrics"]
    if metrics["units_per_em"] != 1000:
        errors.append("UPEM must remain 1000.")
    if not (metrics["descender"] < 0 < metrics["x_height"] < metrics["cap_height"] <= metrics["ascender"]):
        errors.append("Vertical metrics are out of order.")
    if metrics["ascender"] - metrics["descender"] != 1020:
        errors.append("The proposed 820/-200 design envelope must span 1020 units.")
    for prefix in ("typo", "hhea"):
        if (metrics[prefix + "_ascender"], metrics[prefix + "_descender"]) != (metrics["ascender"], metrics["descender"]):
            errors.append(prefix + " metrics disagree with the design envelope.")
    if metrics["win_ascent"] < metrics["ascender"] or metrics["win_descent"] < -metrics["descender"]:
        errors.append("Windows clipping metrics do not cover the design envelope.")
    geometry = data["geometry"]
    if geometry["stem_width"] != 110 or geometry["micro_gap"] != 15:
        errors.append("Stem/gap dimensions disagree with the approved brief.")
    if geometry["curves_allowed"] or geometry["allowed_edge_angles_degrees"] != [0, 45, 90, 135]:
        errors.append("The construction must remain polygonal with axis/45-degree edges.")
    if data["spacing"]["mode"] != "proportional":
        errors.append("Vantablack Gothic must use proportional metrics.")
    glyphs = data["glyphs"]
    codes = [g["codepoint"] for g in glyphs]
    if len(codes) != len(set(codes)) or set(codes) != set(range(32, 127)):
        errors.append("Initial glyph records must map each printable ASCII character exactly once.")
    if len({g["advance"] for g in glyphs}) < 2:
        errors.append("Advance widths must actually be proportional.")
    for glyph in glyphs:
        label = repr(glyph["character"])
        if glyph["character"] != chr(glyph["codepoint"]):
            errors.append(label + ": character/codepoint mismatch.")
        if type(glyph["advance"]) is not int or not 0 < glyph["advance"] <= 1000:
            errors.append(label + ": advance must be a positive integer within one em.")
        if glyph["character"] != " ":
            left, right = glyph["left_sidebearing"], glyph["right_sidebearing"]
            if (left, right) != (24, 24):
                errors.append(label + ": proposed bearings must be 24/24.")
            if glyph["advance"] - left - right < geometry["stem_width"]:
                errors.append(label + ": ink budget is narrower than one structural stem.")
    if data["status"] != "alpha" or data["outline_status"] != "implemented-alpha":
        errors.append("Expected the implemented alpha contract; review changes to the supported status.")
    link_count = 0
    for document in ROOT.rglob("*.md"):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for destination in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            destination = destination.strip().split()[0].strip("<>")
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", destination) or destination.startswith("#"):
                continue
            path_part = unquote(destination.split("#", 1)[0])
            target = (document.parent / path_part).resolve()
            link_count += 1
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(str(document.relative_to(ROOT)) + ": missing or escaping link " + destination)
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print(f"PASS: {len(glyphs)} ASCII metric records; geometry/line-metric contract; {link_count} local Markdown links.")
    print("Run tools/validate_vantablack_font.py for binary, source geometry, shaping, and raster checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
