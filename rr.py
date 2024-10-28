# A classe `RoundRobin` também herda a classe `Miner`, e, desta vez, age de forma
# preemptiva. Um determinado quantum de tempo dita a participação de um `HashJob`
# no processador em um dado instante de tempo. Existem portanto duas maneiras
# do controle ser passado para outro `HashJob`: Pela geração de um hash válido,
# ou pelo fim do quantum. Como pode ser observado, esse algoritmo favorecerá 
# bastante todos os `HashJob`s, já que todos terão uma chance de rodar, mas
# pode ser bastante prejudicial para o tempo de turnaround por exemplo, se 
# durante seu momento com o processador o `HashJob` não consiga gerar um hash
# válido
import time
from typing import List
from miner import Miner
from hash_job import HashJob

class RoundRobinScheduler(Miner):
    def __init__(self, jobs: List[HashJob], difficulty):
        super().__init__(jobs, difficulty)

        # Initialize the queue with a copy of jobs
        self.queue = self.hash_jobs.copy()
        self.sleep_delay = 0.01

        self.quantum_secs = 1
        self.current_job_index = 0
        self.current_job = self.queue[self.current_job_index]

    def run_job(self):
        print(f"Gerando hashes para o HashJob {self.current_job.id}...")
        end_time = self.time + self.quantum_secs

        while self.time < end_time:
            # Perform the hash generation work here
            hash = self.current_job.generate_hash()
            print(f"> {hash}", end="\r")

            if hash[:self.leading_zeros] == self.target:
                print(f"\nHashJob {self.current_job.id} completed with hash {hash}")
                self.current_job.done = True
                # Remove the job from the queue since it's done
                self.queue.pop(self.current_job_index)
                break

            self.time += self.sleep_delay
            time.sleep(self.sleep_delay)

        print()

    def run(self):
        while not self.done:
            # Check if there are still jobs left to process
            if len(self.queue) == 0:
                self.done = True
                break

            # If the current time is less than the job's arrival time, wait.
            if self.time < self.current_job.arrival_time:
                print(f"Esperando o próximo job...", end="\r")
                self.time += self.sleep_delay
                continue

            # Execute the job for the defined quantum if it is not yet done
            if not self.current_job.done:
                self.run_job()

                # Update wait time for other jobs
                for job in self.queue:
                    if job != self.current_job and not job.done:
                        job.wait_time += self.quantum_secs

            # Select the next job
            if len(self.queue) > 0:
                self.current_job_index = (self.current_job_index + 1) % len(self.queue)
                self.current_job = self.queue[self.current_job_index]

        self.print_results()
