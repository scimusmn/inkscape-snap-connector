#! /usr/bin/env python
'''
Copyright (C) 2020 Kate Swanson <sanine>

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
'''

__version__ = "0.1"

import inkex, simplestyle
from simplepath import formatPath
from math import tan, radians

class SnapConnectorEnd(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        
        self.OptionParser.add_option("-t", "--thickness",
                                     action="store", type="float",
                                     dest="thickness", default=10.0,
                                     help="The thickness of the material to snap into")
        self.OptionParser.add_option("-s", "--slot-height",
                                     action="store", type="float",
                                     dest="slot_height", default=10.0,
                                     help="The height of the snap slots")
        self.OptionParser.add_option("-v", "--slot-spacing",
                                     action="store", type="float",
                                     dest="slot_spacing", default=10.0,
                                     help="The distance between the snap slots")

        # inner gutter options
        self.OptionParser.add_option("-w", "--inner-gutter-depth",
                                     action="store", type="float",
                                     dest="inner_gutter_depth", default=10.0,
                                     help="The depth of the inner gutter")
        self.OptionParser.add_option("-x", "--inner-gutter-width",
                                     action="store", type="float",
                                     dest="inner_gutter_width", default=10.0,
                                     help="The width of the inner gutter")

        # outer gutter options
        self.OptionParser.add_option("-y", "--outer-gutter-depth",
                                     action="store", type="float",
                                     dest="outer_gutter_depth", default=10.0,
                                     help="The depth of the outer gutter")
        self.OptionParser.add_option("-z", "--outer-gutter-width",
                                     action="store", type="float",
                                     dest="outer_gutter_width", default=10.0,
                                     help="The width of the outer gutter")

        # finger options
        self.OptionParser.add_option("-a", "--finger-width",
                                     action="store", type="float",
                                     dest="finger_width", default=10.0,
                                     help="The width of the finger")
        self.OptionParser.add_option("-b", "--finger-overhang",
                                     action="store", type="float",
                                     dest="finger_overhang", default=10.0,
                                     help="The width of the finger's overhang")
        self.OptionParser.add_option("-c", "--finger-land",
                                     action="store", type="float",
                                     dest="finger_land", default=10.0,
                                     help="The length of the finger's land")
        self.OptionParser.add_option("-d", "--slip-angle",
                                     action="store", type="float",
                                     dest="slip_angle", default=10.0,
                                     help="The slip (forward-facing) angle in degrees")
        self.OptionParser.add_option("-e", "--return-angle",
                                     action="store", type="float",
                                     dest="return_angle", default=10.0,
                                     help="The return (rear-facing) angle in degrees")

        # units
        self.OptionParser.add_option("-u", "--unit",
                                     action="store", type="string",
                                     dest="unit", default="mm",
                                     help="The unit of the snap dimensions")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def get_points(self):
        thickness = self.options.thickness
        slot_height = self.options.slot_height
        slot_spacing = self.options.slot_spacing

        inner_gutter_depth = self.options.inner_gutter_depth
        inner_gutter_width = self.options.inner_gutter_width

        outer_gutter_depth = self.options.outer_gutter_depth
        outer_gutter_width = self.options.outer_gutter_width

        finger_width = self.options.finger_width
        finger_overhang = self.options.finger_overhang
        finger_land = self.options.finger_land
        slip_angle = self.options.slip_angle
        return_angle = self.options.return_angle

        # compute the point positions for the path
        finger_land_width = finger_overhang - finger_width
        slip_length = finger_land_width / tan(radians(slip_angle))
        return_length = finger_land_width / tan(radians(return_angle))
        finger_length = thickness + return_length + finger_land + slip_length

        beam_width = slot_height - outer_gutter_width - finger_width

        points = [ [ slot_spacing/2, finger_length ],
                   [ slot_spacing/2, finger_length + inner_gutter_depth ],
                   [ slot_spacing/2 + inner_gutter_width, finger_length + inner_gutter_depth ],
                   [ slot_spacing/2 + inner_gutter_width, slip_length + finger_land + return_length ],
                   [ slot_spacing/2 + inner_gutter_width - finger_land_width, slip_length + finger_land ],
                   [ slot_spacing/2 + inner_gutter_width - finger_land_width, slip_length ],
                   [ slot_spacing/2 + inner_gutter_width, 0 ],
                   [ slot_spacing/2 + inner_gutter_width + finger_width, 0 ],
                   [ slot_spacing/2 + inner_gutter_width + finger_width, finger_length + outer_gutter_depth ],
                   [ slot_spacing/2 + inner_gutter_width + finger_width + outer_gutter_width, finger_length + outer_gutter_depth ],
                   [ slot_spacing/2 + inner_gutter_width + finger_width + outer_gutter_width, 0 ],
                   [ slot_spacing/2 + inner_gutter_width + finger_width + outer_gutter_width + beam_width, 0 ],
                   [ slot_spacing/2 + inner_gutter_width + finger_width + outer_gutter_width + beam_width, finger_length ]
                   ]
        return points
        

    def effect(self):
        points = self.get_points()

        u = self.unittouu('1' + self.options.unit)

        path_id = self.uniqueId('path')
        self.path = g = inkex.etree.SubElement(self.current_layer, 'g', {'id':path_id})

        line_style = simplestyle.formatStyle({ 'stroke': '#000000', 'fill': 'none', 'stroke-width': str(self.unittouu('0.1px')) })

        line_path = [ [ 'M', [ 0, points[0][1]*u ]] ]

        # right snap
        for point in points:
            line_path.append([ 'L', [point[0]*u, point[1]*u] ])

        # bottom line
        line_path.append([ 'L', [points[-1][0]*u, 2*points[-1][1]*u] ])
        line_path.append([ 'L', [-points[-1][0]*u, 2*points[-1][1]*u] ])

        # left snap
        for point in reversed(points):
            line_path.append([ 'L', [-point[0]*u, point[1]*u] ])

        line_path.append([ 'Z', [] ])

        line_attrs = { 'style': line_style, 'id':path_id, 'd':formatPath(line_path) }
        inkex.etree.SubElement(self.current_layer, inkex.addNS('path', 'svg'), line_attrs)

if __name__ == '__main__':
    e = SnapConnectorEnd()
    e.affect()
    print('hello!')
        
        
        
