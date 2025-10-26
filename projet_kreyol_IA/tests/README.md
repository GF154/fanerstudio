# 🧪 Tests Unitaires / Unit Tests

## Egzekite tout test yo / Run all tests

```bash
cd projet_kreyol_IA
pytest tests/ -v
```

## Egzekite test ak coverage / Run tests with coverage

```bash
pytest tests/ -v --cov=src --cov=. --cov-report=html
```

Rezilta ap nan `htmlcov/index.html`

## Egzekite yon test espesifik / Run specific test

```bash
# Test validasyon / Validation tests
pytest tests/test_validation.py -v

# Test chunking
pytest tests/test_chunking.py -v

# Test configuration
pytest tests/test_config.py -v

# Test modules
pytest tests/test_modules.py -v
```

## Estrikti Test / Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest configuration
├── test_validation.py       # Tests pou validation (Phase 1)
├── test_chunking.py         # Tests pou chunking (Phase 1)
├── test_config.py           # Tests pou configuration (Phase 2)
├── test_modules.py          # Tests pou modules (Phase 2)
└── README.md               # Sa a / This file
```

## Sa ki teste / What is tested

### ✅ Phase 1 Tests
- `test_validation.py` - Validation functions
- `test_chunking.py` - Smart chunking

### ✅ Phase 2 Tests
- `test_config.py` - Configuration system
- `test_modules.py` - Utils & Cache

## Tests Pa Modil / Tests by Module

### **src/config.py** (test_config.py)
- Config defaults
- Config from environment
- Config paths
- Config to dict

### **src/utils.py** (test_modules.py)
- Smart chunking
- File size formatting
- Text truncation

### **src/translator.py** (test_modules.py)
- Translation cache init
- Cache set and get
- Cache miss handling
- Cache statistics
- Cache clearing

## Rezilta Atandi / Expected Results

```
tests/test_validation.py ......                   [25%]
tests/test_chunking.py ........                   [50%]
tests/test_config.py .....                        [70%]
tests/test_modules.py ..........                  [100%]

============= 29 passed in 3.45s =============
```

## Ajoute nouvo test / Add new tests

1. Kreye nouvo fichye nan `tests/test_*.py`
2. Enpòte modil yo:
   ```python
   from src.config import Config
   from src.pdf_extractor import PDFExtractor
   ```
3. Ekri test yo:
   ```python
   def test_your_feature():
       assert your_function() == expected_result
   ```
4. Egzekite:
   ```bash
   pytest tests/test_your_file.py -v
   ```

## Depandans / Dependencies

```bash
pip install pytest pytest-cov
```

Deja nan `requirements.txt` ✅

## Coverage Target

- **Phase 1:** ~75% coverage
- **Phase 2:** ~80% coverage (goal)
- **Phase 3:** ~90% coverage (target)

## Notes

- Tests are run in isolation
- Temporary directories used for file operations
- Cache tests use tempdir to avoid conflicts
- All tests should pass before committing

---

**Version:** 3.0 (Phase 2)  
**Tests:** 29 total (8 Phase 1 + 8 Phase 1 + 13 Phase 2)
