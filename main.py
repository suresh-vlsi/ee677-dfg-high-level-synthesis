from dfg import DFG, DFGNode

from scheduler import (
    asap_schedule,
    display_asap_schedule,
    alap_schedule,
    display_alap_schedule,
    get_latency
)

from resources import RESOURCE_LIMITS

from list_scheduler import (
    list_schedule,
    display_list_schedule
)

from resources import RESOURCE_LIMITS

from list_scheduler import (
    list_schedule,
    display_list_schedule
)

from fu_binding import (
    bind_functional_units,
    display_fu_binding
)

from register_binding import (
    find_variable_live_ranges,
    allocate_registers,
    display_register_binding
)

from datapath import (
    generate_datapath,
    display_datapath
)

from mux_control import (
    generate_mux_controls,
    display_mux_controls
)

from netlist import (
    generate_netlist,
    display_netlist
)

from verilog_generator import generate_verilog

def parse_dfg(filename):

    dfg = DFG()

    with open(filename, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line.startswith("INPUTS:"):

                data = line.split(":", 1)[1].strip()

                dfg.inputs = [
                    x.strip()
                    for x in data.split(",")
                ]

            elif line.startswith("NODE:"):

                data = line.split(":", 1)[1].strip()

                tokens = data.split()

                node_id = tokens[0]
                operation = tokens[1]

                inputs = tokens[2:-1]

                output = tokens[-1]

                node = DFGNode(
                    node_id,
                    operation,
                    inputs,
                    output
                )

                dfg.add_node(node)

            elif line.startswith("OUTPUTS:"):

                data = line.split(":", 1)[1].strip()

                dfg.outputs = [
                    x.strip()
                    for x in data.split(",")
                ]

    return dfg


def main():

    filename = "input/example.dfg"

    # --------------------------------
    # Step 1: Parse DFG
    # --------------------------------

    dfg = parse_dfg(filename)

    dfg.display()

    # --------------------------------
    # Step 2: Build dependencies
    # --------------------------------

    dfg.build_dependencies()

    dfg.display_dependencies()

    # --------------------------------
    # Topological ordering
    # --------------------------------

    print(
        "========== TOPOLOGICAL ORDER =========="
    )

    order = dfg.topological_sort()

    print(
        " -> ".join(
            node.node_id
            for node in order
        )
    )

    print(
        "========================================"
    )

    # --------------------------------
    # Step 3: ASAP scheduling
    # --------------------------------

    asap_schedule(dfg)

    display_asap_schedule(dfg)

    # --------------------------------
    # Calculate overall latency
    # --------------------------------

    latency = max(
        node.asap
        + get_latency(node.operation)
        - 1
        for node in dfg.nodes
    )

    print(
        f"\nOverall schedule latency: "
        f"{latency} cycles"
    )

    # --------------------------------
    # Step 4: ALAP scheduling
    # --------------------------------

    alap_schedule(
        dfg,
        latency
    )

    display_alap_schedule(dfg)

    # --------------------------------
    # Step 5: List scheduling
    # --------------------------------

    print(
        "\nResource constraints:"
    )

    for operation, count in RESOURCE_LIMITS.items():

        print(
            f"  {operation}: "
            f"{count}"
        )

    schedule, scheduled = list_schedule(
        dfg,
        RESOURCE_LIMITS
    )

    display_list_schedule(
        schedule,
        scheduled
    )

    # --------------------------------
    # Step 6: Functional Unit Binding
    # --------------------------------

    binding = bind_functional_units(
        schedule,
        RESOURCE_LIMITS
    )

    display_fu_binding(
        schedule,
        binding
    )

    # --------------------------------
    # Step 7: Register Binding
    # --------------------------------

    live_ranges = find_variable_live_ranges(
        dfg,
        scheduled
    )

    registers = allocate_registers(
        live_ranges
    )

    display_register_binding(
        live_ranges,
        registers
    )

    # --------------------------------
    # Step 8: Datapath Generation
    # --------------------------------

    datapath = generate_datapath(
        dfg,
        schedule,
        binding,
        registers
    )

    display_datapath(
        datapath
    )

    # --------------------------------
    # Step 9: MUX and Control Generation
    # --------------------------------

    controls = generate_mux_controls(
        dfg,
        schedule,
        binding,
        registers
    )

    display_mux_controls(
        controls
    )

    # --------------------------------
    # Step 10: Netlist Generation
    # --------------------------------

    netlist = generate_netlist(
        dfg,
        schedule,
        binding,
        registers,
        controls
    )

    display_netlist(
        netlist
    )

    # --------------------------------
    # Step 11: Verilog Generation
    # --------------------------------

    verilog_file = generate_verilog(
        dfg,
        schedule,
        binding,
        registers,
        controls
    )

    print(
        "\n========================================"
    )

    print(
        "VERILOG NETLIST GENERATED"
    )

    print(
        f"File: {verilog_file}"
    )

    print(
        "========================================"
    )

    # ====================================
    # Step 12: DFG Visualization
    # ====================================

    print(
        "\n======================================"
    )

    print(
        "GENERATING DFG VISUALIZATION"
    )

    print(
        "======================================"
    )

    try:

        import subprocess
        import sys

        subprocess.run(
            [
                sys.executable,
                "visualizer.py",
                filename
            ],
            check=True
        )

        print(
            "\nDFG VISUALIZATION GENERATED"
        )

        print(
            "Files:"
        )

        print(
            "  docs/dfg_auto.dot"
        )

        print(
            "  docs/dfg_auto.png"
        )

        print(
            "  docs/dfg_auto.svg"
        )

    except Exception as error:

        print(
            "\nWARNING: DFG visualization failed."
        )

        print(
            f"Reason: {error}"
        )

# ====================================
# Program entry point
# ====================================

if __name__ == "__main__":
    main()