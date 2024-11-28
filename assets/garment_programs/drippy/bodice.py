from copy import deepcopy
import numpy as np

import pygarment as pyg

from assets.bodies.body_params import BodyParameters
from assets.garment_programs.base_classes import BaseBodicePanel
from assets.garment_programs import tee
from assets.garment_programs.bodice import BodiceFrontHalf, BodiceBackHalf, BodiceHalf, Shirt
from numpy.linalg import norm


class DrippyBodiceBackHalf(BaseBodicePanel):
    """Panel for the back of basic fitted bodice block"""

    def __init__(self, name: str, body: BodyParameters, design: dict, add_top_dart: bool = False) -> None:
        super().__init__(name, body, design)

        # Overall measurements
        self.width = body['back_width'] / 2
        waist = body['waist_back_width'] / 2  
        # NOTE: no inclination on the side, since there is not much to begin with
        waist_width = self.width if waist < self.width else waist  
        shoulder_incl_angle = np.deg2rad(body['_shoulder_incl'])
        shoulder_incl = (sh_tan := np.tan(shoulder_incl_angle)) * self.width

        # Adjust to make sure length is measured from the shoulder
        # and not the de-fact side of the garment
        back_adjustment = sh_tan * (self.width - body['shoulder_w'] / 2)
        length = body['waist_line'] - back_adjustment
        top_d_width = (self.width - waist) / 6

        # Base edge loop
        self.edges.append(pyg.EdgeSeqFactory.from_verts(
            [0, 0],
            [-waist_width, 0],
            [-self.width, body['waist_line'] - body['_bust_line']],  # from the bottom
            [-self.width, length],   
            [0, length + shoulder_incl],   # Add some fabric for the neck (inclination of shoulders)
        ))
        self.edges.close_loop()

        if add_top_dart:
            # Add top dart
            bust_line = body["waist_line"] - body["_bust_line"]
            t_edge, t_interface = self.add_dart(
                pyg.EdgeSeqFactory.dart_shape(top_d_width, 0.5 * bust_line),
                self.edges[3],
                offset=self.width * 0.45 + top_d_width / 2,
            )
            self.edges.substitute(3, t_edge)
            delta_x = top_d_width * np.cos(shoulder_incl_angle)
            delta_y = top_d_width * np.sin(shoulder_incl_angle)
            t_edge[-1].end[0] += delta_x
            t_edge[-1].end[1] += delta_y

            t_edge[0].start[0] -= delta_x
            t_edge[0].start[1] -= delta_y
            self.edges[0].end[0] -= delta_x
            self.edges[0].end[1] -= delta_y
            self.edges[1].end[0] -= delta_x
            self.edges[1].end[1] -= delta_y
            self.edges[2].end[0] -= delta_x
            self.edges[2].end[1] -= delta_y
            # Take some fabric from the top to match the shoulder width
            self.interfaces = {
                "shoulder": pyg.Interface(self, t_interface),
                # Reference to the corners for sleeve and collar projections
                "shoulder_corner": pyg.Interface(
                    self, pyg.EdgeSequence(self.edges[-6], self.edges[-5])
                ),
                "collar_corner": pyg.Interface(
                    self, pyg.EdgeSequence(self.edges[-2], self.edges[-1])
                ),
            }
        else:
            self.interfaces = {
                "shoulder": pyg.Interface(self, self.edges[-2]),
                # Reference to the corners for sleeve and collar projections
                "shoulder_corner": pyg.Interface(
                    self, pyg.EdgeSequence(self.edges[-3], self.edges[-2])
                ),
                "collar_corner": pyg.Interface(
                    self, pyg.EdgeSequence(self.edges[-2], self.edges[-1])
                ),
            }
        self.interfaces.update(
            {
                "outside": pyg.Interface(self, [self.edges[1], self.edges[2]]),
                "inside": pyg.Interface(self, self.edges[-1]),
                "bottom": pyg.Interface(self, self.edges[0]),
            }
        )

        # Bottom dart as cutout -- for straight line
        if waist < self.get_width(self.edges[2].end[1] - self.edges[2].start[1]):
            w_diff = waist_width - waist
            side_adj = 0  if w_diff < 4 else w_diff / 6  # NOTE: don't take from sides if the difference is too small
            bottom_d_width = w_diff - side_adj
            # bottom_d_width /= 2   # double darts
            bottom_d_depth = 1. * (length - body['_bust_line'])  # calculated value
            bottom_d_position = body['bum_points'] / 4

            # TODOLOW Avoid hardcoding for matching with the bottoms?
            dist = bottom_d_position * 0.5  # Dist between darts -> dist between centers
            b_edge, b_interface = self.add_dart(
                pyg.EdgeSeqFactory.dart_shape(bottom_d_width, 1.2 * bottom_d_depth),
                self.edges[0], 
                offset=bottom_d_position + bottom_d_width + bottom_d_width / 2,
            )

            self.edges.substitute(0, b_edge)
            self.interfaces['bottom'] = pyg.Interface(self, b_interface)

            # Remove fabric from the sides if the diff is big enough
            b_edge[-1].end[0] += side_adj

        # default placement
        self.translate_by([0, body['height'] - body['head_l'] - length - shoulder_incl, 0])

    def get_width(self, level):
        return self.width


