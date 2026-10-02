# DFG-Based High-Level Synthesis Tool

A Python-based educational High-Level Synthesis (HLS) tool that transforms a **Data Flow Graph (DFG)** into a scheduled, resource-bound, register-bound datapath and finally generates synthesizable Verilog RTL.

The project demonstrates the major stages of a classical HLS flow:

```text
Data Flow Graph
      │
      ▼
DFG Parsing
      │
      ▼
List Scheduling
      │
      ▼
Functional Unit Binding
      │
      ▼
Register Binding
      │
      ▼
MUX / Control Generation
      │
      ▼
Netlist Generation
      │
      ▼
Verilog RTL Generation
      │
      ▼
RTL Simulation
      │
      ▼
VCD Waveform
      │
      ▼
Graphical Visualization
```

---

## 1. Project Objective

The objective of this project is to implement a simplified HLS compiler that accepts an arithmetic Data Flow Graph and automatically produces a hardware datapath.

The tool performs:

1. DFG parsing
2. Dependency analysis
3. Resource-constrained list scheduling
4. Functional-unit binding
5. Register allocation
6. Multiplexer/control generation
7. Datapath/netlist generation
8. Verilog RTL generation
9. RTL simulation
10. Waveform generation
11. DFG and datapath visualization

The project is intended for studying:

- High-Level Synthesis
- VLSI CAD
- Digital Design
- Scheduling
- Resource Allocation
- Register Binding
- Datapath Design
- RTL Generation
- Hardware Verification

---

## 2. Example DFG

The current example implements:

```text
N1: x1 = a + b
N2: x2 = c + d
N3: x3 = x1 * x2
N4: x4 = e + f
N5: x5 = x3 + x4
N6: x6 = g * h
N7: y  = x5 + x6
```

Therefore, the overall computation is:

```text
y = ((a + b) * (c + d)) + (e + f) + (g * h)
```

The input DFG is stored in:

```text
input/example.dfg
```

---

## 3. Input Format

The DFG input uses a simple text-based format.

Example:

```text
INPUTS: a,b,c,d,e,f,g,h

NODE: N1 ADD a b x1
NODE: N2 ADD c d x2
NODE: N3 MUL x1 x2 x3
NODE: N4 ADD e f x4
NODE: N5 ADD x3 x4 x5
NODE: N6 MUL g h x6
NODE: N7 ADD x5 x6 y

OUTPUTS: y
```

Each node has the format:

```text
NODE: <node_id> <operation> <input1> <input2> <output>
```

For example:

```text
NODE: N3 MUL x1 x2 x3
```

means:

```text
x3 = x1 * x2
```

---

## 4. Project Structure

```text
CAD assign/
│
├── input/
│   └── example.dfg
│
├── output/
│   ├── datapath.v
│   ├── datapath.vcd
│   └── sim
│
├── tb/
│   └── tb_datapath.sv
│
├── docs/
│   ├── dfg.dot
│   ├── dfg.png
│   ├── dfg_auto.dot
│   ├── dfg_auto.png
│   ├── dfg_auto.svg
│   ├── scheduled_dfg.dot
│   ├── scheduled_dfg.png
│   ├── scheduled_dfg.svg
│   ├── bound_datapath.dot
│   ├── bound_datapath.png
│   ├── bound_datapath.svg
│   └── datapath_architecture.*
│
├── dfg.py
├── scheduler.py
├── list_scheduler.py
├── resources.py
├── fu_binding.py
├── register_binding.py
├── mux_control.py
├── datapath.py
├── netlist.py
├── verilog_generator.py
├── visualizer.py
├── main.py
│
└── README.md
```

---

## 5. Description of Source Files

### `dfg.py`

Defines the Data Flow Graph representation.

Responsibilities:

- DFG node representation
- Input/output representation
- Node dependencies
- Graph construction
- DFG parsing support

### `scheduler.py`

Contains scheduling-related functionality.

The scheduler determines when each operation can execute while respecting dependencies.

### `list_scheduler.py`

Implements resource-constrained list scheduling.

The current example uses:

```text
ADD resources = 1
MUL resources = 1
```

### `resources.py`

Defines the available hardware resources.

Example:

```text
ADD = 1
MUL = 1
```

These constraints determine how many operations of each type can execute simultaneously.

### `fu_binding.py`

Performs functional-unit binding.

Operations are mapped onto physical functional units.

For the current example:

