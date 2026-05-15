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

### SVA Assertions

Four concurrent SVA properties verified using Aldec Riviera-PRO:

| Property | Description |
|----------|-------------|
| Reset | `result == 0` on the cycle after `rst_n` falls |
| Enable hold | `result` stable after 2-cycle pipeline drain on `en` falling |
| Pipeline latency | `result` changes exactly 3 cycles after `en` rises |
| Overflow | `result` never exceeds signed 17-bit bounds |

## Simulation Results

Simulated with A=3, B=4, en=1 for 6 cycles:

## Simulation Results

Time=25   en=1  reset=1  result=0    ← pipeline filling  
Time=35   en=1  reset=1  result=0    ← pipeline filling  
Time=45   en=1  reset=1  result=0    ← pipeline filling  
Time=55   en=1  reset=1  result=12   ← first valid output  
Time=65   en=1  reset=1  result=24  
Time=75   en=1  reset=1  result=36  
Time=85   en=0  reset=1  result=48  
Time=95   en=0  reset=1  result=60   ← pipeline draining  
Time=105  en=0  reset=1  result=72   ← pipeline draining  
Time=115  en=0  reset=1  result=72   ← accumulator holds  

The 3-cycle latency before the first result and the 2-cycle pipeline drain on disable are both expected behaviours.

## Tools

- SystemVerilog (IEEE 1800-2012)
- Icarus Verilog 12.0
- Aldec Riviera-PRO (SVA verification)
- Git / GitHub
