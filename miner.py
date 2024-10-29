# Essa classe `Miner` tem como objetivo agir como o recurso compartilhado. O 
# `Miner` oferece a capacidade de gerar hashes, e essa capacidade é demandada 
# por threads que desejam minerar um certo bloco por meio da geração de um hash
# que esteja abaixo de um determinado `target`. Para decidir qual `Hasher` será
# selecionado para execução, utilizaremos alguns algoritmos de escalonamento, 
# mais especificamente, o FcFs e o Round Robin por ora.
import time
from typing import List
from hasher import Hasher

class Miner:
    def __init__(self, jobs: List[Hasher], difficulty):
        self.hash_jobs = jobs
        self.hash_jobs.sort()

        self.time = time.time()
        self.done = False
        self.leading_zeros = difficulty
        self.target = "0" * self.leading_zeros

    def print_results(self):
        print(f"""
> Algoritmo de escalonamento: {self.__class__.__name__}
> Número de Hashers: {len(self.hash_jobs)}
> Número de zeros (dificuldade do hash): {self.leading_zeros}
        """)
        
        for job in self.hash_jobs:
            print(f"\tTempo de espera (Hasher {job.id}): {job.wait_time:.2f} seconds")

