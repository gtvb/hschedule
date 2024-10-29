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

# A classe `BlockchanMiner` é um pouco diferente da classe `Miner` definida na parte
# de escalonamento.
class BlockchanMiner:
    def __init__(self, id, leading_zeros):
        self.id = id
        self.nonce = 0
        self.done = False
        self.leading_zeros = leading_zeros
        self.target = "0" * leading_zeros

        self.valid_hash = None

    def generate_hash(self):
        s = str(self.nonce).encode("utf-8")
        self.nonce += 1
        return hashlib.sha256(s).hexdigest()
    
    def run(self, allowed_miners_semaphore: threading.BoundedSemaphore, blockchain_semaphore: threading.Semaphore, blockchain):
        allowed_miners_semaphore.acquire()
        print(f"Miner {self.id} está executando...")
        while True:
            hash = self.generate_hash()
            print(f"> {hash}", end="\r")

            if hash[:self.leading_zeros] == self.target:
                allowed_miners_semaphore.release()
                self.valid_hash = hash
                break

            time.sleep(0.01)

        blockchain_semaphore.acquire()
        print(f"Miner {self.id} conseguiu permissão para escrever na blockchain, adicionando...")
        blockchain.append({ "miner": self.id, "hash": self.valid_hash })
        blockchain_semaphore.release()

class BlockchainSimluator:
    def __init__(self, jobs, max_miners=5):
        self.jobs = jobs
        # Esse semáforo permite que controlemos o número de mineiros gerando hashes
        self.allowed_miners_semaphore = threading.BoundedSemaphore(max_miners)
        # Esse semáforo controla a escrita na blockchain
        self.blockchain_semaphore = threading.Semaphore()
        self.blockchain = []

    def start(self):
        threads = [threading.Thread(target=job.run, args=[self.allowed_miners_semaphore, self.blockchain_semaphore, self.blockchain]) for job in self.jobs]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    miners = [
        BlockchanMiner(1, 2),
        BlockchanMiner(2, 2),
        BlockchanMiner(3, 2),
        BlockchanMiner(4, 2),
        BlockchanMiner(5, 2),
        BlockchanMiner(6, 2)
    ]

    sim = BlockchainSimluator(miners, max_miners=3)
    sim.start()

    print(sim.blockchain)