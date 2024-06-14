class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

class Edge:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

# 创建节点
node1 = Node("车站 1")
node2 = Node("车站 2")
node3 = Node("车站 3")

# 创建边
edge1 = Edge(node1, node2)
edge2 = Edge(node2, node3)

# 将边添加到节点的连接列表中
node1.connections.append(edge1)
node2.connections.append(edge1)
node2.connections.append(edge2)
node3.connections.append(edge2)

# 打印地铁网络
for node in [node1, node2, node3]:
    print(f"节点：{node.name}")
    for edge in node.connections:
        print(f" - {edge.source.name} -> {edge.destination.name}")
