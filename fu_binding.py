from collections import defaultdict


def bind_functional_units(schedule, resource_limits):

    # Available physical functional units
    available_units = {}

    for operation, count in resource_limits.items():

        available_units[operation] = [
            f"{operation}{i + 1}"
            for i in range(count)
        ]

    # Store binding
    binding = {}

    # Process schedule cycle by cycle
    for cycle in sorted(schedule):

        # Track which units are already used
        used_units = defaultdict(set)

        for node in schedule[cycle]:

            operation = node.operation

            units = available_units.get(
                operation,
                []
            )

            if not units:

                raise RuntimeError(
                    f"No functional unit available "
                    f"for operation {operation}"
                )

            # Find a free unit
            selected_unit = None

            for unit in units:

                if unit not in used_units[operation]:

                    selected_unit = unit
                    break

            if selected_unit is None:

                raise RuntimeError(
                    f"Resource conflict in cycle "
                    f"{cycle} for {operation}"
                )

            binding[node.node_id] = selected_unit

            used_units[operation].add(
                selected_unit
            )

            # Store binding in DFG node
            node.functional_unit = selected_unit

    return binding


def display_fu_binding(
    schedule,
    binding
):

    print(
        "\n========== FUNCTIONAL UNIT BINDING =========="
    )

    print(
        f"{'Cycle':<8}"
        f"{'Node':<8}"
        f"{'Operation':<12}"
        f"{'Functional Unit':<18}"
    )

    print("-" * 46)

    for cycle in sorted(schedule):

        for node in schedule[cycle]:

            print(
                f"{cycle:<8}"
                f"{node.node_id:<8}"
                f"{node.operation:<12}"
                f"{binding[node.node_id]:<18}"
            )

    print("=" * 46)

    print(
        "\nPhysical Functional Units:"
    )

    units = sorted(
        set(binding.values())
    )

    for unit in units:

        operations = [
            node_id
            for node_id, fu in binding.items()
            if fu == unit
        ]

        print(
            f"  {unit}: "
            + ", ".join(operations)
        )

    print(
        "=============================================\n"
    )