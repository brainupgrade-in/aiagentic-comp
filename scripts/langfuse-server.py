#!/usr/bin/env python3
"""
Lightweight LangFuse-compatible server for Session 12 Lab 09
Uses SQLite for storage and FastAPI for HTTP API
Implements the LangFuse API endpoints needed for the course labs
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


# Database setup
DB_PATH = "/tmp/langfuse.db"


def init_db():
    """Initialize SQLite database with LangFuse schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Traces table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traces (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            user_id TEXT,
            session_id TEXT,
            metadata TEXT,
            tags TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Generations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id TEXT PRIMARY KEY,
            trace_id TEXT NOT NULL,
            name TEXT NOT NULL,
            model TEXT,
            input TEXT,
            output TEXT,
            usage TEXT,
            metadata TEXT,
            cost REAL DEFAULT 0.0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (trace_id) REFERENCES traces (id)
        )
    """)

    # Scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id TEXT PRIMARY KEY,
            trace_id TEXT NOT NULL,
            name TEXT NOT NULL,
            value REAL NOT NULL,
            data_type TEXT DEFAULT 'NUMERIC',
            comment TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (trace_id) REFERENCES traces (id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"✓ Database initialized at {DB_PATH}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield
    # Cleanup on shutdown
    print("✓ LangFuse server shutting down")


# FastAPI app
app = FastAPI(
    title="LangFuse-Compatible Server",
    description="Lightweight LangFuse API for Agentic AI Course",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class TraceCreate(BaseModel):
    id: Optional[str] = None
    name: str
    userId: Optional[str] = None
    sessionId: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class GenerationCreate(BaseModel):
    id: Optional[str] = None
    traceId: str
    name: str
    model: Optional[str] = None
    input: Optional[Any] = None
    output: Optional[Any] = None
    usage: Optional[Dict[str, int]] = None
    metadata: Optional[Dict[str, Any]] = None


class ScoreCreate(BaseModel):
    id: Optional[str] = None
    traceId: str
    name: str
    value: float
    dataType: str = "NUMERIC"
    comment: Optional[str] = None


# Helper functions
def get_db():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)


def verify_auth(authorization: Optional[str] = Header(None)):
    """Verify API key (simplified for course)."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    # Accept any valid-looking key for course purposes
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    return authorization.replace("Bearer ", "")


# API endpoints
@app.get("/api/public/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "database": os.path.exists(DB_PATH),
    }


@app.post("/api/public/traces")
async def create_trace(trace: TraceCreate, api_key: str = Header(None, alias="Authorization")):
    """Create a new trace."""
    verify_auth(api_key)

    trace_id = trace.id or f"trace-{datetime.now().timestamp()}"
    created_at = datetime.now().isoformat()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO traces (id, name, user_id, session_id, metadata, tags, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        trace_id,
        trace.name,
        trace.userId,
        trace.sessionId,
        json.dumps(trace.metadata) if trace.metadata else None,
        json.dumps(trace.tags) if trace.tags else None,
        created_at,
    ))

    conn.commit()
    conn.close()

    return {
        "id": trace_id,
        "name": trace.name,
        "timestamp": created_at,
    }


@app.post("/api/public/generations")
async def create_generation(gen: GenerationCreate, api_key: str = Header(None, alias="Authorization")):
    """Create a new generation."""
    verify_auth(api_key)

    gen_id = gen.id or f"gen-{datetime.now().timestamp()}"
    created_at = datetime.now().isoformat()

    # Calculate cost
    cost = 0.0
    if gen.usage and gen.model:
        PRICING = {
            "llama-3.3-70b-versatile": (0.00000059, 0.00000079),
            "llama-3.2-1b": (0.00000004, 0.00000004),
            "mixtral-8x7b-32768": (0.00000027, 0.00000027),
        }
        input_price, output_price = PRICING.get(gen.model, (0, 0))
        input_tokens = gen.usage.get("input_tokens", 0)
        output_tokens = gen.usage.get("output_tokens", 0)
        cost = (input_tokens * input_price) + (output_tokens * output_price)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO generations (id, trace_id, name, model, input, output, usage, metadata, cost, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        gen_id,
        gen.traceId,
        gen.name,
        gen.model,
        json.dumps(gen.input) if gen.input else None,
        json.dumps(gen.output) if gen.output else None,
        json.dumps(gen.usage) if gen.usage else None,
        json.dumps(gen.metadata) if gen.metadata else None,
        cost,
        created_at,
    ))

    conn.commit()
    conn.close()

    return {
        "id": gen_id,
        "traceId": gen.traceId,
        "cost": cost,
        "timestamp": created_at,
    }


