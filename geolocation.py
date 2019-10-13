#!/usr/bin/env python3

"""
Generates map visual based on IP geolocation from a list of IP addresses. 
Author(s):
    Michael Whiteman (michael.s.whiteman@gmail.com)
"""

from geoip import geolite2
import pandas as pd
import country_converter as coco


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
            countries (list) - ISO3 country codes generated from MaxMind database lookup

        Returns:
            TBD
    """


    data = pd.value_counts(countries).to_frame().reset_index()
    data.columns = ['Country',  'Count']
    shapefile = 'data/ne_110m_admin_0_countries.shp'




def main():
    ip_list = import_addresses()
    countries = geo_lookup(ip_list)


if __name__== "__main__":
  main()