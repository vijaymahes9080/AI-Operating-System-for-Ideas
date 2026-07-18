# backend/app/graph/client.py
import os
import networkx as nx
import logging
from app.config import settings

logger = logging.getLogger("graph")

class LocalGraphClient:
    def __init__(self):
        self.db_path = os.path.join(settings.DATA_DIR, "knowledge_graph.gml")
        self.graph = nx.DiGraph()
        self.load()

    def load(self):
        if os.path.exists(self.db_path):
            try:
                # GML loader
                self.graph = nx.read_gml(self.db_path)
                logger.info(f"Loaded existing Knowledge Graph containing {self.graph.number_of_nodes()} nodes.")
            except Exception as e:
                logger.error(f"Error reading knowledge graph GML: {e}. Reinitializing empty graph.")
                self.graph = nx.DiGraph()
        else:
            self.graph = nx.DiGraph()
            logger.info("Initializing new Knowledge Graph.")

    def save(self):
        try:
            nx.write_gml(self.graph, self.db_path)
        except Exception as e:
            logger.error(f"Failed to write Knowledge Graph to disk: {e}")

    def add_node(self, node_id: str, label: str, properties: dict) -> bool:
        # NetworkX stores node parameters as attributes
        self.graph.add_node(node_id, label=label, **properties)
        self.save()
        return True

    def add_edge(self, source_id: str, target_id: str, edge_type: str, properties: dict = None) -> bool:
        if not self.graph.has_node(source_id) or not self.graph.has_node(target_id):
            logger.error(f"Failed to link edge. Nodes {source_id} or {target_id} do not exist.")
            return False
        
        edge_properties = properties or {}
        self.graph.add_edge(source_id, target_id, type=edge_type, **edge_properties)
        self.save()
        return True

    def get_project_subgraph(self, project_id: str) -> dict:
        """Returns JSON representation of nodes and edges matching project context."""
        nodes = []
        links = []
        
        # Traverse graph nodes. Filter nodes that belong to the active project
        for n_id, data in self.graph.nodes(data=True):
            if data.get("project_id") == project_id or n_id == project_id:
                # Extract clean attributes
                node_item = {"id": n_id}
                node_item.update(data)
                nodes.append(node_item)
                
        # Find connecting edges between these nodes
        node_ids = {node["id"] for node in nodes}
        for u, v, data in self.graph.edges(data=True):
            if u in node_ids and v in node_ids:
                links.append({
                    "source": u,
                    "target": v,
                    "type": data.get("type", "RELATED_TO")
                })
                
        return {"nodes": nodes, "links": links}

    def clear(self):
        self.graph.clear()
        self.save()

graph_client = LocalGraphClient()
