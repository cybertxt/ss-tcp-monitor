import metrics_processor as mp
import os

def prepare_summaries():
    mp.define_summary_item('cwnd')
    mp.define_summary_item('bytes_acked')
    mp.define_summary_item('delivery_rate')
    mp.define_summary_item('busy')
    mp.define_summary_item('minrtt')

def try_fetch_kv(k, l, suffix):
    idx = l.find(k)
    if idx == -1:
        return False
    idx_end = l.find(suffix, idx+len(k)+1)
    if idx_end == -1:
        idx_end = None
    value = float(l[idx+len(k)+1 : idx_end])
    ret = mp.summary_observe(k, value)
    return ret

def process_line(l):
    try_fetch_kv('cwnd', l, ' ')       
    try_fetch_kv('bytes_acked', l, ' ')       
    try_fetch_kv('delivery_rate', l, 'bps')       
    try_fetch_kv('busy', l, 'ms')       
    return try_fetch_kv('minrtt', l, ' ')       

if __name__ == '__main__':
    prepare_summaries()
    while True:
        out = os.popen('ss -Eitn')
        c = 0
        while True:
            l = out.readline()
            if not l:
                break
            if process_line(l):
                c += 1
            if c % 10 == 0:
                mp.push_metrics()
