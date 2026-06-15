.PHONY: help up down restart logs ps clean build rebuild status stop start dirs

# Cores para output
GREEN  := \033[0;32m
YELLOW := \033[1;33m
NC     := \033[0m # No Color

# Carrega variáveis do .env
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

# Regra padrão - executada ao rodar apenas 'make'
.DEFAULT_GOAL := all

all: check-env setup

help: ## Mostra esta mensagem de ajuda
	@echo "${GREEN}Comandos disponíveis:${NC}"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  ${YELLOW}%-15s${NC} %s\n", $$1, $$2}'

dirs: ## Cria todas as pastas necessárias do .env
	@mkdir -p $(ARRPATH)

	@mkdir -p $(ARRPATH)/Prowlarr/config
	@mkdir -p $(ARRPATH)/Prowlarr/backup

	@mkdir -p $(ARRPATH)/Sonarr/config
	@mkdir -p $(ARRPATH)/Sonarr/backup
	@mkdir -p $(ARRPATH)/Sonarr/tvshows

	@mkdir -p $(ARRPATH)/Radarr/config
	@mkdir -p $(ARRPATH)/Radarr/backup
	@mkdir -p $(ARRPATH)/Radarr/movies

	@mkdir -p $(ARRPATH)/Lidarr/config
	@mkdir -p $(ARRPATH)/Lidarr/backup
	@mkdir -p $(ARRPATH)/Lidarr/music

	@mkdir -p $(ARRPATH)/Homarr/config
	@mkdir -p $(ARRPATH)/Homarr/icons
	@mkdir -p $(ARRPATH)/Homarr/data

	@mkdir -p $(ARRPATH)/Jellyfin/config
	@mkdir -p $(ARRPATH)/qbittorrent/config
	@mkdir -p $(ARRPATH)/Downloads

chown: ## Ajusta permissões das pastas
	sudo chown -R $(PUID):$(PGID) $(ARRPATH)
	sudo chown -R $(PUID):$(PGID) $(COURSES_PATH)

setup: dirs chown up ## Setup inicial completo
	@echo "${GREEN}Setup concluído!${NC}"
	@echo "${YELLOW}Não esqueça de configurar o qBittorrent primeiro!${NC}"
	@echo "Execute: make qbit-logs"

up: ## Sobe todos os containers em background
	sudo docker compose up -d
	@echo "${GREEN}Containers iniciados!${NC}"

down: ## Para e remove todos os containers
	@echo "${YELLOW}Parando e removendo containers...${NC}"
	sudo docker compose down
	@echo "${GREEN}Containers removidos!${NC}"

stop: ## Para todos os containers sem removê-los
	@echo "${YELLOW}Parando containers...${NC}"
	sudo docker compose stop
	@echo "${GREEN}Containers parados!${NC}"

start: ## Inicia containers já criados
	@echo "${GREEN}Iniciando containers...${NC}"
	sudo docker compose start
	@echo "${GREEN}Containers iniciados!${NC}"

restart: ## Reinicia todos os containers
	@echo "${YELLOW}Reiniciando containers...${NC}"
	sudo docker compose restart
	@echo "${GREEN}Containers reiniciados!${NC}"

build: ## Baixa as imagens mais recentes
	@echo "${GREEN}Baixando imagens...${NC}"
	sudo docker compose pull
	@echo "${GREEN}Imagens atualizadas!${NC}"

rebuild: build down up ## Atualiza imagens e recria containers

logs: ## Mostra logs de todos os containers
	sudo docker compose logs -f

logs-%: ## Mostra logs de um container específico (ex: make logs-prowlarr)
	sudo docker compose logs -f $*

ps: ## Lista containers em execução
	sudo docker compose ps

status: ps ## Alias para ps

clean: down ## Remove containers e volumes órfãos
	@echo "${YELLOW}Limpando recursos órfãos...${NC}"
	sudo docker system prune -f
	@echo "${GREEN}Limpeza concluída!${NC}"

clean-all: ## Remove containers, volumes e imagens não utilizadas
	@echo "${YELLOW}Removendo tudo (containers, volumes, imagens)...${NC}"
	sudo docker compose down -v
	sudo docker system prune -af --volumes
	@echo "${GREEN}Limpeza completa realizada!${NC}"

qbit-logs: ## Mostra logs do qBittorrent para pegar senha temporária
	@echo "${GREEN}Logs do qBittorrent:${NC}"
	sudo docker logs qbittorrent 2>&1 | grep -i "password\|temporary" || sudo docker logs qbittorrent

urls: ## Mostra URLs de acesso aos serviços
	@echo "${GREEN}URLs dos serviços:${NC}"
	@echo "  Prowlarr:    http://localhost:9696"
	@echo "  Sonarr:      http://localhost:8989"
	@echo "  Radarr:      http://localhost:7878"
	@echo "  Lidarr:      http://localhost:8686"
	@echo "  Homarr:      http://localhost:7575"
	@echo "  Jellyfin:    http://localhost:8096"
	@echo "  qBittorrent: http://localhost:8080"

check-env: ## Verifica se o arquivo .env existe
	@if [ ! -f .env ]; then \
		echo "${YELLOW}Arquivo .env não encontrado!${NC}"; \
		echo "Copie o .env.example para .env e configure as variáveis."; \
		exit 1; \
	fi
