# MoneyMap Backend

A minimal Flask API for tracking expenses. This is the backend half of the
MoneyMap project — the frontend (HTML/CSS/JS) lives in a separate
repository and is deployed on GitHub Pages, while this backend is deployed
on [Render](https://render.com).

- **Live backend URL:** https://moneymap-backend-es0y.onrender.com
- **Live frontend:** https://david555787.github.io/jessielu.github.io/projects/moneymap/
- **Frontend repo:** https://github.com/david555787/jessielu.github.io

## What this backend does

Data is stored in memory (a Python list) — there is no database, so all
data resets whenever the server restarts. This is intentional for a simple
class assignment.

### Endpoints

| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| `POST` | `/add_expense` | JSON: `{ "amount": number, "category": string, "note": string (optional), "date": "YYYY-MM-DD" }` | The newly created expense, including its assigned `id`. `201` on success, `400` if `amount`, `category`, or `date` is missing/invalid. |
| `GET` | `/expenses` | none | A JSON array of all expenses, most recent first. |
| `DELETE` | `/expense/<id>` | `id` in the URL | A confirmation message. `404` if no expense with that id exists. |
| `GET` | `/summary` | none | A JSON object mapping each category to its total spending, e.g. `{ "Food": 45.5, "Transport": 12.0 }`. |

Example request/response for adding an expense:

```
POST /add_expense
Content-Type: application/json

{ "amount": 12.5, "category": "Food", "note": "Lunch", "date": "2026-09-20" }
```

```json
{
  "id": 1,
  "amount": 12.5,
  "category": "Food",
  "note": "Lunch",
  "date": "2026-09-20"
}
```

## How the frontend communicates with the backend

The frontend is a static page (`index.html` + `script.js`) hosted on GitHub
Pages, at a different domain than this backend. It uses the browser's
`fetch()` API to call the four endpoints above:

- On page load, it calls `GET /expenses` and `GET /summary` to populate the
  expense list and the category summary.
- Submitting the form calls `POST /add_expense`, then re-fetches
  `/expenses` and `/summary` to refresh the page.
- Clicking a delete button calls `DELETE /expense/<id>`, then refreshes the
  same way.

Because the frontend and backend are on different origins
(`github.io` vs. `onrender.com`), the backend uses
[flask-cors](https://flask-cors.readthedocs.io/) to allow cross-origin
requests. Without this, the browser would block the frontend's requests.

## Running it locally

1. Clone this repo and `cd` into it.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the server:
   ```
   python app.py
   ```
4. It will start on `http://127.0.0.1:5000`. You can test it with curl:
   ```
   curl http://127.0.0.1:5000/expenses
   ```
   or by pointing a local copy of the frontend at
   `http://127.0.0.1:5000` instead of the deployed Render URL.

Locally, the app falls back to port `5000` if no `PORT` environment
variable is set. On Render, the platform sets `PORT` automatically.

## How secrets are handled

This project does not currently use any API keys or secrets — it's a
simple in-memory data store with no external services. If secrets were
needed in the future (e.g. a database URL or a third-party API key), they
would be stored as environment variables in Render's dashboard, or in a
local `.env` file excluded via `.gitignore`, and never committed to this
repository.

## Tech stack

- Python 3
- Flask
- flask-cors
- Deployed on Render (free tier — the instance spins down when idle, so
  the first request after inactivity may take up to ~50 seconds)

See `prompt_log.md` for the AI tools and prompts used while building this.
