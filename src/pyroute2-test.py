#!/usr/bin/python3

from pr2modules.netlink.rtnl.rtmsg import rtmsg
#from pr2modules.netlink.rtnl.ifinfmsg import ifinfmsg
from pyroute2 import NDB
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

def test_handler(target, event):
    print(target, event)

#print(rtmsg)
ndb = NDB()
ndb.register_handler(rtmsg, test_handler)
#routes = ndb.routes.wait(RTA_VIA='192.168.250.10')
pool = ThreadPool()
results = pool.map(ndb.routes.wait(RTA_VIA='192.168.250.10'))

print("continue work!")

#help(ndb.routes.wait())
#interface = ndb.interfaces.wait(ifname="test")
#address = ndb.addresses.wait(index=interface["index"])


pool.close()
pool.join()