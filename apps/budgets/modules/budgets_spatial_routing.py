"""
InfraFlowX Enterprise Platform - Budgets Spatial Routing & A* Pathfinding
Implements heuristic-guided A* search for emergency transit and inspection tours.
"""

from typing import Dict, List, Any, Tuple
import heapq
import math


class BudgetsSpatialRoutingEngine:
    """
    A* heuristic pathfinding on weighted spatial networks for budgets.
    """

    @classmethod
    def euclidean_heuristic(cls, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

    @classmethod
    def find_astar_path(
        cls,
        node_coords: Dict[str, Tuple[float, float]],
        adjacency_graph: Dict[str, List[Tuple[str, float]]],
        start_node: str,
        goal_node: str,
    ) -> Dict[str, Any]:
        
        if start_node not in node_coords or goal_node not in node_coords:
            return {"path": [], "cost": -1.0, "status": "INVALID_NODES"}

        open_set = [(0.0, start_node)]
        came_from = {}
        g_score = {node: float("inf") for node in node_coords}
        g_score[start_node] = 0.0

        f_score = {node: float("inf") for node in node_coords}
        f_score[start_node] = cls.euclidean_heuristic(node_coords[start_node], node_coords[goal_node])

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal_node:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return {
                    "app_module": "budgets",
                    "path": path,
                    "total_cost": round(g_score[goal_node], 2),
                    "status": "GOAL_REACHED",
                }

            for neighbor, weight in adjacency_graph.get(current, []):
                tentative_g = g_score[current] + weight
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + cls.euclidean_heuristic(node_coords[neighbor], node_coords[goal_node])
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))

        return {"path": [], "cost": -1.0, "status": "NO_PATH_EXISTS"}
