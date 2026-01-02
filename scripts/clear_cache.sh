#!/bin/bash

###############################################################################
# Script de Limpeza de Cache - ENEM Corrections
#
# Este script limpa todos os caches do projeto Django:
# - Cache do Python (__pycache__)
# - Cache do Django (se configurado)
# - Arquivos .pyc compilados
# - Sessões expiradas
# - Arquivos temporários
#
# Uso:
#   ./scripts/clear_cache.sh
#
# Ou torne executável:
#   chmod +x scripts/clear_cache.sh
#   ./scripts/clear_cache.sh
###############################################################################

set -e  # Para se houver erro

echo "🧹 Iniciando limpeza de cache..."
echo ""

# Vai para o diretório raiz do projeto
cd "$(dirname "$0")/.."

# 1. Limpar cache do Python (__pycache__ e .pyc)
echo "📦 Removendo arquivos __pycache__ e .pyc..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "✅ Cache do Python removido"
echo ""

# 2. Limpar cache do Django (se existir)
if [ -d ".django_cache" ]; then
    echo "🗄️  Removendo cache do Django..."
    rm -rf .django_cache
    echo "✅ Cache do Django removido"
    echo ""
fi

# 3. Limpar sessões expiradas do Django
echo "🔐 Limpando sessões expiradas..."
poetry run python manage.py clearsessions 2>/dev/null || echo "⚠️  Comando clearsessions não disponível"
echo ""

# 4. Limpar arquivos temporários
echo "🗑️  Removendo arquivos temporários..."
find . -type f -name "*.log~" -delete 2>/dev/null || true
find . -type f -name "*.swp" -delete 2>/dev/null || true
find . -type f -name ".DS_Store" -delete 2>/dev/null || true
echo "✅ Arquivos temporários removidos"
echo ""

# 5. Limpar cache do navegador (instruções)
echo "🌐 Para limpar o cache do navegador:"
echo "   Chrome/Edge/Brave: Ctrl + Shift + R ou Ctrl + F5"
echo "   Firefox: Ctrl + Shift + R ou Ctrl + F5"
echo "   Safari: Cmd + Shift + R"
echo ""

# 6. Reiniciar servidor (opcional)
echo "🔄 Deseja reiniciar o servidor Django? (s/N)"
read -r resposta
if [[ "$resposta" =~ ^[Ss]$ ]]; then
    echo "🛑 Parando servidor Django..."
    pkill -f "manage.py runserver" 2>/dev/null || echo "   Nenhum servidor rodando"
    sleep 1
    echo "🚀 Iniciando servidor Django..."
    poetry run python manage.py runserver &
    echo "✅ Servidor reiniciado em http://127.0.0.1:8000/"
fi

echo ""
echo "✨ Limpeza de cache concluída com sucesso!"
echo ""
