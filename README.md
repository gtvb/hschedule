### `hschedule`

Esse simples projeto utiliza alguns a técnica de escalonamento para demonstrar
como uma tarefa real pode ser afetada pelas regras desses algoritmos.
Basicamente, escolheu-se o cenário da geração de hashes para mineração de um
"bloco" na blockchain como cenário real. Diante disso, temos tarefas (classe
`HashJob`) que competem para ser enviadas ao mineiro (classe `Miner`), que no
caso se comporta como nosso recurso de processamento. 

```
usage: sched [-h] -a {rr,fcfs} [-d DIFFICULTY]

Como algoritmos de escalonamento e sincronização se comportam diante de um
cenário real

options:
  -h, --help            show this help message and exit
  -a {rr,fcfs}, --algo {rr,fcfs}
  -d DIFFICULTY, --difficulty DIFFICULTY
```
