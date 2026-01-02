# Scripts Utilitários - ENEM Corrections

Este diretório contém scripts úteis para manutenção e desenvolvimento do projeto.

## 📜 Scripts Disponíveis

### `clear_cache.sh`
**Limpeza completa de cache do projeto**

Remove todos os caches do Python e Django para garantir que as mudanças sejam refletidas:
- Cache do Python (`__pycache__`, `*.pyc`, `*.pyo`)
- Cache do Django (`.django_cache`)
- Sessões expiradas
- Arquivos temporários (`.log~`, `.swp`, `.DS_Store`)

**Uso:**
```bash
# Tornar executável (apenas primeira vez)
chmod +x scripts/clear_cache.sh

# Executar
./scripts/clear_cache.sh

# Ou executar direto do bash
bash scripts/clear_cache.sh
```

**Quando usar:**
- Após fazer alterações em templates ou views que não refletem no navegador
- Quando o servidor não carrega mudanças recentes
- Antes de fazer deploy
- Após atualizar dependências

## 🔧 Como Adicionar Novos Scripts

1. Crie um novo arquivo `.sh` neste diretório
2. Adicione o shebang no topo: `#!/bin/bash`
3. Torne-o executável: `chmod +x scripts/seu_script.sh`
4. Documente-o neste README

## 📝 Boas Práticas

- Use `set -e` para parar o script em caso de erro
- Adicione comentários explicativos
- Teste antes de commitar
- Mantenha os scripts simples e focados
