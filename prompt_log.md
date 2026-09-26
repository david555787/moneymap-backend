# Prompt Log

This document lists the AI tools used while building the MoneyMap backend,
and the key prompts that shaped the implementation.

## AI model(s)/tool(s) used

- Claude (Anthropic), used in a chat interface, for planning the project
  structure, generating the initial Flask backend, and debugging deployment
  issues.

## Key prompts

1. **Initial project scaffold** — asked Claude to generate a full-stack
   expense tracker skeleton with a Flask backend and a vanilla JS/HTML
   frontend, specifying the API endpoints needed (`POST /add_expense`,
   `GET /expenses`, `DELETE /expense/<id>`, `GET /summary`), in-memory
   storage for simplicity, and clean, commented code suitable for a class
   assignment.

2. **Splitting frontend and backend into separate repos** — asked Claude to
   help restructure the original combined project into two independent
   pieces: a backend-only Flask API (this repo) and a static frontend
   (deployed separately on GitHub Pages), since the assignment requires the
   two to live in different repositories.

3. **Removing the frontend route from the backend** — asked Claude to update
   `app.py` so it no longer serves an HTML page directly (removing the `/`
   route and `render_template` call), since the backend is now API-only and
   the frontend is hosted elsewhere.

4. **Adding CORS support** — asked Claude to add `flask-cors` so the backend
   can accept requests from a frontend hosted on a different origin
   (GitHub Pages), and to explain why CORS is needed in this setup.

5. **Preparing for Render deployment** — asked Claude to update the app's
   entry point to read the `PORT` environment variable (as Render requires)
   instead of hardcoding port 5000, and to walk through creating a Render
   Web Service connected to this GitHub repo.

6. **Debugging deployment failures** — when the first two Render deploys
   failed, pasted the deploy logs to Claude, which diagnosed two separate
   issues: (a) the deployed code still contained the old frontend-serving
   route because the local file hadn't been fully replaced, and (b) the
   `flask-cors` package was missing from `requirements.txt` even though it
   was imported in `app.py`. Both were fixed based on Claude's diagnosis.

## What was NOT AI-generated

- The actual testing of each deploy (checking logs, confirming the live
  `/expenses` endpoint returns data) was done manually in the browser and
  terminal, not automated by AI.
