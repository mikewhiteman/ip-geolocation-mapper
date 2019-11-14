# Dynamic IP Geolocation Map

## Overview
**Under Development**  
This is a simple utility that accepts a list of n+1 IPv4 addresses, queries them against IP geolocation database, and generates a dynamic heat map showing volume by country of origin. I've found this useful when working with large datasets of IP addresses (such as those generated by WAF, IDS, etc.) to quickly visualize threat volume by country.  

## Usage Instructions
More robust arg parsing coming shortly. Right now IPs are statically loaded via the ip_list file.

## To Do
* Accept file location argument (rather than hardcoded)
* Determine intelligent min/max key range based on `len()` of IP input list
* IPv6 support (requires tweaks in MaxMind database query)

## Example Heatmap
![Example Heatmap](demo/readme.gif)
