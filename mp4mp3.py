import os
import subprocess

# Caminho para a pasta de origem dos arquivos MP4
SOURCE_PATH = "./Videos"

# Caminho para a pasta de destino dos arquivos MP3
DEST_PATH = "./saidaMp3"

# Loop para converter cada arquivo MP4 em MP3 de 128kbps mono
for filename in os.listdir(SOURCE_PATH):
    if filename.endswith(".mp4"):
        # Extrai o nome do arquivo sem a extensão
        name = os.path.splitext(filename)[0]

        # Cria a pasta "saidaMp3" se ainda não existir
        os.makedirs(DEST_PATH, exist_ok=True)

        # Caminhos dos arquivos de entrada e saída
        input_file = os.path.join(SOURCE_PATH, filename)
        output_file = os.path.join(DEST_PATH, f"{name}.mp3")

        # Converte o arquivo MP4 em MP3 de 128kbps mono
        subprocess.run(["ffmpeg", "-i", input_file, "-vn", "-ac", "1", "-b:a", "128k", output_file])

        # Extrai um quadro do vídeo para usar como thumbnail
        thumbnail_file = os.path.join(DEST_PATH, f"{name}.jpg")
        subprocess.run(["ffmpeg", "-i", input_file, "-ss", "00:00:02", "-vframes", "1", thumbnail_file])

        # Adiciona a imagem de capa ao arquivo MP3 usando eyeD3
        subprocess.run(["eyeD3", "--add-image", f"{thumbnail_file}:FRONT_COVER", output_file])

        # Remove a imagem do quadro
        os.remove(thumbnail_file)

print("Conversão concluída!")
