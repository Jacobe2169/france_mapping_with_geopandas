# coding = utf-8

import matplotlib.pyplot as plt
import geopandas as gpd


class FrancePlot():
    def __init__(self, geodataframe_france_data, departement_code_column="code_insee",
                 add_departement_boundaries=False):
        self.gdf = geodataframe_france_data
        if self.gdf.crs.to_epsg() != 2154:
            self.gdf = self.gdf.to_crs(epsg=2154)

        self.dep_boundaries = False
        if add_departement_boundaries:
            self.boundaries = gpd.read_file("data/departement_shp/")
            self.boundaries = self.boundaries.to_crs(epsg=2154)
            self.dep_boundaries = True
        self.gdf["n"] = 1
        self.dep_column = departement_code_column
        self.dom_tom = ['971', '972', '973', '974', '976']
        self.pos_plot = {
            "971": (0, 0),
            "972": (1, 0),
            "973": (2, 0),
            "974": (3, 0),
            "976": (4, 0),
            "MET": (0, 1)

        }
        self.grid_layout_dimension = (5, 5)
        self.bounds = {'971': ((-6314135.79844019, -6214902.48815842),
                               (6059513.04806719, 6150818.180962203)),
                       '972': ((-6392902.221632571, -6344643.781767518),
                               (5896605.605207319, 5969827.776593054)),
                       '973': ((-6907434.038216788, -6389461.492556358),
                               (3966147.584787802, 4447253.7684013825)),
                       '974': ((10160574.364423968, 10294098.082009042),
                               (467800.2585883038, 565330.0495356396)),
                       '976': ((7701147.5351606775, 7767529.316663522),
                               (718881.8245115401, 771306.0070951525)),
                       'MET': ((99040.00733144663, 1242446.4545588917),
                               (6046527.880333825, 7110478.988363011))}
        """
        To compute bounds 
        bounds = {}

        for dom in dom_tom:
            vals = self.gdf[self.gdf.code_insee == dom].bounds.values[0]
            x_lim,y_lim = (vals[0],vals[2]),(vals[1],vals[3])
            bounds[dom] = (x_lim,y_lim)

        vals= self.gdf[~self.gdf.code_insee.isin(dom_tom)].dissolve(by="n").bounds.values[0]
        x_lim,y_lim = (vals[0],vals[2]),(vals[1],vals[3])
        bounds["MET"] = (x_lim,y_lim)
        """

    def plot(self, figsize=(20, 20), title_legend="", boundary_color="#666", boundary_width=0.5, **plot_args):

        fig = plt.figure(figsize=figsize)
        axes = {}
        for k in self.pos_plot:
            if k != "MET":
                ax = plt.subplot2grid(self.grid_layout_dimension, self.pos_plot[k])
                self.gdf.plot(ax=ax, legend=False, **plot_args)
                if self.dep_boundaries:
                    self.boundaries[self.boundaries.code_insee == k].boundary.plot(ax=ax, color=boundary_color,
                                                                                   linewidth=boundary_width)
            else:
                ax = plt.subplot2grid(self.grid_layout_dimension, self.pos_plot[k], rowspan=5, colspan=4)
                self.gdf.plot(ax=ax, legend=True, **plot_args)
                if self.dep_boundaries:
                    self.boundaries[~self.boundaries.code_insee.isin(self.dom_tom)].boundary.plot(ax=ax,
                                                                                                  color=boundary_color,
                                                                                                  linewidth=boundary_width)
            ax.set_xlim(self.bounds[k][0])
            ax.set_ylim(self.bounds[k][1])
            ax.set_axis_off()
            axes[k] = ax

        return fig, axes