import os
import shutil
from datetime import datetime, timedelta

# Diretório de origem dos vídeos
diretorio_origem = "curso"

# Criar diretório de destino
diretorio_destino = "curso_separado"
os.makedirs(diretorio_destino, exist_ok=True)

# Listar os vídeos no diretório de origem
videos = [arquivo for arquivo in os.listdir(diretorio_origem) if arquivo.endswith(".mp4")]
videos.sort()

# Definir a data atual
data_atual = datetime.now()

# Definir a diferença de dias para cada grupo
dias_por_grupo = 20

# Dividir os vídeos em grupos de 10 e criar pastas com datas futuras
for indice, video in enumerate(videos):
    # Calcular a data futura para o grupo
    data_futura = data_atual + timedelta(days=indice // dias_por_grupo)
    nome_pasta = data_futura.strftime("%Y-%m-%d")
    
    # Criar diretório para o grupo
    diretorio_grupo = os.path.join(diretorio_destino, nome_pasta)
    os.makedirs(diretorio_grupo, exist_ok=True)
    
    # Mover o vídeo para o diretório do grupo
    caminho_origem = os.path.join(diretorio_origem, video)
    caminho_destino = os.path.join(diretorio_grupo, video)
    shutil.move(caminho_origem, caminho_destino)
    print(f"Movendo {video} para {caminho_destino}")

print("Separação de vídeos concluída.")
