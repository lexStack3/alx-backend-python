# Messaging App - Robust API Development with Django
A backend-focused project designed to introduce learners to the full lifecycle of building **robust RESTful APIs** using **Django** and optional enhancements with **Django REST Framework (DRF)**. This project emphasizes clean architecture, scalable design, and Django best practices, serving as a foundation for any backend developer mastering API development.

## Project Overview
This project guides me through building a production-ready messaging API system. I will:
- Scaffold a Django project from scratch
- Design relational data models
implement one-to-one, one-to-many, and many-to-many relationships
- Build RESTful endpoints using Django's modular approach
- Follow best practices for project structure, environment management, and documentation
- Validate APIs with real data using tools like Postman or Swagger

The final product is clean, maintainable API layer that simulate a real-world messaging platform.


## Project Objectives
By the end of this project, I will be able to:
- Create a Django/DRF-powered backend system
- Define scalable data models using Django ORM
- Build and manage database relationships effectively
- Structure Django apps modularly
- Configure versioned API routes using `path()`, `include()`, and DRF routers
- Implement serializers and viewsets for complex nested relationships
- Follow best practices for readability, security, and maintainability
- Test my APIs using Postman or Django test client

## Learning Outcomes
Completing this project enables me to:
- Understand Django project scaffolding and app structure
- Translate requirements into relational database schemas
- Use Django ORM for migrations and CRUD operations
- Build RESTful endpoints returning JSON data
- Apply modular development strategies with reusable apps
- Use DRF serializers and viewsets to handle nested data
- Maintain clean URL routing with versioning (e.g., `/api/v1`)
- Write well-documented and production-ready backend code

## Key Implementation Phases
### 1. Project Setup & Environment Configuration
- Create virtual environment
- Install Django and DRF
- Run `django-admin startproject messaging_app`
- Create messaging app: `python manage.py startapp chats`
- Configure `settings.py` (installed app, CORS, middleware, etc.)

### 2. Defining Data Models
Models include:
- #### User - Extended from Django's `AbstractUser` to support:
  - `user_id` (UUID)
  - name fields
  - email, password hash
  - phone number
  - role (`guest`, `host`, `admin`)
  - timestamps

- #### Conversation
  - `conversation_id` (UUID)
  - participants (FK to User)
  - timestamps

- #### Message
  - `message_id` (UUID)
  - `sender` → User
  - `conservation` → Conversation
  - `message_body`
  - timestamp

> **I will use Django ORM to:**
>  - Add fields
>  - Apply constraints
>  - Run migrations
>  - Verify data in Django admin

### 3. Establishing Relationships
- ForeignKey, ManyToMany, OneToOne relationships
- Add `related_name`, `on_delete` behavior
- Test relationships in Django shell

### 4. Creating Serializers
Implement serializers for:
- UserSerializer
- ConversationSerializer
- MessageSerializer
> Include nested messages inside a conversation.

### 5. Building API Endpoints (Views)
- Using DRF viewsets:
  - `ConversationViewSet`
  - `MessageViewSet`
- Endpoints include:
  - List/create conversations
  - Send messages within a conversation

### 6. Configuring URL Routing
- Use DRF `DefaultRouter`
- Register routes for conversations and messages
- Include them under `/api/` inside `messaging_app/urls.py`

### 7. Running & Testing
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Fix any raised errors and validate endpoints using Postman, Curl, or Swagger.

## Respository Structure
```markdown

alx-backend-python/
│
└── messaging_app/
    ├── messaging_app/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── ...
    ├── chats/
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── ...
    └── manage.py
```

## Endpoints Overview
Resource | Endpoint | Methods | Description
--- | --- | --- | ---
Conversations | `/api/conversations/` | GET, POST | List conversations, Create Conversation
Conversations Detail | `/api/conversations/<id>/` | GET | Retrieve single conversation
Messages | `/api/messages/` | GET, POST | List messages, Send message
Message by Conversation | `/api/conversations/<id>/messages/` | GET | List all messages inside a conversation


