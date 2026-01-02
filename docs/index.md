# ENEM Corrections - Documentação

Bem-vindo à documentação oficial do sistema **ENEM Corrections**, uma plataforma completa para correção e gestão de redações do ENEM.

## 📋 Visão Geral

O ENEM Corrections é um sistema web desenvolvido em Django que permite:

- **Alunos**: Enviar redações e acompanhar suas notas e evolução
- **Professores**: Corrigir redações com base nas 5 competências do ENEM
- **Administradores**: Gerenciar usuários, visualizar estatísticas e controlar o sistema

## 🏗️ Arquitetura

O sistema é organizado em módulos Django (apps) especializados:

- **accounts**: Autenticação e gerenciamento de usuários
- **profiles**: Perfis de estudantes e professores
- **essays**: Gestão de redações e correções
- **performance**: Métricas e análise de desempenho
- **dashboard**: Interface visual do sistema
- **visual**: Componentes visuais reutilizáveis

## 🚀 Início Rápido

### Pré-requisitos

- Python >= 3.12
- Poetry (gerenciador de dependências)
- PostgreSQL (produção) ou SQLite (desenvolvimento)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/mandresoeiro/enem-corrections.git
cd enem-corrections

# Instale as dependências
poetry install

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações

# Execute as migrações
poetry run python manage.py migrate

# Crie um superusuário
poetry run python manage.py createsuperuser

# Inicie o servidor
poetry run python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

## 📚 Documentação

### Configuração
- [Settings Django](configuracao/settings.md)
- [Variáveis de Ambiente](configuracao/env.md)

### Apps
- [Accounts - Autenticação](apps/accounts.md)
- [Profiles - Perfis de Usuário](apps/profiles.md)
- [Essays - Redações](apps/essays.md)
- [Performance - Métricas](apps/performance.md)
- [Dashboard - Interface](apps/dashboard.md)

### API REST
- [API Accounts](api/accounts-api.md)
- [API Essays](api/essays-api.md)
- [API Performance](api/performance-api.md)

### Arquitetura
- [Visão Geral da Arquitetura](architecture.md)

## 🛠️ Tecnologias

- **Backend**: Django 5.1, Django REST Framework
- **Autenticação**: dj-rest-auth, django-allauth, JWT
- **Banco de Dados**: PostgreSQL / SQLite
- **Frontend**: Django Templates, TailwindCSS
- **Geração de PDF**: WeasyPrint
- **Admin**: Jazzmin

## 📝 Licença

Este projeto está sob licença MIT.

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor, leia o guia de contribuição antes de submeter PRs.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através do GitHub Issues.
