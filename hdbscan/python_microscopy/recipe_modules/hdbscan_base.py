from PYME.recipes.base import register_module, ModuleBase, Filter, OutputModule
from PYME.recipes.traits import Input, Output, Float, Enum, CStr, Bool, Int, List, DictStrStr, DictStrList, ListFloat, ListStr, Button, ToolbarButton
import matplotlib as plt
import numpy as np
import pylab
from PIL import Image
from PYME.IO import tabular
from PYME.Analysis.BleachProfile.kinModels import *
# from geometric_negative_binomial_fitting import fitting_setup
# from PYME.recipes import modules

from PYME.LMVis.pipeline import *


@register_module('HDBSCANClustering')
class HDBSCANClustering(ModuleBase):
    """
    Performs HDBSCAN clustering on input dictionary

    Parameters
    ----------

        minPtsForCore: The minimum size of clusters. Technically the only required parameter.
        searchRadius: Extract DBSCAN clustering based on search radius. Skipped if 0 or None.

    Notes
    -----

    See https://github.com/scikit-learn-contrib/hdbscan
    Lots of other parameters not mapped.

    """
    input_name = Input('filtered')
    # input_vert = Input('vert')
    columns = ListStr(['x', 'y'])
    search_radius = Float()
    min_clump_size = Int(100)
    clump_column_name = CStr('hdbscan_id')
    clump_prob_column_name = CStr('hdbscan_prob')
    clump_dbscan_column_name = CStr('dbscan_id')
    output_name = Output('hdbscan_clustered')

    def execute(self, namespace):

        # print('testing showpoints again')
        # print(namespace['showplots'])
        inp = namespace[self.input_name]
        mapped = tabular.mappingFilter(inp)
        # vert_data = namespace[self.input_vert]
        import hdbscan
        clusterer = hdbscan.HDBSCAN(min_cluster_size=self.min_clump_size)

        clusterer.fit(np.vstack([inp[k] for k in self.columns]).T)

        # Note that hdbscan gives unclustered points label of -1, and first value starts at 0.
        # shift hdbscan labels up by one to match existing convention that a clumpID of 0 corresponds to unclumped
        mapped.addColumn(str(self.clump_column_name), clusterer.labels_ + 1)
        mapped.addColumn(str(self.clump_prob_column_name), clusterer.probabilities_)

        if not self.search_radius is None and self.search_radius > 0:
            #Extract dbscan clustering from hdbscan clusterer
            dbscan = clusterer.single_linkage_tree_.get_clusters(self.search_radius, self.min_clump_size)

            # shift dbscan labels up by one to match existing convention that a clumpID of 0 corresponds to unclumped
            mapped.addColumn(str(self.clump_dbscan_column_name), dbscan + 1)

        # propogate metadata, if present
        try:
            mapped.mdh = inp.mdh
            print('testing for mdh')
        except AttributeError:
            pass

        namespace[self.output_name] = mapped
        print('finished clustering')
