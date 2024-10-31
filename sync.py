# Para desenvolver a ideia do sincronismo entre processos, e mantendo a ideia e
# a temática de criptomoedas e suas aplicações, vamos implementar um simples
# esquema onde existem alguns `Hasher`s que devem ser processados em uma fila, e
# uma blockchain fictícia, que servirá como nosso recurso compartilhado. No
# momento em que um mineiro terminar de processar um valor de hash contido em
# um `Hasher`, ele vai solicitar permissão para escrever na blockchain, o que
# é uma operação atômica (somente um mineiro deve escrever um novo "bloco") na
# blockchain por vez. Para controlar o acesso de mineiros aos `Hasher`s,
# utilizaremos um semáforo de contagem, que vai dar a permissão para que até
# `n` (sendo `n` o valor máximo suportado por esse semáforo) mineiros trabalhem
# tentando gerar um bloco válido. Qualquer valor acima disso fará com que os
# outros mineiros (threads) disponíveis aguardem o término do `Hasher` atual. 
import hashlib
import threading
import time
import argparse
import random
from pprint import pprint

class BlockchanMiner:
    def __init__(self, id, leading_zeros):
        self.id = id
        self.nonce = 0
        self.leading_zeros = leading_zeros
        self.target = "0" * leading_zeros
        self.valid_hash = None
        self.mined = False

        self.add_delay_secs = 1

    def generate_hash(self):
        s = (str(self.id) + str(self.nonce)).encode("utf-8")
        self.nonce += 1
        return hashlib.sha256(s).hexdigest()

    def run(self, allowed_miners_semaphore: threading.BoundedSemaphore, blockchain_semaphore: threading.Semaphore, blockchain):
        allowed_miners_semaphore.acquire()
        print(f"Miner `{self.id}` está gerando hashes...")

        while not self.mined:
            hash = self.generate_hash()

            if hash[:self.leading_zeros] == self.target:
                self.valid_hash = hash
                self.mined = True
                print(f"✅ Miner {self.id} achou um hash válido: {self.valid_hash}")
                break
            time.sleep(0.01)

        allowed_miners_semaphore.release()

        print(f"⏱️ Miner {self.id}  está aguardando para escrever na blockchain...")
        blockchain_semaphore.acquire()

        print(f"⛓️ Miner {self.id} está adicionando bloco na blockchain...")
        blockchain.append({"miner": self.id, "hash": self.valid_hash, "num_zeros": self.target})
        time.sleep(self.add_delay_secs)
        print(f"⛓️ Miner {self.id} adicionou o bloco na blockchain.")

        blockchain_semaphore.release()



class BlockchainSimulator:
    def __init__(self, jobs, max_miners=5):
        self.jobs = jobs
        self.allowed_miners_semaphore = threading.BoundedSemaphore(max_miners)
        self.blockchain_semaphore = threading.Semaphore(1)
        self.blockchain = []

    def start(self):
        threads = [threading.Thread(target=job.run, args=[self.allowed_miners_semaphore, self.blockchain_semaphore, self.blockchain]) for job in self.jobs]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="sync", description="Mecanismos de sincronização aplicados na geração de hashes")
    
    parser.add_argument("-n", "--njobs", required=True, type=int, help="Número de jobs")
    parser.add_argument("-m", "--allowed_miners", required=True, type=int, help="Quantos mineiros podem ser selecionados pelo semáforo de contagem")
    parser.add_argument("-s", "--seed", type=int, help="Seed para gerar os mesmos valores aleatórios, se necessário")
    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)

    ids = set()
    diffs = []

    while len(ids) < args.njobs:
        ids.add(random.randint(1, 1000))

    while len(diffs) < args.njobs:
        diffs.append(random.randint(1, 3))

    ids = list(ids)

    print("Informações geradas para os Miners:")
    for i in range(args.njobs):
        print(f"{i}: Miner {ids[i]} - Dificuldade = {diffs[i]}")
    input("Digite qualquer coisa para começar: ")

    miners = [BlockchanMiner(ids[i], diffs[i]) for i in range(args.njobs)]
    sim = BlockchainSimulator(miners, args.allowed_miners)
    sim.start()

    pprint(sim.blockchain)