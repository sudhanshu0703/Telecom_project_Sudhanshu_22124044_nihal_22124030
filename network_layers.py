"""
Network Layer - Addressing and routing (Step 3 & 4)
Implements Dijkstra's shortest path routing
"""
import heapq

class NetworkLayer:
    def __init__(self):
        # Node addresses (IP-like)
        self.nodes = {
            "sensor1": "192.168.1.10",
            "router1": "192.168.1.1",
            "router2": "192.168.2.1",
            "gateway": "192.168.3.1",
            "server":  "192.168.3.100"
        }
        # Topology with link costs (latency in ms)
        self.topology = {
            "sensor1": {"router1": 5},
            "router1": {"sensor1": 5, "router2": 10, "gateway": 20},
            "router2": {"router1": 10, "gateway": 8},
            "gateway": {"router1": 20, "router2": 8, "server": 3},
            "server":  {"gateway": 3}
        }

    def dijkstra(self, source, destination):
        """Step 4: Path selection using Dijkstra's routing protocol"""
        distances = {node: float('inf') for node in self.topology}
        distances[source] = 0
        previous = {node: None for node in self.topology}
        pq = [(0, source)]

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)
            if curr_node == destination:
                break
            for neighbor, weight in self.topology[curr_node].items():
                distance = curr_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = curr_node
                    heapq.heappush(pq, (distance, neighbor))

        # Reconstruct path
        path = []
        node = destination
        while node:
            path.insert(0, node)
            node = previous[node]
        return path, distances[destination]

    def add_ip_header(self, segment, src, dst):
        header = f"SRC:{self.nodes[src]}|DST:{self.nodes[dst]}|".encode('utf-8')
        return header + segment