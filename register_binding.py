def find_variable_live_ranges(
    dfg,
    scheduled
):

    live_ranges = {}

    for node in dfg.nodes:

        variable = node.output

        # Ignore final primary output
        # for register allocation
        if variable in dfg.outputs:
            continue

        production_cycle = scheduled[
            node.node_id
        ]

        # Find all consumers
        consumer_cycles = []

        for successor in node.successors:

            consumer_cycles.append(
                scheduled[successor.node_id]
            )

        if consumer_cycles:

            last_use = max(
                consumer_cycles
            )

        else:

            # Value is never consumed
            last_use = production_cycle + 1

        live_ranges[variable] = (
            production_cycle,
            last_use
        )

    return live_ranges

def live_ranges_overlap(
    range1,
    range2
):

    start1, end1 = range1
    start2, end2 = range2

    return (
        start1 < end2
        and start2 < end1
    )

def allocate_registers(
    live_ranges
):

    registers = {}

    # Process variables by
    # production time
    variables = sorted(
        live_ranges,
        key=lambda variable: (
            live_ranges[variable][0],
            variable
        )
    )

    for variable in variables:

        assigned = False

        for register in sorted(
            set(registers.values())
        ):

            conflict = False

            for other_variable, other_register in registers.items():

                if other_register != register:
                    continue

                if live_ranges_overlap(
                    live_ranges[variable],
                    live_ranges[other_variable]
                ):

                    conflict = True
                    break

            if not conflict:

                registers[variable] = register
                assigned = True
                break

        if not assigned:

            register_number = (
                len(set(registers.values()))
                + 1
            )

            register = f"R{register_number}"

            registers[variable] = register

    return registers

def display_register_binding(
    live_ranges,
    registers
):

    print(
        "\n========== REGISTER BINDING =========="
    )

    print(
        f"{'Variable':<12}"
        f"{'Live Range':<15}"
        f"{'Register':<10}"
    )

    print("-" * 37)

    for variable in sorted(
        live_ranges,
        key=lambda x: live_ranges[x][0]
    ):

        start, end = live_ranges[
            variable
        ]

        print(
            f"{variable:<12}"
            f"[{start}, {end})"
            f"{'':<8}"
            f"{registers[variable]:<10}"
        )

    print("=" * 37)

    print(
        "\nPhysical Registers:"
    )

    for register in sorted(
        set(registers.values())
    ):

        variables = [
            variable
            for variable, reg
            in registers.items()
            if reg == register
        ]

        print(
            f"  {register}: "
            + ", ".join(variables)
        )

    print(
        "=======================================\n"
    )