```text
ADD1:
    N1
    N2
    N4
    N5
    N7

MUL1:
    N6
    N3
```

Thus, seven operations are implemented using only:

```text
1 ADD unit
1 MUL unit
```

This demonstrates resource sharing.

### `register_binding.py`

Performs register allocation based on variable live ranges.

Current register assignment:

```text
R1:
    x1
    x3
    x5

R2:
    x6

R3:
    x2
    x4
```

Therefore six intermediate variables are stored using only three physical registers.

### `mux_control.py`

Generates the control information required to select operands for the shared functional units.

The generated architecture contains multiplexers such as:

```text
ADD1_A_MUX
ADD1_B_MUX
MUL1_A_MUX
MUL1_B_MUX
```

### `netlist.py`

Generates a textual hardware netlist.

The netlist contains:

- Registers
- Functional units
- Multiplexers
- Connections
- Operation cycles
- Output connections

### `datapath.py`

Represents the hardware datapath structure generated from the scheduling and binding information.

### `verilog_generator.py`

Generates Verilog RTL from the scheduled and bound datapath.

The generated file is:

```text
output/datapath.v
```

### `visualizer.py`

Automatically creates Graphviz visualizations of the DFG.

Generated files include:

```text
docs/dfg_auto.dot
docs/dfg_auto.png
docs/dfg_auto.svg
```

### `main.py`

Main driver program.

It executes the HLS flow:

```text
Parse
  ↓
Schedule
  ↓
FU Binding
  ↓
Register Binding
  ↓
MUX/Control
  ↓
Netlist
  ↓
Verilog
  ↓
Visualization
```

---

## 6. Scheduling

The example uses resource-constrained list scheduling.

Resource constraints:

```text
ADD = 1
MUL = 1
```

The resulting schedule is:

| Cycle | Operations |
|------:|------------|
| 1 | N1, N6 |
| 2 | N2 |
| 3 | N3, N4 |
| 4 | N5 |
| 5 | N7 |

Therefore:

```text
Cycle 1:
    N1 = a + b
    N6 = g * h

Cycle 2:
    N2 = c + d

Cycle 3:
    N3 = x1 * x2
    N4 = e + f

Cycle 4:
    N5 = x3 + x4

Cycle 5:
    N7 = x5 + x6
```

The schedule requires:

```text
Latency = 5 cycles
```

---

## 7. Functional Unit Binding

The scheduler determines which operations execute in each cycle.

Binding maps those operations to physical hardware.

The resulting functional units are:

```text
ADD1
MUL1
```

The mapping is:

```text
ADD1:
    N1
    N2
    N4
    N5
    N7

MUL1:
    N6
    N3
```

This is an example of **resource sharing**.

Instead of creating five independent adders, all ADD operations reuse one physical ADD unit.

Instead of creating two independent multipliers, both multiplication operations reuse one physical multiplier.

---

## 8. Register Binding

Variable live ranges are analyzed before assigning physical registers.

The resulting allocation is:

```text
R1:
    x1
    x3
    x5

R2:
    x6

R3:
    x2
    x4
```

Therefore:

```text
6 logical variables
        ↓
3 physical registers
```

This reduces hardware resources through register reuse.

---

## 9. Generated Netlist

The physical hardware contains:

```text
REGISTERS:

R1
R2
R3
```

Functional units:

```text
ADD1
MUL1
```

Multiplexers:

```text
ADD1_A_MUX
ADD1_B_MUX
MUL1_A_MUX
MUL1_B_MUX
```

The major connections are:

```text
Cycle 1:
    ADD1(a,b) → R1
    MUL1(g,h) → R2

Cycle 2:
    ADD1(c,d) → R3

Cycle 3:
    MUL1(R1,R3) → R1
    ADD1(e,f)   → R3

Cycle 4:
    ADD1(R1,R3) → R1

Cycle 5:
    ADD1(R1,R2) → y
```

---

## 10. Datapath Architecture

The generated architecture consists of:

```text
             ┌─────────────┐
Inputs ─────►│ Multiplexers│
             └──────┬──────┘
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
     ┌─────────┐        ┌───────────┐
     │  ADD1   │        │   MUL1    │
     │  ADDER  │        │ MULTIPLIER│
     └────┬────┘        └─────┬─────┘
          │                   │
          ▼                   ▼
       ┌──────┐            ┌──────┐
       │  R1  │            │  R2  │
       └──────┘            └──────┘
          │
          ▼
       ┌──────┐
       │  R3  │
       └──────┘
          │
          ▼
       Output y
```

