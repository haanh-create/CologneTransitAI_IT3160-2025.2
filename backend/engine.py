import networkx as nx
import json
import os


def _normalize_line(line):
    """Normalize a line value to a list of strings (handles str, list, None)."""
    if line is None:
        return []
    if isinstance(line, list):
        return [str(l) for l in line]
    return [str(line)]


class TransitEngine:
    def __init__(self, data_path):
        self.data_path = data_path
        self.graph = nx.Graph()
        self.disabled_lines = set()
        self.load_network()

    def load_network(self):
        if not os.path.exists(self.data_path):
            print(f"Warning: Data file {self.data_path} not found.")
            return

        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Add nodes
        for node in data['nodes']:
            self.graph.add_node(node['id'], **node)

        # Add edges
        for edge in data['edges']:
            self.graph.add_edge(
                edge['source'],
                edge['target'],
                line=edge['line'],
                weight=edge['length'],
                length=edge['length']
            )

        print(f"Loaded graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges.")

    def _is_edge_disabled(self, edge_data):
        """Return True if ALL lines of this edge are disabled (or has no lines)."""
        lines = _normalize_line(edge_data.get('line'))
        if not lines:
            return False  # unknown line, keep active
        # Edge is disabled only when every line it belongs to is disabled
        return all(line in self.disabled_lines for line in lines)

    def get_all_lines(self):
        lines = set()
        for u, v, data in self.graph.edges(data=True):
            for line in _normalize_line(data.get('line')):
                lines.add(line)
        return sorted(list(lines))

    def toggle_line(self, line_name, disabled=True):
        if disabled:
            self.disabled_lines.add(line_name)
        else:
            self.disabled_lines.discard(line_name)
        return list(self.disabled_lines)

    def find_path(self, start_node_id, end_node_id):
        # Filtered graph — exclude edges where ALL lines are disabled
        active_edges = [
            (u, v, d) for u, v, d in self.graph.edges(data=True)
            if not self._is_edge_disabled(d)
        ]

        sub_graph = nx.Graph()
        sub_graph.add_nodes_from(self.graph.nodes(data=True))
        sub_graph.add_edges_from(active_edges)

        try:
            path = nx.shortest_path(sub_graph, source=start_node_id, target=end_node_id, weight='weight')

            # Construct path details
            path_details = []
            total_distance = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge_data = self.graph.get_edge_data(u, v)
                dist = edge_data.get('length', 0)
                total_distance += dist
                lines = _normalize_line(edge_data.get('line'))
                path_details.append({
                    "from": u,
                    "to": v,
                    "line": lines[0] if lines else None,
                    "distance": dist,
                    "from_name": self.graph.nodes[u].get('name'),
                    "to_name": self.graph.nodes[v].get('name')
                })

            return {
                "success": True,
                "path": path,
                "details": path_details,
                "total_distance": total_distance
            }
        except nx.NetworkXNoPath:
            return {"success": False, "error": "No path found (lines might be disabled)"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_network_data(self):
        """Return nodes and edges for visualization."""
        nodes = []
        for node_id, data in self.graph.nodes(data=True):
            nodes.append(data)

        edges = []
        for u, v, data in self.graph.edges(data=True):
            lines = _normalize_line(data.get('line'))
            # Use the first line name for display; edge is active if any line is active
            display_line = lines[0] if lines else None
            active = not self._is_edge_disabled(data)
            edges.append({
                "source": u,
                "target": v,
                "line": display_line,
                "length": data.get('length'),
                "active": active
            })

        return {"nodes": nodes, "edges": edges, "disabled_lines": list(self.disabled_lines)}
