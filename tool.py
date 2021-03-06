#!/usr/bin/env python

import jinja2
import yaml
import json
import sys
import argparse

# Parse the input file and pass to variable infile

parser = argparse.ArgumentParser(description='Generate Cisco IOS config.')
parser.add_argument('infile', metavar='input file', type=str, nargs=1, help='list of device ip addresses')
args = parser.parse_args()
data_file = args.infile[0]

# Create template environment

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='.'))

# Gather data from customer file, open the output file, load json
# Populating various variables for later conditions

infile = open(data_file, 'r')
data = json.load(infile)
deployment_type = data['deployment']
cfg_base = env.get_template('cfg-base.j2')
site_crit = {'deployment_type','dual_wan','dual_router','lan_tagged'}
site = { key:value for key,value in data.items() if key in site_crit }

# Determine routing protocols from data file and set varaibles

router_list = data['routers']
for router in router_list:
  routing_list = router['routing']

ospf = False
ospf_index = ([i for i, s in enumerate(routing_list) if s['protocol'] == 'ospf'])
if ospf_index:
  ospf_index = ospf_index[0]
  ospf = True

bgp = False
bgp_index = ([i for i, s in enumerate(routing_list) if s['protocol'] == 'bgp'])
if bgp_index:
  bgp_index = bgp_index[0]
  bgp = True

# These may be unnecessary as logic is built into templates now
# however dual router sites need two passes

x = 1
# data['type']='dual_wan_dual_router_untagged_lan'
# print (data['deployment_type'])
for data in data['routers']:
  outfile = "rtr-config-" + str(x) + ".cfg"
  outfile = open(outfile,'w+')
  output = cfg_base.render(data=data,site=site,ospf_index=ospf_index,bgp_index=bgp_index)
  print (output)
  outfile.write(output)
  x = x + x
