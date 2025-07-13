"""
Attack Tree Loader and Visualiser
"""

import json
import networkx as nx
import matplotlib.pyplot as plt


class AttackTree:
    """Class to load and visualise attack trees from JSON data"""
    def __init__(self):
        self.graph = nx.DiGraph()  # Directed graph for attack tree
        self.tree_data = None

    def load_from_json(self, file_path):
        """Load attack tree from JSON file"""
        try:
            with open(file_path, 'r') as file:
                self.tree_data = json.load(file)
            print(f"✓ Loaded attack tree: {self.tree_data['name']}")
            return True
        except FileNotFoundError:
            print(f"✗ Error: Could not find file {file_path}")
            return False
        except json.JSONDecodeError:
            print(f"✗ Error: Invalid JSON in {file_path}")
            return False

    def build_graph(self):
        """Convert JSON data to NetworkX graph"""
        if not self.tree_data:
            print("✗ No data loaded. Call load_from_json first.")
            return
            
        # Clear any existing graph
        self.graph.clear()
        
        # Recursively add nodes and edges
        self._add_node_recursive(self.tree_data['root'], None)
        print(f"✓ Built graph with {self.graph.number_of_nodes()} nodes")

    def _add_node_recursive(self, node, parent_id):
        """Recursively add nodes to the graph"""
        # Add current node
        self.graph.add_node(node['id'], 
                        name=node['name'], 
                        type=node['type'],
                        value=node.get('value', 0))
        
        # Add edge from parent (if exists)
        if parent_id:
            self.graph.add_edge(parent_id, node['id'])
        
        # Recursively add children
        if 'children' in node:
            for child in node['children']:
                self._add_node_recursive(child, node['id'])

    def visualise(self, show_values=True):
        """Display the attack tree with optional value display"""
        if self.graph.number_of_nodes() == 0:
            print("✗ No graph to display. Call build_graph first.")
            return
            
        # Create the plot
        plt.figure(figsize=(16, 12))
        
        # Use consistent layout with seed for reproducibility
        pos = nx.spring_layout(self.graph, k=4, iterations=50, seed=42)
        
        # Draw nodes with different colours based on type
        node_colours = []
        node_sizes = []
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id]['type']
            if node_type == 'leaf':
                node_colours.append('lightcoral')  # Red for leaf nodes
                node_sizes.append(3000)  # Larger for leaf nodes
            else:
                node_colours.append('lightblue')   # Blue for OR/AND nodes
                node_sizes.append(2500)
        
        # Draw the graph
        nx.draw(self.graph, pos, 
                node_color=node_colours,
                node_size=node_sizes,
                font_size=9,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                arrowsize=25)
        
        # Add labels with values more prominently
        labels = {}
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            name = node_data['name']
            
            # Show values prominently for leaf nodes
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
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8),
                    verticalalignment='top')
        
        plt.title(self.tree_data['name'], size=18, weight='bold', pad=20)
        plt.axis('off')  # Hide axes
        plt.show()

    def update_node_value(self, node_id, value):
        """Update the value of a specific node"""
        if node_id in self.graph.nodes():
            self.graph.nodes[node_id]['value'] = value
            print(f"✓ Updated {self.graph.nodes[node_id]['name']} = £{value:,.2f}")
            return True
        else:
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
        """Interactive method to input values for all leaf nodes"""
        if self.graph.number_of_nodes() == 0:
            print("✗ No graph loaded. Load and build a graph first.")
            return

        print("\n" + "="*50)
        print("RISK VALUE INPUT")
        print("="*50)
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
                        # Skip - keep current value
                        break
                    else:
                        value = float(user_input)
                        if value >= 0:
                            self.update_node_value(leaf['id'], value)
                            break
                        else:
                            print("Please enter a positive number or 0")
                except ValueError:
                    print("Please enter a valid number")

        print("\n✓ All values updated!")

    def calculate_risk(self):
        """Calculate overall risk assessment from leaf node values"""
        if self.graph.number_of_nodes() == 0:
            print("✗ No graph loaded. Load and build a graph first.")
            return 0

        # Start calculation from root node
        root_nodes = [node for node in self.graph.nodes() 
                    if self.graph.in_degree(node) == 0]

        if not root_nodes:
            print("✗ No root node found")
            return 0

        root_node = root_nodes[0]
        total_risk = self._calculate_node_risk(root_node)

        print(f"\n" + "="*60)
        print(f"RISK ASSESSMENT SUMMARY")
        print(f"="*60)
        print(f"Total Business Risk Exposure: £{total_risk:,.2f}")
        print(f"="*60)
        
        return total_risk

    def _calculate_node_risk(self, node_id):
        """Recursively calculate risk for a node and its children"""
        node_data = self.graph.nodes[node_id]

        # If it's a leaf node, return its value
        if node_data['type'] == 'leaf':
            return node_data['value']

        # Get all child nodes
        children = list(self.graph.successors(node_id))

        if not children:
            return 0

        # Calculate risk based on node type
        child_risks = [self._calculate_node_risk(child) for child in children]

        if node_data['type'] == 'OR':
            # OR gate: take maximum risk (worst case scenario)
            return max(child_risks) if child_risks else 0
        elif node_data['type'] == 'AND':
            # AND gate: sum all risks (all must happen)
            return sum(child_risks)
        else:
            # Default to OR logic
            return max(child_risks) if child_risks else 0

    def get_risk_breakdown(self):
        """Get detailed breakdown of risk calculations"""
        if self.graph.number_of_nodes() == 0:
            return {}

        breakdown = {}
        leaf_nodes = self.get_leaf_nodes()

        print(f"\n" + "-"*50)
        print("DETAILED RISK BREAKDOWN")
        print("-"*50)

        total_leaf_value = 0
        for leaf in leaf_nodes:
            value = leaf['value']
            total_leaf_value += value
            breakdown[leaf['name']] = value
            if value > 0:
                print(f"{leaf['name']}: £{value:,.2f}")

        overall_risk = self.calculate_risk()

        print(f"\nSum of individual attacks: £{total_leaf_value:,.2f}")
        print(f"Calculated overall risk: £{overall_risk:,.2f}")

        if overall_risk < total_leaf_value:
            print("(Lower overall risk due to OR-gate logic - not all attacks likely)")
        elif overall_risk > total_leaf_value:
            print("(Higher overall risk due to AND-gate combinations)")

        return breakdown


# Test the class
if __name__ == "__main__":
    # Create attack tree instance
    tree = AttackTree()
    
    # Load and build the payment system attack tree
    if tree.load_from_json('data/attack_trees/payment_system.json'):
        tree.build_graph()
        
        # Ask for input first
        tree.input_values_interactive()
        
        # Calculate and show risk assessment
        tree.get_risk_breakdown()
        overall_risk = tree.calculate_risk()
        
        # Show the final visual result
        print("\nDisplaying attack tree with risk values...")
        tree.visualise(show_values=True)
