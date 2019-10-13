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
    targets = []
    with open('ip_list.txt') as f:
        for ip in f:
            targets.append(ip)
    return targets


def geo_lookup(ip_addresses):
    countries = []
    for ip in ip_addresses:
        match = geolite2.lookup(ip.strip())
        if match:
            iso3_code = coco.convert(names=match.country, to='ISO3')
            countries.append(iso3_code)
    return countries



# def generate_map(countries):
#     data = pd.value_counts(countries).to_frame().reset_index()



def main():
    ip_list = import_addresses()
    countries = geo_lookup(ip_list)


if __name__== "__main__":
  main()