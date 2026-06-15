# Pegar a pasta
# Pegar a temporada
# Listar todos os arquivos de modo que fiquem ordenados
# Renomear os arquivos usando o padrão Nome - S01E01
# Renomear usando a API do qbitorrent

import os
import qbittorrentapi
import re

NAME_SERIE	= "Hora de Aventura"
FOLDER		= "/home/daniel/Arr/Downloads/Hora de Aventura"
SEASON		= 1

# files = os.listdir(FOLDER)
#
# files_list = list(files)
# files_list.sort()
#
# for i in range(len(files_list)):
#
# 	season	= f"0{SEASON}" if SEASON < 10 else f"{SEASON}"
# 	episode	= f"0{i + 1}" if i + 1 < 10 else f"{i + 1}"
#
# 	print(f"{NAME_SERIE} - S{season}E{episode} -> {files_list[i]}")

qbt_client = qbittorrentapi.Client(
	host='localhost',
	port=8080,
	username='admin',
	password='cachorro123456'
)

try:
	qbt_client.auth_log_in()
	# print(f"Conectado ao qBittorrent v{qbt_client.app.version}")
except qbittorrentapi.LoginFailed as e:
	print(f"Erro ao conectar: {e}")
	exit(1)

torrents = qbt_client.torrents_info()

# Encontrar por nome
torrent = None
for t in torrents:
	if NAME_SERIE in t.name:
		torrent = t
		break

if (torrent == None):
	print("Não foi possível encontrar: " + NAME_SERIE)


# arquivos_s01 = [f for f in torrent.files if "Temp 01" in f.name]
#
# file_ep_1 = arquivos_s01[0]
#
# print(*[f.name for f in arquivos_s01], sep="\n")
#
# # torrent.rename_file(
# # 	file_id=file_ep_1.index,
# # 	new_file_name=f"{NAME_SERIE} - S01E01 - Pânico na Festa do Pijama.mkv")


videos = qbt_client.torrents_info(
	category="renomear",
	sort="name"
)[0]

pattern_season = r'(\d+)[ªº]\s+Temporada'

for i in videos.files:
	original_path = i.name
	parts = original_path.split('/')
	folder = '/'.join(parts[:-1])
	file_name = parts[-1]

	match_season = re.search(pattern_season, folder)
	if match_season:
		season = match_season.group(1)

		if season == "9":
			# episode_match = re.search(r'Epi\s+(\d+)\s+-\s+(.+?)\s+-\s+TORRENTMEGAFILMES', file_name)
			# episode_match = re.search(r'Epi\s+(\d+)(?:\s+-\s+(.+?))?(?:\.mkv)?$', file_name)
			episode_match = re.search(r'S(\d+)E(\d+)', file_name)
			# print(file_name)

			if episode_match:
				episode = episode_match.group(2)
				# episode_name = episode_match.group(2) if episode_match.group(2) else "Sem nome"
				episode_name = "Sem nome"
				print(f"{folder}/{NAME_SERIE} - S{season}E{episode} - {episode_name}.mp4")
				torrent.rename_file(
					file_id=i.index,
					new_file_name=f"{folder}/{NAME_SERIE} - S{season}E{episode} - {episode_name}.mp4"
				)




	# print(f"{folder}/{NAME_SERIE} - S{1}E{1}")
