"""
Attack Tree Loader and Visualiser

Functionality for visualising and analysing attack trees. 
Uses graph theory to help users understand security risks.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt


class AttackTree:
    """Class to load and visualise attack trees from JSON data"""

    def __init__(self):
        """Create empty attack tree instance."""
        self.graph = nx.DiGraph()  # Directed graph for attack tree
        self.tree_data = None      # Raw JSON data

    def load_from_json(self, filepath):
        """Load attack tree from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.tree_data = json.load(file)
            print(f"✓ Loaded attack tree: {self.tree_data['name']}")
            return True
        except FileNotFoundError:
            print(f"✗ Error: Could not find file {filepath}")
            return False
        except json.JSONDecodeError:
            print(f"✗ Error: Invalid JSON in {filepath}")
            return False

    def build_graph(self):
        """Convert JSON data to NetworkX graph"""
        if not self.tree_data:
            print("✗ No data loaded. Call load_from_json first.")
            return

        # Clear existing graph
        self.graph.clear()

        # Build graph from root node
        self._add_node_recursive(self.tree_data['root'], None)
        print(f"✓ Built graph with {self.graph.number_of_nodes()} nodes")

    def _add_node_recursive(self, node, parent_id):
        """Add nodes and edges recursively."""
        # Add current node with attributes
        self.graph.add_node(node['id'],
                        name=node['name'],
                        type=node['type'],
                        value=node.get('value', 0))

        # Add edge from parent
        if parent_id:
            self.graph.add_edge(parent_id, node['id'])

        # Recursively add children
        if 'children' in node:
            for child in node['children']:
                self._add_node_recursive(child, node['id'])

    def visualise(self, show_values=True):
        """Display attack tree as graph."""
        if self.graph.number_of_nodes() == 0:
            print("✗ No graph to display. Call build_graph first.")
            return

        plt.figure(figsize=(16, 12))

        # Fixed layout for consistent positioning
        pos = nx.spring_layout(self.graph, k=4, iterations=50, seed=42)

        # Draw nodes with different colours based on type
        node_colours = []
        node_sizes = []
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id]['type']
            if node_type == 'leaf':
                node_colours.append('lightcoral')  # Red for attacks
                node_sizes.append(3000)
            else:
                node_colours.append('lightblue')   # Blue for logic gates
                node_sizes.append(2500)

        # Draw graph
        nx.draw(self.graph, pos,
                node_color=node_colours,
                node_size=node_sizes,
                font_size=9,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                arrowsize=25)

        # Add labels with values
        labels = {}
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            name = node_data['name']

            if show_values and node_data['type'] == 'leaf' and node_data['value'] > 0:
                labels[node_id] = f"{name}\n\n£{node_data['value']:,.0f}"
            else:
                labels[node_id] = name

        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, font_weight='bold')

        # Add a summary box for total risk
        if show_values:
            total_risk = sum(self.graph.nodes[node_id]['value']
                            for node_id in self.graph.nodes()
                            if self.graph.nodes[node_id]['type'] == 'leaf')
            plt.text(0.02, 0.98, f"Total Risk Exposure: £{total_risk:,.0f}",
                    transform=plt.gca().transAxes, fontsize=12, fontweight='bold',
                    bbox={"boxstyle": "round,pad=0.3", "facecolor": "yellow", "alpha": 0.8},
                    verticalalignment='top')

        plt.title(self.tree_data['name'], size=18, weight='bold', pad=20)
        plt.axis('off')
        plt.show()

    def update_node_value(self, node_id, value):
        """Update risk value for specific node"""
        if node_id in self.graph.nodes():
            self.graph.nodes[node_id]['value'] = value
            print(f"✓ Updated {self.graph.nodes[node_id]['name']} = £{value:,.2f}")
            return True
        print(f"✗ Node {node_id} not found")
        return False

    def get_leaf_nodes(self):
        """Get all leaf nodes (where users can input values)"""
        leaf_nodes = []
        for node_id in self.graph.nodes():
            if self.graph.nodes[node_id]['type'] == 'leaf':
                node_data = self.graph.nodes[node_id]
                leaf_nodes.append({
                    'id': node_id,
                    'name': node_data['name'],
                    'value': node_data['value']
                })
        return leaf_nodes

    def input_values_interactive(self):
        """Interactive input for risk values."""
        if self.graph.number_of_nodes() == 0:
            print("✗ No graph loaded. Load and build a graph first.")
            return

        print("=" * 60)
        print("RISK VALUE INPUT")
        print("=" * 60)
        print("Enter the cost impact (in £) if each attack succeeds:")
        print("(Press Enter to skip, or enter 0 for no impact)")
        print()

        leaf_nodes = self.get_leaf_nodes()

        for leaf in leaf_nodes:
            while True:
                try:
                    current_value = leaf['value']
                    prompt = f"{leaf['name']} (current: £{current_value:,.2f}): £"
                    user_input = input(prompt).strip()

                    if user_input == "":
                        break

                    value = float(user_input)
                    if value >= 0:
                        self.update_node_value(leaf['id'], value)
                        break
                    print("Please enter a positive number or 0")
                except ValueError:
                    print("Please enter a valid number")

        print("\n✓ All values updated!")

    def calculate_risk(self):
        """Calculate overall risk using attack tree logic."""
        if self.graph.number_of_nodes() == 0:
            print("✗ No graph loaded. Load and build a graph first.")
            return 0

        # Find root node
        root_nodes = [node for node in self.graph.nodes()
                    if self.graph.in_degree(node) == 0]

        if not root_nodes:
            print("✗ No root node found")
            return 0

        root_node = root_nodes[0]
        total_risk = self._calculate_node_risk(root_node)

        print("\n" + "=" * 60)
        print("RISK ASSESSMENT SUMMARY")
        print("=" * 60)
        print(f"Total Business Risk Exposure: £{total_risk:,.2f}")
        print("=" * 60)

        return total_risk

    def _calculate_node_risk(self, node_id):
        """Calculate risk for node using OR/AND logic."""
        node_data = self.graph.nodes[node_id]

        # Leaf nodes return their value
        if node_data['type'] == 'leaf':
            return node_data['value']

        # Get all child nodes
        children = list(self.graph.successors(node_id))
        if not children:
            return 0

        # Calculate risk based on node type
        child_risks = [self._calculate_node_risk(child) for child in children]

        # Apply gate logic
        if node_data['type'] == 'OR':
            # OR gate: take maximum risk (worst case scenario)
            return max(child_risks) if child_risks else 0 # Worst case
        if node_data['type'] == 'AND':
            return sum(child_risks)
        return max(child_risks) if child_risks else 0 # Default OR

    def get_risk_breakdown(self):
        """Show detailed risk calculation breakdown."""
        if self.graph.number_of_nodes() == 0:
            return {}

        breakdown = {}
        leaf_nodes = self.get_leaf_nodes()

        print("\n" + "-"*50)
        print("DETAILED RISK BREAKDOWN")
        print("-"*50)

        total_leaf_value = 0
        for leaf in leaf_nodes:
            value = leaf['value']
            total_leaf_value += value
            breakdown[leaf['name']] = value
            if value > 0:
                print(f"{leaf['name']}: £{value:,.2f}")

        calculated_risk = self.calculate_risk()

        print(f"\nSum of individual attacks: £{total_leaf_value:,.2f}")
        print(f"Calculated overall risk: £{calculated_risk:,.2f}")

        if calculated_risk < total_leaf_value:
            print("(Lower overall risk due to OR-gate logic - not all attacks likely)")
        elif calculated_risk > total_leaf_value:
            print("(Higher overall risk due to AND-gate combinations)")

        return breakdown