The actual generated architecture diagrams are available in:

```text
docs/
```

---

## 11. Verilog Generation

The HLS tool generates:

```text
output/datapath.v
```

The generated RTL contains:

- Primary inputs
- Clock
- Reset
- Physical registers
- ADD functional unit
- MUL functional unit
- Multiplexer logic
- Cycle counter
- Sequential control
- Output logic

The generated module is:

```text
generated_datapath
```

---

## 12. RTL Simulation

The testbench is:

```text
tb/tb_datapath.sv
```

The example input values are:

```text
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7
h = 8
```

Expected intermediate values:

```text
x1 = a + b
   = 1 + 2
   = 3

x2 = c + d
   = 3 + 4
   = 7

x3 = x1 * x2
   = 3 * 7
   = 21

x4 = e + f
   = 5 + 6
   = 11

x5 = x3 + x4
   = 21 + 11
   = 32

x6 = g * h
   = 7 * 8
   = 56

y = x5 + x6
  = 32 + 56
  = 88
```

Therefore:

```text
Expected y = 88
```

---

## 13. Running the Complete HLS Flow

Open PowerShell in the project root:

```powershell
cd "C:\Users\Lenovo\CAD assign"
```

Run:

```powershell
python main.py input/example.dfg
```

The program generates the netlist, Verilog RTL and DFG visualization.

---

## 14. Graphviz

Graphviz is required for DFG visualization.

The project uses:

```text
dot
```

to convert `.dot` files into graphical formats.

Verify Graphviz:

```powershell
dot -V
```

Expected output is similar to:

```text
dot - graphviz version 16.1.0
```

Generate a PNG manually if required:

```powershell
dot -Tpng docs/dfg_auto.dot -o docs/dfg_auto.png
```

Generate SVG:

```powershell
dot -Tsvg docs/dfg_auto.dot -o docs/dfg_auto.svg
```

---

## 15. Verilog Compilation

If Icarus Verilog is installed, compile the generated RTL and testbench:

```powershell
iverilog -g2012 -o output/sim output/datapath.v tb/tb_datapath.sv
```

This produces:

```text
output/sim
```

---

## 16. Run the Simulation

Run:

```powershell
vvp output/sim
```

Expected result:

```text
======================================
          HLS DATAPATH TEST
======================================

Expected y = 88
Actual y   = 88

--------------------------------------
RESULT: PASS
======================================
```

A successful simulation confirms that the generated datapath produces the expected result.

---

## 17. Waveform Generation

The testbench generates:

```text
output/datapath.vcd
```

The VCD contains the simulated signal activity.

Important signals include:

```text
clk
reset

a
b
c
d
e
f
g
h

y
```

---

## 18. Viewing the Waveform

If GTKWave is installed:

```powershell
gtkwave output/datapath.vcd
```

The waveform can be used to inspect:

- Clock transitions
- Reset behavior
- Input values
- Output computation
- Cycle-by-cycle datapath activity

---

## 19. Visualization Outputs

The project generates several graphical representations.

### Original DFG

```text
docs/dfg.png
```

or:

```text
docs/dfg_auto.png
```

This shows the original computational dependencies.

### Scheduled DFG

```text
docs/scheduled_dfg.png
```

This shows operations grouped according to execution cycles.

```text
Cycle 1 → N1, N6
Cycle 2 → N2
Cycle 3 → N3, N4
Cycle 4 → N5
Cycle 5 → N7
```

### Bound Datapath

```text
docs/bound_datapath.png
```

This illustrates:

- Shared functional units
- Physical registers
- Multiplexers
- Data connections

### Datapath Architecture

```text
docs/datapath_architecture.png
```

This provides a higher-level view of the generated hardware architecture.

---

## 20. Complete HLS Flow

```text
                 INPUT
                   │
                   ▼
          ┌─────────────────┐
          │   example.dfg   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │   DFG Parser    │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ List Scheduler  │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │   FU Binding    │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Register Binding│
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ MUX / Control   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Netlist Builder │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Verilog Generator│
          └────────┬────────┘
                   │
                   ▼
             datapath.v
                   │
                   ▼
          ┌─────────────────┐
          │ Icarus Verilog  │
          └────────┬────────┘
                   │
                   ▼
               Simulation
                   │
                   ▼
             datapath.vcd
                   │
                   ▼
              GTKWave
```

