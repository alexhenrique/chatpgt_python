import os
import subprocess

def mixagem_audios_pasta(pasta_audios, pasta_musicas, pasta_saida):
    # Cria a pasta de saída, se não existir
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Lista todos os arquivos de áudio na pasta de entrada
    arquivos_audios = os.listdir(pasta_audios)

    # Verifica se há pelo menos 20 arquivos de áudio
    if len(arquivos_audios) < 20:
        print("É necessário ter pelo menos 20 arquivos de áudio para a mixagem.")
        return

    # Carrega as músicas de relaxamento e aplica fade-in e fade-out
    musicas_relaxamento = []
    for musica in os.listdir(pasta_musicas):
        musica_path = os.path.join(pasta_musicas, musica)
        musicas_relaxamento.append(musica_path)

    # Loop pelos arquivos de áudio na pasta de entrada
    for arquivo_audio in arquivos_audios:
        arquivo_audio_path = os.path.join(pasta_audios, arquivo_audio)

        # Seleciona uma música de relaxamento aleatória
        musica_relaxamento = musicas_relaxamento[len(arquivo_audio) % len(musicas_relaxamento)]

        # Verifica se a música de fundo é mais curta que o arquivo de voz
        if float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', musica_relaxamento])) < float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', arquivo_audio_path])):
            print(f"A música de fundo selecionada é mais curta do que o arquivo de voz '{arquivo_audio}'. Selecionando uma nova música de fundo...")
            musica_relaxamento = musicas_relaxamento[len(arquivo_audio) % len(musicas_relaxamento)]

        # Caminho do arquivo de saída
        novo_arquivo_path = os.path.join(pasta_saida, arquivo_audio)

        # Comando do FFmpeg para realizar a mixagem dos áudios
        comando = [
            'ffmpeg',
            '-i', arquivo_audio_path,
            '-i', musica_relaxamento,
            '-filter_complex', '[1]afade=t=in:ss=0:d=5,afade=t=out:st=duration-5:d=5,volume=0.3[a];[0:a][a]amix=inputs=2:duration=longest',
            '-c:a', 'libmp3lame',
            '-q:a', '2',
            '-y', novo_arquivo_path
        ]

        # Executa o comando do FFmpeg
        subprocess.call(comando)

    print("Mixagem concluída!")
# Configurações
_audios = './audios'
_musicas = './relaxamento'
_saida = './saida'
# Executa a mixagem
mixagem_audios_pasta(_audios, _musicas, _saida)
