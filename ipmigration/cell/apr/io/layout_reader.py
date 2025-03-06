# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

#gds reader

import klayout.db as db

import logging
logger = logging.getLogger(__name__)


def load_layout(path, circuit_name):
    '''
    Parameters
    ----------
    path : TYPE
        DESCRIPTION.
    circuit_name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    pass
    


def layout_extract(layout, cell, tech):
    """
    Extract a device level netlist of 3-terminal MOSFETs from the cell 'cell' of layout 'layout'.
    layout: db.Layout
        Layout object. 
    cell: db.Cell 
        The cell of the circuit
    tech:
        tech object
    :return: db.LayoutToNetlist object
    """

    # Without netlist comparision capabilities.
    l2n = db.LayoutToNetlist(db.RecursiveShapeIterator(layout, cell, []))
    
    layer_in_layout = [(t.layer, t.datatype) for t in layout.layer_infos()]
    layer_dict = {}
    
    for layer in tech.layer_list:
        if tech.output_map[layer] in layer_in_layout:
            layer_dict[layer] =  l2n.make_layer(layout.layer(tech.output_map[layer]),layer)
        else:
            print(layer, 'not found!')
            #logger.debug
    # rnwell = make_layer(l_nwell)
    # rpwell = make_layer(l_pwell)
    # rndiff = make_layer(l_ndiffusion)
    # # rndiff_label = make_text_layer(l_ndiffusion)
    # rpdiff = make_layer(l_pdiffusion)
    # # rpdiff_label = make_text_layer(l_pdiffusion)
    # rpoly = make_layer(l_poly)
    # # rpoly_lbl = make_layer(l_poly_label)
    # rndiff_cont = make_layer(l_ndiff_contact)
    # rpdiff_cont = make_layer(l_pdiff_contact)
    # rpoly_cont = make_layer(l_poly_contact)
    # rmetal1 = make_layer(l_metal1)
    # rmetal1_lbl = make_layer(l_metal1_label)
    # rvia1 = make_layer(l_via1)
    # rmetal2 = make_layer(l_metal2)
    # rmetal2_lbl = make_layer(l_metal2_label)
    
    #compute layers
    active = layer_dict['AA']
    nwell  = layer_dict['NW']
    pplus  = layer_dict['SP']
    nplus  = layer_dict['SN']
    poly   = layer_dict['GT']
    
    # active_in_nwell = active & nwell
    # pactive = active_in_nwell & pplus
    # pgate = pactive & poly
    # psd = pactive - pgate
    # active_outside_nwell = active - nwell
    # nactive = active_outside_nwell & nplus
    # ngate = nactive & poly
    # nsd = nactive - ngate
    
    rdiff_cont =  layer_dict['CT']
    
    rpactive = layer_dict['AA'] & layer_dict['NW']
    rpgate =   rpactive         & layer_dict['GT']
    rpsd =     rpactive         - rpgate

    rnactive = layer_dict['AA'] - layer_dict['NW']
    rngate =   rnactive         & layer_dict['GT']
    rnsd =     rnactive         - rngate

    l2n.register(rpactive, 'pactive')
    l2n.register(rpgate, 'pgate')
    l2n.register(rpsd, 'psd')

    l2n.register(rnactive, 'nactive')
    l2n.register(rngate, 'ngate')
    l2n.register(rnsd, 'nsd')

    bulk = l2n.make_layer('PW')#?

    # 3 terminal PMOS transistor device extraction
    pmos_ex = db.DeviceExtractorMOS3Transistor("PMOS")
    l2n.extract_devices(pmos_ex, {"SD": rpsd, "G": rpgate, "W": layer_dict['NW'], "tS": rpsd, "tD": rpsd, "tG": layer_dict['GT']})

    # 3 terminal NMOS transistor device extraction
    nmos_ex = db.DeviceExtractorMOS3Transistor("NMOS")
    l2n.extract_devices(nmos_ex, {"SD": rnsd, "G": rngate, "W": bulk, "tS": rnsd, "tD": rnsd, "tG": layer_dict['GT']})

    # # 4 terminal PMOS transistor device extraction
    # pmos_ex = db.DeviceExtractorMOS4Transistor("PMOS")
    # l2n.extract_devices(pmos_ex, {"SD": rpsd, "G": rpgate, "W": rnwell, "tS": rpsd, "tD": rpsd, "tG": rpoly, "tB": rnwell})
    #
    # # 4 terminal NMOS transistor device extraction
    # nmos_ex = db.DeviceExtractorMOS4Transistor("NMOS")
    # l2n.extract_devices(nmos_ex, {"SD": rnsd, "G": rngate, "W": rpwell, "tS": rnsd, "tD": rnsd, "tG": rpoly, "tB": rpwell})

    # Define connectivity for netlist extraction

    # Intra-layer? necessary?
    l2n.connect(layer_dict['CT'])
    l2n.connect(rpsd)
    l2n.connect(rnsd)
    l2n.connect(layer_dict['GT'])
    l2n.connect(layer_dict['M1'])

    # TODO: what if more than 2 metal layers?

    # Inter-layer
    l2n.connect(rpsd, rdiff_cont)
    # l2n.connect(rpsd, rpdiff_label)
    l2n.connect(rnsd, rdiff_cont)
    # l2n.connect(rnsd, rndiff_label)

    l2n.connect(layer_dict['GT'], layer_dict['CT'])
    l2n.connect(layer_dict['M1'], layer_dict['CT'])
    l2n.connect(rnsd, layer_dict['CT'])
    l2n.connect(rpsd, layer_dict['CT'])
    # l2n.connect(layer_dict['M1'], layer_dict['V1'])

    # l2n.connect(rpoly, rpoly_lbl)  # attaches labels
    l2n.connect(layer_dict['M1'], layer_dict['M1'])  # attaches labels
    # l2n.connect(rmetal2, rmetal2_lbl)  # attaches labels

    l2n.connect_global(layer_dict['NW'], 'NWELL') # VDD
    l2n.connect_global(bulk, 'PWELL') # GND

    # Perform netlist extraction
    logger.debug("Extracting netlist from layout")
    l2n.extract_netlist()
    
    cir = list(l2n.netlist().each_circuit())[0]
    nets = list(cir.each_net())
    
    shapes_of_net = {}
    for net in nets:  
        shapes_of_net[str(net)] = {}
        for layer in layer_dict:
            shapes_of_net[str(net)][layer] = []          
            
            
    for net in nets:      
        for layer in layer_dict:
            shapes_of_net[str(net)][layer].append(l2n.shapes_of_net(net,layer_dict[layer]))
        
    
    
    return l2n,shapes_of_net
    