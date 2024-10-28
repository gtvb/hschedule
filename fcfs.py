# A classe `FirstComeFirstServed` herda a classe `Miner`, e utiliza o algoritmo
# do FcFs para executar todos os jobs. Isso significa que, dadas as informações
# de tempo de chegada e ticks de um `HashJob`, o `FirstComeFirstServed` ordena
# a lista de jobs por ordem de chegada e simplesmente executa a função de
# `proof_of_work` responsável pela geração de hashes. Podemos observar algumas
# coisas diante do uso desse algoritmo de escalonamento quanto à métricas de
# avaliação. O tempo de espera dos `HashJob` não escalonados será grande, mesmo
# que o `target` de hash seja de dificuldade fácil. O tempo de resposta, que
# leva em conta a primeira interação do processo disputador pelo processador,
# também não vai ser muito interessante, principalmente para o último
# `HashJob`. 
import time

from typing import List
from miner import Miner
from hash_job import HashJob

class FirstComeFirstServedScheduler(Miner):
    def __init__(self, jobs: List[HashJob], difficulty):
        super().__init__(jobs, difficulty)

        self.done = False
        self.current_job_index = 0
        self.current_job = self.hash_jobs[self.current_job_index]
    
    def schedule(self):
        if self.current_job_index + 1 >= len(self.hash_jobs):
            self.done = True
            return

        self.current_job_index += 1
        self.current_job = self.hash_jobs[self.current_job_index]

    def run_job(self):
        if not self.current_job:
            return

        print(f"Gerando hashes para o HashJob {self.current_job.id}...")
        start = time.time()
        while True:
            # Generate a SHA256 of the internal `HashJob` structure, 
            # returning its hexadecimal representation.
            hash = self.current_job.generate_hash()
            print(f"> {hash}", end="\r")

            if hash[:self.leading_zeros] == self.target:
                print(f"HashJob {self.current_job.id} completed with hash {hash}\n")
                self.current_job.done = True
                break

            # Facilitate visualization with a short sleep
            time.sleep(0.01)

        # The time used for this HashJob will be counted as wait time for the others.
        elapsed = time.time() - start
        for job in self.hash_jobs:
            if job != self.current_job and not job.done:
                job.wait_time += elapsed

    def run(self):
        # While we have jobs to process
        while not self.done:
            self.run_job()
            self.schedule()

        self.print_results()

