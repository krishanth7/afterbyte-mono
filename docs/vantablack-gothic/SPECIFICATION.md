# Vantablack Gothic — Programmatic Font System
Version: 0.1 design specification · Status: specification only · Maintainer: Krishanth

## 1. Concept Overview

### Core thesis
Vantablack Gothic is a severe, high-density proportional display sans serif. Tall masses, compressed counters, clipped corners, and deliberately interrupted crossbars turn text into an architectural surface. It is intended for headlines, fictional aerospace telemetry, industrial identities, game titles, and dystopian HUD art direction.

The visual mood board consists of blackened steel panels, monolithic service towers, machined stencil plates, angular hazard markings, and tightly packed instrument labels. White or pale text on black emphasizes the cuts; black on white reveals counter collapse and spacing faults. Accent colors belong to the specimen interface, not the font itself.

This is a distinct design study housed alongside Afterbyte Mono. Afterbyte remains a pixel monospace concept; Vantablack is proportional and hyper-condensed. “Variable-width” here means different glyph advances, not an implemented OpenType variable font or a wdth axis.

### Design scope
The initial target is one static Regular style containing 95 printable ASCII characters plus an unencoded .notdef. Additional symbols and languages require their own coverage reviews. No font binaries, drawn alphabet, affiliation with a material manufacturer, trademark clearance, or production readiness is claimed by this specification.

### Intended reading conditions
Design first for 80–240 CSS px in the initial specimen. Also proof at 32, 48, and 64 px as stress tests. This is an initial test range, not a validated minimum size. At 1000 UPEM, a 15-unit separation is only 0.72 px at 48 px and 1.2 px at 80 px. The gaps and narrow apertures must be judged in actual rasterized output.

Use a conventional text face for body copy, dense instructions, and critical status messages. Never replace accessible source text with unlabelled outlines.

## 2. Specification Matrix

### Metrics and geometry
All outline coordinates are integer font units, with y increasing upward.

| Parameter | Value | Interpretation |
| --- | --- | --- |
| UPEM | 1000 | Em scale; not a clipping box |
| Baseline | 0 | Common origin for letters and figures |
| Cap height | 780 | Uppercase and lining numeral top |
| X-height | 580 | Lowercase body top |
| Ascender | 820 | b, d, f, h, k, l and selected marks |
| Descender | −200 | g, j, p, q, y maximum depth |
| Typographic line gap | 0 | Initial line box height 1020 |
| Vertical/horizontal stem | 110 | Heavy monolinear structural strokes |
| Default side bearings | 24 each | Measured against final ink bounds |
| Crossbar gap | 15 | Intentional detached-link clearance |
| Default chamfer | 55 × 55 | Equal x/y corner offsets |
| Ink trap depth | 15 | Initial triangular negative-space notch |
| Zero separator bar | 50 | Identification detail, distinct from a structural stem |
| Dot block | 110 × 110 | i, j, period and colon dots |
| Coordinate quantum | 1 | Round after Boolean construction |
| Edge directions | 0°, 45°, 90°, 135° modulo 180° | Axis and exact diagonal segments only |
| Curve segments | None | Polygon-only outlines |
| Overshoot | 0 | Initial rigid-grid decision |
| Default extra tracking | 0 | Bearings already supply tight spacing |
| Minimum interglyph clearance | 15 | Must pass contour collision checks after kerning |
| Baseline numerals | 0–780 | Proportional lining figures initially |

The outline extent −200…820 spans 1020 units and can exceed a 1000-unit em. Do not scale this extent down to 1000. For a TrueType build, keep head.unitsPerEm = 1000; set OS/2.sTypoAscender = 820, sTypoDescender = −200, sTypoLineGap = 0, hhea.ascent = 820, hhea.descent = −200, and hhea.lineGap = 0. Start usWinAscent = 820 and usWinDescent = 200; expand Windows clipping metrics if later reviewed glyph bounds exceed them. Set sxHeight = 580 and sCapHeight = 780 where supported. All are proposed output-table values to validate, not existing binaries.

### Proportional advance widths
The companion [system.json](system.json) enumerates every initial character and its proposed advance. Ink width = advance − 48 for ordinary non-space glyphs. Space has no contours and advances 250 units. These are starting masters, subject to reviewed changes documented in both files.