## Best Practices Followed

Area | Best Practices
--- | ---
Project Structure | Organized apps, clean folder structure, reusable modules
Environment Config | `.env` files, no hardcoded secrets
Models | Keep business logic outside models use managers for abstractions
Migrations | Commit all migrations; test on fresh DB
Routing | Namespaced and versioned (`/api/v1/`) routes
Security | Proper CORS handling, secure settings
Testing | Use API clients (Django test client/Postman)
Documentation | Clear README, inline comments, optional Swagger docs
---

## Conversations API
### 1. List All Conversations
**GET** `/api/conversations/`
Response Example
```json
[
  {
    "conversation_id": "d2a8c3f2-9c8b-46f7-aa14-15aa32e2f4b7",
    "participants": [
      {
        "user_id": "01f23cf0-2c43-4d55-acbb-34ab1c1122aa",
        "first_name": "Alexander",
        "last_name": "Edim"
      }
    ],
    "created_at": "2025-01-10T12:00:00Z",
    "messages": []
  }
]
```
### 2. Create a New Conversation
**POST** `/api/conversations/`
Request Body
```json
{
  "participants": ["01f23cf0-2c43-4d55-acbb-34ab1c1122aa", "15c33eaf-1182-42ff-b9ce-91df892bc8c1"]
}
```
Response
```Json
{
  "conversation_id": "d2a8c3f2-9c8b-46f7-aa14-15aa32e2f4b7",
  "participants": [...],
  "created_at": "2025-01-10T12:05:00Z"
}
```

### 3. Retrieve Conversation Details
**GET** `/api/conversations/<conversation_id>/`
Response
```json
{
  "conversation_id": "d2a8c3f2-9c8b-46f7-aa14-15aa32e2f4b7",
  "participants": [...],
  "messages": [...],
  "created_at": "2025-01-10T12:05:00Z"
}
```
## Messages API
### 4. List All Messages
**GET** `/api/messages/`
Response
```json
[
  {
    "message_id": "51dfbfcd-f313-4f8b-bc44-82e6f7f0ca61",
    "sender": "01f23cf0-2c43-4d55-acbb-34ab1c1122aa",
    "conversation": "d2a8c3f2-9c8b-46f7-aa14-15aa32e2f4b7",
    "message_body": "Hello!",
    "sent_at": "2025-01-10T12:10:00Z"
  }
]
```
### 5. Send a Message (Create)
**POST** `/api/messages/`
Request
```json
{
  "sender": "01f23cf0-2c43-4d55-acbb-34ab1c1122aa",
  "conversation": "d2a8c3f2-9c8b-46f7-aa14-15aa32e2f4b7",
  "message_body": "Hey, are you available?"
}
```
Response
```json
{
  "message_id": "51dfbfcd-f313-4f8b-bc44-82e6f7f0ca61",
  "message_body": "Hey, are you available?",
  "sent_at": "2025-01-10T12:15:00Z"
}
```
## Message By Conversation
### 6. List Messages in a Specific Conversation
**GET** `/api/conversations/<conversation_id>/messages/`
Response
```json
[
  {
    "message_id": "51dfbfcd-f313-4f8b-bc44-82e6f7f0ca61",
    "sender": {
      "user_id": "01f23cf0-2c43-4d55-acbb-34ab1c1122aa",
      "first_name": "Alexnader",
      "last_name": "Edim"
    },
    "message_body": "Hello!",
    "sent_at": "2025-01-10T12:10:00Z"
  }
]
```
## Error Response
All error responses follow this format:
```json
{
  "detail": "Error message here."
}
```
**Examples:**
- `400 Bad Request` → invalid data
- `404 Not Found` → conversation/message not found
- `401 Unauthorized` → missing or invalid credentials

## Final Notes
This project equips me with real-world backend development skills using Django and DRF. I've learn how to structure scalable APIs, manage complex relationships, and follow professional engineering practices.
