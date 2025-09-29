# llmops-py

A Python implementation of the LLMOps (Large Language Model Operations) toolkit, designed to simplify the lifecycle management of large language model applications, including model deployment, application configuration, knowledge base management, plugin integration, and more.


## Project Overview

`llmops-py` provides a comprehensive LLMOps solution, helping developers quickly build, deploy, and manage applications based on large language models. By encapsulating core capabilities such as model configuration, conversation management, knowledge base retrieval, and tool invocation, it reduces the complexity of LLM application development.


## Core Features

1. **AI Application Management**  
   - Lifecycle management of applications (creation, modification, duplication, deletion, and publishing)  
   - Version control for application configurations (model parameters, conversation rounds, preset prompts, etc.)  
   - Debug session and long-term memory management

2. **Knowledge Base Module**  
   - Document upload, parsing, chunking, and vector storage  
   - Semantic-based document retrieval (supports custom retrieval strategies)  
   - Tracking of document processing progress and status management

3. **Plugin Integration**  
   - Built-in tool support (e.g., Google Search, DALL-E image generation, weather queries)  
   - Third-party API tool integration and configuration  
   - Automation of tool invocation workflows and parameter management

4. **Task Scheduling**  
   - Asynchronous task processing via Celery (document building, vector computation, etc.)  
   - Distributed task execution and monitoring


## Tech Stack

- **Backend Framework**: Flask  
- **Task Queue**: Celery  
- **Cache/Message Broker**: Redis  
- **Databases**: MySQL (relational data), Vector Database (knowledge base vector storage)  
- **Authentication**: JWT  
- **Model Support**: Compatible with mainstream LLM models (e.g., OpenAI, custom models)  
- **Document Processing**: Supports parsing and chunking of formats like Markdown  


## Environment Requirements

- Python 3.9+  
- MySQL 5.7+  
- Redis 6.0+  
- Dependencies: See `requirements.txt`  


## Installation Steps

1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd llmops-py
   ```

2. **Create and Activate a Virtual Environment**  
   ```bash
   python -m venv .venv
   # Activate on Linux/Mac
   source .venv/bin/activate
   # Activate on Windows
   .venv\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**  
   ```bash
   # Run database migrations (using Alembic)
   alembic upgrade head
   ```

5. **Configure Environment Variables**  
   Create a `.env` file with required parameters (example):  
   ```ini
   # Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=password
   DB_NAME=llmops

   # Redis Configuration (Celery broker/backend)
   REDIS_URL=redis://localhost:6379/1

   # JWT Secret
   JWT_SECRET_KEY=your-secure-secret-key

   # Model Configuration
   OPENAI_API_KEY=your-openai-key
   ```


## Starting the Services

1. **Start the Flask Application**  
   ```bash
   # Development mode
   flask run --host=0.0.0.0 --port=5000
   # Or production mode with gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 "app.http.app:create_app()"
   ```

2. **Start Celery Worker (for asynchronous tasks)**  
   ```bash
   celery -A app.http.app worker -l info
   ```

3. **Start Celery Beat (for scheduled tasks, if needed)**  
   ```bash
   celery -A app.http.app beat -l info
   ```


## API Documentation

Detailed API documentation is available in `docs/01.ProjectAPI.md`, covering these core modules:

- **Authentication**: User login and permission verification  
- **Applications**: App creation, configuration updates, and publishing management  
- **Knowledge Base**: Document upload, retrieval, and chunk management  
- **Plugins**: Tool lists and invocation configurations  
- **Tasks**: Asynchronous task status queries  


## Directory Structure

```
llmops-py/
├── app/                  # Flask application entry
├── internal/
│   ├── core/             # Core components (embedding models, etc.)
│   ├── handler/          # API handlers
│   ├── service/          # Business logic services
│   ├── task/             # Celery tasks
│   ├── lib/              # Utility functions
│   └── migration/        # Database migration scripts
├── storage/              # Storage-related (vector databases, files, etc.)
├── docs/                 # Documentation (API, database schema, etc.)
├── requirements.txt      # Dependency list
└── README.md             # Project description
```


## Example Usage

### Create an Application

```bash
# Call the API to create an application
curl -X POST http://127.0.0.1:5000/apps \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Application",
    "icon": "https://example.com/icon.png",
    "description": "My first LLM application"
  }'
```

### Upload a Knowledge Base Document

Upload a document via the API to trigger processing. The document will be automatically parsed, chunked, and stored as vectors (ensure the Celery Worker is running first).


## License

[MIT](LICENSE)
