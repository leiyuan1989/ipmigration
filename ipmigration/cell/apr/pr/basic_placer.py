# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import json
import time,os
import logging
logger = logging.getLogger(__name__)


#

class Placer(object):
    def __init__(self, load, folder):
        self.load = load
        self.folder = folder
        


class Placement(object):
    """ Dual row cell.
    """    
    def __init__(self,columns=1):
        self.columns = columns
        self.upper = [None] * columns
        self.lower = [None] * columns    
        
    
    def __repr__(self):
        """ Pretty-print
        """

        return (
                " | ".join(['{:^16}'.format(str(t)) for t in self.upper]) +
                " || \n" +
                " | ".join(['{:^16}'.format(str(t)) for t in self.lower])
        )
    
    
    def to_json(self):
        pass
    
    def __len__(self):
        return max(len(self.upper),len(self.lower))
        
    
    
    def store_placement(self, folder, placement_file):
        """
        Dump the transistor placement to a file such that it can be loaded in a later run.
        :param placement_path: Path to the output file.
        """
        # logger.info(f"Store transistor placement: {placement_path}")
        # assert self._abstract_cell is not None, "No placement known yet."

        pmos_loc = {}
        nmos_loc = {}
        for i,t in enumerate(self.upper):
            if t:
                pmos_loc[i] = t.name+'/' + t.drain_net + '/' + t.gate_net + '/' +t.source_net
            else:
                pmos_loc[i] = 'none'
        
        for i,t in enumerate(self.lower):
            if t:
                nmos_loc[i] = t.name+'/' + t.drain_net + '/' + t.gate_net + '/' +t.source_net
            else:
                nmos_loc[i] = 'none'         


        time.strftime("%b_%d_%H_%M")
        data = {
            "cell_name": placement_file,
            "pmos_loc": pmos_loc,
            "nmos_loc": nmos_loc
        }

        placement_file = os.path.join(folder,placement_file)
        with open(placement_file, "w") as f:
            json.dump(data, f, indent=None, sort_keys=True)

    def load_placement(self, folder, placement_file, devices_list):
        """
        Load the transistor placement from a file 
        """
        data = None
        with open(os.path.join(folder,placement_file), "r") as f:
            data = json.load(f)

        



        cell_name = data["cell_name"]
        if cell_name != self.cell_name:
            logger.error(f"Placement file is for wrong cell: '{cell_name}' instead of '{self.cell_name}'")
            exit(1)

        transistor_locations = data["transistor_locations"]
        assert isinstance(transistor_locations, dict), "'transistor_locations' must be a dictionary."

        transistor_nets = data["transistor_nets"]
        assert isinstance(transistor_nets, dict), "'transistor_nets' must be a dictionary."

        transistors_by_name = {
            t.name: t for t in self._transistors_abstract
        }

        # Do sanity checks.
        present_transistor_names = set(transistor_locations.keys())
        expected_transistor_names = set(transistors_by_name.keys())

        missing_transistors = expected_transistor_names - present_transistor_names
        excess_transistors = present_transistor_names - expected_transistor_names

        # All required transistors should be given a placement.
        if missing_transistors:
            logger.error("Placement for some transistors is not defined: {}".format(", ".join(missing_transistors)))
            exit(1)

        if excess_transistors:
            logger.error("Unknown transistor names in placement file: {}".format(", ".join(excess_transistors)))
            exit(1)

        # Find the width of the cell.
        most_right_location = max((x for x, y in transistor_locations.values()))
        max_y = max((y for x, y in transistor_locations.values()))
        assert max_y <= 1

        # Create Cell object that holds the placement of the transistors.
        cell = Cell(width=most_right_location + 1)

        # Assign transistor positions.
        matrix = [cell.lower, cell.upper]
        for transistor_name, (x, y) in transistor_locations.items():
            # Get transistor.
            t = transistors_by_name[transistor_name]

            # Load the orientation of the transistor.
            source, gate, drain = transistor_nets[transistor_name]
            # Check that the nets are correct.
            assert gate == t.gate_net, f"Gate net mismatch in transistor {transistor_name}."

            # Check that the nets are correct.
            assert {source, drain} == {t.source_net, t.drain_net}, \
                f"Source/drain net mismatch in transistor {transistor_name}."

            # Flip the transistor if necessary.
            if source == t.source_net:
                # No flipping necessary.
                assert drain == t.drain_net
            else:
                t = t.flipped()

            assert gate == t.gate_net
            assert source == t.source_net
            assert drain == t.drain_net

            assert matrix[y][x] is None, f"Transistor position is used multiple times: {(x, y)}"
            matrix[y][x] = t

        self._placements = iter([cell])