| Set | Character: advance in units |
| --- | --- |
| A–I | A:460 B:440 C:430 D:460 E:390 F:370 G:460 H:450 I:158 |
| J–R | J:330 K:440 L:360 M:620 N:470 O:460 P:420 Q:480 R:450 |
| S–Z | S:420 T:410 U:450 V:460 W:660 X:460 Y:450 Z:400 |
| a–i | a:400 b:410 c:360 d:410 e:400 f:250 g:410 h:410 i:158 |
| j–r | j:190 k:380 l:158 m:600 n:410 o:410 p:410 q:410 r:270 |
| s–z | s:360 t:260 u:410 v:400 w:580 x:400 y:400 z:350 |
| 0–9 | 0:430 1:250 2:400 3:400 4:420 5:400 6:430 7:380 8:430 9:430 |

### Construction contract
1. Build filled polygons directly. Do not apply a generic stroked path with a miter limit: it can clip the required apexes.
2. Axis strokes are exactly 110 units before intentional notch subtraction. Diagonal bands use equal x/y offsets for parallel 45° edges; their perpendicular thickness is quantized, approximately 110, and must be measured separately. Exact 110 perpendicular width and integer 45° offsets cannot both be maintained because of the square-root-of-two factor.
3. Use equal-offset chamfers; a typical bottom-right Q-tail segment changes x by +d and y by −d. A complete tail is a finite-width filled polygon, not a zero-width line.
4. Sharp V/W/M/K apexes remain unrounded. To preserve exact 45° edges in very tall condensed letters, combine vertical runs with shorter 45° segments. Do not stretch a long diagonal into a non-45° slope.
5. Interpret slashed crossbars as 45°-clipped bar ends, not long sloping bars. E/F/H/A detach the middle bar from its adjacent stems by a 15-unit horizontal gap; the A bar fits inside the leg envelope.
6. A 15-unit connection gap is an axis-measured subtraction. It is not the same measurement as a 15-unit perpendicular diagonal clearance.
7. Build counters by subtracting inner polygons from solids. Normalize winding, remove overlaps and self-intersections, and reject zero-area contours.
8. Default lowercase crossbar zone is y = 360…470; uppercase crossbar zone is y = 335…445. Use higher waists on a/e through their y = 360…470 bars. Lowercase dot blocks occupy y = 670…780.
9. Start open-letter apertures at 30 units vertical clearance, then proof C/G/c/e/s. This narrow opening is distinct from the 15-unit crossbar detachments.
10. No unreviewed negative bearings, synthetic bold, automatic smoothing, or automatic global condensation. Preserve integer coordinate constraints after every Boolean operation.

### Spacing
Start with 24-unit left and right ink bearings: two upright neighboring stems yield a nominal 48-unit channel. Proposed kern values are AV −12, AW −8, AT −8, TA −8, To −10, VA −12, WA −8, Yo −12, LT −8. These are review candidates, not measured final kerning.

Evaluate clearance over the entire outline, especially diagonal overhangs and Q tails. The 15-unit floor is a rejection threshold, not permission to squeeze all pairs to that value. Do not reduce source advances merely to simulate tracking.

## 3. Glyph Morphology Breakdown