# Menu interface for attack tree comparison
if __name__ == "__main__":
    # Create attack tree instance
    tree = AttackTree()


    # Enhanced menu for pre/post digitalisation comparison
    print("=" * 60)
    print("PAMPERED PETS RISK ASSESSMENT TOOL")
    print("=" * 60)
    print("Compare risks before and after digitalisation:")
    print()
    print("CURRENT BUSINESS (Pre-Digitalisation):")
    print("1. Payment System Risks (Current)")
    print("2. Supply Chain Risks (Current)")
    print()
    print("AFTER DIGITALISATION (Post-Implementation):")
    print("3. Payment System Risks (Digitalised)")
    print("4. Supply Chain Risks (Digitalised)")
    print()
    print("COMPARISON MODES:")
    print("5. Compare Payment Systems (Current vs Digitalised)")
    print("6. Compare Supply Chains (Current vs Digitalised)")
    print("=" * 60)

    # File mapping for menu choices
    attack_trees = {
        "1": ("data/attack_trees/payment_system_current.json", "Payment System (Current)"),
        "2": ("data/attack_trees/supply_chain_current.json", "Supply Chain (Current)"),
        "3": ("data/attack_trees/payment_system_digitalised.json", "Payment System (Digitalised)"),
        "4": ("data/attack_trees/supply_chain_digitalised.json", "Supply Chain (Digitalised)")
    }

    while True:
        choice = input("Enter choice (1-6): ").strip()

        if choice in ["1", "2", "3", "4"]:
            # Single analysis
            file_path, description = attack_trees[choice]
            print(f"\nAnalysing: {description}")
            print("-" * 60)

            if tree.load_from_json(file_path):
                tree.build_graph()
                tree.input_values_interactive()
                tree.get_risk_breakdown()
                overall_risk = tree.calculate_risk()
                print(f"\nDisplaying {description} with risk values...")
                tree.visualise(show_values=True)
            break

        if choice == "5":
            # Compare payment systems
            print("\nCOMPARISON MODE: Payment Systems")
            print("=" * 60)
            print("You'll analyse both current and digitalised payment systems")
            print("This helps compare risks before and after transformation")
            print()

            results = {}
            for scenario, (file_path, description) in [
                ("current", attack_trees["1"]),
                ("digitalised", attack_trees["3"])
            ]:
                print(f"\n>>> ANALYSING: {description.upper()} <<<")
                tree_instance = AttackTree()
                if tree_instance.load_from_json(file_path):
                    tree_instance.build_graph()
                    tree_instance.input_values_interactive()
                    risk = tree_instance.calculate_risk()
                    results[scenario] = {
                                        "risk": risk,
                                        "tree": tree_instance,
                                        "description": description
                                        }

            # Show comparison summary
            print("\n" + "=" * 60)
            print("PAYMENT SYSTEM RISK COMPARISON SUMMARY")
            print("=" * 60)
            if "current" in results and "digitalised" in results:
                current_risk = results["current"]["risk"]
                digital_risk = results["digitalised"]["risk"]
                difference = digital_risk - current_risk

                print(f"Current System Risk:      £{current_risk:,.2f}")
                print(f"Digitalised System Risk:  £{digital_risk:,.2f}")
                print(f"Risk Change:              £{difference:,.2f}")

                if difference > 0:
                    print(f"📈 Digitalisation INCREASES risk by £{difference:,.2f}")
                elif difference < 0:
                    print(f"📉 Digitalisation REDUCES risk by £{abs(difference):,.2f}")
                else:
                    print("⚖️  Risk remains the same")

                print("\nRecommendation based on your Assignment 1 analysis:")
                print("Proceed with digitalisation but implement security controls")
            break

        if choice == "6":
            # Compare supply chains
            print("\nCOMPARISON MODE: Supply Chains")
            print("=" * 60)
            print("You'll analyse both current and digitalised supply chain risks")
            print()

            results = {}
            for scenario, (file_path, description) in [
                ("current", attack_trees["2"]),
                ("digitalised", attack_trees["4"])
            ]:
                print(f"\n>>> ANALYSING: {description.upper()} <<<")
                tree_instance = AttackTree()
                if tree_instance.load_from_json(file_path):
                    tree_instance.build_graph()
                    tree_instance.input_values_interactive()
                    risk = tree_instance.calculate_risk()
                    results[scenario] = {
                        "risk": risk,
                        "tree": tree_instance,
                        "description": description
                        }

            # Show comparison summary
            print("\n" + "=" * 60)
            print("SUPPLY CHAIN RISK COMPARISON SUMMARY")
            print("=" * 60)
            if "current" in results and "digitalised" in results:
                current_risk = results["current"]["risk"]
                digital_risk = results["digitalised"]["risk"]
                difference = digital_risk - current_risk

                print(f"Current Supply Chain Risk:      £{current_risk:,.2f}")
                print(f"Digitalised Supply Chain Risk:  £{digital_risk:,.2f}")
                print(f"Risk Change:                    £{difference:,.2f}")

                if difference > 0:
                    print(f"📈 Digitalisation INCREASES risk by £{difference:,.2f}")
                elif difference < 0:
                    print(f"📉 Digitalisation REDUCES risk by £{abs(difference):,.2f}")
                else:
                    print("⚖️  Risk remains the same")

                print("\nRecommendation based on your Assignment 1 analysis:")
                print("Maintain local suppliers - reject international cost savings")
            break

        print("Please enter a number between 1-6")
