# FastAPI is used for the Python backend

The Python backend is built with FastAPI. The platform is API-first — both the React Native student app and the Teacher/Admin web portal consume the same backend API. FastAPI's async-native design is a natural fit for LLM-heavy workloads: ExplanationSession responses stream token-by-token to the student rather than waiting for a full response, which requires first-class async streaming support. Django makes this complex (requires Django Channels); FastAPI handles it natively. SQLAlchemy is used as the ORM; authentication is handled via fastapi-users.

## Considered Options

- **Django + DRF**: Batteries-included (built-in ORM, admin, auth) but async streaming for LLM calls is complex. Better suited to full-stack content-heavy apps than API-first LLM backends.
- **Flask**: Simple, but limited async support and no natural fit for streaming.
- **FastAPI** ✅: Async-native, API-first, straightforward LLM streaming support. Lightweight enough to not impose structure we don't need.
