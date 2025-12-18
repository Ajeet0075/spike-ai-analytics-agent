from fastapi import FastAPI
from pydantic import BaseModel
from app.orchestrator import handle_query

app = FastAPI()


class QueryRequest(BaseModel):
    query: str
    propertyId: str | None = None


@app.post("/query")
async def query_endpoint(req: QueryRequest):
    return handle_query(req)
