import time
import argparse
import random

from hasher import Hasher
from fcfs import FirstComeFirstServedScheduler
from rr import RoundRobinScheduler

def main():
    parser = argparse.ArgumentParser(
            prog="sched",
            description="Como algoritmos de escalonamento e sincronização se comportam diante de um cenário real",
            )

    parser.add_argument("-n", "--njobs", required=True, default=4, type=int)
    parser.add_argument("-a", "--algo", choices=["rr", "fcfs"], required=True)
    parser.add_argument("-s", "--seed", type=int)
    parser.add_argument("-d", "--difficulty", default=3)
    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)

    ids = set()
    times = set()

    while len(ids) < args.njobs:
        ids.add(random.randint(1, 1000))

    while len(times) < args.njobs:
        times.add(random.randrange(0, 4000, 100))

    ids = list(ids)
    times = list(times)
    print("Informações geradas para os Hashers:")
    for i in range(args.njobs):
        print(f"{i}: Hasher {ids[i]}: Tempo de chegada = `now()` + {times[i]} segundos")

    input("Digite qualquer coisa para começar")

    now = time.time()
    hash_jobs = [Hasher(ids[i], now + times[i]) for i in range(args.njobs)]

    miner = None
    if args.algo == "rr":
        miner = RoundRobinScheduler(hash_jobs, args.difficulty)
    else:
        miner = FirstComeFirstServedScheduler(hash_jobs, args.difficulty)

    miner.run()
    miner.print_results()
    
if __name__ == "__main__":
    main()