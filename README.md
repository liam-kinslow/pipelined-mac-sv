# Pipelined MAC Unit (SystemVerilog)

A parameterised 3-stage pipelined Multiply-Accumulate (MAC) unit implemented in SystemVerilog, verified with a SystemVerilog testbench using Icarus Verilog.

## What is a MAC?

A MAC unit computes:
MAC operations are the fundamental computation in neural network inference — every layer of a neural network is a matrix multiplication, which is a series of MAC operations. Hardware accelerators like Google's TPU are built around large arrays of MAC units running in parallel.

## Architecture

The design uses a 3-stage pipeline to maximise clock frequency:

| Stage | Operation |
|-------|-----------|
| Stage 1 | Register inputs A and B |
| Stage 2 | Multiply A × B |
| Stage 3 | Accumulate product into running sum |

Each stage is separated by flip-flops clocked on the rising edge. The enable signal (`en`) is pipelined in step with the data to ensure correct accumulator gating.

- Input width: parameterised via `WIDTH` (default 8-bit)
- Output width: `2*WIDTH+1` bits to prevent overflow
- Signed arithmetic throughout
- Active-low synchronous reset (`rst_n`)
- Pipeline latency: 3 clock cycles

## Simulation Results

Simulated with A=3, B=4, en=1 for 6 cycles:
Time=55  en=1 result=12
Time=65  en=1 result=24
Time=75  en=1 result=36
Time=85  en=0 result=48
Time=95  en=0 result=60   ← pipeline draining
Time=105 en=0 result=72   ← pipeline draining
Time=115 en=0 result=72   ← accumulator holds

The 3-cycle latency before the first result and the 2-cycle pipeline drain on disable are both expected behaviours.

## Tools

- SystemVerilog (IEEE 1800-2012)
- Icarus Verilog 12.0
- Git / GitHub