### Uppercase A–Z
| Glyph | Structural recipe and distinguishing detail |
| --- | --- |
| A | Two vertical lower legs transition via 45° shoulders into a clipped apex. A detached middle bar has 15-unit gaps at both leg interfaces and clipped ends. Keep the counter open above the bar. |
| B | Full left stem; two stacked chamfered chambers. Upper counter is shorter than lower; cut a 15-unit trap at the waist junction without piercing the spine. |
| C | Open octagonal shell. Subtract the right-side opening and clip upper/lower terminals at 45°. Start the visible aperture at 30 units. |
| D | Left spine and a tall rectilinear bowl; two right chamfers replace a round shoulder and foot. |
| E | Spine plus full top and bottom rails. Middle rail floats 15 units off the spine; its terminal is clipped. Preserve all three levels distinctly. |
| F | E construction without the lower rail. Middle rail retains the 15-unit spine separation. |
| G | C shell plus an inward horizontal right spur and short vertical jaw. The spur must not close the C aperture. |
| H | Two 110-unit stems and a detached y=335…445 bar, separated 15 units from both stems. Stems continue to cap height. |
| I | One 110-unit vertical beam; advance 158 gives 24-unit bearings. No slab serifs. Distinguish from 1 by the latter's flag and wider advance. |
| J | High right stem, bottom chamber with chamfered corners and short left return. Open upper-left silhouette. |
| K | Left stem with upper/lower angular arms built from vertical continuations and exact 45° runs. Pointed, unsmoothed central fork. |
| L | Full spine and heavy bottom rail with a clipped outer terminal. No detached middle element. |
| M | Two outside beams; stepped inner diagonals form a sharp central valley. Wider advance accommodates the 110-unit structure. |
| N | Two outside beams connected by a vertical-plus-45° stepped diagonal. A one-piece full-height shallow diagonal is forbidden. |
| O | An octagonal square hybrid: tall rectangular shell, 55-unit corner chamfers, inset polygon counter. No Bézier circle. |
| P | Full stem and upper chamfered chamber only. Open lower-right quadrant differentiates it from R/B. |
| Q | O shell with a straight 45° lower-right tail. Plan tail within y≥−110 and width 432 ink units; verify bearings against the tail's actual bounds. |
| R | P upper chamber plus a sharp 45° leg transitioning to a vertical foot if needed for the condensed width. Trap at the bowl/leg junction. |
| S | Continuous angular ribbon through top, middle, and bottom zones. Chamfered opposing terminals and narrow, distinct apertures. |
| T | Full top beam and centered vertical spine. Clip top-beam ends without narrowing the spine. |
| U | Two stems connected by a bottom beam with 55-unit lower corner cuts; top remains open. |
| V | Tall parallel outer runs transition to exact 45° lower diagonals meeting in a sharp baseline point. |
| W | Two joined V modules with pointed valleys; use wider 660-unit advance to preserve counters. |
| X | Four vertical-end runs feed exact 45° segments into a hard central crossing. Avoid rounded joins. |
| Y | Forked upper arms converge through 45° segments into a lower stem. Keep the junction from becoming a filled block. |
| Z | Full top/bottom rails joined by a segmented vertical-plus-45° diagonal; clip opposing outer corners. |

### Lowercase a–z
| Glyph | Structural recipe and distinguishing detail |
| --- | --- |
| a | Single-storey high-waisted angular bowl, right stem, small upper-right aperture. Counter and y=360…470 waist must remain separate from e. |
| b | Ascender to 820; chamfered body chamber to 580 on the right. Lower junction receives a shallow trap. |
| c | Lowercase open octagon with matching clipped terminals and 30-unit initial aperture. |
| d | Mirror the b chamber with right ascender; redraw the junction rather than mechanically reflecting spacing. |
| e | Angular bowl with high y=360…470 horizontal bar and pinched right aperture. Bar connects the spine; right opening distinguishes it from a. |
| f | Narrow 820-unit ascender with clipped head and horizontal arm near x-height. No ornamental hook. |
| g | Single-storey body with descending right stem and angular lower return to −200; maintain two visibly separate zones. |
| h | 820-unit left ascender and stepped shoulder to a 580-unit right stem; rectangular internal opening. |
| i | 110-unit stem to 580 and a separate 110-square dot at 670…780; advance 158. |
| j | Dot aligned to its descending stem; lower return within −200. Final outlines must retain 24-unit bearings. |
| k | Ascender plus compressed K arms below x-height; sharp fork and trap. |
| l | Single ascender beam to 820, advance 158; distinguish from i by absence of a dot and from I by height in mixed text. |
| m | Three beams, two stepped shoulders, generous 600-unit advance; preserve both internal channels. |
| n | Two body beams and a stepped top shoulder; traps at shoulder junctions. |
| o | 580-unit octagonal body, inset polygon counter, no smooth curvature. |
| p | Left descender to −200 and upper-right body chamber. |
| q | Left body chamber and right descender to −200; omit the uppercase Q tail. |
| r | Body-height spine with short angular shoulder and clipped open terminal; no closed bowl. |
| s | Compact S ribbon with a slightly high waist and opposing apertures. |
| t | Stem to 700, cross-arm near 470…580, clipped short lower return. |
| u | Open top, two beams and bottom chamfered connection; differentiate from n by open shoulder. |
| v | Body-height version of V with long vertical runs and a sharp 45° lower join. |
| w | Paired v structure, advance 580; preserve central separation. |
| x | Body-height X using exact 45° central segments and vertical terminal runs. |
| y | v-like upper fork and descending angular stem to −200. Avoid a decorative curved tail. |
| z | Angular upper/lower rails and segmented diagonal to fit the 350-unit advance. |

