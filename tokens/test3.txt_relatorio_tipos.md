# Relatório de Tipos Inferidos

**Total de linhas analisadas:** 10

**Data de geração:** 2025-11-07 01:30:49


---


## Tabela de Tipos por Linha


| Linha | Contexto | Tipo Inferido | Notação Posfixa |
|-------|----------|---------------|-----------------|
| 1 | `( real mem_store )` | 🔢 `real` | `REAL(0.5) STORE(I)` |
| 2 | `( int mem_store )` | 🔢 `int` | `INT(5) STORE(N)` |
| 3 | `( int mem_store ) #2` | 🔢 `int` | `INT(0) STORE(SUM)` |
| 4 | `( ( memid memid < ) ( ( memid int + ) mem_store ) while )` | ⚪ `void` | `REF(I) REF(N) OP(<) REF(I) INT(1) OP(+) STORE(I...` |
| 5 | `( int mem_store ) #3` | 🔢 `int` | `INT(1) STORE(I)` |
| 6 | `( memid memid + )` | 🔢 `int` | `REF(SUM) REF(N) OP(+)` |
| 7 | `( memid )` | 🔢 `int` | `REF(SUM)` |
| 8 | `( int mem_store ) #4` | 🔢 `int` | `INT(10) STORE(MAX)` |
| 9 | `( ( memid memid > ) ( memid ) ( memid ) if )` | 🔢 `int` | `REF(SUM) REF(MAX) OP(>) REF(SUM) REF(MAX) IF` |
| 10 | `( memid memid - )` | 🔢 `int` | `REF(MAX) REF(SUM) OP(-)` |


---


## Estatísticas


### Distribuição de Tipos

- 🔢 `int`: 8 (80.0%)
- 🔢 `real`: 1 (10.0%)
- ⚪ `void`: 1 (10.0%)

### Taxa de Sucesso

**100.0%** das linhas foram tipadas com sucesso.
