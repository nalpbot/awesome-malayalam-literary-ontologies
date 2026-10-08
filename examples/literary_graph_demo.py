import networkx as nx

G = nx.MultiDiGraph()

# Literary entities
G.add_node("O. V. Vijayan", type="Author")
G.add_node("Khasakkinte Itihasam", type="Work")
G.add_node("Migration", type="Theme")
G.add_node("Existentialism", type="Theme")
G.add_node("Khasak", type="Place")

# Literary relationships
G.add_edge(
    "O. V. Vijayan",
    "Khasakkinte Itihasam",
    relation="wrote"
)

G.add_edge(
    "Khasakkinte Itihasam",
    "Migration",
    relation="hasTheme"
)

G.add_edge(
    "Khasakkinte Itihasam",
    "Existentialism",
    relation="hasTheme"
)

G.add_edge(
    "Khasakkinte Itihasam",
    "Khasak",
    relation="setIn"
)

print("Literary Knowledge Graph")
print("------------------------")

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

print("\nRelationships:")

for source, target, data in G.edges(data=True):
    print(
        f"{source} --[{data['relation']}]--> {target}"
    )