class DrippyBodiceHalf(BodiceHalf):
    """Definition of a half of an upper garment with sleeves and collars"""

    def __init__(self, name: str, body: BodyParameters, design: dict, fitted: bool = True) -> None:
        super(BodiceHalf, self).__init__(name)

        design = deepcopy(design)   # Recalculate freely!

        # Torso
        if fitted:
            self.ftorso = BodiceFrontHalf(
                f'{name}_ftorso', body, design).translate_by([0, 0, 30])
            self.btorso = DrippyBodiceBackHalf(
                f"{name}_btorso", body, design
            ).translate_by([0, 0, -25])
        else:
            self.ftorso = tee.TorsoFrontHalfPanel(
                f'{name}_ftorso', body, design).translate_by([0, 0, 30])
            self.btorso = tee.TorsoBackHalfPanel(
                f'{name}_btorso', body, design).translate_by([0, 0, -25])

        # Interfaces
        self.interfaces.update({
            'f_bottom': self.ftorso.interfaces['bottom'],
            'b_bottom': self.btorso.interfaces['bottom'],
            'front_in': self.ftorso.interfaces['inside'],
            'back_in': self.btorso.interfaces['inside']
        })

        # Sleeves/collar cuts
        self.sleeve = None
        self.collar_comp = None
        self.eval_dep_params(body, design)

        if design['shirt']['strapless']['v'] and fitted:  # NOTE: Strapless design only for fitted tops
            self.make_strapless(body, design)
        else:
            # Sleeves and collars
            self.add_sleeves(name, body, design)
            self.add_collars(name, body, design)
            self.stitching_rules.append((
                self.ftorso.interfaces['shoulder'], 
                self.btorso.interfaces['shoulder']
            ))  # tops

        # Main connectivity
        self.stitching_rules.append((
            self.ftorso.interfaces['outside'], self.btorso.interfaces['outside']))   # sides


class DrippyFittedShirt(pyg.Component):
    """Panel for the front of upper garments with darts to properly fit it to
    the shape"""

    def __init__(self, body: BodyParameters, design: dict, fitted: bool = True) -> None:
        name_with_params = f"{self.__class__.__name__}"
        super().__init__(name_with_params)

        design = self.eval_dep_params(design)

        self.right = DrippyBodiceHalf(f'right', body, design, fitted=fitted)
        self.left = DrippyBodiceHalf(
            f"left",
            body,
            design["left"] if design["left"]["enable_asym"]["v"] else design,
            fitted=fitted,
        ).mirror()

        self.stitching_rules.append((self.right.interfaces['front_in'],
                                     self.left.interfaces['front_in']))
        self.stitching_rules.append((self.right.interfaces['back_in'],
                                     self.left.interfaces['back_in']))

        # Adjust interface ordering for correct connectivity
        self.interfaces = {   # Bottom connection
            'bottom': pyg.Interface.from_multiple(
                self.right.interfaces['f_bottom'].reverse(),
                self.left.interfaces['f_bottom'],
                self.left.interfaces['b_bottom'].reverse(),
                self.right.interfaces['b_bottom'],)
        }

    def eval_dep_params(self, design):
        # NOTE: Support for full collars with partially strapless top
        # or combination of paneled collar styles
        # requres further development
        # TODOLOW enable this one to work
        if design["left"]["enable_asym"]["v"]:
            # Force no collars since they are not compatible with each other
            design = deepcopy(design)
            design["collar"]["component"]["style"]["v"] = None
            design["left"]["collar"]["component"] = dict(style=dict(v=None))

            # Left-right design compatibility
            design["left"]["shirt"].update(length={})
            design["left"]["shirt"]["length"]["v"] = design["shirt"]["length"]["v"]

            design["left"]["collar"].update(fc_depth={}, bc_depth={})
            design["left"]["collar"]["fc_depth"]["v"] = design["collar"]["fc_depth"][
                "v"
            ]
            design["left"]["collar"]["bc_depth"]["v"] = design["collar"]["bc_depth"][
                "v"
            ]

        return design

    def length(self):
        return self.right.length()
