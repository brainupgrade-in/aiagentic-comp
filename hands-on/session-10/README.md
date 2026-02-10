# Session 10: Docker for AI Applications — Hands-on Labs

## Prerequisites

- Session 9 completed (FastAPI + LangGraph agent working)
- Docker installed (optional — labs validate files even without Docker)
- Python 3.10+ installed

```bash
# Check Docker is installed (optional)
docker --version

# No pip packages needed — these labs generate Docker files
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs Docker? |
|-----|-------|-------------------|---------------|
| 01 | Docker Basics | Containers vs VMs concepts, first Dockerfile | No |
| 02 | Writing Dockerfiles | Core instructions, FastAPI Dockerfile | No |
| 03 | Layer Caching | Bad vs good layer ordering, cache optimization | No |
| 04 | Multi-Stage Builds | Builder + runtime stages, image size reduction | No |
| 05 | .dockerignore | Build context optimization, file exclusion | No |
| 06 | Security Hardening | Non-root user, health checks, ENV management | No |
| 07 | Docker Compose | Multi-service AI stack, networking, volumes | No |
| 08 | **Challenge** | Complete production Docker setup for UniGPS | Optional |

## How to Run

```bash
cd hands-on/session-10

# Run a lab (generates files in /tmp/docker-lab-XX/)
python lab01_docker_basics.py

# Check the solution
python solutions/lab01_docker_basics.py

# If Docker is available, lab 08 can actually build:
python lab08_challenge.py
# Then: cd /tmp/docker-lab-08 && docker build -t unigps-agent:1.0 .
```

## Tips

- All 8 labs work WITHOUT Docker installed — they generate and validate files
- If Docker is available, you can build and test the generated Dockerfiles
- Look for `# TODO` markers — that's where you write Dockerfile content
- Each lab has 2 TODOs with instructions
- Generated files appear in `/tmp/docker-lab-XX/` directories
- Compare your work with `solutions/` when done

## What Gets Generated

Each lab creates real Docker files you can inspect:
- `Dockerfile` — the container build instructions
- `.dockerignore` — build context exclusions
- `docker-compose.yml` — multi-service configuration
- `requirements.txt` — Python dependencies
- `main.py` — sample FastAPI application

## Estimated Time

~60-75 minutes for all labs (including the challenge)
