
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, start_http_server
import threading

app = FastAPI(title="Sharded Data Service")


# Configuration
N_SHARDS = 3
shards = [{} for _ in range(N_SHARDS)]  # List of dictionaries representing shards


# Prometheus Metrics
REQUEST_COUNTER = Counter("requests_total", "Total requests per shard", ["shard"])
SHARD_SIZE = Gauge("shard_size", "Number of items per shard", ["shard"])

# Start Prometheus metrics server in a background thread
def start_metrics():
    start_http_server(8001)  # Metrics exposed on port 8001

threading.Thread(target=start_metrics, daemon=True).start()


# Pydantic Model (v2 compatible)
class StoreRequest(BaseModel):
    userId: int
    data: str

    model_config = {"extra": "forbid"}  # No extra fields allowed

# API Endpoints
@app.post("/store")
def store_data(req: StoreRequest):
    shard_index = req.userId % N_SHARDS
    shards[shard_index][req.userId] = req.data

    # Update Prometheus metrics
    REQUEST_COUNTER.labels(shard=str(shard_index)).inc()
    SHARD_SIZE.labels(shard=str(shard_index)).set(len(shards[shard_index]))

    return {"message": f"Stored in shard {shard_index}"}

@app.get("/shards")
def get_shards():
    """Return current shard distribution for demo/debug"""
    return {f"shard_{i}": shards[i] for i in range(N_SHARDS)}

# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
