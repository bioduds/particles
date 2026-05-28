# Guia de Desenvolvimento

## Iniciar Ambiente de Desenvolvimento

Com hot reload automático:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

## Criar Token de Autenticação

```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py shell
```

Dentro do shell:
```python
from rest_framework.authtoken.models import Token
from users.models import User

user = User.objects.get(username='admin')
token, created = Token.objects.get_or_create(user=user)
print(token.key)
```

## Testar API

Usar o token obtido acima:

```bash
TOKEN="seu_token_aqui"

# Listar usuários
curl -H "Authorization: Token $TOKEN" http://localhost/api/users/

# Dados do usuário atual
curl -H "Authorization: Token $TOKEN" http://localhost/api/users/me/

# Listar disciplinas
curl -H "Authorization: Token $TOKEN" http://localhost/api/subjects/

# Listar tarefas
curl -H "Authorization: Token $TOKEN" http://localhost/api/tasks/
```

## Acessos

- **Admin**: http://localhost/admin (admin/admin123)
- **API**: http://localhost/api/
- **Browsable API**: http://localhost/api/users/

## Comandos Úteis

```bash
# Ver logs em tempo real
docker-compose -f docker-compose.dev.yml logs -f web

# Criar novo superuser
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser

# Fazer migration
docker-compose -f docker-compose.dev.yml exec web python manage.py makemigrations
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Shell Django
docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# Rodar testes
docker-compose -f docker-compose.dev.yml exec web pytest

# Parar ambiente
docker-compose -f docker-compose.dev.yml down
```

## Hot Reload

O código local é sincronizado com o container via volume. Qualquer mudança em `.py` recarrega automaticamente o Django!

## Endpoints da API

### Autenticação
- `POST /api/auth/token/` - Obter token
- `POST /api/auth/logout/` - Logout

### Usuários
- `GET /api/users/` - Listar usuários
- `GET /api/users/me/` - Dados do usuário logado
- `POST /api/users/` - Criar novo usuário

### Disciplinas
- `GET /api/subjects/` - Listar disciplinas
- `POST /api/subjects/` - Criar disciplina
- `POST /api/subjects/{id}/add_student/` - Adicionar aluno
- `POST /api/subjects/{id}/remove_student/` - Remover aluno

### Tarefas
- `GET /api/tasks/` - Listar tarefas
- `POST /api/tasks/` - Criar tarefa
- `GET /api/tasks/{id}/` - Detalhes da tarefa

### Submissões
- `GET /api/submissions/` - Listar submissões
- `POST /api/submissions/{id}/submit/` - Submeter tarefa
- `POST /api/submissions/{id}/grade/` - Avaliar tarefa

### Comentários
- `GET /api/comments/` - Listar comentários
- `POST /api/comments/` - Criar comentário
