"""
InfraFlowX Enterprise Platform - Organizations Network Graph & Topology Optimizer
Implements Dijkstra shortest path, Kruskal minimum spanning tree, and graph bottleneck detection.
"""

from typing import Dict, List, Any, Tuple
import heapq


class OrganizationsNetworkOptimizerEngine:
    """
    Graph theory algorithms for infrastructure network optimization in organizations.
    """

    @classmethod
    def find_shortest_network_path(cls, nodes: List[str], edges: List[Dict[str, Any]], start_node: str, end_node: str) -> Dict[str, Any]:
        """
        Dijkstra's shortest path algorithm.
        edges: List of {"from": "A", "to": "B", "weight": 10.5}
        """
        adj = {node: [] for node in nodes}
        for e in edges:
            u, v, w = e["from"], e["to"], e.get("weight", 1.0)
            if u in adj and v in adj:
                adj[u].append((v, w))
                adj[v].append((u, w))

        dist = {node: float("inf") for node in nodes}
        prev = {node: None for node in nodes}
        dist[start_node] = 0.0

        pq = [(0.0, start_node)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end_node:
                break

            for v, weight in adj.get(u, []):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))

        path = []
        curr = end_node
        while curr:
            path.append(curr)
            curr = prev[curr]
        path.reverse()

        return {
            "app_module": "organizations",
            "start_node": start_node,
            "end_node": end_node,
            "shortest_distance": round(dist[end_node], 2) if dist[end_node] != float("inf") else -1.0,
            "optimal_path": path if path and path[0] == start_node else [],
            "path_reachable": dist[end_node] != float("inf"),
        }
