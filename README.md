# Heritage Hop: fleet and dispatch simulation (Old Delhi pilot)

Team Circuit Breakers, Netaji Subhas University of Technology
SEVA First Innovation Challenge 2026 (Registration ID REG-010-OP-343)
Team: Yash Tyagi (leader), Aditya Pratap Singh, Srijan Sachan, Alok Sisodiya
Mentor: Dr. Shantanu Das

## What this is

Heritage Hop is our concept for easing congestion in Old Delhi's heritage core (Red Fort, Chandni Chowk, Jama Masjid). Visitors park at edge lots and ride a loop of small battery-electric shuttles into the core. A sensing node on each shuttle counts passengers and reports position, and a dispatch engine adds or holds buses.

This repository holds the **fleet and dispatch simulation**: a Python model that estimates how many shuttles are needed and how long people would wait. It is a **simulated / virtual model**, not a field-measured result.

## What the model does

- Simulates a 10-hour day, one step per minute.
- Passengers arrive at the parking lot at a rate that peaks mid-day (base average 10 people per minute, about 600 per hour).
- Each shuttle carries up to 24 people per trip (30 seats x 0.8 load) and takes 30 minutes for a full loop (20 minutes travel plus 10 minutes dwell).
- Compares fixed fleets (same number of buses all day) with an adaptive policy: start with fewer buses, add one when 40 or more people are waiting, send one back to the depot when the queue drops below 5.
- Reports average wait, 95th percentile wait (p95), longest queue, bus load and people served.

## Files

| File | Purpose |
|---|---|
| `fleet_sim_nochart.py` | Base simulation, prints a results table |
| `fleet_sim_sensitivity.py` | 27 sensitivity cases (demand x round-trip time x policy) plus a seed check |
| `Fleet_Sim_nochart_result.png` | Screenshot of the base results |
| `Fleet_Sim_sensitivity_result.png` | Screenshot of the sensitivity results |

## How to run

Requires Python 3 only. No extra libraries are needed.

```
python fleet_sim_nochart.py
python fleet_sim_sensitivity.py
```

The random seed is fixed (`SEED = 7`), so results repeat exactly. Change `SEED`, `CAP`, `RTT`, `Q_ADD`, `Q_DROP` or `DEMAND_SCALE` at the top of the file to test other assumptions.

## Base results (demand 1.0, round trip 30 min)

| Policy | Avg wait (min) | p95 wait (min) | Max queue | Bus load |
|---|---|---|---|---|
| Fixed 13 | 30.5 | 66 | 723 | 0.93 |
| Fixed 15 | 9.0 | 24 | 316 | 0.84 |
| Fixed 17 | 1.1 | 4 | 79 | 0.74 |
| Adaptive 10 to 17 | 1.3 | 3 | 54 | 0.90 |

## What we learned from the model

- 15 buses is enough on average demand, but at the mid-day peak 17 buses (or adaptive 10 to 17) are needed to keep waits short.
- Round-trip time matters most. At a 40-minute loop every policy fails, so real loop and dwell times must be measured on site.
- Adaptive dispatch matches buses to demand but cannot fix a capacity shortage.
- Across seeds 1, 2, 3 and 7 the adaptive policy stays near a 1.2 to 1.3 minute average wait with 0.90 load.

## Assumptions (not much field data)

- Demand profile, loop time, dwell time and 24 usable places per trip are assumed.
- We will replace them with our own measurements from Old Delhi (vehicle counts, interviews, timed trips).
- Sources for the published figures used in the project deck are in our evidence dossier.

## Limitations

- Demand is one-way (arrivals at the lot only); there is no return flow from the core.
- Travel time per loop is fixed, with no random traffic delays.
- All shuttles are identical, and nobody leaves the queue.
- Results are modelled under these assumptions and are not field-measured.

## Development note

["The first version of the code was written with an AI assistant and was then read, tested and modified by the team."]

## License

MIT (see `LICENSE`).
