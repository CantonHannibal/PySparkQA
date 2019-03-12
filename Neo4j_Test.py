from py2neo import Node, Relationship,Graph


test_graph = Graph(
    "http://localhost:7474",
)

a=Node('Genre',name="音乐")
b=Node('Genre',name="恐怖")
print(a,b)