@app.post("/api/public/scores")
async def create_score(score: ScoreCreate, api_key: str = Header(None, alias="Authorization")):
    """Create a new score."""
    verify_auth(api_key)

    score_id = score.id or f"score-{datetime.now().timestamp()}"
    created_at = datetime.now().isoformat()

    conn = get_db()
    cursor = conn.cursor()

    # Verify trace exists
    cursor.execute("SELECT id FROM traces WHERE id = ?", (score.traceId,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail=f"Trace {score.traceId} not found")

    cursor.execute("""
        INSERT INTO scores (id, trace_id, name, value, data_type, comment, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        score_id,
        score.traceId,
        score.name,
        score.value,
        score.dataType,
        score.comment,
        created_at,
    ))

    conn.commit()
    conn.close()

    return {
        "id": score_id,
        "traceId": score.traceId,
        "name": score.name,
        "value": score.value,
    }


@app.get("/api/public/traces")
async def get_traces(
    userId: Optional[str] = None,
    sessionId: Optional[str] = None,
    api_key: str = Header(None, alias="Authorization"),
):
    """Get traces with optional filtering."""
    verify_auth(api_key)

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM traces WHERE 1=1"
    params = []

    if userId:
        query += " AND user_id = ?"
        params.append(userId)

    if sessionId:
        query += " AND session_id = ?"
        params.append(sessionId)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    traces = []
    for row in rows:
        trace_id = row[0]

        # Get generations
        cursor.execute("SELECT * FROM generations WHERE trace_id = ?", (trace_id,))
        gens = cursor.fetchall()

        # Get scores
        cursor.execute("SELECT * FROM scores WHERE trace_id = ?", (trace_id,))
        scores = cursor.fetchall()

        # Calculate total cost
        total_cost = sum(g[8] for g in gens)  # cost column

        traces.append({
            "id": row[0],
            "name": row[1],
            "userId": row[2],
            "sessionId": row[3],
            "metadata": json.loads(row[4]) if row[4] else {},
            "tags": json.loads(row[5]) if row[5] else [],
            "createdAt": row[6],
            "generations": len(gens),
            "scores": len(scores),
            "cost": total_cost,
        })

    conn.close()

    return {
        "data": traces,
        "meta": {
            "totalItems": len(traces),
        },
    }


@app.get("/api/public/traces/{trace_id}")
async def get_trace(trace_id: str, api_key: str = Header(None, alias="Authorization")):
    """Get a specific trace with all details."""
    verify_auth(api_key)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM traces WHERE id = ?", (trace_id,))
    trace_row = cursor.fetchone()

    if not trace_row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Trace {trace_id} not found")

    # Get generations
    cursor.execute("SELECT * FROM generations WHERE trace_id = ?", (trace_id,))
    gen_rows = cursor.fetchall()

    # Get scores
    cursor.execute("SELECT * FROM scores WHERE trace_id = ?", (trace_id,))
    score_rows = cursor.fetchall()

    conn.close()

    generations = []
    total_cost = 0.0
    for row in gen_rows:
        generations.append({
            "id": row[0],
            "name": row[2],
            "model": row[3],
            "input": json.loads(row[4]) if row[4] else None,
            "output": json.loads(row[5]) if row[5] else None,
            "usage": json.loads(row[6]) if row[6] else {},
            "metadata": json.loads(row[7]) if row[7] else {},
            "cost": row[8],
            "createdAt": row[9],
        })
        total_cost += row[8]

    scores = []
    for row in score_rows:
        scores.append({
            "id": row[0],
            "name": row[2],
            "value": row[3],
            "dataType": row[4],
            "comment": row[5],
            "createdAt": row[6],
        })

    return {
        "id": trace_row[0],
        "name": trace_row[1],
        "userId": trace_row[2],
        "sessionId": trace_row[3],
        "metadata": json.loads(trace_row[4]) if trace_row[4] else {},
        "tags": json.loads(trace_row[5]) if trace_row[5] else [],
        "createdAt": trace_row[6],
        "generations": generations,
        "scores": scores,
        "cost": total_cost,
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "LangFuse-Compatible Server",
        "version": "1.0.0",
        "description": "Lightweight LangFuse API for Agentic AI Course",
        "endpoints": {
            "health": "/api/public/health",
            "traces": "/api/public/traces",
            "generations": "/api/public/generations",
            "scores": "/api/public/scores",
        },
        "database": DB_PATH,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("  LangFuse-Compatible Server")
    print("=" * 60)
    print(f"  Database: {DB_PATH}")
    print(f"  API: http://localhost:3000")
    print(f"  Health: http://localhost:3000/api/public/health")
    print("=" * 60)
    print()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,
        log_level="info",
    )
