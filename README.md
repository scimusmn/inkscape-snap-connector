# inkscape-snap-connector

This is a little Inkscape plugin to generate snap connectors for laser cutting.

## Installation
To install, simply put `snap_connector_end.inx` and `snap_connector_end.py` in your Inkscape extensions folder (found at Edit > Preferences > System: User extensions) and restart Inkscape.

## Usage
The extension can be accessed via Extensions > Render > Snap Connector (End Type). It will prompt for twelve parameters:

1. **Material Thickness:** The thickness of the material to snap into
2. **Slot Height:** The height of the snap slots
3. **Slot Spacing:** The distance between the snap slots
4. **Inner Gutter Depth:** The depth of the inner flex gutter
5. **Inner Gutter Width:** The width of the inner flex gutter
6. **Outer Gutter Depth:** The depth of the outer flex gutter
7. **Outer Gutter Width:** The width of the outer flex gutter
8. **Finger Width:** The width of the snap finger
9. **Finger Overhang Width:** The width of the thicker overhang clip
10. **Finger Land Length:** The length of the flat region on the overhang clip
11. **Slip Angle:** The slip (forward-facing) angle in degrees
12. **Return Angle:** The return (rear-facing) angle in degrees
