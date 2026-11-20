"""Compare each trace against ordinary LRU on exactly the same requests."""
import random
from app import play
from baseline import admit as always


def score(policy, seed, batches):
    rng=random.Random(seed)
    base=actual=guard_base=guard_actual=0
    for k in range(batches):
        hot = list(range(rng.randrange(5,13)))
        stream=[]
        for cycle in range(8):
            for _ in range(5):
                rng.shuffle(hot)
                stream.extend(hot)
            start=1000*(1+cycle)
            stream.extend(range(start,start+rng.randrange(17,27)))
        steady=[rng.choice(hot) for _ in range(200)]
        unique=list(range(200))
        base+=play(stream,always)
        actual+=play(stream,policy)
        for trace in (steady,unique):
            guard_base+=play(trace,always)
            guard_actual+=play(trace,policy)
    return dict(traces=batches,fetches=actual,lru_fetches=base,controls=guard_actual,
                lru_controls=guard_base,passed=actual<=0.75*base and guard_actual<=1.05*guard_base)
