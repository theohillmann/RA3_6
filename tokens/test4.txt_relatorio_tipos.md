# Relatório de Tipos Inferidos

**Total de linhas analisadas:** 138

**Data de geração:** 2025-11-06 22:16:47


---


## Tabela de Tipos por Linha


| Linha | Contexto | Tipo Inferido | Notação Posfixa |
|-------|----------|---------------|-----------------|
| 1 | `( int int + )` | 🔢 `int` | `INT(10) INT(8) OP(+)` |
| 2 | `( int real + )` | 🔢 `real` | `INT(10) REAL(3.5) OP(+)` |
| 3 | `( real int + )` | 🔢 `real` | `REAL(3.5) INT(10) OP(+)` |
| 4 | `( real real + )` | 🔢 `real` | `REAL(3.5) REAL(2.5) OP(+)` |
| 5 | `( int int - )` | 🔢 `int` | `INT(35) INT(13) OP(-)` |
| 6 | `( int real - )` | 🔢 `real` | `INT(35) REAL(2.5) OP(-)` |
| 7 | `( real int - )` | 🔢 `real` | `REAL(10.5) INT(3) OP(-)` |
| 8 | `( real real - )` | 🔢 `real` | `REAL(10.5) REAL(3.5) OP(-)` |
| 9 | `( int int * )` | 🔢 `int` | `INT(5) INT(6) OP(*)` |
| 10 | `( int real * )` | 🔢 `real` | `INT(5) REAL(2.5) OP(*)` |
| 11 | `( real int * )` | 🔢 `real` | `REAL(2.5) INT(4) OP(*)` |
| 12 | `( real real * )` | 🔢 `real` | `REAL(2.5) REAL(4.0) OP(*)` |
| 13 | `( int int / )` | 🔢 `real` | `INT(27) INT(9) OP(/)` |
| 14 | `( int int / ) #2` | 🔢 `real` | `INT(10) INT(3) OP(/)` |
| 15 | `( int real / )` | 🔢 `real` | `INT(10) REAL(3.5) OP(/)` |
| 16 | `( real int / )` | 🔢 `real` | `REAL(10.5) INT(3) OP(/)` |
| 17 | `( real real / )` | 🔢 `real` | `REAL(10.5) REAL(2.5) OP(/)` |
| 18 | `( int int % )` | 🔢 `int` | `INT(17) INT(6) OP(%)` |
| 19 | `( int int % ) #2` | 🔢 `int` | `INT(100) INT(7) OP(%)` |
| 20 | `( int real % )` | ❌ `error` | `INT(10) REAL(3.5) OP(%)` |
| 21 | `( real int % )` | ❌ `error` | `REAL(3.5) INT(2) OP(%)` |
| 22 | `( real real % )` | ❌ `error` | `REAL(3.5) REAL(2.5) OP(%)` |
| 23 | `( int int ^ )` | 🔢 `int` | `INT(4) INT(3) OP(^)` |
| 24 | `( int int ^ ) #2` | 🔢 `int` | `INT(2) INT(10) OP(^)` |
| 25 | `( real int ^ )` | 🔢 `real` | `REAL(2.5) INT(3) OP(^)` |
| 26 | `( real int ^ ) #2` | 🔢 `real` | `REAL(4.0) INT(2) OP(^)` |
| 27 | `( int real ^ )` | ❌ `error` | `INT(4) REAL(3.5) OP(^)` |
| 28 | `( real real ^ )` | ❌ `error` | `REAL(2.5) REAL(2.5) OP(^)` |
| 29 | `( int int ^ ) #3` | 🔢 `int` | `INT(4) INT(5) OP(^)` |
| 30 | `( int int < )` | ✅ `bool` | `INT(12) INT(1) OP(<)` |
| 31 | `( int int < ) #2` | ✅ `bool` | `INT(1) INT(12) OP(<)` |
| 32 | `( real int < )` | ✅ `bool` | `REAL(3.5) INT(5) OP(<)` |
| 33 | `( int real < )` | ✅ `bool` | `INT(5) REAL(3.5) OP(<)` |
| 34 | `( real real < )` | ✅ `bool` | `REAL(3.5) REAL(5.5) OP(<)` |
| 35 | `( int int <= )` | ✅ `bool` | `INT(5) INT(5) OP(<=)` |
| 36 | `( int int <= ) #2` | ✅ `bool` | `INT(5) INT(3) OP(<=)` |
| 37 | `( real real <= )` | ✅ `bool` | `REAL(3.5) REAL(3.5) OP(<=)` |
| 38 | `( int int > )` | ✅ `bool` | `INT(10) INT(5) OP(>)` |
| 39 | `( int int > ) #2` | ✅ `bool` | `INT(5) INT(10) OP(>)` |
| 40 | `( real real > )` | ✅ `bool` | `REAL(5.5) REAL(3.5) OP(>)` |
| 41 | `( int int >= )` | ✅ `bool` | `INT(10) INT(10) OP(>=)` |
| 42 | `( int int >= ) #2` | ✅ `bool` | `INT(5) INT(10) OP(>=)` |
| 43 | `( int int == )` | ✅ `bool` | `INT(10) INT(10) OP(==)` |
| 44 | `( int int == ) #2` | ✅ `bool` | `INT(10) INT(5) OP(==)` |
| 45 | `( real real == )` | ✅ `bool` | `REAL(3.5) REAL(3.5) OP(==)` |
| 46 | `( int int != )` | ✅ `bool` | `INT(10) INT(5) OP(!=)` |
| 47 | `( int int != ) #2` | ✅ `bool` | `INT(10) INT(10) OP(!=)` |
| 48 | `( ( int int < ) int int if )` | 🔢 `int` | `INT(1) INT(12) OP(<) INT(100) INT(200) IF` |
| 49 | `( ( int int > ) real real if )` | 🔢 `real` | `INT(10) INT(5) OP(>) REAL(3.5) REAL(2.5) IF` |
| 50 | `( ( int int == ) int int if )` | 🔢 `int` | `INT(5) INT(5) OP(==) INT(10) INT(20) IF` |
| 51 | `( ( int int < ) int real if )` | 🔢 `real` | `INT(1) INT(12) OP(<) INT(100) REAL(2.5) IF` |
| 52 | `( ( int int > ) real int if )` | 🔢 `real` | `INT(10) INT(5) OP(>) REAL(3.5) INT(20) IF` |
| 53 | `( int int int if )` | ❌ `error` | `INT(10) INT(100) INT(200) IF` |
| 54 | `( real int int if )` | ❌ `error` | `REAL(3.5) INT(100) INT(200) IF` |
| 55 | `( ( int int > ) int while )` | ⚪ `void` | `INT(10) INT(5) OP(>) INT(100) WHILE` |
| 56 | `( ( int int < ) real while )` | ⚪ `void` | `INT(1) INT(12) OP(<) REAL(3.5) WHILE` |
| 57 | `( ( int int == ) int while )` | ⚪ `void` | `INT(5) INT(5) OP(==) INT(42) WHILE` |
| 58 | `( int int while )` | ⚪ `void` | `INT(10) INT(100) WHILE` |
| 59 | `( real int while )` | ⚪ `void` | `REAL(3.5) INT(100) WHILE` |
| 60 | `( int mem_store )` | 🔢 `int` | `INT(55) STORE(X)` |
| 61 | `( int mem_store ) #2` | 🔢 `int` | `INT(100) STORE(underscore)` |
| 62 | `( memid int - )` | 🔢 `int` | `REF(X) INT(7) OP(-)` |
| 63 | `( memid int + )` | ❌ `error` | `REF(Y) INT(3) OP(+)` |
| 64 | `( memid int * )` | ❌ `error` | `REF(UNDEFINED) INT(10) OP(*)` |
| 65 | `( int mem_store ) #3` | 🔢 `int` | `INT(10) STORE(MEM)` |
| 66 | `( int mem_store ) #4` | 🔢 `int` | `INT(20) STORE(MEM)` |
| 67 | `( int int + ) #2` | 🔢 `int` | `INT(10) INT(8) OP(+)` |
| 68 | `( int res )` | ❌ `error` | `INT(4) RES` |
| 69 | `( ( int res ) int * )` | 🔢 `int` | `INT(4) RES INT(2) OP(*)` |
| 70 | `( int ( int res ) + )` | 🔢 `int` | `INT(80) INT(4) RES OP(+)` |
| 71 | `( int int + ) #3` | 🔢 `int` | `INT(10) INT(5) OP(+)` |
| 72 | `( real real - ) #2` | 🔢 `real` | `REAL(3.5) REAL(2.5) OP(-)` |
| 73 | `( int res ) #2` | 🔢 `real` | `INT(1) RES` |
| 74 | `( int int / ) #3` | 🔢 `real` | `INT(10) INT(0) OP(/)` |
| 75 | `( int int / ) #4` | 🔢 `real` | `INT(0) INT(0) OP(/)` |
| 76 | `( int int % ) #3` | 🔢 `int` | `INT(10) INT(0) OP(%)` |
| 77 | `( ( int int + ) ( int int * ) * )` | 🔢 `int` | `INT(10) INT(5) OP(+) INT(3) INT(2) OP(*) OP(*)` |
| 78 | `( ( ( int int + ) int * ) int - )` | 🔢 `int` | `INT(2) INT(3) OP(+) INT(4) OP(*) INT(5) OP(-)` |
| 79 | `( ( int real + ) int * )` | 🔢 `real` | `INT(10) REAL(3.5) OP(+) INT(2) OP(*)` |
| 80 | `( ( int int / ) int + )` | 🔢 `real` | `INT(5) INT(2) OP(/) INT(3) OP(+)` |
| 81 | `( int ( int int < ) + )` | ❌ `error` | `INT(10) INT(12) INT(1) OP(<) OP(+)` |
| 82 | `( ( int int == ) int * )` | ❌ `error` | `INT(5) INT(5) OP(==) INT(2) OP(*)` |
| 83 | `( ( int int == ) ( int int == ) + )` | ❌ `error` | `INT(5) INT(5) OP(==) INT(1) INT(1) OP(==) OP(+)` |
| 84 | `( int int + ) #4` | 🔢 `int` | `INT(10) INT(5) OP(+)` |
| 85 | `( int int - ) #2` | 🔢 `int` | `INT(10) INT(5) OP(-)` |
| 86 | `( int int * ) #2` | 🔢 `int` | `INT(10) INT(5) OP(*)` |
| 87 | `( int int / ) #5` | 🔢 `real` | `INT(10) INT(5) OP(/)` |
| 88 | `( int int % ) #4` | 🔢 `int` | `INT(10) INT(5) OP(%)` |
| 89 | `( int int ^ ) #4` | 🔢 `int` | `INT(10) INT(5) OP(^)` |
| 90 | `( int int < ) #3` | ✅ `bool` | `INT(10) INT(5) OP(<)` |
| 91 | `( int int <= ) #3` | ✅ `bool` | `INT(10) INT(5) OP(<=)` |
| 92 | `( int int > ) #3` | ✅ `bool` | `INT(10) INT(5) OP(>)` |
| 93 | `( int int >= ) #3` | ✅ `bool` | `INT(10) INT(5) OP(>=)` |
| 94 | `( int int == ) #3` | ✅ `bool` | `INT(10) INT(5) OP(==)` |
| 95 | `( int int != ) #3` | ✅ `bool` | `INT(10) INT(5) OP(!=)` |
| 96 | `( real real + ) #2` | 🔢 `real` | `REAL(10.5) REAL(5.5) OP(+)` |
| 97 | `( real real - ) #3` | 🔢 `real` | `REAL(10.5) REAL(5.5) OP(-)` |
| 98 | `( real real * ) #2` | 🔢 `real` | `REAL(10.5) REAL(5.5) OP(*)` |
| 99 | `( real real / ) #2` | 🔢 `real` | `REAL(10.5) REAL(5.5) OP(/)` |
| 100 | `( real real % ) #2` | ❌ `error` | `REAL(10.5) REAL(5.5) OP(%)` |
| 101 | `( real int ^ ) #3` | 🔢 `real` | `REAL(10.5) INT(5) OP(^)` |
| 102 | `( real real < ) #2` | ✅ `bool` | `REAL(10.5) REAL(5.5) OP(<)` |
| 103 | `( int real + ) #2` | 🔢 `real` | `INT(10) REAL(5.5) OP(+)` |
| 104 | `( int real - ) #2` | 🔢 `real` | `INT(10) REAL(5.5) OP(-)` |
| 105 | `( int real * ) #2` | 🔢 `real` | `INT(10) REAL(5.5) OP(*)` |
| 106 | `( int real / ) #2` | 🔢 `real` | `INT(10) REAL(5.5) OP(/)` |
| 107 | `( int real % ) #2` | ❌ `error` | `INT(10) REAL(5.5) OP(%)` |
| 108 | `( int real < ) #2` | ✅ `bool` | `INT(10) REAL(5.5) OP(<)` |
| 109 | `( real int + ) #2` | 🔢 `real` | `REAL(10.5) INT(5) OP(+)` |
| 110 | `( real int - ) #2` | 🔢 `real` | `REAL(10.5) INT(5) OP(-)` |
| 111 | `( real int * ) #2` | 🔢 `real` | `REAL(10.5) INT(5) OP(*)` |
| 112 | `( real int / ) #2` | 🔢 `real` | `REAL(10.5) INT(5) OP(/)` |
| 113 | `( real int % ) #2` | ❌ `error` | `REAL(10.5) INT(5) OP(%)` |
| 114 | `( real int < ) #2` | ✅ `bool` | `REAL(10.5) INT(5) OP(<)` |
| 115 | `( int real ^ ) #2` | ❌ `error` | `INT(2) REAL(3.5) OP(^)` |
| 116 | `( real real ^ ) #2` | ❌ `error` | `REAL(4.0) REAL(2.5) OP(^)` |
| 117 | `( int real ^ ) #3` | ❌ `error` | `INT(2) REAL(1.5) OP(^)` |
| 118 | `( real mem_store )` | 🔢 `real` | `REAL(0.5) STORE(I)` |
| 119 | `( int mem_store ) #5` | 🔢 `int` | `INT(5) STORE(N)` |
| 120 | `( int mem_store ) #6` | 🔢 `int` | `INT(0) STORE(SUM)` |
| 121 | `( ( memid memid < ) ( ( memid int + ) mem_store ) while )` | ⚪ `void` | `REF(I) REF(N) OP(<) REF(I) INT(1) OP(+) STORE(I...` |
| 122 | `( int mem_store ) #7` | 🔢 `int` | `INT(1) STORE(I)` |
| 123 | `( memid memid + )` | 🔢 `int` | `REF(SUM) REF(N) OP(+)` |
| 124 | `( memid )` | 🔢 `int` | `REF(SUM)` |
| 125 | `( int mem_store ) #8` | 🔢 `int` | `INT(10) STORE(MAX)` |
| 126 | `( ( memid memid > ) ( memid ) ( memid ) if )` | 🔢 `int` | `REF(SUM) REF(MAX) OP(>) REF(SUM) REF(MAX) IF` |
| 127 | `( memid memid - )` | 🔢 `int` | `REF(MAX) REF(SUM) OP(-)` |
| 128 | `( int mem_store ) #9` | 🔢 `int` | `INT(12) STORE(A)` |
| 129 | `( int mem_store ) #10` | 🔢 `int` | `INT(9) STORE(B)` |
| 130 | `( int mem_store ) #11` | 🔢 `int` | `INT(0) STORE(R)` |
| 131 | `( ( memid memid > ) ( ( memid memid + ) mem_store ) ( int mem_store ) if )` | 🔢 `int` | `REF(A) REF(B) OP(>) REF(A) REF(B) OP(+) STORE(R...` |
| 132 | `( int mem_store ) #12` | 🔢 `int` | `INT(5) STORE(XX)` |
| 133 | `( int mem_store ) #13` | 🔢 `int` | `INT(5) STORE(YY)` |
| 134 | `( ( memid memid == ) ( ( memid int + ) mem_store ) ( memid ) if )` | 🔢 `int` | `REF(XX) REF(YY) OP(==) REF(R) INT(1) OP(+) STOR...` |
| 135 | `( ( memid int * ) )` | 🔢 `int` | `REF(R) INT(2) OP(*)` |
| 136 | `( int mem_store ) #14` | 🔢 `int` | `INT(15) STORE(Z)` |
| 137 | `( ( memid memid > ) ( ( memid memid - ) mem_store ) ( memid ) if )` | 🔢 `int` | `REF(Z) REF(R) OP(>) REF(Z) REF(R) OP(-) STORE(R...` |
| 138 | `( memid ) #2` | 🔢 `int` | `REF(R)` |


---


## Estatísticas


### Distribuição de Tipos

- 🔢 `int`: 46 (33.3%)
- 🔢 `real`: 40 (29.0%)
- ✅ `bool`: 27 (19.6%)
- ❌ `error`: 19 (13.8%)
- ⚪ `void`: 6 (4.3%)

### Taxa de Sucesso

**86.2%** das linhas foram tipadas com sucesso.