---

## 21. Design Equation

The implemented computation is:

\[
y=((a+b)(c+d))+(e+f)+(gh)
\]

where:

```text
+  → ADD functional unit
*  → MUL functional unit
```

The HLS scheduler determines when these operations execute.

The binding stage determines which physical functional unit executes each operation.

The register allocation stage determines where intermediate values are stored.

---

## 22. Hardware Resource Summary

For the current example:

| Resource | Quantity |
|---|---:|
| ADD functional units | 1 |
| MUL functional units | 1 |
| Physical registers | 3 |
| Multiplexers | 4 |
| Scheduling cycles | 5 |
| Logical operations | 7 |

The design therefore demonstrates hardware resource sharing.

---

## 23. Verification

The generated RTL was verified using a SystemVerilog testbench.

Test case:

```text
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7
h = 8
```

Expected:

```text
y = 88
```

Observed:

```text
y = 88
```

Verification result:

```text
PASS
```

---

## 24. Technologies Used

The project uses:

- Python
- Graphviz
- Verilog
- SystemVerilog
- Icarus Verilog
- GTKWave
- VS Code
- PowerShell

Optional Linux/WSL environment:

- Ubuntu
- WSL2

---

## 25. Running on Linux / WSL

From the project directory:

```bash
cd ~/hls_dfg
```

Run:

```bash
python3 main.py input/example.dfg
```

Verify Graphviz:

```bash
dot -V
```

Compile Verilog:

```bash
iverilog -g2012 -o output/sim output/datapath.v tb/tb_datapath.sv
```

Run:

```bash
vvp output/sim
```

View waveform:

```bash
gtkwave output/datapath.vcd
```

---

## 26. Troubleshooting

### Graphviz not recognized

If PowerShell reports:

```text
dot : The term 'dot' is not recognized
```

temporarily add Graphviz to PATH:

```powershell
$env:Path += ";C:\Program Files\Graphviz\bin"
```

Then verify:

```powershell
dot -V
```

### Icarus Verilog not recognized

Verify:

```powershell
iverilog -V
```

If unavailable, install Icarus Verilog and restart VS Code.

### GTKWave cannot open the VCD

First verify that the VCD exists:

```powershell
Get-Item output/datapath.vcd
```

Then:

```powershell
gtkwave output/datapath.vcd
```

### Python script cannot find the DFG

Make sure the terminal is located at the project root:

```text
C:\Users\Lenovo\CAD assign
```

Check:

```powershell
Get-Location
```

Then run:

```powershell
python main.py input/example.dfg
```

---

## 27. Future Improvements

Possible extensions include:

- ASAP scheduling
- ALAP scheduling
- Force-directed scheduling
- Mobility analysis
- Multiple resource constraints
- Latency-constrained scheduling
- Register lifetime visualization
- Automatic FSM generation
- Clock-enable generation
- Pipelined datapath generation
- Memory binding
- Multiplexer optimization
- Bit-width optimization
- Power-aware scheduling
- Area estimation
- Timing estimation
- RTL synthesis using Yosys
- Technology mapping
- Formal verification
- Automatic testbench generation
- Support for more arithmetic operators
- GUI-based DFG editor

---

## 28. Educational Significance

This project demonstrates the transformation:

```text
Algorithm
   ↓
Data Flow Graph
   ↓
Schedule
   ↓
Resource Allocation
   ↓
Register Allocation
   ↓
Datapath
   ↓
RTL
   ↓
Hardware Simulation
```

It provides a practical implementation of fundamental concepts in:

**High-Level Synthesis and VLSI CAD.**

---

## 29. Final Result

For the example DFG:

```text
y = ((a+b)*(c+d)) + (e+f) + (g*h)
```

the tool successfully produces:

```text
7 computational operations
        ↓
5-cycle schedule
        ↓
1 ADD + 1 MUL
        ↓
3 physical registers
        ↓
MUX-controlled datapath
        ↓
Verilog RTL
        ↓
Simulation PASS
        ↓
VCD waveform
        ↓
Graphical DFG/datapath visualizations
```

---

## 30. Author

**HLS DFG-to-Netlist / RTL Generation Project**

Developed as an educational VLSI CAD / High-Level Synthesis project.

```text
DFG → Scheduling → Binding → Datapath → Netlist → RTL → Simulation
```

**End of Project**
