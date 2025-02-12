# -*- coding: utf-8 -*-
"""
Created on Thu May 23 16:33:10 2024

@author: leiyuan
"""
from typing import Dict, List, Tuple, Union
from klayout import db


import logging

logger = logging.getLogger(__name__)


#TODO, is an example now
layermap_reverse = {(1, 0): 'nwell',
 (2, 0): 'pwell',
 (3, 0): 'ndiffusion',
 (4, 0): 'pdiffusion',
 (3, 1): 'nplus',
 (4, 1): 'pplus',
 (5, 0): 'poly',
 (6, 0): 'pdiff_contact',
 (6, 1): 'ndiff_contact',
 (7, 0): 'poly_contact',
 (8, 0): 'metal1',
 (8, 1): 'metal1_label',
 (8, 2): 'metal1_pin',
 (9, 0): 'via1',
 (10, 0): 'metal2',
 (10, 1): 'metal2_label',
 (10, 2): 'metal2_pin',
 (100, 0): 'abutment_box',
 (101, 0): 'neighbour_cells_horizontal',
 (101, 1): 'neighbour_cells_vertical'}

def remap_layers(layout: db.Layout, output_map: Dict[str, Union[Tuple[int, int], List[Tuple[int, int]]]]) -> db.Layout:
    """
    Rename layer to match the scheme defined in the technology file.
    :param layout:
    :param output_map: Output mapping from layer names to layer numbers.
    :return:
    """
    logger.debug("Remap layers.")
    layout2 = db.Layout()

    for top1 in layout.each_cell():
        top2 = layout2.create_cell(top1.name)
        layer_infos1 = layout.layer_infos()
        for layer_info in layer_infos1:

            src_layer = (layer_info.layer, layer_info.datatype)

            if src_layer not in layermap_reverse:
                msg = "Layer {} not defined in `layermap_reverse`.".format(src_layer)
                logger.warning(msg)
                dest_layers = src_layer
            else:
                src_layer_name = layermap_reverse[src_layer]

                if src_layer_name not in output_map:
                    msg = "Layer '{}' will not be written to the output. This might be alright though.". \
                        format(src_layer_name)
                    logger.warning(msg)
                    continue

                dest_layers = output_map[src_layer_name]

            if not isinstance(dest_layers, list):
                dest_layers = [dest_layers]

            src_idx = layout.layer(layer_info)
            for dest_layer in dest_layers:
                dest_idx = layout2.layer(*dest_layer)
                top2.shapes(dest_idx).insert(top1.shapes(src_idx))

    return layout2
