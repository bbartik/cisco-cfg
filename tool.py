
import jinja2
import yaml
import json
import sys

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='.'))

# Gather data from customer file, open the output file, load json
# Determine deployment type from data

infile = open('data1.txt','r')
outfile = open('rtr-config.cfg','w+')
data = json.load(infile)
deployment_type = data['deployment']

# Determine routing protocols from data file and set varaibles

routing_list = data['routing']

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


# The first pass configure the interface config file

cfg_intf = env.get_template('cfg-intf-temp.j2')

if deployment_type == 'single_wan_untagged_lan':
  print ('This is for an untagged LAN site')
  data['type']='single_wan_untagged_lan'
  output = cfg_intf.render(data=data)
  print (output)
  outfile.write(output)
elif deployment_type == 'single_wan_tagged_lan':
  print ('This is for a tagged LAN site')
  data['type']='single_wan_tagged_lan'
  output = cfg_intf.render(data=data)
  print (output)
  outfile.write(output)
  
# if ospf is in the data file, confiugure ospf template

if ospf:
  print ('Configuring OSPF...')
  cfg_ospf = env.get_template('cfg-ospf-temp.j2')
  output = cfg_ospf.render(data=data,ospf_index=ospf_index)
  print (output)
  outfile.write(output)

if bgp:
  print ('Configuring BGP...')
  cfg_bgp = env.get_template('cfg-bgp-temp.j2')
  output = cfg_bgp.render(data=data,bgp_index=bgp_index)
  print (output)
  outfile.write(output)


