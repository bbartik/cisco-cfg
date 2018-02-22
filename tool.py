
import jinja2
import yaml
import json

env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
intf_yaml = env.get_template("yaml-intf-temp.j2")

# Gather data from customer file

infile = open('data1.txt','r')
out_intf = open('rtr-config.cfg','w+')
data = json.load(infile)
deployment_type = data['deployment']

# Determine routing protocols from data file and set varaibles

routing_list = data['routing']
ospf_index = [i for i, s in enumerate(routing_list) if 'ospf' in s]
bgp_index = [i for i, s in enumerate(routing_list) if 'bgp' in s]

if ospf_index:
  ospf = True
if bgp_index:
  bgp = True

# The first pass configure the interface yaml file

if deployment_type == 'single_wan_untagged_lan':
  print ('This is for an untagged LAN site')
  data['type']='single_wan_untagged_lan'
  output = intf_yaml.render(data=data)
  out_intf.write(output)
elif deployment_type == 'single_wan_tagged_lan':
  print ('This is for a tagged LAN site')
  data['type']='single_wan_tagged_lan'
  output = intf_yaml.render(data=data)
  out_intf.write(output)

# if ospf is in the data file, confiugure ospf template

if ospf:
  print ('Configuring OSPF...')
  ospf_yaml = env.get_template("cfg-ospf-temp.j2")
  output = ospf_yaml.render(data=data,ospf_index=ospf_index)
  print (output)
  # out_intf.write(output)
  
