# FastAPI Module with Router

This module provides a convenient way to add routes to your FastAPI project.

## Installation

You can add router by importing it from `llm` module:

```python
from llm.router import router as llm_router

app.include_router(
    llm_router,
    prefix="/llm",
    tags=["LLM services"],
)
```
