# 🏦 Credit Risk AI

An intelligent REST API for credit risk analysis powered by AI. The system receives financial data from a client and returns a calculated credit score along with a detailed analysis generated in natural language by an AI model.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Customers](#customers)
  - [Credit Analysis](#credit-analysis)
- [Score Calculation Engine](#score-calculation-engine)
- [Project Structure](#project-structure)

---

## About the Project

Credit Risk AI solves a real problem in the fintech world: slow and manual credit decision-making. The API automates credit analysis by combining a custom scoring engine with an AI-generated explanation, helping financial institutions make faster and more reliable credit decisions.

The project was built with a production-grade architecture, following clean code principles, layered architecture, and REST best practices.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.13** | Main language |
| **FastAPI** | REST API framework |
| **PostgreSQL** | Relational database |
| **SQLAlchemy** | ORM for database interaction |
| **Pydantic** | Data validation and serialization |
| **Groq + LLaMA 3** | AI-generated credit analysis |
| **JWT (python-jose)** | Authentication and authorization |
| **bcrypt** | Password hashing |
| **Docker** | PostgreSQL containerization |
| **Alembic** | Database migrations |
| **Uvicorn** | ASGI server |

---

## Architecture

The project follows a layered architecture pattern, separating concerns across distinct layers:

```
Request → Endpoint (Controller) → Service (Business Logic) → Model (Database)
                ↕
           Schema (Validation)
```

- **Endpoints** — handle HTTP requests and responses
- **Services** — contain all business rules
- **Models** — define database entities
- **Schemas** — validate input and output data with Pydantic
- **Core** — global configuration, database connection, and security

---

## Features

- ✅ Customer registration with financial profile
- ✅ Automated credit score calculation engine
- ✅ Risk level classification (Low / Medium / High)
- ✅ AI-generated credit analysis in Portuguese using Groq + LLaMA 3
- ✅ JWT authentication (register and login)
- ✅ Protected endpoints — requires valid token
- ✅ Full Swagger documentation at `/docs`
- ✅ PostgreSQL via Docker
- ✅ Layered architecture with clean code practices

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.13+](https://www.python.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/tiagosilva06/credit-risk-ai.git
cd credit-risk-ai
```

2. Create and activate virtual environment:

```bash
python -m venv venv

# Windows (Git Bash)
source venv/Scripts/activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/creditrisk

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Groq AI
GROQ_API_KEY=your-groq-api-key-here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### Running the Application

1. Start the PostgreSQL database:

```bash
docker compose up -d
```

2. Start the API server:

```bash
uvicorn app.main:app --reload
```

3. Access the Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Documentation

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and get JWT token | No |

**Register example:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Login returns:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Customers

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/customers/` | Create a customer | ✅ Yes |
| GET | `/api/v1/customers/{id}` | Get customer by ID | ✅ Yes |

**Create customer example:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 35,
  "monthly_income": 8000.00,
  "current_score": 720,
  "active_debts": 1500.00,
  "patrimony": 150000.00,
  "employment_status": "employed"
}
```

Employment status options: `employed`, `self_employed`, `unemployed`

---

### Credit Analysis

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/v1/analyses/` | Request credit analysis | ✅ Yes |
| GET | `/api/v1/analyses/` | List all analyses | ✅ Yes |
| GET | `/api/v1/analyses/{id}` | Get analysis by ID | ✅ Yes |

**Request analysis example:**
```json
{
  "customer_id": 1,
  "requested_amount": 10000.00
}
```

**Response example:**
```json
{
  "id": 1,
  "customer_id": 1,
  "score": 72,
  "risk_level": "medium",
  "ai_explanation": "Resumo do Perfil Financeiro: O cliente apresenta um perfil financeiro estável...",
  "requested_amount": 10000.00,
  "created_at": "2026-05-10T21:39:17.502977"
}
```

---

## Score Calculation Engine

The scoring engine evaluates 6 financial attributes, generating a score from 0 to 100:

| Attribute | Weight | Logic |
|---|---|---|
| **Age** | Up to 25 pts | Older = more financial responsibility |
| **Monthly Income** | Up to 25 pts | Higher income = higher limit capacity |
| **Current Credit Score** | Up to 25 pts | Reflects payment history and reliability |
| **Debt Ratio** | Up to 15 pts | Active debts vs income — penalizes high commitment |
| **Patrimony** | Up to 10 pts | Assets indicate financial stability |
| **Employment Status** | Up to 10 pts | Employed > Self-employed > Unemployed |

**Risk Level Classification:**

| Score | Risk Level |
|---|---|
| 75 - 100 | 🟢 Low |
| 50 - 74 | 🟡 Medium |
| 0 - 49 | 🔴 High |

---

## Project Structure

```
credit-risk-ai/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── customer.py
│   │           └── credit_analysis.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── customer.py
│   │   ├── credit_analysis.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── customer.py
│   │   ├── credit_analysis.py
│   │   └── user.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── credit_analysis_service.py
│   └── main.py
├── tests/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

> Built with Python, FastAPI, and Groq AI — targeting the fintech and startup ecosystem.