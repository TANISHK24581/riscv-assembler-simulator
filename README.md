# RISC-V Assembler and Simulator

A Python-based assembler and instruction-level simulator for a subset of the RISC-V RV32I instruction set architecture.

---

## Overview

This project implements a simple assembler and simulator for the 32-bit RISC-V integer instruction set (RV32I).  
The assembler translates RISC-V assembly programs into binary machine instructions, which are then executed by the simulator to model instruction-level behavior.

The project was developed as part of a Computer Organisation course to understand instruction encoding, execution flow, and low-level program behavior.

---

## Components

- **Assembler.py**
  - Parses RISC-V assembly instructions
  - Resolves labels and immediates
  - Encodes instructions into 32-bit binary machine code

- **Simulator.py**
  - Executes the generated machine code
  - Simulates program counter updates, register file, and data memory
  - Produces execution traces including register states and memory contents

---

## Supported Instructions

The project supports a subset of the RV32I instruction set, including:

- **R-type:** `add`, `sub`, `slt`, `srl`, `or`, `and`
- **I-type:** `addi`, `lw`, `jalr`
- **S-type:** `sw`
- **B-type:** `beq`, `bne`, `blt`
- **J-type:** `jal`

---

## HOW TO RUN

### Assembler
```bash
python Assembler.py <input_assembly_file> <output_binary_file>
```
### Simulator
```bash
python Simulator.py <input_binary_file> <output_trace_file>
