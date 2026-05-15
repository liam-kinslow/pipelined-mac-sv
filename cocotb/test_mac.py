import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from collections import deque

class MACModel:
    def __init__(self):
        self.accumulator = 0
        self.pipeline = deque([{'a': 0, 'b': 0, 'en': 0},
                               {'a': 0, 'b': 0, 'en': 0},
                               {'a': 0, 'b': 0, 'en': 0}])
    
    def step(self, a, b, en):
        self.pipeline.append({'a': a, 'b': b, 'en': en})
        oldest = self.pipeline.popleft()
        if oldest['en']:
            self.accumulator += oldest['a'] * oldest['b']
        return self.accumulator
    
    def reset(self):
        self.accumulator = 0
        self.pipeline = deque([{'a': 0, 'b': 0, 'en': 0},
                               {'a': 0, 'b': 0, 'en': 0},
                               {'a': 0, 'b': 0, 'en': 0}])


@cocotb.test()
async def test_reset(dut):
    model = MACModel()

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    dut.en.value = 0
    dut.a.value = 0
    dut.b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    assert dut.result.value.to_signed() == 0, \
        f"Reset failed: result={dut.result.value.to_signed()}"


@cocotb.test()
async def test_accumulation(dut):
    model = MACModel()

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    dut.en.value = 0
    dut.a.value = 0
    dut.b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    dut.en.value = 1
    dut.a.value = 3
    dut.b.value = 4

    for _ in range(9):
        expected = model.step(3, 4, 1)
        await RisingEdge(dut.clk)
        got = dut.result.value.to_signed()
        assert got == expected, \
            f"Accumulation failed: expected {expected} got {got}"


@cocotb.test()
async def test_enable(dut):
    model = MACModel()

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    dut.en.value = 0
    dut.a.value = 0
    dut.b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    dut.en.value = 1
    dut.a.value = 3
    dut.b.value = 4

    # Accumulate for 6 cycles
    for _ in range(6):
        expected = model.step(3, 4, 1)
        await RisingEdge(dut.clk)

    # Disable enable
    dut.en.value = 0

    # Check accumulator holds
    for _ in range(4):
        expected = model.step(3, 4, 0)
        await RisingEdge(dut.clk)
        got = dut.result.value.to_signed()
        assert got == expected, \
            f"Enable hold failed: expected {expected} got {got}"


@cocotb.test()
async def test_random(dut):
    model = MACModel()

    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    dut.en.value = 0
    dut.a.value = 0
    dut.b.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)

    dut.en.value = 1

    for _ in range(20):
        a = random.randint(-128, 127)
        b = random.randint(-128, 127)
        dut.a.value = a
        dut.b.value = b
        expected = model.step(a, b, 1)
        await RisingEdge(dut.clk)
        got = dut.result.value.to_signed()
        assert got == expected, \
            f"Random test failed: expected {expected} got {got}"