import logging
from typing import Dict, List, Tuple
from klayout import db
import os

from .basic_writer import remap_layers
# from ..layout import layers

logger = logging.getLogger(__name__)


class OasisWriter:
    """
    Writer for OASIS output.
    """

    def __init__(self,
                 db_unit: float,
                 output_map: Dict[str, Tuple[int, int]]):
        self.db_unit = db_unit
        self.output_map = output_map

    def write_layout(self,
                     layout: db.Layout,
                     pin_geometries: Dict[str, List[Tuple[str, db.Shape]]],
                     top_cell: db.Cell,
                     output_dir: str,
                     ) -> None:
        # Re-map layers
        layout = remap_layers(layout, self.output_map)

        # Set database unit.
        # klayout expects dbu to be in µm, the tech file takes it in meters.
        layout.dbu = self.db_unit * 1e6
        logger.debug("dbu = {} µm".format(layout.dbu))

        # Possibly scale the layout.
        scaling_factor = 1
        if scaling_factor != 1:
            logger.info("Scaling layout by factor {}".format(scaling_factor))
            layout.transform(db.DCplxTrans(scaling_factor))

        
        save_options = db.SaveLayoutOptions()
        save_options.oasis_permissive = True
        
        # Write OAS.
        oasis_file_name = '{}.oas'.format(top_cell.name)
        oasis_out_path = os.path.join(output_dir, oasis_file_name)
        logger.info("Write OASIS: %s", oasis_out_path)
        layout.write(oasis_out_path, save_options)
