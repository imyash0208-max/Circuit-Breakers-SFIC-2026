import random, statistics as st

SEED, DAY_MIN = 7, 600           # 10-hour day, one step = 1 minute
CAP           = 24                # usable seats per trip (30 seats x 0.8 load, as on slide 9)
RTT           = 30                # round trip: 20 min travel + 10 min dwell
Q_ADD, Q_DROP = 40, 5             # adaptive thresholds (people waiting)

DEMAND_SCALE = 1.0                # 1.0 = base demand; try 0.75 and 1.25

def rate(t):                      # arrivals per minute, mean 10/min = 600 per hour
    import math
    return DEMAND_SCALE * (6 + 8 * math.sin(math.pi * t / DAY_MIN) ** 2)

def run(n_base, n_max=None, seed=SEED):
    random.seed(seed)
    n_max = n_max or n_base
    queue, waits, served, loads = [], [], 0, []
    buses = [i * (RTT / n_base) for i in range(n_base)]   # next time each bus is at the lot
    depot = n_max - n_base                                  # spare buses
    maxq = 0
    for t in range(DAY_MIN):
        for _ in range(int(random.gauss(rate(t), 2) + 0.5)):   # new arrivals this minute
            queue.append(t)
        maxq = max(maxq, len(queue))
        if len(queue) >= Q_ADD and depot > 0:              # adaptive: add a bus
            buses.append(t); depot -= 1
        for i, nxt in enumerate(buses):
            if nxt <= t:                                   # bus is at the lot
                take = min(len(queue), CAP)
                for _ in range(take):
                    waits.append(t - queue.pop(0))
                served += take; loads.append(take / CAP)
                buses[i] = t + RTT
        if len(queue) <= Q_DROP and len(buses) > n_base:   # adaptive: send an extra bus to depot
            buses.pop(); depot += 1
    return dict(avg_wait=st.mean(waits), p95=sorted(waits)[int(.95 * len(waits))],
                max_q=maxq, load=st.mean(loads), served=served)

if __name__ == "__main__":
    policies = [("Fixed 15", 15, 15), ("Fixed 17", 17, 17), ("Adaptive 10 to 17", 10, 17)]
    print(f"{'Demand':>7}{'RTT':>5}  {'Policy':18}{'avg wait':>9}{'p95':>6}{'max queue':>10}{'load':>7}")
    for scale in (0.75, 1.0, 1.25):
        for rtt in (25, 30, 40):
            DEMAND_SCALE, RTT = scale, rtt
            for name, b, m in policies:
                r = run(b, m)
                print(f"{scale:7.2f}{rtt:5d}  {name:18}{r['avg_wait']:9.1f}{r['p95']:6d}{r['max_q']:10d}{r['load']:7.2f}")
        print()
    # check the seed too (base case): different random arrivals, same conclusion?
    DEMAND_SCALE, RTT = 1.0, 30
    print("Seed check, base case, adaptive 10 to 17:")
    for seed in (1, 2, 3, 7):
        r = run(10, 17, seed=seed)
        print(f"  seed {seed}: avg wait {r['avg_wait']:.1f} min, p95 {r['p95']} min, load {r['load']:.2f}")
