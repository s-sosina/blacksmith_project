# Architectural Decisions

## Sprint 1: Stack Selection

**Decision:** Python 3.11+, FastAPI, Pydantic V2, pytest.

**Context:** We are building the backend spine for a mobility intelligence platform. This service will ingest wearable telemetry, validate it, and pass it to analytics to generate clinical insights. 

**Rationale:** 
- Python is the native language of the ML/biomechanics ecosystem.
- FastAPI provides the async throughput needed for high-volume wearable data ingestion.
- Pydantic enforces strict physical and logical boundaries on clinical data at the API edge.

**Rejected Alternatives:**
- Node.js/Express: Lacks native ML/data-science libraries.
- Go: Lacks native ML libraries; too much boilerplate for a rapid MVP spine.
- Django: Too heavy. We don't need an ORM or admin panel for a pure API service.
- Flask: Lacks native async, which we need for scaling wearable ingestion.
- 
- ## ML Service Rationale

**Why Python + FastAPI for ML specifically:**

1. **Model Integration Path:** Our analytics layer will eventually load trained ML models (scikit-learn, PyTorch, or similar). Python is the only language with native support for these frameworks. Using any other language would require complex bridging layers.

2. **Data Science Ecosystem:** Wearable telemetry analysis requires signal processing (SciPy), numerical computation (NumPy), and data manipulation (Pandas). These are all Python-native. Building in another language would mean reimplementing or wrapping these tools.

3. **Schema Validation for Clinical Data:** Pydantic enforces physical boundaries (e.g., stride length must be positive, gait symmetry must be 0-1). This prevents invalid data from reaching the ML models, which is critical for reliable predictions.

4. **Async Throughput for Telemetry:** Wearable devices generate high-volume time-series data. FastAPI's async capabilities allow us to handle concurrent data ingestion efficiently, which is essential when scaling from one patient to hundreds.

5. **Rapid Iteration:** ML workflows require frequent experimentation with features and models. Python's simplicity and FastAPI's minimal boilerplate allow us to iterate quickly without being blocked by language complexity.