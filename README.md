# OneTask 🚀

**OneTask** é uma aplicação web de gerenciamento de tarefas (Task Management) desenvolvida com Django. Ela oferece uma experiência personalizada, permitindo que cada usuário gerencie seu fluxo de trabalho através de status customizáveis, uma visão Kanban intuitiva e integração direta com o GitHub.

---

## 🌟 Funcionalidades Principais

- **🔐 Autenticação Completa**: Sistema de login e logout seguro.
- **📊 Dashboard Inteligente**: Resumo visual do progresso, com contagem automática de tarefas por status.
- **📋 Quadro Kanban**: Visualização em colunas que permite organizar as tarefas de forma ágil.
- **🎨 Status Personalizáveis**: Cada usuário pode criar seus próprios status (ex: "Para Fazer", "Bug", "Homologação") com cores e ordens específicas.
- **🤖 Automação via Signals**: Ao se cadastrar, o usuário recebe automaticamente um conjunto de status padrão (Pendente, Em Andamento, Em Revisão, Concluída).
- **🐙 Integração com GitHub**: Importação de issues do GitHub diretamente para o OneTask.
- **📅 Datas de Entrega**: Controle de prazos com campos de `due_date`.
- **🐳 Docker Ready**: Pronto para ser executado em containers.

---

## 🛠️ Tecnologias Utilizadas

- **Back-end**: Python 3.x, Django 6.0+
- **Front-end**: Django Templates, CSS3 (Vanilla), JavaScript (ES6+)
- **Banco de Dados**: SQLite (Desenvolvimento/Padrão)
- **Infraestrutura**: Docker & Docker Compose
- **Bibliotecas Auxiliares**:
  - `python-dotenv`: Gerenciamento de variáveis de ambiente.
  - `sqlparse`: Formatação de queries SQL.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior
- Pip (gerenciador de pacotes)
- *Opcional*: Docker e Docker Compose

### Instalação Local (Manual)

1. **Clonar o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd OneTask
   ```

2. **Criar e ativar o ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate  # Windows
   ```

3. **Instalar dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variáveis de ambiente**:
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   DEBUG=True
   SECRET_KEY=sua-chave-secreta
   GITHUB_PAT=seu_token_do_github_aqui
   ```

5. **Rodar as migrações e o servidor**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Acesse: `http://127.0.0.1:8000`

### Execução via Docker

```bash
docker-compose up --build
```

---

## 📂 Estrutura do Código

- `core/`: Aplicativo principal da lógica de negócio.
  - `models.py`: Definição de `Task` (Tarefa) e `TaskStatus` (Status).
  - `views.py`: Controladores para Dashboard, Kanban, CRUDs e APIs.
  - `forms.py`: Formulários Django para validação de dados.
  - `signals.py`: Lógica para criação automática de status ao registrar usuário.
  - `templates/`: Interface do usuário organizada por módulos.
- `onetask_project/`: Configurações globais do projeto Django.
- `static/`: Arquivos estáticos (CSS, Imagens, JS).

---

## 🔌 APIs Internas

O projeto expõe endpoints internos para interações dinâmicas:

- `POST /api/task/import/`: Importa uma tarefa (usado pela integração GitHub).
- `POST /api/task/<id>/status/`: Atualiza o status de uma tarefa (usado para mover cards no Kanban).

---

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de **IA para Não Programadores**. Sinta-se à vontade para explorar e expandir!
