# API Accounts

## 🔐 Autenticação

Todas as requisições (exceto login e registro) requerem autenticação JWT.

```http
Authorization: Bearer <access_token>
```

## 📡 Endpoints

### Login

```http
POST /auth/login/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "senha123"
}
```

**Response 200:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@example.com",
    "role": "student",
    "first_name": "João",
    "last_name": "Silva"
  }
}
```

### Logout

```http
POST /auth/logout/
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "detail": "Successfully logged out."
}
```

### Refresh Token

```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response 200:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Registro

```http
POST /auth/registration/
Content-Type: application/json

{
  "username": "novousuario",
  "email": "novo@example.com",
  "password1": "SenhaForte123!",
  "password2": "SenhaForte123!"
}
```

**Response 201:**
```json
{
  "user": {
    "id": 5,
    "username": "novousuario",
    "email": "novo@example.com",
    "role": "student"
  },
  "access": "...",
  "refresh": "..."
}
```

### Listar Usuários

```http
GET /api/accounts/users/
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: Número da página (default: 1)
- `page_size`: Itens por página (default: 20)
- `role`: Filtrar por role (student/teacher/admin)
- `search`: Buscar por username ou email

**Response 200:**
```json
{
  "count": 50,
  "next": "http://api.example.com/api/accounts/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "aluno1",
      "email": "aluno1@example.com",
      "role": "student",
      "first_name": "João",
      "last_name": "Silva",
      "is_active": true,
      "date_joined": "2025-01-01T10:00:00Z"
    }
  ]
}
```

### Detalhes do Usuário

```http
GET /api/accounts/users/{id}/
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "id": 1,
  "username": "aluno1",
  "email": "aluno1@example.com",
  "role": "student",
  "first_name": "João",
  "last_name": "Silva",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2025-01-01T10:00:00Z",
  "last_login": "2025-12-08T10:30:00Z"
}
```

### Atualizar Usuário

```http
PATCH /api/accounts/users/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "João Pedro",
  "last_name": "Silva Santos"
}
```

**Response 200:**
```json
{
  "id": 1,
  "username": "aluno1",
  "email": "aluno1@example.com",
  "first_name": "João Pedro",
  "last_name": "Silva Santos"
}
```

### Deletar Usuário

```http
DELETE /api/accounts/users/{id}/
Authorization: Bearer <access_token>
```

**Response 204 No Content**

## ❌ Errors

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**400 Bad Request:**
```json
{
  "email": ["Este campo é obrigatório."],
  "password": ["A senha deve ter no mínimo 8 caracteres."]
}
```

## 🔒 Permissões

- Listar usuários: Apenas autenticados
- Ver detalhes: Apenas autenticados
- Atualizar: Apenas o próprio usuário ou admin
- Deletar: Apenas admin

## 💡 Exemplos com cURL

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"aluno@example.com","password":"Aluno123!"}'
```

**Listar usuários:**
```bash
curl -X GET http://localhost:8000/api/accounts/users/ \
  -H "Authorization: Bearer <seu_token>"
```

## 📚 SDKs e Integrações

### JavaScript/Fetch

```javascript
// Login
const response = await fetch('http://localhost:8000/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'aluno@example.com',
    password: 'Aluno123!'
  })
});
const data = await response.json();
localStorage.setItem('access_token', data.access);
```

### Python/Requests

```python
import requests

# Login
response = requests.post('http://localhost:8000/auth/login/', json={
    'email': 'aluno@example.com',
    'password': 'Aluno123!'
})
tokens = response.json()
access_token = tokens['access']

# Listar usuários
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get('http://localhost:8000/api/accounts/users/', headers=headers)
users = response.json()
```
