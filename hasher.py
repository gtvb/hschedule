# A classe `HashJob` é responsável por ser um wrapper sobre todas as informações
# que precisamos manter para entender como os algoritmos de escalonemento se 
# comportam. Basicamente, precisamos manter o tempo de espera desse job, além 
# de providenciar a carga de trabalho básica, que se resume à geração de hashes.
import hashlib

class Hasher:
    def __init__(self, id, arrival_time):
        self.id = id
        self.arrival_time = arrival_time
        self.wait_time = 0.0
        self.nonce = 0
        self.done = False

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    # Esse método apenas une o `id` e o `nonce` em uma
    # string e os retorna para criarmos o hash
    def generate_hashable_str(self):
        s1 = str(self.id)
        s2 = str(self.nonce)
        return s1 + s2


    def generate_hash(self):
        s = self.generate_hashable_str().encode("utf-8")
        self.nonce += 1
        return hashlib.sha256(s).hexdigest()
