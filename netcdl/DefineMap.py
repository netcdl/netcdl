
hosts = dict()
networks = dict()

def add_host(name, val):
    hosts[name] = val

def lookup_host(name):
    return hosts.get(name, name)

def add_network(name, val):
    networks[name] = val

def lookup_network(name):
    return networks.get(name, name)
