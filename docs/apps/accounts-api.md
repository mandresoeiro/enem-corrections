# 🔐 Accounts API – Endpoints de Autenticação

A API de autenticação utiliza **dj-rest-auth** + **SimpleJWT** para fornecer um fluxo seguro e moderno.

---

# 🔑 Login

**POST `/auth/login/`**

### Request
```json
{
  "email": "usuario@example.com",
  "password": "senha123"
}
```

### Response
```json
{
  "access": "token_jwt",
  "refresh": "refresh_token",
  "user": {
    "id": 1,
    "username": "usuario",
    "email": "usuario@example.com",
    "role": "student"
  }
}
```

---

# 🚪 Logout

**POST `/auth/logout/`**

### Response
```json
{
  "detail": "Successfully logged out."
}
```

---

# 🔄 Refresh Token

**POST `/auth/token/refresh/`**

### Request
```json
{
  "refresh": "refresh_token_value"
}
```

### Response
```json
{
  "access": "new_access_token"
}
```

---

# 🆕 Registro

**POST `/auth/registration/`**

### Request
```json
{
  "username": "novo",
  "email": "novo@example.com",
  "password1": "Senha@123",
  "password2": "Senha@123"
}
```

### Response
```json
{
  "user": {
    "id": 10,
    "username": "novo",
    "email": "novo@example.com",
    "role": "student"
  },
  "access": "token",
  "refresh": "refresh_token"
}
```

---

# 👥 Gestão de Usuários

## Listar Usuários  
**GET `/api/accounts/users/`**

Retorna lista paginada de usuários.

---

## Detalhes do Usuário  
**GET `/api/accounts/users/{id}/`**

---

## Atualizar Usuário  
**PATCH `/api/accounts/users/{id}/`**

### Exemplo:
```json
{
  "first_name": "João Pedro",
  "last_name": "Silva"
}
```

---

# 🔒 Permissões

- Rotas protegidas por JWT exigem header:
```
Authorization: Bearer <access_token>
```

- Permissões por role:
  - `teacher` → pode editar
  - `student` → somente leitura (em alguns endpoints)

---
