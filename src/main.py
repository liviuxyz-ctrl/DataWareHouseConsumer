from fastapi import FastAPI
from src.api import assets, data_sources, data
from src.config.settings import Config
from src.db.database import DatabaseManager

app = FastAPI()

app.include_router(assets.router, prefix="/api/v1")
app.include_router(data_sources.router, prefix="/api/v1")
app.include_router(data.router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    db_manager = DatabaseManager()
    db_manager.create_keyspace()
    db_manager.create_tables()

@app.on_event("shutdown")
def on_shutdown():
    db_manager = DatabaseManager()
    db_manager.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
