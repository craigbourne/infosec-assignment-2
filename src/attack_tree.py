"""
Attack Tree Loader and Visualiser
Author: [Your Name]
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
        plt.figure(figsize=(14, 10))
        
        # Use hierarchical layout
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Draw nodes with different colours based on type
        node_colours = []
        node_sizes = []
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id]['type']
            if node_type == 'leaf':
                node_colours.append('lightcoral')  # Red for leaf nodes
                node_sizes.append(2500)  # Slightly larger for leaf nodes
            else:
                node_colours.append('lightblue')   # Blue for OR/AND nodes
                node_sizes.append(2000)
        
        # Draw the graph
        nx.draw(self.graph, pos, 
                node_color=node_colours,
                node_size=node_sizes,
                font_size=8,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                arrowsize=20)
        
        # Add labels with optional values
        labels = {}
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            name = node_data['name']
            
            if show_values and node_data['type'] == 'leaf' and node_data['value'] > 0:
                labels[node_id] = f"{name}\n£{node_data['value']:,.0f}"
            else:
                labels[node_id] = name
        
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=7)
        
        plt.title(self.tree_data['name'], size=16, weight='bold')
        plt.axis('off')  # Hide axes
        plt.tight_layout()
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

# Test the class
if __name__ == "__main__":
    # Create attack tree instance
    tree = AttackTree()
    
    # Load and display the payment system attack tree
    if tree.load_from_json('data/attack_trees/payment_system.json'):
        tree.build_graph()
        tree.visualise(show_values=False)  # Show without values first
        
        # Let user input values
        tree.input_values_interactive()
        
        # Show again with values
        print("\nDisplaying updated attack tree with values...")
        tree.visualise(show_values=True)