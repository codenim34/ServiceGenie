# ServiceGenie Backend - Organized Structure

## 📁 Directory Structure

```
Backend/
├── app/                      # Application code
│   ├── api/                  # API routes
│   │   └── v1/              # API version 1
│   │       ├── api.py       # Router aggregator
│   │       └── endpoints/   # Individual endpoint modules
│   │           ├── users.py
│   │           ├── products.py
│   │           ├── orders.py
│   │           ├── categories.py
│   │           └── payment.py
│   ├── core/                # Core functionality
│   │   ├── config.py        # Settings & configuration
│   │   ├── database.py      # Database connection
│   │   ├── firebase.py      # Firebase Admin SDK
│   │   └── security.py      # Auth & security
│   └── models/              # Data models (Pydantic)
│       ├── user.py
│       ├── product.py
│       ├── order.py
│       └── category.py
├── scripts/                 # Utility scripts
│   ├── __init__.py
│   └── seed_db.py          # Database seeding
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration
│   ├── test_api.py         # API endpoint tests
│   └── test_db_connection.py  # Database connection test
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (gitignored)
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # Documentation
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_api.py
pytest tests/test_db_connection.py
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

## 🔧 Scripts

### Database Connection Test
```bash
python tests/test_db_connection.py
```

### Seed Database
```bash
python scripts/seed_db.py
```

## 📝 Module Organization

### app/api/
- **Purpose**: HTTP endpoints and routing logic
- **Pattern**: One file per resource (users, products, etc.)
- **Responsibilities**: Request validation, response formatting, business logic orchestration

### app/core/
- **Purpose**: Core application configuration and utilities
- **Pattern**: Singleton services and configurations
- **Responsibilities**: Database connections, auth, settings management

### app/models/
- **Purpose**: Data models and schemas
- **Pattern**: Pydantic models for validation
- **Responsibilities**: Data structure definitions, validation rules

### scripts/
- **Purpose**: Standalone utility scripts
- **Pattern**: Executable Python scripts
- **Responsibilities**: Database seeding, data migration, setup tasks

### tests/
- **Purpose**: Test suite
- **Pattern**: Mirror app structure, prefix with `test_`
- **Responsibilities**: Unit tests, integration tests, fixtures

## 🎯 Best Practices

1. **Modular Design**: Each module has a single responsibility
2. **Clear Separation**: API logic separate from business logic
3. **Type Safety**: Use Pydantic models for all data
4. **Testing**: Test files mirror app structure
5. **Documentation**: Docstrings in all public functions

## 🚀 Development Workflow

1. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Test Database Connection**
   ```bash
   python tests/test_db_connection.py
   ```

4. **Seed Database (Optional)**
   ```bash
   python scripts/seed_db.py
   ```

5. **Run Tests**
   ```bash
   pytest
   ```

6. **Start Development Server**
   ```bash
   uvicorn main:app --reload
   ```

## 📦 Adding New Features

### New API Endpoint
1. Create model in `app/models/`
2. Create endpoint in `app/api/v1/endpoints/`
3. Register route in `app/api/v1/api.py`
4. Add tests in `tests/`

### New Utility Script
1. Create script in `scripts/`
2. Import from `app/` as needed
3. Make executable and document in README

### New Test
1. Create test file in `tests/` with `test_` prefix
2. Use fixtures from `conftest.py`
3. Follow existing patterns

## 🔍 Code Organization Principles

- **DRY**: Don't Repeat Yourself
- **SOLID**: Single responsibility, Open/Closed, etc.
- **Clean Code**: Readable, maintainable, testable
- **Type Hints**: Use Python type hints everywhere
- **Documentation**: Clear docstrings and comments
