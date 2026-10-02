class DFGNode:

    def __init__(self, node_id, operation, inputs, output):

        self.node_id = node_id
        self.operation = operation
        self.inputs = inputs
        self.output = output

        # Dependency information
        self.predecessors = []
        self.successors = []

        # Scheduling information
        self.asap = None
        self.alap = None
        self.mobility = None

        # Binding information
        self.functional_unit = None

    def __repr__(self):

        return (
            f"DFGNode("
            f"id={self.node_id}, "
            f"op={self.operation}, "
            f"inputs={self.inputs}, "
            f"output={self.output})"
        )


class DFG:

    def __init__(self):

        self.inputs = []
        self.nodes = []
        self.outputs = []

    def add_node(self, node):

        self.nodes.append(node)

    def get_node(self, node_id):

        for node in self.nodes:

            if node.node_id == node_id:
                return node

        return None

    def get_node_by_output(self, variable):

        for node in self.nodes:

            if node.output == variable:
                return node

        return None

    def build_dependencies(self):

        # Clear existing dependencies
        for node in self.nodes:

            node.predecessors = []
            node.successors = []

        # Determine dependencies
        for node in self.nodes:

            for input_variable in node.inputs:

                producer = self.get_node_by_output(
                    input_variable
                )

                if producer is not None:

                    # producer -> current node

                    if producer not in node.predecessors:

                        node.predecessors.append(
                            producer
                        )

                    if node not in producer.successors:

                        producer.successors.append(
                            node
                        )

    def topological_sort(self):

        # Calculate indegree of every node
        indegree = {}

        for node in self.nodes:

            indegree[node.node_id] = len(
                node.predecessors
            )

        # Nodes with no predecessors
        ready = []

        for node in self.nodes:

            if indegree[node.node_id] == 0:

                ready.append(node)

        order = []

        while ready:

            current = ready.pop(0)

            order.append(current)

            # Remove current node from the graph
            for successor in current.successors:

                indegree[successor.node_id] -= 1

                if indegree[successor.node_id] == 0:

                    ready.append(successor)

        # If not all nodes were processed,
        # the graph contains a cycle.
        if len(order) != len(self.nodes):

            raise ValueError(
                "DFG contains a cycle. "
                "The DFG must be acyclic."
            )

        return order

    def display(self):

        print("\n========== DFG ==========")

        print("\nPrimary Inputs:")
        print(self.inputs)

        print("\nOperations:")

        for node in self.nodes:

            print(
                f"{node.node_id}: "
                f"{node.operation} "
                f"{node.inputs} -> "
                f"{node.output}"
            )

        print("\nPrimary Outputs:")
        print(self.outputs)

        print("=========================\n")

    def display_dependencies(self):

        print(
            "\n========== DEPENDENCY GRAPH =========="
        )

        for node in self.nodes:

            predecessors = [
                n.node_id
                for n in node.predecessors
            ]

            successors = [
                n.node_id
                for n in node.successors
            ]

            print(f"\nNode: {node.node_id}")

            print(
                f"  Operation    : "
                f"{node.operation}"
            )

            print(
                f"  Inputs       : "
                f"{node.inputs}"
            )

            print(
                f"  Output       : "
                f"{node.output}"
            )

            print(
                f"  Predecessors : "
                f"{predecessors}"
            )

            print(
                f"  Successors   : "
                f"{successors}"
            )

        print(
            "\n======================================\n"
        )