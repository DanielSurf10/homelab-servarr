import os
import re
import shutil

# ================= CONFIGURAÇÕES =================
NOME_SERIE = "Hora de Aventura"
PASTA_DESTINO_RAIZ = "Hora de Aventura (Organizada)"
# Mude para False se quiser apenas COPIAR e manter a bagunça original como backup
MOVER_ARQUIVOS = False
# =================================================

def criar_pasta(caminho):
    if not os.path.exists(caminho):
        os.makedirs(caminho)

def detectar_info(nome_arquivo, nome_pasta_pai):
    # 1. Tenta detectar se já está renomeado (Ex: Hora de Aventura - S06E03.mp4)
    match_clean = re.search(r'[Ss](\d+)[Ee](\d+)', nome_arquivo)
    if match_clean:
        return int(match_clean.group(1)), match_clean.group(2)

    # 2. Se não, tenta detectar pelo padrão antigo "Temp 03 - Epi 25"
    match_epi = re.search(r'Epi\s*(\d+)', nome_arquivo, re.IGNORECASE)
    match_temp_file = re.search(r'Temp\s*(\d+)', nome_arquivo, re.IGNORECASE)

    # Tenta pegar temporada do arquivo, se não der, pega da pasta
    temporada = None
    if match_temp_file:
        temporada = int(match_temp_file.group(1))
    else:
        # Tenta pegar da pasta (Ex: "3ª Temporada")
        match_folder = re.search(r'(\d+)', nome_pasta_pai)
        if match_folder and "Temporada" in nome_pasta_pai:
            temporada = int(match_folder.group(1))
        elif "Curta" in nome_pasta_pai:
            temporada = 0

    if match_epi and temporada is not None:
        return temporada, match_epi.group(1)

    # 3. Padrão Temporada 10 (Números soltos)
    match_loose = re.match(r'^(\d+)\s*-', nome_arquivo)
    if match_loose and temporada is not None:
        return temporada, match_loose.group(1)

    # 4. Multi-episódios (13E14E15)
    match_multi = re.match(r'^(\d+(?:[Ee]\d+)+)', nome_arquivo)
    if match_multi and temporada is not None:
        return temporada, match_multi.group(1)

    return None, None

def main():
    pasta_atual = os.getcwd()
    criar_pasta(PASTA_DESTINO_RAIZ)

    print(f"🧹 Iniciando limpeza em: {pasta_atual}")
    print(f"📂 Destino: {PASTA_DESTINO_RAIZ}\n")

    contagem = 0

    for root, dirs, files in os.walk(pasta_atual):
        # Evita processar a própria pasta de destino para não entrar em loop
        if PASTA_DESTINO_RAIZ in root:
            continue

        nome_pasta_pai = os.path.basename(root)

        for arquivo in files:
            if not arquivo.endswith(('.mkv', '.mp4', '.avi')):
                continue

            # Pula o próprio script
            if arquivo == os.path.basename(__file__):
                continue

            temporada, episodio = detectar_info(arquivo, nome_pasta_pai)

            if temporada is not None and episodio is not None:
                # Define o nome da pasta da temporada (Season 01, Season 02...)
                nome_pasta_season = f"Season {temporada:02d}"
                if temporada == 0:
                    nome_pasta_season = "Season 00" # Curtas/Especiais

                # Cria o caminho final
                caminho_destino_season = os.path.join(PASTA_DESTINO_RAIZ, nome_pasta_season)
                criar_pasta(caminho_destino_season)

                # Define o novo nome padronizado
                ext = os.path.splitext(arquivo)[1]
                novo_nome = f"{NOME_SERIE} - S{temporada:02d}E{episodio}{ext}"

                origem = os.path.join(root, arquivo)
                destino = os.path.join(caminho_destino_season, novo_nome)

                # Verifica se não é o mesmo arquivo
                if os.path.abspath(origem) == os.path.abspath(destino):
                    continue

                print(f"Moveu: {arquivo} \n   --> {nome_pasta_season}/{novo_nome}")

                try:
                    if MOVER_ARQUIVOS:
                        shutil.move(origem, destino)
                    else:
                        shutil.copy2(origem, destino)
                    contagem += 1
                except Exception as e:
                    print(f"❌ Erro ao mover: {e}")

    print(f"\n✅ Concluído! {contagem} episódios organizados na pasta '{PASTA_DESTINO_RAIZ}'.")
    print("Agora você pode apontar o Sonarr para essa nova pasta.")

if __name__ == "__main__":
    main()
