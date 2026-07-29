# Homelab Servarr

## Descricao
Stack de servicos baseada no ecossistema Arr, com automacao de midia, streaming e infraestrutura para uso domestico. A arquitetura integra busca, download, organizacao e consumo de arquivos de forma automatizada por meio de containers docker.

## Catalogo de Servicos
* **Homarr:** Dashboard central de gerenciamento e monitoramento da rede.
* **Sonarr:** Gerenciamento e automacao de series de TV.
* **Radarr:** Gerenciamento e automacao de filmes.
* **Lidarr:** Gerenciamento e automacao de musicas.
* **Suwayomi:** Servidor para download e organizacao de mangas.
* **Prowlarr:** Agregador e indexador central de trackers torrent.
* **qBittorrent:** Cliente torrent responsavel pelo download dos arquivos.
* **FlareSolverr:** Proxy para resolucao de desafios do Cloudflare.
* **DF Indexer:** Scraper em Python focado em trackers brasileiros.
* **Redis:** Banco de dados em memoria utilizado para cache do indexador.
* **Jellyfin:** Servidor de streaming e consumo de midia.
* **Watchtower:** Atualizador automatico de containers docker.

## Pre-requisitos
* Docker
* Docker Compose
* Sistema operacional baseado em Linux

## Como Usar

### 1. Variaveis de Ambiente
Crie um arquivo contendo as definicoes do seu ambiente local:
* **ARRPATH:** Caminho base para os arquivos de configuracao
* **COURSES_PATH:** Diretorio de armazenamento externo
* **PUID:** Identificador do usuario do sistema
* **PGID:** Identificador do grupo do sistema
* **TZ:** Fuso horario local

### 2. Inicializacao do Sistema
Execute o comando de preparacao do ambiente:
make setup

### 3. Configuracao Inicial dos Servicos
* **qBittorrent:** Acesse a porta 8080, verifique a senha inicial nos logs do container e altere as credenciais nas configuracoes de WebUI.
* **Prowlarr:** Adicione o qBittorrent como cliente de download e vincule os indexadores.
* **Sonarr e Radarr:** Configure as pastas de destino finais para as midias e vincule as chaves de API correspondentes no Prowlarr.
* **Jellyfin:** Avance o assistente inicial e mapeie as pastas de midias configuradas.

### 4. Ativacao de Indexadores Brasileiros
* Mova o arquivo prowlarr.yml para o diretorio de definicoes customizadas do Prowlarr.
* Reinicie o container do Prowlarr.
* Adicione o DF Indexer no painel web selecionando os scrapers necessarios.

## Portas e Servicos
* **Homarr:** 7575
* **qBittorrent:** 8080
* **Jellyfin:** 8096
* **Prowlarr:** 9696
* **Sonarr:** 8989
* **Radarr:** 7878
* **Lidarr:** 8686
* **Suwayomi:** 4567
* **FlareSolverr:** 8191
* **DF Indexer:** 7006
