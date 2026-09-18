# Day 18 (continued) — Dashboard Visual Redesign

## What changed
Rebuilt the dashboard from a single-column list into a full product
layout: sidebar navigation, top bar with live greeting/time, stat cards
with icon treatments, a Detection Overview panel (trend chart + accuracy
gauge), a Flagged Rate donut, a Most Flagged Domains panel, an activity
feed, and a filterable, sortable-by-click data table for recent scans
with risk-level and status pill badges.

## Design principle maintained throughout
Every number on the dashboard traces back to a real, live prediction
stored in MySQL - nothing is fabricated or hardcoded placeholder data,
unlike a typical mockup/template. The one clearly-labeled static figure
(98% Model Precision) is the actual Day 13 cross-validated result, not
an invented number.

## Real bugs encountered and fixed during this pass
- Donut/gauge center text rendering outside the chart entirely: required
  a `position: relative` sized wrapper div (`donut-chart-box` /
  `gauge-chart-box`) around the recharts ResponsiveContainer, with the
  center label absolutely positioned at top:50%/left:50% relative to
  THAT wrapper - not the outer flex container. Multiple incremental CSS
  patches caused drift; resolved by doing one complete, from-scratch
  rewrite of both App.jsx and App.css rather than continuing to patch.
- Lesson for future iterations: for structural/layout bugs, a full file
  rewrite is often faster and more reliable than accumulating targeted
  edits, especially across a long session with many small changes.

## New functional pieces added alongside the redesign
- Manual "Scan Email" page (paste sender/subject/body, get instant score)
  as an alternative to file upload.
- Risk-level classification (High/Medium/Low) derived from the Day 13
  threshold logic, displayed as color-coded badges.
- Filterable scans table (All / Phishing / Legitimate).

## Known limitation: responsive layout incomplete

Mobile hamburger navigation was implemented and works correctly. However,
a CSS grid sizing issue causes content overlap at medium/laptop
viewport widths (~1100-1400px) when transitioning between the two-column
dashboard layout and single-column mobile layout. Root cause identified
as a grid blowout (flex/grid items default to min-width: auto rather
than 0, allowing content to overflow its column). A partial fix was
attempted but introduced a new layout issue in the top bar; reverted
pending further investigation.

**Status:** deprioritized in favor of completing Day 19 (feedback loop)
within the project timeline. Desktop (primary demo target) and mobile
(via hamburger nav) both render correctly; only the intermediate range
is affected. Documented as a known issue rather than left silently
broken - candidate for Day 20 polish time if the schedule allows.