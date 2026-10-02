from collections import defaultdict

OPERATION_LATENCY = {
    "ADD": 1,
    "SUB": 1,
    "MUL": 1,
    "DIV": 3
}


def get_latency(operation):

    if operation not in OPERATION_LATENCY:

        raise ValueError(
            f"Unknown operation: {operation}"
        )

    return OPERATION_LATENCY[operation]


def asap_schedule(dfg):

    # Obtain dependency-respecting order
    order = dfg.topological_sort()

    for node in order:

        # No predecessors
        if not node.predecessors:

            node.asap = 1

        else:

            earliest_start = 1

            for predecessor in node.predecessors:

                predecessor_latency = get_latency(
                    predecessor.operation
                )

                predecessor_finish = (
                    predecessor.asap
                    + predecessor_latency
                )

                earliest_start = max(
                    earliest_start,
                    predecessor_finish
                )

            node.asap = earliest_start

    return order


def display_asap_schedule(dfg):

    print("\n========== ASAP SCHEDULE ==========")

    schedule = defaultdict(list)

    for node in dfg.nodes:

        schedule[node.asap].append(node)

    for cycle in sorted(schedule):

        operations = schedule[cycle]

        names = [
            node.node_id
            for node in operations
        ]

        print(
            f"Cycle {cycle}: "
            + ", ".join(names)
        )

    print("===================================\n")

def alap_schedule(dfg, latency):

    # Get reverse topological order
    order = dfg.topological_sort()

    reverse_order = list(reversed(order))

    for node in reverse_order:

        # If node has no successors,
        # it must finish by the final latency.
        if not node.successors:

            node.alap = (
                latency
                - get_latency(node.operation)
                + 1
            )

        else:

            latest_start = float("inf")

            for successor in node.successors:

                successor_alap = successor.alap

                node_latest_start = (
                    successor_alap
                    - get_latency(node.operation)
                )

                latest_start = min(
                    latest_start,
                    node_latest_start
                )

            node.alap = latest_start

    # Calculate mobility
    for node in dfg.nodes:

        node.mobility = (
            node.alap - node.asap
        )

    return order

def display_alap_schedule(dfg):

    print("\n========== ASAP / ALAP / MOBILITY ==========")

    print(
        f"{'Node':<8}"
        f"{'Operation':<12}"
        f"{'ASAP':<8}"
        f"{'ALAP':<8}"
        f"{'Mobility':<10}"
    )

    print("-" * 46)

    for node in dfg.nodes:

        print(
            f"{node.node_id:<8}"
            f"{node.operation:<12}"
            f"{node.asap:<8}"
            f"{node.alap:<8}"
            f"{node.mobility:<10}"
        )

    print("=" * 46)