import time
import argparse

from hasher import Hasher
from fcfs import FirstComeFirstServedScheduler
from rr import RoundRobinScheduler


def main():
    parser = argparse.ArgumentParser(
            prog="sched",
            description="Como algoritmos de escalonamento e sincronização se comportam diante de um cenário real",
            )

    parser.add_argument("-a", "--algo", choices=["rr", "fcfs"], required=True)
    parser.add_argument("-d", "--difficulty", default=3)
    args = parser.parse_args()

    now = time.time()
    hash_jobs = [
            Hasher(1, now + 400),
            Hasher(2, now + 500),
            Hasher(3, now + 100),
            Hasher(4, now + 1000)
    ]

    miner = None
    if args.algo == "rr":
        miner = RoundRobinScheduler(hash_jobs, args.difficulty)
    else:
        miner = FirstComeFirstServedScheduler(hash_jobs, args.difficulty)

    miner.run()
    
if __name__ == "__main__":
    main()
