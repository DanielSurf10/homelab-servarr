import re
import os
import qbittorrentapi

# ================= CONFIGURAÇÕES =================
# Dados do seu qBittorrent (conforme seu docker compose)
QBIT_HOST = 'localhost'
QBIT_PORT = 8080
QBIT_USER = 'admin'
QBIT_PASS = 'cachorro123456' # Se você mudou, coloque a nova senha

# Filtro para não renomear o qBittorrent inteiro sem querer
# O script só vai mexer nos torrents que tiverem essa TAG ou CATEGORIA
# Dica: Crie uma categoria "renomear" no qbit e coloque os torrents lá antes de rodar
CATEGORIA_ALVO = "renomear"

NOME_SERIE = "Hora de Aventura"
DRY_RUN = False # Mude para False para executar de verdade

# =================================================

def conectar_qbit():
    qbt_client = qbittorrentapi.Client(
        host=QBIT_HOST,
        port=QBIT_PORT,
        username=QBIT_USER,
        password=QBIT_PASS
    )
    try:
        qbt_client.auth_log_in()
        print(f"✅ Conectado ao qBittorrent v{qbt_client.app.version}")
        return qbt_client
    except qbittorrentapi.LoginFailed as e:
        print("❌ Falha no login. Verifique usuário e senha.")
        exit(1)

def limpar_nome(nome_atual, num_temporada):
    # Lógica de Regex idêntica ao script anterior
    base, ext = os.path.splitext(nome_atual)

    # Padrão SxxExx
    match_sxe = re.search(r'[Ss](\d+)[Ee](\d+(?:[Ee]\d+)*)', base)
    if match_sxe:
        s = int(match_sxe.group(1))
        e = match_sxe.group(2)
        return f"{NOME_SERIE} - S{s:02d}E{e}{ext}"

    # Padrão "Epi XX"
    match_epi = re.search(r'Epi\s*(\d+)', base, re.IGNORECASE)
    if match_epi:
        e = int(match_epi.group(1))
        return f"{NOME_SERIE} - S{num_temporada:02d}E{e:02d}{ext}"

    # Padrão numérico simples
    match_num = re.match(r'^(\d+)', base)
    if match_num:
        e = int(match_num.group(1))
        return f"{NOME_SERIE} - S{num_temporada:02d}E{e:02d}{ext}"

    return None

def main():
    client = conectar_qbit()

    # Busca apenas os torrents da categoria especificada
    torrents = client.torrents_info(category=CATEGORIA_ALVO)

    if not torrents:
        print(f"⚠️  Nenhum torrent encontrado na categoria '{CATEGORIA_ALVO}'.")
        print("   -> Vá no qBittorrent, clique com botão direito nos torrents da série e defina a categoria.")
        return

    print(f"📦 Encontrados {len(torrents)} torrents para analisar...\n")

    for torrent in torrents:
        print(f"Torrent: {torrent.name}")

        # Tenta adivinhar a temporada pelo nome da PASTA do torrent ou Categoria
        # Ex: "Hora de Aventura Temporada 1"
        match_temp = re.search(r'(\d+)', torrent.name)
        temporada = int(match_temp.group(1)) if match_temp else 0

        # Lista arquivos DENTRO do torrent
        files = client.torrents_files(torrent.hash)

        for file in files:
            old_path = file.name # Caminho completo dentro do torrent
            filename = os.path.basename(old_path)

            # Ignora arquivos que não são vídeo
            if not filename.endswith(('.mkv', '.mp4', '.avi')):
                continue

            new_filename = limpar_nome(filename, temporada)

            if new_filename and new_filename != filename:
                # O qBittorrent pede o caminho antigo completo e o novo nome
                print(f"  [Renomear API] {filename}")
                print(f"              -> {new_filename}")

                if not DRY_RUN:
                    try:
                        client.torrents_rename_file(torrent_hash=torrent.hash, old_path=old_path, new_path=new_filename)
                    except Exception as e:
                        print(f"  ❌ Erro: {e}")
            elif not new_filename:
                print(f"  ⚠️  Ignorado: {filename}")

if __name__ == "__main__":
    main()


# Pegar a pasta
# Pegar a temporada
# Listar todos os arquivos de modo que fiquem ordenados
# Renomear os arquivos usando o padrão Nome - S01E01
# Renomear usando a API do qbitorrent
