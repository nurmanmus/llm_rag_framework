from core.default_app import app
from llm.router import router as llm_router

app.include_router(
    llm_router,
    prefix="/llm",
    tags=["LLM services"],
)
