import random, statistics, json
from task3 import *
S=7148; m=next_prime(1000+S); rng=random.Random(S)
keys=[f"SC{x:010d}" for x in rng.sample(range(10_000_000_000),5000)]
missing=[f"SC{x:010d}" for x in rng.sample(range(9_999_990_000,10_000_000_000),500)]
results={}
for hname,hfn in [("division",division_hash),("multiplication",multiplication_hash)]:
    ch=ChainedHash(m,hfn)
    for k in keys:ch.insert(k)
    suc=[ch.search(k)[1] for k in keys]
    uns=[ch.search(k)[1] for k in missing]
    op=LinearProbingHash(m,hfn)
    for k in keys:op.insert(k)
    osuc=[op.search(k)[1] for k in keys]
    ouns=[op.search(k)[1] for k in missing]
    results[hname]={"chaining":{**ch.stats(),"avg_success_probes":statistics.mean(suc),"avg_unsuccessful_probes":statistics.mean(uns)},
    "linear_probing":{**op.stats(),"avg_success_probes":statistics.mean(osuc),"avg_unsuccessful_probes":statistics.mean(ouns)}}
print(json.dumps({"m":m,"n":len(keys),"results":results},indent=2))
