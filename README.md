# SwapSphere – Smart Bartering Marketplace

> **Semester Project – CS3200 Spring 2025**  
> Team **SKAAM**
> **Made by: Suleman Sheikh, Kenny Chen, Ayaan Noorulamin Patel, Aidan Allajbej, Mitchell McNew**
> **The secret key: someCrazyS3cR3T!Key.!**
> **Link to video: https://drive.google.com/file/d/1K6GC1016xu5L2X2qYwsYHic7eEu3COb2/view?usp=sharing**
---

## Table of Contents
1. [Project Vision](#project-vision)
2. [Key Features](#key-features)
3. [User Personas & UX Flows](#user-personas--ux-flows)
4. [System Architecture](#system-architecture)
5. [Tech Stack](#tech-stack)
6. [Local Development Setup](#local-development-setup)
7. [Running with Docker Compose](#running-with-docker-compose)
8. [Database Schema & ER Diagram](#database-schema--er-diagram)
9. [REST API Quick Reference](#rest-api-quick-reference)
10. [Streamlit UI Pages](#streamlit-ui-pages)
11. [Testing & Linting](#testing--linting)
12. [Contributing](#contributing)
13. [License](#license)

---

## Project Vision
**SwapSphere** re‑imagines Facebook Marketplace as a *barter‑first* platform where buyers and sellers trade items (and optional cash top‑ups) through AI‑assisted matching, real‑time price data, and built‑in fraud protection.

*Pain points addressed*
* ✔️ Uncertain pricing – we scrape market prices & compute fairness scores.
* ✔️ Unsafe meet‑ups – escrow & user‑level trust scores reduce risk.
* ✔️ Tedious haggling – structured negotiations + cash adjustment logic.

> “Your stuff *is* your money.”

---

## Key Features
| Area | Highlight |
|------|-----------|
| **AI Trade Matching** | Recommends swaps that balance total value; exposed via `/trades/suggestions`. |
| **Real‑Time Valuations** | `/market_valuations` aggregates e‑commerce price feeds. |
| **Negotiation Console** | Streamlit chat UI (\*pages/04_Buyer_Negotiation.py\*) with live counter‑offers. |
| **Fraud Monitoring** | Admin dashboard flagging suspicious trades, user trust scores. |
| **Analytics** | Data‑analyst pages chart trade frequency, top categories, heat‑maps. |
| **Bulk Seller Tools** | Upload CSV of items, manage inventory, view KPI dashboards. |

---

## User Personas & UX Flows
* **Jake – Buyer** – seeks fair sneaker trades.
* **Emma – Seller** – power user managing dozens of listings.
* **Lisa – System Admin** – monitors fraud & platform health.
* **Raj – Data Analyst** – mines trends to tune AI models.

Wireframes and numbered user stories live in **docs/Phase‑2‑Submission.pdf**.

---

## System Architecture
```
┌───────────────┐        REST/JSON        ┌───────────────┐
│  Streamlit UI │  ◀──────────────────▶  │  Flask API    │
│  (frontend)   │                         │  (backend)    │
└───────────────┘                         └───────┬───────┘
                                                │SQLAlchemy
                                        ┌────────▼────────┐
                                        │   MySQL 8.0     │
                                        └─────────────────┘
```
* **Docker Compose** orchestrates the three services.
* **ML micro‑service hooks** (`backend/ml_models/`) can be scaled separately.

---

## Tech Stack
| Layer | Technology |
|-------|------------|
| Front‑end | **Streamlit 1.33**, Plotly Express |
| Back‑end | **Flask 2.3** with Blueprints (buyer, seller, admin) |
| ORM / DB | **MySQL 8.0**, SQLAlchemy (light use) |
| Auth & Security | Flask‑Login, JWT (road‑map), HTTPS via reverse proxy |
| Data Science | scikit‑learn (pricing model v1), pandas |
| DevOps | Docker 24, Docker Compose v2, GitHub Actions (unit tests & lints) |

---

## Local Development Setup
1. **Clone repo**
   ```bash
   git clone https://github.com/your‑org/swapsphere.git
   cd swapsphere
   ```
2. **Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **MySQL** – either start the provided Docker DB or set `MYSQL_*` env vars to an existing instance.
4. **Environment variables** – copy `.env.example` → `.env` and fill in secrets.
5. **Run services**
   ```bash
   # terminal 1 – backend API
   cd backend
   flask --app rest_entry run -h 0.0.0.0 -p 4000

   # terminal 2 – Streamlit
   cd frontend
   streamlit run Home.py --server.port 8501
   ```

---

## Running with Docker Compose
Simplest path – build everything in one shot:
```bash
docker compose up --build
```
* Streamlit ➜ http://localhost:8501  
* Flask API ➜ http://localhost:4000  
* MySQL ➜ localhost:3306 (user/pass in `.env`)

Stop & remove containers:
```bash
docker compose down -v
```

---

## Database Schema & ER Diagram
Diagrams are in `/docs/diagrams/`:
* **global_er.svg** – high‑level entities & relationships.
* **relational_schema.png** – physical design generated from DataGrip.

> Key tables: **Users**, **Items**, **Trades**, **Trade_Items**, **Fraud_Reports**, **Messages**, **Logs**.

SQL DDL is auto‑generated into `database/schema.sql` and executed on container start.

---

## REST API Quick Reference
| Resource | GET | POST | PUT | DELETE |
|----------|-----|------|-----|--------|
| **/users** | profile, list | register | edit profile, trust score (admin) | ban / deactivate |
| **/items** | browse, seller inventory | upload item(s) | update item | delete item |
| **/trades** | view history, one trade | create offer | update status / counteroffer | cancel trade |
| **/trades/suggestions** | *AI matching* | — | — | — |
| **/reviews** | read reviews | leave review | edit | delete |
| **/messages** | chat history | send message | — | — |
| **/fraud_reports** | view flags | report fraud | update status (admin) | delete false flag |
| **/analytics/** | trends, categories, heat‑map, export | — | — | — |

> See `backend/*_routes.py` for implementation details.

---

## Streamlit UI Pages
```
frontend/
├── 00_Buyer_Home.py          # hero dashboard for buyers
├── 01_Trade_Matching.py      # AI swap recommender
├── 02_Market_Valuations.py   # price feed table
├── 03_Negotiate_Deal.py      # quick cash‑top‑up proposals
├── 04_Buyer_Negotiation.py   # real‑time chat
├── …
└── 15_Manage_Listings.py     # seller inventory CRUD
```
All pages share a dynamic sidebar (`modules/nav.py`) that adapts links based on `st.session_state['role']`.

---

## Testing & Linting
* **Backend** – pytest + coverage, run `pytest -q`.
* **Frontend** – Streamlit pages use lightweight mocks; key logic functions are unit tested.
* **Style** – black, isort, flake8 (`make lint`).
* **CI** – GitHub Actions executes tests on every push & PR.

---

## Contributing
1. Fork & create a feature branch (`feat/<topic>`).
2. Write tests & docs.
3. Open a PR – one of the maintainers will review.

### Commit Guidelines
* Conventional Commits (`feat:`, `fix:`, `docs:` …).
* Reference related Persona Story in the body (e.g. `[#Jake‑2]`).

---

## License
SwapSphere is released under the **MIT License** – see `LICENSE` for full text.
