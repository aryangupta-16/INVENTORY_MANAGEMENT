# Inventory Management — Backend (FastAPI)

Backend service for the Inventory Management application. It provides user authentication, customer and product management, stock tracking, purchase recording, and an AI agent interface powered by LangChain/LangGraph + Ollama.

## Tech Stack
- FastAPI: Web framework and routing
- SQLAlchemy + SQLite: ORM and default local database (`./test.db`)
- Pydantic v2: Request/response validation and serialization
- Uvicorn: ASGI server
- JWT (`python-jose`, `pyjwt`): Authentication, `HTTPBearer` guard
- Passlib + bcrypt: Password hashing and verification
- Dotenv: Environment configuration
- LangChain, LangGraph: Agent workflow orchestration
- Ollama (ChatOllama) and optional OpenAI (ChatOpenAI): LLM backends
- Sentence-Transformers, FAISS: Vector and embedding utilities (ready for future use)

Python version: `>= 3.13` (per `pyproject.toml`).

## Core Features
- Users
	- Register, login (JWT issued), `GET /users/me`, update, delete
- Products
	- Create, list with filters (name/category/price range), get by id, update, delete
	- Low-stock detection based on `threshold`
- Stock
	- Add/remove stock with audit history and reasons
	- Per-product change history, low-stock overview
- Customers & Purchases
	- Create/list/delete customers
	- Record purchases (updates customer pending amount and reduces product stock)
	- Get all purchases for the vendor
- AI Agent
	- Single entrypoint `POST /chat/v1` that routes queries to Customer or Inventory agents via LangGraph
	- Agents call typed tools for data access and modifications

## Architecture
- `app/main.py`: FastAPI app, CORS, router mounts, DB init
- Routers (`app/api/*`): HTTP endpoints for users, products, stock, customers, and AI agent
- Services (`app/service/*`): Business logic (validation, orchestration)
- Repositories (`app/repository/*`): SQLAlchemy data access
- Models (`app/model/*`): ORM entities (User, Product, Stock, Customer, CustomerPurchase)
- Schemas (`app/schema/*`): Pydantic models for requests/responses
- Security (`app/utils/security.py`): JWT create/decode, current user guard (`HTTPBearer`)
- Passwords (`app/utils/password.py`): Hash/verify via Passlib+bcrypt
- Exceptions (`app/exception.py`, `app/utils/error_handler.py`): Custom HTTP exceptions and global handlers
- LLM & Agents (`app/llm/*`, `app/agents/*`, `app/graph/*`, `app/tools/*`): LLM config, agent orchestration and tool-backed actions
- Database (`app/config/database.py`): SQLAlchemy engine/session (`sqlite:///./test.db`), `Base` declarative

## Authentication
- JWT bearer required for most routes via `Authorization: Bearer <token>`
- Obtain token using `POST /users/login` with email/password

## API Overview (summary)

Users (`/users`)
- `POST /users/register` → create account
- `POST /users/login` → returns `{ access_token, token-type }`
- `GET /users/me` → current user
- `GET /users/{user_id}` → user by id
- `GET /users` → list users (protected)
- `PUT /users/me` → update current user
- `DELETE /users/me` → delete current user

Products (`/products`)
- `POST /products` → create product
- `GET /products` → list with optional filters: `name`, `category`, `price_min`, `price_max`, `skip`, `limit`
- `GET /products/low` → low-stock products
- `GET /products/{product_id}` → get product
- `PUT /products/{product_id}` → update product
- `DELETE /products/{product_id}` → delete product

Stock (`/stock`)
- `POST /stock/add` → add stock `{ product_id, change, reason? }`
- `POST /stock/remove` → remove stock `{ product_id, change, reason? }`
- `GET /stock/{product_id}/history` → chronological changes
- `GET /stock/low` → low-stock products

Customers (`/customers`)
- `POST /customers` → create customer
- `GET /customers` → list customers
- `DELETE /customers/{customer_id}` → delete customer
- `POST /customers/purchase` → record purchase `{ customer_id, product_id, quantity, paid }`
- `GET /customers/purchases` → list purchases

AI Agent (`/chat/v1`)
- `POST /chat/v1` → body `{ query: string }`
	- Routes to `CustomerAgent` or `InventoryAgent` via `RouterAgent` (LangGraph)
	- Agents use bound tools to read/write data (e.g., check/add/reduce stock, list customers, record purchases)

## Getting Started

1) Create a virtual environment (macOS zsh)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

2) Install dependencies (from `pyproject.toml` list)

```bash
pip install bcrypt email-validator faiss-cpu fastapi jwt langchain langchain-core langchain-ollama langchain-openai openai-agents "passlib[bcrypt]" pydantic pyjwt python-dotenv "python-jose[cryptography]" sentence-transformers sqlalchemy uvicorn
```

3) Environment variables
- `OPENAI_API_KEY` (optional) if you switch to `ChatOpenAI` in `app/llm/ollama_llm.py`
- Ollama must be installed and the model available (default: `llama3.1`) for `ChatOllama`

On macOS, install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
```

4) Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at `http://localhost:8000/docs`.

## Development Notes
- Database: default SQLite file `./test.db`. Tables auto-created on startup via `Base.metadata.create_all`.
- Auth: `HTTPBearer` protects most routes; attach `Authorization: Bearer <token>`.
- Error handling: request validation errors and uncaught exceptions return structured JSON.
- Switching LLMs: edit `app/llm/ollama_llm.py` to use `ChatOpenAI(model="gpt-4")` instead of `ChatOllama` (requires `OPENAI_API_KEY`).
- Agents & Tools: Tools are pure Python functions calling repository layer; safe DB session management is handled for non-FastAPI contexts.

## Folder Structure (backend)

```
app/
	api/               # FastAPI routers (Users, Products, Stock, Customers, AI Agent)
	agents/            # RouterAgent, InventoryAgent, CustomerAgent
	config/            # DB engine/session
	graph/             # LangGraph workflow (`build_graph`) and state
	llm/               # LLM configuration (Ollama/OpenAI)
	model/             # SQLAlchemy models
	repository/        # Data access methods (CRUD, queries)
	schema/            # Pydantic request/response models
	service/           # Business logic
	tools/             # Tool functions bound to agents (inventory, customer)
	utils/             # Security, password, error handlers
main.py              # FastAPI app bootstrap
```

---

For questions or improvements, consider enhancing tests under `app/tests` and adding migrations or a production-ready database. 
