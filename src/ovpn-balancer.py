#!/usr/bin/python3

from socket import IP_RECVRETOPTS
import paramiko
import re
import configparser
from pyroute2 import IPRoute
from pyroute2 import NDB

# RTNL - Routing Netlink программный интерфейс служит для передачи информаии между ядром Linux и пространством пользователя.

# Пример
# IPRoute низкоуровневый RTNL API, другой подход использовать высокоуровневый RTNL API - NDB 
with IPRoute() as ipr:
    
    routes = ipr.get_routes()
    iface_links = ipr.get_links('all')
    # Имя интерфейса по индексу и атрибутам
    #iface_links[1]['attrs'][0][1]

# пример для получения всех маршрутов привязанных к интерфейсу
# производим проверку по списку интерфейсов и получаем значение в объекте интерфейса - ключ словаря index
# в маршрутах индекс интерфейса представлен как элемет кортежа с 0 элементом RTA_OIF и первым индексом(число) интерфейса
    for i in iface_links[:]:
        index = iface_links.index(i)
        if iface_links[index]['attrs'][0][1] == 'tun05':
            iface_num = iface_links[index]['index']                 # получаем номер интерфейса
            #print('Index of interface is', index)
            for r in routes[:]:                                     # получаем и выводим все маршруты идущие через заданный интерфейс
                index_r = routes.index(r)
                if routes[index_r]['attrs'][3][1] == iface_num:
                    #print(routes[index_r], '\n')
                    pass
# NDB высокоуровневый RTNL(Routing Netlink) API
with NDB() as ndb:
    for record in ndb.interfaces.summary():
        print(record.ifname, record.address, record.state)
    ndb = NDB(log="debug")
    ndb.routes.wait()
    #print(ndb.routes.dump())
    # (ndb.routes.dump().join(ndb.interfaces.dump(), condition=lambda l, r: l.oif == r.index)
    # .select('dst', 'gateway', 'oif', 'ifname', 'address')
    # .transform(address=lambda x: '%s%s.%s%s.%s%s' % tuple(x.split(':')))
    # .format('csv'))
