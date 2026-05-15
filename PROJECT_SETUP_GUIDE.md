# NHS Innovation Service - Complete Setup Guide

This guide details how to set up the project from a completely fresh machine, including fixes for known environment and dependency issues.

## Section 1: Prerequisites & System Setup

**1. Operating System & Tools**
*   **Linux (Ubuntu 22.04+ recommended):** The environment verified for this project.
*   **Git:** To manage the repositories.
*   **curl:** For testing and verification.

**2. Language Runtimes**
*   **Python 3.12:** The informational frontend is built on this. Ensure `python3-venv` is installed.
*   **Node.js (v20+):** Required for the Transactional Frontend (Angular) and the Backend API.
*   **NVM (Node Version Manager):** Recommended to manage Node versions easily.

**3. Docker & Infrastructure**
*   **Docker Desktop or Docker Engine:** To run Elasticsearch and Postgres.
*   **Docker Compose (v2.0+):** To orchestrate the services.

**4. System Cleanliness (The "Gotcha" Fix)**
*   **Postgres Conflict:** If your fresh machine has a "native" Postgres service running, it will block Docker from binding to port 5432.
    *   *Command:* `sudo systemctl stop postgresql && sudo systemctl disable postgresql`
*   **Port Check:** Ensure ports **5432** (Database) and **9200** (Elasticsearch) are free.

---

## Section 2: Infrastructure Configuration

**1. Clone the Repositories**
Ensure you pull the correct branches. We use `develop` as the baseline because it contains crucial environment fixes.
```bash
git clone -b develop <informational-frontend-repo-url> innovation-service-informational-frontend
git clone -b develop <backend-api-repo-url> innovation-service-backend-api
git clone -b develop <transactional-frontend-repo-url> innovation-service-transactional-frontend
```

**2. Environment Variables (.env)**
Navigate to `innovation-service-informational-frontend` and create your `.env` file based on `.env.example`.
*   Ensure the DB credentials match what is configured in `docker-compose.yml`.
*   Ensure `DJANGO_SETTINGS_MODULE=is_homepage.settings.dev`.

**3. The "Clean Slate" Docker Start**
*If you ever reinstall or switch Elasticsearch versions, old volumes will cause an `IndexFormatTooNewException`. Wipe them first.*
```bash
cd innovation-service-informational-frontend
docker compose down -v  # Wipes all previous database/search volumes. Do not do this in production!
docker compose up -d
```
*Wait about 30 seconds for Elasticsearch to fully initialize.*

**4. Verification**
*   **Database:** `docker ps` should show `docker-postgres-db-1` as Up.
*   **Search:** `curl -X GET "localhost:9200"` should return a JSON object confirming Elasticsearch 8.x is running.

---

## Section 3: Python Environment & Wagtail Fixes

**1. Create & Activate the Virtual Environment**
```bash
cd innovation-service-informational-frontend
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install Requirements**
```bash
pip install -r requirements.txt
```

**3. The Wagtail 4 Legacy Import Patch (Crucial Fix)**
*The project uses dependencies (like `wagtail_pdf_view`) that still reference the old `wagtail.core` path instead of `wagtail.models`. This causes `ModuleNotFoundError` during startup.*
*   To fix this, run Wagtail’s built-in module path updater against your `.venv` directory:
```bash
wagtail updatemodulepaths .venv/
```
*(This should output that it patched around 18 files.)*

**4. Run Database Migrations**
*We use `run_django.py` as a wrapper to ensure `.env` variables are correctly loaded.*
```bash
python3 run_django.py migrate
```

**5. Create Superuser (Admin Access)**
```bash
python3 run_django.py createsuperuser
# Enter details (e.g., admin / admin@example.com / nsite123)
```

---

## Section 4: Data Initialization & Performance

**1. Initialize the Search Index**
*Wagtail needs to sync its database structure with Elasticsearch before you can start adding content.*
```bash
python3 run_django.py update_index
```

**2. Seed Content (Testing Dataset)**
*Run the provided automation script to create 40+ pages (News, Case Studies, Innovation Guides, and Generic Pages).*
```bash
python3 seed_content.py
```
*Crucial: After seeding content, you **MUST** run the indexer again so they appear in search results:*
```bash
python3 run_django.py update_index
```

**3. Start the Development Server**
```bash
python3 run_django.py runserver 0.0.0.0:8000
```

**4. Verify Caching (The Automated Test)**
*In a separate terminal, run the verification scripts to ensure all pages are hitting the local disk cache.*
*   **For Users (with cookies):** `python3 test_cache_user.py`
*   **For Bots (without cookies):** `python3 test_cache_bot.py`

*   **Target Output:** You want to see `hit` in the `Req 3` column.
*   **Note:** Seeing `skip` or `miss` on the first request is normal (it's either setting a CSRF cookie or populating the cache for the first time).

**5. Accessing the Site**
*   **Website:** `http://localhost:8000`
*   **Wagtail Admin:** `http://localhost:8000/admin` (Use the credentials from Section 3).

