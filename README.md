# TSUKOMI StudyHub

TSUKOMI StudyHub is an exam-focused learning platform for **TSUKOMI PADHAYEGA**. It helps RGPV B.Tech students discover lectures, watch embedded YouTube classes, and access lecture notes after completing the required watch time.

Built with Flask and MongoDB, the project includes a public student-facing StudyHub and a protected admin workspace for managing video content.

## Features

- Public lecture library with YouTube thumbnails
- Search by lecture title, subject, or unit
- Filters for year, semester, subject, and unit
- Pagination for growing content libraries
- Year → semester → subject course selector
- Dynamic lecture pages at `/watch/<slug>`
- Related-lecture recommendations
- Embedded YouTube player with watch-progress tracking
- Notes unlocked after the configured watch duration
- Direct Google Drive notes links after unlock
- Admin dashboard for adding, editing, publishing, unpublishing, and deleting videos
- Content and watch analytics dashboard
- MongoDB-backed videos and analytics events
- Admin login protections: password hashing support, CSRF protection, rate limiting, session expiry, and safe redirects
- Search-engine support through `robots.txt` and `sitemap.xml`

## Technology

- Python / Flask
- MongoDB Atlas / PyMongo
- Jinja templates, HTML, CSS, and JavaScript
- YouTube IFrame API

## Run locally

1. Create and activate a virtual environment.

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root. Never commit it.

   ```env
   MONGO_URI=your-mongodb-atlas-connection-string
   DB_NAME=tsukomi_studyhub
   SECRET_KEY=generate-a-long-random-secret
   ADMIN_USERNAME=your-admin-username
   ADMIN_PASSWORD_HASH=your-password-hash
   REQUIRED_WATCH_SECONDS=40
   PORT=5000
   FLASK_DEBUG=1
   ```

4. Generate a secure admin password hash.

   ```bash
   python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('choose-a-long-unique-password'))"
   ```

5. Start the app.

   ```bash
   python app.py
   ```

Open `http://127.0.0.1:5000` for the public site and `http://127.0.0.1:5000/admin/login` for administration.

## Content workflow

1. Sign in to the admin dashboard.
2. Add a title, YouTube URL, notes/Google Drive URL, year, semester, subject, and unit.
3. Save as a draft or publish it immediately.
4. Published lectures appear in the public StudyHub automatically.

## Security notes

- `.env` is ignored by Git and must never be uploaded.
- Use `ADMIN_PASSWORD_HASH` instead of a plaintext password.
- Use HTTPS in production and set `SESSION_COOKIE_SECURE=1`.
- For stronger production administration controls, restrict `/admin` with an IP allowlist, VPN, or Cloudflare Access.
- Google Drive links are direct links after notes unlock; use signed/protected delivery if stronger note protection is needed.

## License

Private project for TSUKOMI PADHAYEGA.
