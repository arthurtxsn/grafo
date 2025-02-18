import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Capital data
data = {
    "Estado": ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
               "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
               "RO", "RR", "RS", "SC", "SE", "SP", "TO"],
    "Capital": ["Rio Branco", "Maceió", "Manaus", "Macapá", "Salvador", "Fortaleza", "Brasília",
                "Vitória", "Goiânia", "São Luís", "Belo Horizonte", "Campo Grande", "Cuiabá",
                "Belém", "João Pessoa", "Recife", "Teresina", "Curitiba", "Rio de Janeiro",
                "Natal", "Porto Velho", "Boa Vista", "Porto Alegre", "Florianópolis", "Aracaju",
                "São Paulo", "Palmas"],
    "Latitude": [-9.97499, -9.66599, -3.10194, 0.034934, -12.9714, -3.71722, -15.7801, -20.3155,
                 -16.6869, -2.53073, -19.9208, -20.4697, -15.601, -1.45502, -7.11509, -8.04756,
                 -5.08921, -25.4284, -22.9068, -5.79448, -8.76077, 2.82384, -30.0346, -27.5954,
                 -10.9472, -23.5505, -10.1842],
    "Longitude": [-67.8243, -35.735, -60.025, -51.0694, -38.5014, -38.5434, -47.9292, -40.3128,
                  -49.2648, -44.3068, -43.9378, -54.6201, -56.0974, -48.5044, -34.8631, -34.877,
                  -42.8016, -49.2733, -43.1729, -35.211, -63.9039, -60.6753, -51.2177, -48.548,
                  -37.0731, -46.6333, -48.3336],
    "Temperatura Média": [25.5, 25.4, 27.6, 27.0, 25.3, 26.5, 21.0, 24.6, 23.2, 26.7,
                          22.1, 24.0, 27.5, 26.9, 25.7, 25.4, 27.2, 17.6, 23.2, 26.4,
                          26.5, 27.8, 19.5, 20.4, 25.6, 19.3, 26.2]
}

#Criando DataFrame
df = pd.DataFrame(data)


average2024 = 0.79
df["Temperatura Média"] += average2024

#filtering capitals
df_heat = df[df["Temperatura Média"] >= 25].reset_index(drop=True)

#crianting grafo
grafo = nx.Graph()

#add node in grafo
for _, row in df_heat.iterrows():
    name = f"{row['Capital']} ({row['Latitude']}, {row['Longitude']})"
    grafo.add_node(name, temperature=row["Temperatura Média"])

#defining starting city
startingCity = "Salvador"
initial_coords = df_heat.loc[df_heat["Capital"] == startingCity, ["Latitude", "Longitude"]].values
if initial_coords.size == 0:
    raise ValueError(f"A cidade inicial '{startingCity}' não está no conjunto filtrado!")

initial_coords = initial_coords[0]

#add edge in grafo
for _, row in df_heat.iterrows():
    if row["Capital"] != startingCity:
        node_start = f"{startingCity} ({initial_coords[0]}, {initial_coords[1]})"
        node_end = f"{row['Capital']} ({row['Latitude']}, {row['Longitude']})"
        distance = geodesic(initial_coords, (row["Latitude"], row["Longitude"])).kilometers
        grafo.add_edge(node_start, node_end, weight=distance)


pos = {f"{row['Capital']} ({row['Latitude']}, {row['Longitude']})": 
       (row["Longitude"], row["Latitude"]) for _, row in df_heat.iterrows()}

#draw grafo
temperaturas = [grafo.nodes[n]["temperature"] for n in grafo.nodes]


node_sizes = [temp * 10 for temp in temperaturas]


plt.figure(figsize=(12, 8))
nx.draw(grafo, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=node_sizes, font_size=10)

plt.title("Mapa de Conexões das Capitais Brasileiras (Nós proporcionais à temperatura)")
plt.show()
