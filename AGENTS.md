# AGENTS.md

Read this file at the start of every session.
**NO OVERNGINEERING**
## Project

RAG over the Egyptian Civil Code (bilingual Arabic/English PDF). The service answers questions with article citations. The project is a course final project, graded by the rubric in `README.md`.

## Spec (read before working)
**NO OVERNGINEERING**
`spec/` is local only and is listed in `.gitignore`.

- `spec/mission.md`: the problem, principles, and scope (core vs stretch vs out of scope).
- `spec/tech-stack.md`: tools, reasons for each choice, and known PDF extraction issues.
- `spec/roadmap.md`: ordered small phases. Each phase has an owner tag and a "Done when" check.

At the start of a session:

1. Open `spec/roadmap.md`.
2. Find the first phase that is not done.
3. Check its owner tag.

When a phase passes its "Done when" check, mark it `[x]`.

## Collaboration mode (important)
**NO OVERNGINEERING**
The user wants to **learn** and also **finish in 2 days** (deadline about 2026-10-10).

- **You** phases: the user writes the code. Do not write the solution. Explain the concept, give hints and small examples, ask guiding questions, and review the user's code. Give more direct help if the user is stuck for a long time or asks for it.
- **Claude** phases: write the code simple and clear and **NO OVERNGINEERING**. Briefly explain the key decisions so the user can defend them in review.
- **Pair** phases: write the skeleton, interfaces, and boilerplate. Leave the core logic as clear `TODO`s for the user, then review that logic.
- If time runs short, tell the user, and propose to switch a phase to **Claude**. Do not switch silently.

## Key decisions
**NO OVERNGINEERING**
- LLM: two providers behind one OpenAI-compatible client, chosen per request.
  - `api`: OpenRouter (`https://openrouter.ai/api/v1`). The key comes from the `X-LLM-API-Key` header or from `.env`. Never log the key.
  - `local`: vLLM with `Qwen/Qwen2.5-1.5B-Instruct-AWQ` on the user's RTX 3050 (4 GB). It runs in compose profile `gpu`.
- Front end: plain HTML + JS, served by FastAPI at `/`, with a provider toggle.
- RAGAS always uses the `api` provider as the judge.
- BentoML: a batchable `Embedder` service for bge-m3, plus the FastAPI app mounted with `@bentoml.asgi_app`. `RAGPipeline` takes the embedder as a parameter.
- Image registry: Docker Hub. Experiment tracking: an MLflow server in Compose.
- Embeddings: `BAAI/bge-m3`. The comparison model is `intfloat/multilingual-e5-base`.
- Vector store: Qdrant in local mode. The index folder goes inside the Docker image.
- Chunk by article. Sources are article citations, never chunk IDs.
- Flag repealed articles. Do not delete them.

## Course source of truth
**NO OVERNGINEERING**
`The-MLOps-Practitioner-Handbook-3-tracks.pdf` is the course handbook. Project 2 is on pages 64–69 and 76, and the 10-point rubric is on page 67. If the spec and the handbook disagree, the handbook wins.

- MLflow is required (rubric 04). Langfuse does not replace MLflow. Langfuse is a separate requirement for request tracing.
- BentoML + Locust is the core of rubric 07. Local vLLM is also core.
- We do not run AWQ quantization ourselves, and re-ranker distillation is out of scope. The README must say so (honesty clause).

## Process rules (from the handbook)
**NO OVERNGINEERING**
- Do not commit to `main` directly. Work on a branch, open a PR, and merge after CI is green.
- Do not add a Makefile. Put the real commands in the README.
- Never commit `.env`, keys, raw `data/` files (DVC tracks them), or `.venv`.
- Put screenshots and measured numbers in `reports/`.
- Honesty clause: report negative results. Never invent numbers.
- Keep a session changelog in the README.

## Conventions
**NO OVERNGINEERING**
- Package code: `src/legal_rag/`. Tests: `tests/`. Reports: `reports/`. Docker: `docker/`. DVC: `pipelines/`. BentoML: `serving/`. Locust: `loadtest/`. Grafana/Langfuse: `monitoring/`.
- Use `uv` for dependencies, `ruff` + pre-commit for lint, and `pytest` with a 70% coverage gate for tests.
- Use `pydantic-settings` for config and JSON logs with a `correlation_id`. Do not use `print()` in `src/`.
- Load models in the FastAPI `lifespan`, never per request.
- Write prose in Simplified Technical English (short sentences, active voice).
