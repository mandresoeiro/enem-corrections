# 🎓 ENEM Corrections — Plataforma de Correção de Redações

Plataforma web desenvolvida em **Django** para gestão, submissão e correção de redações no modelo ENEM, com foco em organização, clareza arquitetural e experiência do usuário.

O projeto simula um sistema educacional real, com dashboards, upload de arquivos, controle de usuários e estrutura modular preparada para evolução.

---

## 🚀 Visão Geral

O **ENEM Corrections** foi criado para resolver um problema comum em ambientes educacionais:
a **gestão centralizada e organizada de redações**, correções e desempenho dos alunos.

A aplicação contempla desde a submissão de redações até a visualização de resultados em um painel dedicado.

---

## 🧱 Arquitetura do Projeto

O projeto segue uma **arquitetura modular**, separando responsabilidades por domínio:

```text
enem-corrections/
├── accounts/        # Autenticação e usuários
├── profiles/        # Perfis e dados dos usuários
├── essays/          # Redações e submissões
├── dashboard/       # Painel do aluno
├── performance/     # Métricas e desempenho
├── core/            # Configurações centrais do projeto
├── docs/            # Documentação
├── visual/          # Componentes visuais
├── media/           # Uploads (PDFs)
```

## ⚙️ Stack Tecnológica

- Python
- Django
- Django Templates
- SQLite (ambiente de desenvolvimento)
- Poetry (gerenciamento de dependências)
- HTML / CSS
- Arquitetura modular

## ✨ Funcionalidades Implementadas

- Autenticação de usuários
- Submissão de redações em PDF
- Dashboard do aluno com:
  - lista de redações enviadas
    - acesso a materiais (ex: flipbook)
    - visualização organizada
- Upload e gerenciamento de arquivos
- Estrutura preparada para métricas de desempenho
- Separação clara entre domínio, visual e lógica

## ▶️ Executando o Projeto Localmente

1. Clone o repositório
   git clone https://github.com/mandrsoeiro/enem-corrections.git
   cd enem-corrections

2. Instale as dependências
   poetry install

3. Configure o ambiente

Crie o arquivo .env com base no exemplo:

cp .env.example .env

4. Execute as migrações
   poetry run python manage.py migrate

5. Inicie o servidor
   poetry run python manage.py runserver

Acesse em:
👉 http://127.0.0.1:8000

## 🔒 Segurança & Boas Práticas

- Variáveis sensíveis isoladas em .env
- .env ignorado no versionamento
- Estrutura preparada para evolução com Django Rest Framework
- Código organizado para leitura e manutenção

## 🧭 Próximos Passos (Roadmap)

- API REST com Django Rest Framework

- Controle de permissões (aluno / corretor / admin)

- Sistema de correção por competências do ENEM

- Relatórios de desempenho

- Integração com frontend desacoplado

## 👨‍💻 Autor

Marcio Soeiro
Desenvolvedor Backend Python
Foco em Django, APIs REST e arquitetura limpa.
🔗 GitHub: https://github.com/mandrsoeiro

## Licença

Projeto desenvolvido para fins educacionais e demonstração técnica.

---

## 4️⃣ SALVE O ARQUIVO

No VS Code:

- `Ctrl + S`

---

## 5️⃣ FINALIZE O CONFLITO (terminal)

```bash
git add README.md
git commit -m "docs: resolve merge conflict and add professional README"
git push
```

## ✅ COMO SABER SE DEU CERTO

No GitHub:

- Não pode existir <<<<<<< nem >>>>>>>
- Títulos grandes
- Blocos de código cinza
- Estrutura bonita e legível
- Se aparecer assim → conflito resolvido + README profissional 🎯
