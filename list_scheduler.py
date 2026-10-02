from collections import defaultdict

from scheduler import get_latency


def is_ready(node, scheduled):

    for predecessor in node.predecessors:

        if predecessor.node_id not in scheduled:
            return False

    return True


def list_schedule(
    dfg,
    resource_limits
):

    # Nodes that have already been scheduled
    scheduled = {}

    # Final schedule
    schedule = defaultdict(list)

    # Current clock cycle
    cycle = 1

    while len(scheduled) < len(dfg.nodes):

        # --------------------------------
        # Find ready operations
        # --------------------------------

        ready = []

        for node in dfg.nodes:

            if node.node_id in scheduled:
                continue

            if is_ready(node, scheduled):

                ready.append(node)

        # --------------------------------
        # Sort ready operations
        #
        # Priority:
        # 1. Mobility
        # 2. ASAP time
        # 3. Node ID
        # --------------------------------

        ready.sort(
            key=lambda node: (
                node.mobility,
                node.asap,
                node.node_id
            )
        )

        # --------------------------------
        # Track resources used
        # --------------------------------

        resources_used = defaultdict(int)

        # --------------------------------
        # Schedule ready operations
        # --------------------------------

        for node in ready:

            operation = node.operation

            limit = resource_limits.get(
                operation,
                0
            )

            if resources_used[operation] >= limit:
                continue

            # Schedule node
            schedule[cycle].append(node)

            scheduled[node.node_id] = cycle

            resources_used[operation] += 1

        # --------------------------------
        # Safety check
        # --------------------------------

        if not schedule[cycle]:

            raise RuntimeError(
                f"No operation could be scheduled "
                f"in cycle {cycle}. "
                f"Check resource constraints."
            )

        cycle += 1

    return schedule, scheduled

def display_list_schedule(
    schedule,
    scheduled
):

    print(
        "\n========== LIST SCHEDULE =========="
    )

    for cycle in sorted(schedule):

        nodes = schedule[cycle]

        names = [
            node.node_id
            for node in nodes
        ]

        print(
            f"Cycle {cycle}: "
            + ", ".join(names)
        )

    print(
        "===================================\n"
    )

    print(
        "========== OPERATION TIMES =========="
    )

    for node_id in sorted(scheduled):

        print(
            f"{node_id}: "
            f"Cycle {scheduled[node_id]}"
        )

    print(
        "=====================================\n"
    )