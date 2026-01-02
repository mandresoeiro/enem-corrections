#!/bin/bash

###############################################################################
# Script para Servir Documentação MkDocs
#
# Este script inicia o servidor de documentação do MkDocs
#
# Uso:
#   ./scripts/serve_docs.sh
###############################################################################

set -e

echo "📚 Iniciando servidor de documentação MkDocs..."
echo ""

# Vai para o diretório raiz do projeto
cd "$(dirname "$0")/.."

# Verifica se o mkdocs está instalado
if ! poetry run mkdocs --version > /dev/null 2>&1; then
    echo "❌ MkDocs não encontrado!"
    echo "📦 Instalando MkDocs..."
    poetry add mkdocs mkdocs-material --group dev
fi

echo "🚀 Servidor de documentação disponível em: http://127.0.0.1:8001/"
echo "📝 Pressione Ctrl+C para parar o servidor"
echo ""

# Inicia o servidor MkDocs
poetry run mkdocs serve --dev-addr 127.0.0.1:8001
