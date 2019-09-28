#!/usr/bin/env python3

"""
Generates map visual based on IP geolocation from a list of IP addresses
Author(s):
    Michael Whiteman (michael.s.whiteman@gmail.com)
"""

from geoip import geolite2


def import_addresses():
    targets = []
    with open('ip_list.txt') as f:
        for ip in f:
            targets.append(ip)
    return targets


def geo_lookup(ip):
    ip = ip.strip()
    match = geolite2.lookup(ip)
    if match:
        return f"Found a match! {ip} is from {match.country}"
    else:
        return f"{ip} does not have a match in Geolite DB"


def main():
    ip_list = import_addresses()
    for ip in ip_list:
        print(geo_lookup(ip))


if __name__== "__main__":
  main()