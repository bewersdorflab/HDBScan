
from PYME.recipes.base import register_module, ModuleBase, Filter, OutputModule
from PYME.recipes.traits import Input, Output, Float, Enum, CStr, Bool, Int, List, DictStrStr, DictStrList, ListFloat, ListStr, Button, ToolbarButton
import matplotlib as plt
import numpy as np
import pylab
from PIL import Image
from PYME.IO import tabular

from PYME.recipes.tablefilters import FilterTable
from PYME.recipes.base import ModuleCollection
# from dye_kinetics.python_microscopy.recipe_modules import kinetics_base

class HDBScan(object):
    def __init__(self, vis_frame):
        self.vis_frame = vis_frame
        self.pipeline = vis_frame.pipeline

        vis_frame.AddMenuItem('Fitting', 'HDBScan', self.OnHDBScan, helpText='')


    def OnClumpHDBSCAN(self, event=None):
        from matplotlob import pylab
        """
        Runs HDBSCAN clustering algorithm from https://github.com/scikit-learn-contrib/hdbscan and appends the results to the pipeline.
        Via the HDBSCANClustering in the localisations recipes module

        Args exposed in the GUI
            min_clump_size: The minimum size of clusters. Technically the only required parameter.
            search_radius: Extract DBSCAN clustering based on search radius. Skipped if 0 or None.
        """

        from PYME.recipes import localisations

        clumper = localisations.HDBSCANClustering()

        if clumper.configure_traits(kind='modal'):
            namespace = {clumper.input_name: self.pipeline}
            clumper.execute(namespace)

            for key in [clumper.clump_column_name, clumper.clump_prob_column_name, clumper.clump_dbscan_column_name]:

                if key in namespace[clumper.output_name].keys():
                    # print('type of the pipeline', type(self.pipeline))
                    # print(dir(self.pipeline))
                    self.pipeline.addColumn(key, namespace[clumper.output_name][key])
        pylab.figure()
        pylab.scatter(np.unique(self.pipeline['t']), np.unique(self.pipeline['t'], return_counts=True)[1])
        pylab.xlabel('frame index')
        pylab.ylabel('localisation count')


def Plug(vis_frame):
    vis_frame.hdbscan_manager = HDBScan(vis_frame)