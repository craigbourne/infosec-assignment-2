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
    
    def visualise(self):
        """Display the attack tree"""
        if self.graph.number_of_nodes() == 0:
            print("✗ No graph to display. Call build_graph first.")
            return
            
        # Create the plot
        plt.figure(figsize=(12, 8))
        
        # Use hierarchical layout
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Draw nodes with different colors based on type
        node_colors = []
        for node_id in self.graph.nodes():
            node_type = self.graph.nodes[node_id]['type']
            if node_type == 'leaf':
                node_colors.append('lightcoral')  # Red for leaf nodes
            else:
                node_colors.append('lightblue')   # Blue for OR/AND nodes
        
        # Draw the graph
        nx.draw(self.graph, pos, 
                node_color=node_colors,
                node_size=2000,
                font_size=8,
                font_weight='bold',
                arrows=True,
                edge_color='gray',
                arrowsize=20)
        
        # Add labels
        labels = {node_id: self.graph.nodes[node_id]['name'] 
                for node_id in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=6)
        
        plt.title(self.tree_data['name'], size=16, weight='bold')
        plt.axis('off')  # Hide axes
        plt.tight_layout()
        plt.show()

# Test the class
if __name__ == "__main__":
    # Create attack tree instance
    tree = AttackTree()
    
    # Load and display the payment system attack tree
    if tree.load_from_json('data/attack_trees/payment_system.json'):
        tree.build_graph()
        tree.visualise()