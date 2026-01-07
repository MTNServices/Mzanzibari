# Deploying to Render

This guide walks you through deploying **Mzanzibari POS** to [Render](https://render.com) with GitHub Actions.

## Prerequisites

- GitHub repository pushed to [github.com/MTNServices/Mzanzibari](https://github.com/MTNServices/Mzanzibari)
- Render account (free tier available)

## Deployment Steps

### 1. Create Render Account & Generate API Key

1. Go to [render.com](https://render.com) and sign up (free).
2. Navigate to **Account > API Tokens** and generate a new API key.
3. Copy the token; you'll use it in the next step.

### 2. Add Render API Key to GitHub Secrets

1. In your repository, go to **Settings > Secrets and variables > Actions**.
2. Click **New repository secret**.
3. Name: `RENDER_API_KEY`
4. Value: paste your Render API token.
5. Click **Add secret**.

### 3. Deploy Infrastructure via GitHub Actions

The workflow below will auto-deploy your web service and Postgres database to Render on each push.

**Workflow File:** `.github/workflows/render-deploy.yml`

See the file in the repo — it will:
- Build and test the Django app
- Deploy to Render if tests pass
- Create web + postgres services
- Automatically configure environment variables

Push the repo and watch the deployment in the GitHub Actions tab and at [dashboard.render.com](https://dashboard.render.com).

### 4. Verify Deployment

Once the workflow completes:

1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click on your **mzanzibari-web** service.
3. View logs to confirm Gunicorn started.
4. Copy the live URL (e.g., `https://mzanzibari-web.onrender.com`).
5. Test the API:
   ```bash
   curl https://mzanzibari-web.onrender.com/api/products/
   ```

### 5. Create a Superuser

Run a one-time command to create an admin user:

```bash
# In Render Dashboard, click "mzanzibari-web" > "Shell"
python manage.py createsuperuser
# Follow the prompts
```

Then visit `https://mzanzibari-web.onrender.com/admin/` and log in.

---

## Free Tier Limits

- **Web service:** 0.5 vCPU, 512MB RAM (auto-spins down after 15 min of inactivity).
- **PostgreSQL:** 512MB storage (great for prototypes).
- Free databases are paused; web service wakes them on request.

For production traffic, upgrade to paid plans.

---

## Environment Variables on Render

The `render.yaml` file defines:

| Variable | Source |
|----------|--------|
| `DJANGO_SETTINGS_MODULE` | `config.settings_production` |
| `DATABASE_URL` | Postgres connection string (auto-generated) |
| `SECRET_KEY` | Generate & set manually in dashboard if needed |
| `ALLOWED_HOSTS` | `*.render.com` (auto-includes deployed domain) |
| `DEBUG` | `False` (production mode) |

**To set custom `SECRET_KEY`:**

1. Generate a new key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. In Render Dashboard, go to **mzanzibari-web > Environment**.
3. Add `SECRET_KEY` with the value from above.
4. Re-deploy.

---

## Troubleshooting

### Build fails: `psycopg2-binary` error
- This is expected on Render (PostgreSQL adapter). The build will succeed on re-run.

### Web service won't start
1. Check logs: Render Dashboard > **mzanzibari-web** > **Logs**.
2. Common issues:
   - Database not migrated. Re-run deploy or manually run migrations in shell.
   - Missing environment variable. Double-check `render.yaml`.

### Database connection refused
- On free tier, the Postgres service may be paused. Render auto-resumes; wait a few seconds.

---

## Next Steps

- **Add a Frontend:** Serve a React app from Vercel/Netlify, pointing to your Render API.
- **Custom Domain:** Render Dashboard > **mzanzibari-web** > **Custom Domain**.
- **Monitoring:** Use Render logs or integrate with a logging service (e.g., Sentry).
- **CI/CD:** The workflow already runs tests on push; extend to run E2E tests or lint before deploy.

---

For more info, see [Render Django docs](https://render.com/docs/deploy-django).
