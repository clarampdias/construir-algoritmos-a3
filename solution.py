# pip install requests python-dotenv folium
# Autenticação
import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

load_dotenv(".env")

s = requests.Session()
res = s.post(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}"
)
print(res.text)

# Busca por linha
linhas_jabaquara = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca=JABAQUARA"
)
linhas_jabaquara = linhas_jabaquara.json()
print(f"Total de linhas encontradas: {len(linhas_jabaquara)}")

# Linha escolhida: 695X (sentido 1), cl=1441 - a de Jabaquara com mais paradas
CODIGO_LINHA = 1441

# Busca por paradas
res = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha?codigoLinha={CODIGO_LINHA}"
)
paradas = res.json()
print(f"Total de paradas: {len(paradas)}")

# Posições em tempo real
pos = s.get(
    f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha?codigoLinha={CODIGO_LINHA}"
)
pos = pos.json()
onibus = pos["vs"]
print(f"Ônibus em circulação: {len(onibus)}")

# Criação do mapa
m = Map(
    location=[paradas[0]["py"], paradas[0]["px"]],
    zoom_start=13,
)

# Paradas (azul)
for i in paradas:
    Marker(
        location=[i["py"], i["px"]],
        popup=i["np"],
        icon=Icon(color="blue"),
    ).add_to(m)

# Ônibus em tempo real (vermelho)
for b in onibus:
    Marker(
        location=[b["py"], b["px"]],
        popup=f"Ônibus {b['p']}",
        icon=Icon(color="red"),
    ).add_to(m)

m.save("mapa.html")
print("Mapa salvo em mapa.html")

# Como abrir o mapa:
# 1. python solution.py
# 2. python -m http.server 8000
# 3. http://localhost:8000/mapa.html