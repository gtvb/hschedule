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
import random 
from pprint import pprint

class BlockchanMiner:
    def __init__(self, id, leading_zeros):
        self.id = id
        self.nonce = 0  # Start nonce with miner's unique ID
        self.leading_zeros = leading_zeros
        self.target = "0" * leading_zeros
        self.valid_hash = None
        self.mined = False

        self.add_delay_secs = 2

    def generate_hash(self):
        s = (self.id + str(self.nonce)).encode("utf-8")
        self.nonce += 1
        return hashlib.sha256(s).hexdigest()

    def run(self, allowed_miners_semaphore: threading.BoundedSemaphore, blockchain_semaphore: threading.Semaphore, blockchain):
        allowed_miners_semaphore.acquire()
        print(f"Miner `{self.id}` is allowed to hash...")

        # Mining loop
        while not self.mined:
            hash = self.generate_hash()
            print(f" > Miner `{self.id}` hash: {hash}", end="\r")

            if hash[:self.leading_zeros] == self.target:
                self.valid_hash = hash
                self.mined = True  # Mark as mined
                print(f"✅ Miner {self.id} found valid hash: {self.valid_hash}")
                break
            time.sleep(0.01)

        allowed_miners_semaphore.release()

        print(f"⏱️ Miner {self.id} is waiting to write to the blockchain...")
        blockchain_semaphore.acquire()

        print(f"⛓️ Miner {self.id} is adding block to blockchain...")
        blockchain.append({"miner": self.id, "hash": self.valid_hash})
        time.sleep(self.add_delay_secs)
        print(f"⛓️ Miner {self.id} added block to blockchain.")

        blockchain_semaphore.release()



class BlockchainSimulator:
    def __init__(self, jobs, max_miners=5):
        self.jobs = jobs
        self.allowed_miners_semaphore = threading.BoundedSemaphore(max_miners)
        self.blockchain_semaphore = threading.Semaphore(1)  # Binary semaphore for blockchain access
        self.blockchain = []

    def start(self):
        threads = [threading.Thread(target=job.run, args=[self.allowed_miners_semaphore, self.blockchain_semaphore, self.blockchain]) for job in self.jobs]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    miners = [BlockchanMiner(f"miner-{i}", random.randint(1, 3)) for i in range(1, 25)]
    print([miner.leading_zeros for miner in miners])
    sim = BlockchainSimulator(miners, max_miners=15)
    sim.start()

    print("\nFinal Blockchain State:")
    pprint(sim.blockchain)
