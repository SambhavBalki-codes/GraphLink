# GraphLink

GraphLink is a full-stack social-network analysis and friend-recommendation platform. It models friendships as an undirected graph, ranks potential connections using multiple graph signals, and explains why each recommendation was selected.

The project combines a FastAPI and PostgreSQL backend with a React visualization dashboard. It includes shortest-path search, network-degree analysis, an interactive network graph, cache and request observability, reproducible recommendation evaluation, and typed OpenAPI responses.

> Portfolio project demonstrating graph algorithms, API design, performance optimization, observability, and explainable product UI.

## Contents

- [Highlights](#highlights)
- [Architecture](#architecture)
- [Recommendation algorithms](#recommendation-algorithms)
- [Tech stack](#tech-stack)
- [Local setup](#local-setup)
- [API reference](#api-reference)
- [Caching and performance](#caching-and-performance)
- [Observability](#observability)
- [Reproducible evaluation](#reproducible-evaluation)
- [Testing](#testing)
- [Further improvements in progress](#further-improvements-in-progress)

## At a glance

| Area | Implementation |
|---|---|
| Graph model | Undirected adjacency list with BFS traversal |
| Recommendation ranking | Mutual-friend baseline and weighted multi-signal scoring |
| Persistence | PostgreSQL with SQLAlchemy and Alembic |
| API | FastAPI with typed Pydantic response contracts |
| Performance | Cached graph snapshot, TTL/LRU recommendation cache, batched user hydration |
| Frontend | React, Vite, Tailwind CSS, interactive 2D graph |
| Evaluation | Reproducible Precision@K, Recall@K, and NDCG@K |

## Highlights

- Graph-based friend recommendations over the Stanford SNAP Facebook dataset
- V1 baseline ranking by mutual-friend count
- V2 multi-signal ranking using:
  - Mutual-friend ratio
  - Adamic-Adar weighting
  - BFS network distance
- Shortest connection path reconstruction with BFS
- Interactive network graph exploration
- Explainable recommendation cards with score-component breakdowns
- Thread-safe TTL/LRU recommendation cache
- Cached in-memory adjacency graph with invalidation after graph mutations
- Request latency, error, cache, and graph-build metrics
- Reproducible Precision@K, Recall@K, and NDCG@K evaluation
- Pydantic response schemas and generated FastAPI OpenAPI documentation
- PostgreSQL schema constraints and Alembic migrations
- Backend unit and integration test coverage

## Product flow

1. Friendship records are stored in PostgreSQL.
2. The backend builds an in-memory adjacency list from the friendship edges.
3. For a selected user, second-degree candidates are discovered through direct friends.
4. Candidates are scored with either the V1 or V2 algorithm.
5. Results are returned with mutual friends, distance, score, and signal explanations.
6. The React frontend presents the network, recommendations, paths, and operational metrics.

## Architecture

```text
                         +----------------------+
                         |      React + Vite    |
                         |  Landing / Dashboard |
                         | Users / Graph / Path |
                         +----------+-----------+
                                    |
                              Axios / JSON API
                                    |
                         +----------v-----------+
                         |       FastAPI        |
                         | Routes + Pydantic    |
                         | Services + Metrics   |
                         +----+------------+----+
                              |            |
                  +-----------v--+   +-----v-----------+
                  | PostgreSQL   |   | Graph services  |
                  | Users/edges  |   | BFS + ranking   |
                  +--------------+   +-----+-----------+
                                           |
                                  +--------v---------+
                                  | TTL/LRU caches   |
                                  | Graph snapshot   |
                                  | Recommendations  |
                                  +------------------+
```

### Backend layers

- `app/routes/` - HTTP endpoints and response models
- `app/services.py` - application workflows, cache coordination, and database hydration
- `app/graph.py` - adjacency-list construction, BFS, Adamic-Adar, scoring, and recommendations
- `app/crud.py` - SQLAlchemy database operations
- `app/cache.py` - graph snapshot and recommendation caches
- `app/observability.py` - in-memory request and recommendation metrics
- `app/schemas.py` - request and response contracts
- `migrations/` - Alembic database migrations

### Frontend pages

- Landing page - product overview and algorithm explanation
- Dashboard - network totals, cache health, graph build time, and request latency
- Users - paginated user directory with search
- Profile - user details, friends, network degrees, and recommendations
- Path Finder - shortest path between two users
- Network Graph - interactive graph sample with selectable nodes

## Recommendation algorithms

### V1: Mutual Friend Count

The baseline ranks candidates by the number of shared neighbors:

```text
score(u, v) = |N(u) intersection N(v)|
```

It is simple and interpretable, but treats every mutual friend equally.

### V2: Multi-Signal Score

The default algorithm combines three normalized signals:

```text
score =
    0.40 * mutual_ratio
  + 0.40 * normalized_adamic_adar
  + 0.20 * (1 / bfs_distance)
```

The Adamic-Adar signal reduces the influence of high-degree mutual friends. A shared connection with a smaller neighborhood contributes more than a highly connected hub.

Every V2 recommendation includes the raw signals and weighted components used to calculate the final score. The frontend exposes these values through the `Why this match?` control.

## Dataset

GraphLink is designed to work with the [Stanford SNAP Facebook combined dataset](https://snap.stanford.edu/data/egonets-Facebook.html).

The loader expects the edge list at:

```text
data/facebook_combined.txt
```

The loader:

- Clears existing users and friendships
- Creates one application user for each dataset node
- Converts source node identifiers into application database IDs
- Stores each undirected friendship in canonical order
- Reports the number of users and friendships loaded

## Tech stack

### Backend

- Python
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Pydantic Settings
- Alembic
- Pytest
- Uvicorn

### Frontend

- React
- Vite
- React Router
- Axios
- Tailwind CSS
- Lucide React
- `react-force-graph-2d`

## Project structure

```text
GraphLink/
├── app/
│   ├── cache.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── graph.py
│   ├── main.py
│   ├── models.py
│   ├── observability.py
│   ├── schemas.py
│   ├── services.py
│   └── routes/
├── data/
│   └── facebook_combined.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── migrations/
├── scripts/
│   ├── benchmark.py
│   ├── evaluate.py
│   └── load_snap.py
├── tests/
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- PostgreSQL 14 or newer
- npm

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/SambhavBalki-codes/GraphLink.git
cd GraphLink
```

### 2. Create and activate a Python environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL databases

Create one application database and one test database:

```sql
CREATE DATABASE graphlink;
CREATE DATABASE graphlink_test;
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and set valid PostgreSQL connection strings:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/graphlink
TEST_DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/graphlink_test
```

Do not commit `.env`. It is ignored by Git.

### 6. Apply migrations

```bash
alembic upgrade head
```

### 7. Load the SNAP dataset

Place `facebook_combined.txt` in `data/`, then run:

```bash
python scripts/load_snap.py
```

The loader is destructive: it clears the current users and friendships before importing the dataset.

### 8. Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend URLs:

- API root: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 9. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5174`.

The Vite development server proxies `/api` requests to the backend at `http://localhost:8000`.

### Quick start summary

Once PostgreSQL is running and `.env` is configured, the shortest path to a local demo is:

```bash
alembic upgrade head
python scripts/load_snap.py
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

### Docker Compose setup

Docker Desktop provides the fastest reproducible setup:

```powershell
docker compose up --build -d
docker compose exec backend python scripts/load_snap.py
```

Open `http://localhost:5174`. The backend is available at
`http://localhost:8000/docs`.

To stop the stack:

```powershell
docker compose down
```

The PostgreSQL volume is retained between restarts. To remove the database
volume and reload the dataset from scratch:

```powershell
docker compose down -v
```

### Production environment

Set these variables in the backend deployment:

```env
DATABASE_URL=postgresql+psycopg://user:password@host:5432/graphlink
TEST_DATABASE_URL=postgresql+psycopg://user:password@host:5432/graphlink
CORS_ORIGINS=https://your-frontend-domain.example
```

Set this variable when the frontend and backend use different domains:

```env
VITE_API_URL=https://your-backend-domain.example
```

For a single-domain Docker deployment, keep `VITE_API_URL=/api`; Nginx
forwards those requests to the backend service.

## API reference

FastAPI generates the complete interactive API reference at `/docs`. The main endpoints are:

### Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users` | Create a user |
| `GET` | `/users?skip=0&limit=20` | List users |
| `GET` | `/users/{user_id}` | Get a user |
| `PATCH` | `/users/{user_id}` | Update a user |
| `DELETE` | `/users/{user_id}` | Delete a user |
| `GET` | `/users/{user_id}/friends` | List direct friends |
| `GET` | `/users/{user_id}/stats` | Get user statistics |
| `GET` | `/users/{user_id}/network` | Count first-, second-, and third-degree connections |

### Recommendations and paths

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/users/{user_id}/recommendations?limit=10&algorithm=v2` | Get ranked recommendations |
| `GET` | `/users/{user_id}/path/{other_user_id}` | Find a shortest connection path |
| `POST` | `/friendships` | Create a friendship |
| `DELETE` | `/friendships` | Delete a friendship |

Supported recommendation algorithms:

- `v1` - mutual-friend baseline
- `v2` - multi-signal ranking

Example recommendation response:

```json
{
  "user_id": 1,
  "algorithm": "v2",
  "recommendations": [
    {
      "user_id": 42,
      "name": "User_42",
      "mutual_friend_count": 4,
      "mutual_friends": [
        {"user_id": 7, "name": "User_7"}
      ],
      "reason": "You share 4 mutual friends.",
      "score": 0.5186,
      "distance": 2,
      "signals": {
        "mutual_ratio": 0.5,
        "adamic_adar": 1.2042,
        "adamic_adar_normalized": 0.5464,
        "distance_score": 0.5,
        "mutual_component": 0.2,
        "adamic_adar_component": 0.2186,
        "distance_component": 0.1,
        "final_score": 0.5186
      }
    }
  ]
}
```

### Operational endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Database health check |
| `GET` | `/stats` | Total users and friendships |
| `GET` | `/cache/stats` | Cache size, hit rate, TTL, evictions, expirations, and graph build metrics |
| `GET` | `/metrics` | Request and recommendation latency metrics |

## Caching and performance

GraphLink uses two in-process caches:

### Graph snapshot cache

- Stores the adjacency list built from PostgreSQL friendship edges
- Avoids rebuilding the full graph for every request
- Tracks graph build count and build duration
- Invalidates after friendship or user mutations

### Recommendation cache

- Uses `(user_id, limit, algorithm)` as the cache key
- Prevents V1/V2 and different-limit responses from overwriting one another
- Uses LRU eviction with a bounded maximum size
- Uses a five-minute TTL by default
- Tracks hits, misses, evictions, expirations, and invalidations
- Invalidates after topology-changing mutations

The current cache is process-local. For a multi-worker production deployment, replace it with a shared cache such as Redis or configure cache ownership per worker.

## Observability

The backend records:

- Request count and errors by HTTP method and path
- Average endpoint latency
- Recommendation computation latency
- Recommendation cache hits
- Recent average request latency
- Graph snapshot build duration
- Cache hit rate, evictions, expirations, and invalidations

Request logs use the `graphlink.api` logger and include method, path, status code, and duration.

These metrics are intentionally exposed through JSON endpoints for the dashboard. A production deployment can forward the same measurements to Prometheus, OpenTelemetry, or another metrics backend.

## Reproducible evaluation

The evaluation runner compares V1 and V2 using the same fixed user cohort and hidden edges for each run. It reports:

- Precision@K
- Recall@K
- NDCG@K
- Mean and standard deviation across runs
- V2 Precision@K improvement over V1

Run the default evaluation:

```bash
python scripts/evaluate.py
```

Run a configured experiment:

```bash
python scripts/evaluate.py \
  --k 10 \
  --test-users 100 \
  --hide-ratio 0.2 \
  --runs 5 \
  --split-seed 42 \
  --evaluation-seed 1000 \
  --output evaluation.json
```

Use `.csv` to export per-run metric rows:

```bash
python scripts/evaluate.py --output evaluation.csv
```

The experiment hides a deterministic percentage of known edges from each sampled user's test graph, generates recommendations from the remaining graph, and measures how many hidden connections are recovered.

## Benchmarking

The synthetic benchmark measures graph construction and recommendation runtime at increasing network sizes:

```bash
python scripts/benchmark.py
```

It currently exercises networks of 1,000, 5,000, and 10,000 users and reports average graph-build and recommendation times.

## Testing

The backend test suite covers:

- Graph construction
- BFS paths and network degrees
- Adamic-Adar and multi-signal scoring
- Recommendation ranking and filtering
- User and friendship API behavior
- Cache reuse, TTL expiration, LRU eviction, and invalidation
- Metrics collection
- Typed response contracts and OpenAPI schema references
- Evaluation metric correctness and reproducibility

Run all backend tests:

```bash
pytest tests -q
```

Validate Python syntax:

```bash
python -m compileall -q app scripts tests
```

Run frontend checks:

```bash
cd frontend
npm run lint
npm run build
```

The current backend suite contains 41 tests covering graph logic, API behavior, cache behavior, metrics, response contracts, and evaluation reproducibility.

## Data integrity

The friendship model enforces undirected-edge invariants at the database layer:

- `user_id_1 < user_id_2` prevents duplicate directional representations
- Composite primary key prevents duplicate pairs
- Foreign keys ensure both users exist
- Application validation rejects self-friendships
- Email addresses are unique and indexed

## Further improvements in progress

The following improvements are planned as the project continues toward a more production-ready deployment:

- Move process-local caches to Redis for multi-worker deployments
- Add Prometheus/OpenTelemetry exporters
- Add CI for backend tests, frontend build, lint, and coverage
- Add Docker Compose for PostgreSQL, backend, and frontend
- Add a deployed demo and screenshots
- Add persistent evaluation reports and experiment history
- Add database query profiling and further batch-loading optimizations

## License

No license file is currently included. Add an explicit license, such as MIT, before distributing the repository publicly.
