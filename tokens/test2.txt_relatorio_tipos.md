# Relatório de Tipos Inferidos

**Total de linhas analisadas:** 11

**Data de geração:** 2025-11-07 01:30:41


---


## Tabela de Tipos por Linha


| Linha | Contexto | Tipo Inferido | Notação Posfixa |
|-------|----------|---------------|-----------------|
| 1 | `( int mem_store )` | 🔢 `int` | `INT(12) STORE(A)` |
| 2 | `( int mem_store ) #2` | 🔢 `int` | `INT(9) STORE(B)` |
| 3 | `( int mem_store ) #3` | 🔢 `int` | `INT(0) STORE(R)` |
| 4 | `( ( memid memid > ) ( ( memid memid + ) mem_store ) ( int mem_store ) if )` | 🔢 `int` | `REF(A) REF(B) OP(>) REF(A) REF(B) OP(+) STORE(R...` |
| 5 | `( int mem_store ) #4` | 🔢 `int` | `INT(5) STORE(X)` |
| 6 | `( int mem_store ) #5` | 🔢 `int` | `INT(5) STORE(Y)` |
| 7 | `( ( memid memid == ) ( ( memid int + ) mem_store ) ( memid ) if )` | 🔢 `int` | `REF(X) REF(Y) OP(==) REF(R) INT(1) OP(+) STORE(...` |
| 8 | `( ( memid int * ) )` | 🔢 `int` | `REF(R) INT(2) OP(*)` |
| 9 | `( int mem_store ) #6` | 🔢 `int` | `INT(15) STORE(Z)` |
| 10 | `( ( memid memid > ) ( ( memid memid - ) mem_store ) ( memid ) if )` | 🔢 `int` | `REF(Z) REF(R) OP(>) REF(Z) REF(R) OP(-) STORE(R...` |
| 11 | `( memid )` | 🔢 `int` | `REF(R)` |


---


## Estatísticas


### Distribuição de Tipos

- 🔢 `int`: 11 (100.0%)

### Taxa de Sucesso

**100.0%** das linhas foram tipadas com sucesso.
