### `hschedule`

Para utilizar o programa de escalonamento utilizando o binário `python`, basta executar: `python schedule.py -h` e ver as opções
```
usage: sched [-h] -n NJOBS -a {rr,fcfs} [-s SEED] [-d DIFFICULTY]

Como algoritmos de escalonamento se comportam diante de um cenário real

options:
  -h, --help            show this help message and exit
  -n NJOBS, --njobs NJOBS
                        Número de jobs
  -a {rr,fcfs}, --algo {rr,fcfs}
                        Algoritmo que será utilizado, podendo ser `rr` (Round Robin) ou `fcfs` (First Come First Served)
  -s SEED, --seed SEED  Seed para gerar os mesmos valores aleatórios, se necessário
  -d DIFFICULTY, --difficulty DIFFICULTY
                        Define o nível de dificuldade. Quanto maior, mais difícil
```

Para utilizar o programa de sincronização utilizando o binário `python`, basta executar: `python sync.py -h` e ver as opções
```
usage: sync [-h] -n NJOBS -m ALLOWED_MINERS [-s SEED]

Mecanismos de sincronização aplicados na geração de hashes

options:
  -h, --help            show this help message and exit
  -n NJOBS, --njobs NJOBS
                        Número de jobs
  -m ALLOWED_MINERS, --allowed_miners ALLOWED_MINERS
                        Quantos mineiros podem ser selecionados pelo semáforo de contagem
  -s SEED, --seed SEED  Seed para gerar os mesmos valores aleatórios, se necessário
```