### Numerals
| Glyph | Recipe |
| --- | --- |
| 0 | Tall chamfered shell with a centered vertical 50-unit solid separator through its counter. “Vertical slash-through” is interpreted as a vertical bar, not an oblique slash. Keep two open counter channels; do not make an empty cut. |
| 1 | Upright heavy spine with a sharp top-left 45° flag; wider than I. Small baseline foot only if proofing requires it, documented as a design revision. |
| 2 | Angular top chamber flowing into a stepped descending diagonal and full bottom rail. |
| 3 | Two open-left chambers with a hard waist and deep left notches; avoid resembling B. |
| 4 | Open upper-left triangulated structure, right stem and horizontal crossbar; diagonal uses 45° with vertical continuation. |
| 5 | Heavy top rail and left upper stem, high waist and lower-right chamber. |
| 6 | Lower closed chamber and clipped upper-left rise; upper-right aperture remains open. |
| 7 | Heavy top rail and segmented downward diagonal; no additional crossbar initially. |
| 8 | Two closed chamfered counters; upper chamber smaller, center trap keeps the waist clear. |
| 9 | Upper closed chamber with right descending structural leg ending at baseline; lower-left aperture remains open. |

Proportional figures are the default. A tabular-figure alternate set may later use a uniform advance through tnum; it is not part of the initial implemented scope.

