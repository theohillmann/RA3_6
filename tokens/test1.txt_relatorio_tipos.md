# Relatório de Tipos Inferidos

**Total de linhas analisadas:** 20

**Data de geração:** 2025-11-06 20:53:14


---


## Tabela de Tipos por Linha


| Linha | Contexto | Tipo Inferido | Notação Posfixa |
|-------|----------|---------------|-----------------|
| 1 | `( int int + )` | 🔢 `int` | `INT(10) INT(8) OP(+)` |
| 2 | `( int int - )` | 🔢 `int` | `INT(35) INT(13) OP(-)` |
| 3 | `( int res )` | ❌ `error` | `INT(4) RES` |
| 4 | `( int int * )` | 🔢 `int` | `INT(5) INT(6) OP(*)` |
| 5 | `( int int / )` | 🔢 `int` | `INT(27) INT(9) OP(/)` |
| 6 | `( int int % )` | 🔢 `int` | `INT(17) INT(6) OP(%)` |
| 7 | `( int int ^ )` | 🔢 `int` | `INT(4) INT(3) OP(^)` |
| 8 | `( ( int res ) int * )` | 🔢 `int` | `INT(4) RES INT(2) OP(*)` |
| 9 | `( int ( int res ) + )` | 🔢 `int` | `INT(80) INT(4) RES OP(+)` |
| 10 | `( int mem_store )` | 🔢 `int` | `INT(55) STORE(X)` |
| 11 | `( memid int - )` | 🔢 `int` | `REF(X) INT(7) OP(-)` |
| 12 | `( int mem_store ) #2` | 🔢 `int` | `INT(12) STORE(MEM)` |
| 13 | `( memid int / )` | 🔢 `int` | `REF(MEM) INT(3) OP(/)` |
| 14 | `( memid int + )` | ❌ `error` | `REF(Y) INT(3) OP(+)` |
| 15 | `( int real / )` | ❌ `error` | `INT(10) REAL(3.5) OP(/)` |
| 16 | `( int real % )` | ❌ `error` | `INT(10) REAL(3.5) OP(%)` |
| 17 | `( real int % )` | ❌ `error` | `REAL(3.5) INT(2) OP(%)` |
| 18 | `( int int ^ ) #2` | 🔢 `int` | `INT(4) INT(5) OP(^)` |
| 19 | `( int res ) #2` | 🔢 `int` | `INT(1) RES` |
| 20 | `( int ( int int < ) + )` | ❌ `error` | `INT(10) INT(12) INT(1) OP(<) OP(+)` |


---


## Estatísticas


### Distribuição de Tipos

- 🔢 `int`: 14 (70.0%)
- ❌ `error`: 6 (30.0%)

### Taxa de Sucesso

**70.0%** das linhas foram tipadas com sucesso.
