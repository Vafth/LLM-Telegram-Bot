from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers.gateway import router


app = FastAPI(
    title   = "Gateway",
    version = "0.1.0",
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code = 500,
        content     = {"detail": "Internal server error"},
    )

app.include_router(router)

# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "gateway"}