### Punctuation and symbol system
| Group | Construction |
| --- | --- |
| . : | One or two 110-square blocks. Period y=0…110; colon y=110…220 and 450…560. |
| , ; | Square dot head plus a hard 45° descending tail; tail remains above −160. Semicolon adds the high colon block. |
| ! ? | 110-square baseline dot with a distinct gap above it. Question mark has angular upper chamber and central drop. |
| ' " | One or two heavy short vertical marks; clipped 45° feet. No round teardrops. |
| ` | Angular descending mark near ascender height; remains distinct from apostrophe. |
| - _ = | 110-unit horizontal rails; hyphen centered optically, underscore below baseline, equals uses two rails with an open channel. |
| + | Equal-weight crossing bars centered around y=390. |
| / and backslash | 45° band segment extended by vertical runs if necessary to respect width and height; neither diagonal becomes a smooth curve. |
| ( ) [ ] | Square brackets use rectilinear beams; parentheses use chamfered polygon profiles. Preserve bracket/parenthesis distinction. |
| { } | Stepped outer rails, central angular inward notch. Keep total width sufficient for the central negative space. |
| < > ^ | Exact 45° chevrons with sharp apexes; use short arms rather than distorting the angle. |
| * # | Star built from square and diagonal arms; hash from heavy crossing rails and clear internal cells. |
| % | Two small hollow chamfered chambers and an isolated 45° separator; larger advance avoids counter closure. |
| & @ | Polygonal multi-chamber constructions; ampersand has a distinct crossing, at-sign has an internal a-like element and open outer exit. |
| $ | S ribbon with centered vertical identification bar; prevent the bar from merging all internal space. |
| vertical bar | One 110-unit vertical beam with the same narrow advance as I; proof with I/l/1. |
| ~ | Stepped angular wave built from horizontal and 45° segments. |
| space | No contours; 250-unit advance. |

Initial coverage includes all ASCII punctuation listed in system.json. Planned extension: nonbreaking space, £, ¥, €, ₹, en/em dash, smart quotes, ellipsis, and four arrows. These require original sources, Unicode mapping, and tests before any support claim.

## 4. Implementation Blueprint

### Step 1 — Freeze the design contract
Review this document and system.json together. Record unresolved optical choices as issues. The JSON stores numeric targets and 95 planned glyph records, not outlines. Select and document a font-asset license before accepting drawn glyph sources. The current MIT repository license continues to cover the specification and support scripts.

### Step 2 — Define reproducible sources
Use one UTF-8 JSON record per glyph or one UFO source after selecting the compiler. Record Unicode, glyph name, advance, contour points, counter operations, and provenance. A suggested polygon record is:

```json
{
  "glyph_name": "example",
  "unicode": null,
  "advance": 450,
  "status": "draft",
  "contours": [
    {"role": "outer", "points": [[24, 0], [134, 0], [134, 780], [24, 780]]}
  ]
}
```

This isolated rectangle only illustrates the record format; it is not a complete letter or font sample. Distinguish clockwise solids from counter contours after Boolean subtraction. Keep source coordinates in font units, not SVG screen coordinates.

### Step 3 — Implement reusable geometry
Create rectangle, equal-offset chamfered-box, diagonal-band, triangle-trap, union, and subtraction primitives. Validate every source edge: horizontal, vertical, or abs(dx)=abs(dy). Quantize Boolean intersection results to the integer grid, then recheck direction and topology; rounding can invalidate a formerly valid diagonal.

For the first exact prototype, construct H at advance 450: left stem x=24…134, right stem x=316…426, both y=0…780; detached bar spans x=149…301, y=335…445. Its clipped corners must remain inside that box. This leaves the required 15-unit gaps to both stems and 24-unit bearings. Use O, A, Q, a, e, 0, and 1 as the remaining control glyphs.

### Step 4 — Choose the compiler
Recommended path: original polygon JSON → normalized contours → UFO or direct TrueType outlines → TTF → WOFF2. FontForge is one possible compiler; a FontTools-based compiler is an alternative. Pin tool versions only after a successful build and capture the actual dependency lock.

FontForge's documented Python API supplies font creation, character creation, outline pens, overlap removal, direction correction, validation, saving, and generation. Reference: [FontForge Python API](https://fontforge.org/docs/scripting/python/fontforge.html).

A FontForge adapter should:
- Create the family with em=1000 and independent typographic/hhea metrics. FontForge ascent/descent define the em split: use 800/200 to total 1000, then set the OS/2 and hhea ascender/descender values explicitly to 820/−200. Verify generated tables; do not set ascent=820 and descent=200 and accidentally create a 1020-unit em.
- Set familyname, fullname, fontname (VantablackGothic-Regular), weight, version, copyright, and the selected license metadata.
- Create .notdef first and each supported Unicode character with createChar; draw closed contours via glyphPen; set glyph.width to the proposed proportional advance.
- Normalize overlap and winding with removeOverlap and correctDirection, then validate and inspect results.
- Save editable sources and generate the TTF only after outline coverage and validation pass.
- Convert to WOFF2 with a toolchain supporting it, then reopen and compare cmap, metrics, names, and outlines.

This is a pipeline specification, not a runnable font compiler or a claim that FontForge has been installed and tested.

### Step 5 — Implement spacing and shaping
Use advance widths from JSON as initial horizontal metrics. Set post.isFixedPitch=0. Keep default shaping proportional. Add only measured pair kerning through a GPOS kern feature; do not create a fake variable-width axis. If tabular figures are later drawn, implement tnum as a separately reviewed alternate set.

### Step 6 — Validate source and binaries
The included command below validates the design contract and documentation links only:

```sh
python3 tools/validate_vantablack_spec.py
```

It cannot validate outlines that have not been drawn. A future build must additionally reject:
- Missing .notdef, duplicate Unicode mappings, unsupported advertised coverage, and empty non-space glyphs.
- Incorrect UPEM, mismatched cap/x-height metadata, clipping line metrics, or fixed-pitch flags.
- Open contours, self-intersections, zero-area contours, wrong winding, unsupported edge angles, and unintended overlaps.
- Advance widths inconsistent with source records or bearings below the reviewed limits.
- Crossbar gaps that merge, Q tails outside the clip envelope, unreadable 0/O and 1/I/l pairs, and kerning collisions.
- Missing font-license metadata, malformed required tables, or WOFF2 round-trip discrepancies.

Use an independent font validator and actual text shaping/rendering in addition to the compiler's own validation. Run proof sheets on Windows, macOS, Linux, and at least two browser engines before claiming cross-platform support.

### Step 7 — Build the specimen and release
Use actual font files in a specimen with live editable text, size and spacing controls, light/dark backgrounds, and an explicit fallback-font loading state. Include mixed case, all punctuation, telemetry columns, and ambiguous pairs at every proof size. Keep native text, visible keyboard focus, labelled controls, reduced-motion support, and a conventional fallback face.

Release an alpha only after original outlines and build validation exist. Bundle source revision, build instructions, versioned binaries, glyph coverage, font license, known limitations, and SHA-256 checksums. Do not publish placeholder binaries or present system-font art as a completed Vantablack specimen.
