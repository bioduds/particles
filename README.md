# Aulas - Plataforma de Gerenciamento de Tarefas para Alunos

Plataforma web educacional para gerenciar tarefas, notas e comunicação entre alunos e professores.

## Stack Tecnológico

- **Backend**: Django 4.2 + Django REST Framework
- **Banco de Dados**: PostgreSQL 15
- **Cache**: Redis 7
- **Reverse Proxy**: Nginx Alpine
- **Container**: Docker Compose

## Começar Rápido

### Pré-requisitos

- Docker e Docker Compose instalados
- Git

### 1. Clonar e iniciar

```bash
git clone <seu-repo>
cd Aulas
docker-compose up -d
```

### 2. Acessar a aplicação

- **Admin Dashboard**: http://localhost/admin
  - Usuário: `admin`
  - Senha: `admin123`

- **API**: http://localhost/api/
- **Health Check**: http://localhost/health

## Estrutura do Projeto

```
Aulas/
├── project/              # Configurações Django
├── users/                # App de usuários
├── tasks/                # App de tarefas
├── classes/              # App de disciplinas
├── nginx/                # Configuração Nginx
├── requirements.txt      # Dependências Python
├── Dockerfile            # Build Django
├── docker-compose.yml    # Orquestração
└── manage.py             # CLI Django
```

## Modelos de Dados

### User (Customizado)
- Roles: student, teacher, admin
- Bio, avatar, timestamps

### Subject (Disciplina)
- Professor + alunos
- Descrição

### Task (Tarefa)
- Disciplina, título, descrição
- Data de entrega, pontuação máxima

### Submission (Entrega)
- Tarefa + aluno
- Arquivo, status (pending/submitted/graded)

### Grade (Nota)
- Submissão, score, feedback
- Professor que avaliou

### Comment (Comentário)
- Submissão, autor, texto

## Variáveis de Ambiente

Copiar `.env.example` para `.env`:

```bash
cp .env.example .env
```

Configurar conforme necessário para produção.

## Comandos Úteis

```bash
# Ver logs
docker-compose logs -f web

# Acessar shell Django
docker-compose exec web python manage.py shell

# Criar superuser adicional
docker-compose exec web python manage.py createsuperuser

# Rodar testes
docker-compose exec web pytest

# Migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## Próximos Passos (Fases 2-4)

- **Fase 2**: API REST com Django REST Framework
- **Fase 3**: Frontend com Django Templates + React (opcional)
- **Fase 4**: Testes e polimento

## Contribuindo

1. Create sua branch: `git checkout -b feature/nome`
2. Commit: `git commit -m "Descrição"`
3. Push: `git push origin feature/nome`
4. PR para main

## Licença

MIT
