#!/usr/bin/env python3

"""
Generates map visual based on IP geolocation from a list of IP addresses. 
Author(s):
    Michael Whiteman (michael.s.whiteman@gmail.com)
"""

from geoip import geolite2
import geopandas as gpd
import pandas as pd
import country_converter as coco
import matplotlib as mpl
import json
from bokeh.io import output_notebook, show, output_file
from bokeh.io import curdoc
from bokeh.models import HoverTool
from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer


def import_ip_addresses():

    """
    Imports IP addresses from text file for geomapping
        Args:
            None - will be set by arg later

        Returns:
            targets (list): List of IP addresses to geomap
    """
    targets = []
    with open('ip_list.txt') as f:
        for ip in f:
            targets.append(ip)
    return targets


def geo_lookup(ip_addresses):

    """
    Looks up IP addresses using the MaxMind geoIP database
        Args:
            ip_addresses (list)

        Returns:
            countries (list): List of ISO3 country codes
    """

    countries = []
    for ip in ip_addresses:
        match = geolite2.lookup(ip.strip())
        if match:
            iso3_code = coco.convert(names=match.country, to='ISO3')
            countries.append(iso3_code)
    return countries



def generate_map(countries):

    """
    Generates Geopandas map using the converted ISO3 country codes
        Args:
            countries (list): ISO3 country codes 

        Returns:
            TBD
    """
    #Build the Pandas data frame
    data = pd.value_counts(countries).to_frame().reset_index()
    data.columns = ['Country',  'Count']
    shapefile = 'data/ne_110m_admin_0_countries.shp'

    #Read shapefile using the Geopandas library
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3',  'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']

    #Set missing countries count to 0 or else it will be invisible on the map
    for country in gdf['country_code']:
        if country not in countries:
            data = data.append({'Country':country, 'Count':0}, ignore_index=True)

    merged = gdf.merge(data, left_on = 'country_code', right_on = 'Country', how = 'left')
    merged_json = json.loads(merged.to_json())
    json_data = json.dumps(merged_json)

    return merged


def display_map(map_data):

    """
    Displays the merged frames using the Bokeh framework
        Args:
            TBD

        Returns:
            TBD
    """
    #Build the Pandas data frame
    map_json = json.loads(map_data.to_json())
    geo_json = json.dumps(map_json)

    #Imports GeoJSON source data
    geodata = GeoJSONDataSource(geojson = geo_json)

    #Select color pallete from brewer (https://bokeh.pydata.org/en/latest/docs/reference/palettes.html#brewer-palettes)
    color_palette = brewer['Blues'][8]

    #Reverse color order so darkest color is highest volume
    color_palette = color_palette[::-1]

    #Map colors based on data range
    color_mapper = LinearColorMapper(palette = color_palette, low = 0, high = 120) #Add logic to make this dnyamic range

    #Add mouse hover feature
    hover = HoverTool(tooltips = [ ('Country/region','@Country'),('Count', '@Count')])

    #Generate color key 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal')

    #Create figure
    display = figure(title = 'Request Frequency Based on GeoIP', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
    display.xgrid.grid_line_color = None
    display.ygrid.grid_line_color = None

    #Render patches
    display.patches('xs','ys', source = geodata,fill_color = {'field' :'Count', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)

    display.add_layout(color_bar, 'below')

    curdoc().title = "Request Frequency by Country"
    curdoc().add_root(display)

    show(display)


def main():
    
    ip_list = import_ip_addresses()
    countries = geo_lookup(ip_list)
    map_data= generate_map(countries)
    display_map(map_data)

if __name__== "__main__":
  main()
