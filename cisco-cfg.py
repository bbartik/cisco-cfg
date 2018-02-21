
import jinja2

def debug(text):
  print (text)
  return ''

#vlanDict = {'123': 'TEST-VLAN-123', '234': 'TEST-VLAN-234', '345': 'TEST-VLAN-345'}

myCfgDict = {
  "hostname" : "Wan-Router-1",
  "domain_name" : "bb.lab",
  "local_admin" : "cisco",
  "local_password" : "cisco",
  "wan_intf" : "Ethernet1/1",
  "wan_ip" : "100.1.1.1",
  "wan_mask" : "255.255.255.0",
  "lan_intf" : "Ethernet1/2",
  "lan_ip" : "192.168.1.1",
  "lan_mask" : "255.255.255.0",
  "ospf_proc" : "1",
  "ospf_net" : "192.168.1.0",
  "ospf_mask" : "0.0.0.255",
  "ospf_area" : "1",
  "bgp_asn" : "65000",
  "bgp_net" : "192.168.1.0",
  "bgp_mask" : "255.255.255.0",
  "bgp_nbr_ip" : "100.1.1.2",
  "bgp_nbr_asn" : "100"
}
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
env.filters['debug']=debug

template = env.get_template("ios-template.cfg")

output = template.render(cfg=myCfgDict)
print (output)





