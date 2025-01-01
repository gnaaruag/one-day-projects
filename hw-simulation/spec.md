### implements a simplified 4 bit ALU 

#### Inputs

- 4 bit A (A<sub>3</sub>A<sub>2</sub>A<sub>1</sub>A<sub>0</sub>) - Operand
- 4 bit B (B<sub>3</sub>B<sub>2</sub>B<sub>1</sub>B<sub>0</sub>) - Operand
- 1 bit M - Mode Selector (Allows to choose between logical and arithmetic ops)
- 2 bit S (S<sub>1</sub>S<sub>0</sub>) - Allows to choose specific operation after M selection

#### Components

- 3x8 Multiplexer

- Half Adder circuit
- Subtractor circuit
- A increment circuit
- B increment circuit

- A.B circuit
- A+B circuit
- A⊕B circuit
- ~A circuit

#### Table (simplified version of SN54/74LS181)

| S1 | S0 | Arithmetic (M=0)  | Logical (M=1) |
|----|----|------------------ |---------------|
| 0  | 0  |          ADD      |        AND    |
| 0  | 1  |          SUB      |        OR     |
| 1  | 0  |          A INC    |        NOT    |
| 1  | 1  |          B INC    |        XOR    |
