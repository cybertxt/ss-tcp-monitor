from prometheus_client import Summary,CollectorRegistry,push_to_gateway

smap = dict()

def define_summary_item(key):
    smap[key] = dict()
    smap[key]['j'] = 'tcp-monitor-' + key
    smap[key]['r'] = CollectorRegistry()
    smap[key]['s'] = Summary(key, 
        'Tcp ' + key + ' from ss when socket closing', 
        registry=smap[key]['r'])

def summary_observe(key, value):
    if key not in smap:
        return False
    smap[key]['s'].observe(value)
    print('observed ' + key + ':' + str(value))
    return True

def push_metrics():
    for s in smap:
        push_to_gateway('localhost:9091', job=smap[s]['j'], registry=smap[s]['r'])
    print('pushed to gateway')
