"""
Utilities for geospatial analysis of 311 requests and Neighborhood Councils.

1. AnimatedMap class is used to display requests for a given NC.
2. nc_choropleth is a simple function that builds a choropleth map for the given data set.
"""

from collections import defaultdict, OrderedDict

import folium
from folium import plugins




class AnimatedMap:
    """
    Wrap the annimated map so we can try it with different Neighborhood Councils.

    Usage:
      1) Create instance with boundary and 311 reports.
      2) Set for a specific NC.
      3) Access the nc_hmap property for the map.
    """
    
    def __init__(self, observations, boundaries):
        """
        observations - 311 data for all NC's and a specific request type
        boundaries - shape file with geometry's
        """
        self.observations_gdf = observations
        self.boundaries_gdf = boundaries
        self.nc_name = None
        
    def nc(self, nc_name):
        
        self.nc_name = nc_name
        
        self._nc_row = self.boundaries_gdf.query(f"name == @self.nc_name", engine='python').reset_index().iloc[0]
        
        nc_geometry = self._nc_row['geometry']
        
        self.nc_id = self._nc_row['nc_id']
        
        self._observation_subset_gdf = self.observations_gdf.query(f"nc == @self.nc_id", engine='python').reset_index()

        self.map_center = [nc_geometry.centroid.y, nc_geometry.centroid.x]
                
        self.nc_hmap = folium.Map(location = self.map_center, 
                                  tiles='Stamen Toner', 
                                  zoom_start = 14,
                                 width="100%",
                                 height="100%")
        folium.GeoJson(data=nc_geometry).add_to(self.nc_hmap)
        plugins.Fullscreen().add_to(self.nc_hmap)
        
        self._annimated_map_data()
        self._side_effect_city()
        
    def _annimated_map_data(self):
        """
        Build data sorted by day.
        """
        self.hm_data = defaultdict(list)
        for row in self._observation_subset_gdf.itertuples():
            self.hm_data[row.day].append([row.geometry.y, row.geometry.x])
    
        self.hm_data = OrderedDict(sorted(self.hm_data.items(), key=lambda t: t[0]))
        
    def _side_effect_city(self):
        plugins.HeatMapWithTime(data=list(self.hm_data.values()),
                                index=list(self.hm_data.keys()), 
                                radius=10,
                                auto_play=True,
                                max_opacity=0.8).add_to(self.nc_hmap)


def nc_choropleth(gdf, label, column_list):
    """
    Build folium choropleth.  This is a bit hard coded for analysis at hand!

    Inputs:
      gdf - geodataframe for NC's that include density and count columns
      label - count or density
      column_list - column selector

    Note:  Hacky, specific, but it works for now.
    """
    
    choropleth_map = folium.Map(location = [34.05, -118.25], zoom_start = 10)
    plugins.Fullscreen().add_to(choropleth_map)
    folium.Choropleth(
       geo_data=gdf,
       #name='Choropleth',
       data=gdf, #bulky_items_merged_gdf,
       columns=column_list, #['nc_id','count'],
       key_on="feature.properties.nc_id",
       fill_color='YlOrRd',
       #threshold_scale=myscale,
       fill_opacity=1,
       line_opacity=0.2,
       legend_name="311 " + label, #'311 request counts',
       smooth_factor=0
    ).add_to(choropleth_map)

    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    nc_info = folium.features.GeoJson(
        gdf,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'nc_id', label],
            aliases=['Neighborhood: ','NC ID: ', label + ': '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    choropleth_map.add_child(nc_info)
    choropleth_map.keep_in_front(nc_info)
    folium.LayerControl().add_to(choropleth_map)


    return choropleth_map
