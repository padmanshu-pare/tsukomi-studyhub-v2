# TSUKOMI StudyHub — V1

A Flask + MongoDB educational website for TSUKOMI PADHAYEGA.

## Current features

- Public StudyHub homepage
- Dynamic video pages: `/watch/<slug>`
- Admin login
- Admin video publishing
- Full YouTube URL input (no manual video-ID extraction)
- Automatic YouTube ID extraction
- YouTube IFrame API player
- Autoplay disabled
- Real elapsed playback-time counter
- Pause stops the counter
- Forward seeking does not add the skipped time
- Fixed 2-minute watch requirement
- Notes unlock after required watch time
- Server-side session/heartbeat layer for the unlock flow

## Important limitation

The browser and YouTube player are still involved in playback, so client-side tracking cannot be an unbreakable DRM system. The backend layer reduces simple client-side bypasses, but a determined user can still manipulate a browser. For production, consider protected file delivery or signed/expiring resource URLs.

## Local setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB Atlas

Create a MongoDB Atlas cluster and copy its connection string.

Create `.env` from `.env.example`:

```bash
copy .env.example .env
```

Then fill in:

- MONGO_URI
- DB_NAME
- SECRET_KEY
- ADMIN_USERNAME
- ADMIN_PASSWORD_HASH (recommended; do not store the raw password)

Generate the password hash with:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('choose-a-long-unique-password'))"
```

Paste the output into `ADMIN_PASSWORD_HASH`. The app temporarily supports the
older `ADMIN_PASSWORD` setting for migration, but it should be removed once the
hash is configured. In production also set `SESSION_COOKIE_SECURE=1` after
HTTPS is enabled.

### 4. Start the app

```bash
python app.py
```

Open:

http://127.0.0.1:5000

Admin:

http://127.0.0.1:5000/admin

## Adding a video

Inside Admin:

1. Enter title.
2. Paste the complete YouTube URL.
3. Paste the notes/PDF URL.
4. Add subject/unit.
5. Publish.

The site creates a dynamic URL such as:

`/watch/coa-unit-3-cache-memory`

No new HTML file is required.

## Next development phases

- Google Analytics + UTM
- Search/filtering
- Better admin UI
- Video analytics dashboard
- Note categories
- Protected/signed PDF delivery
- Deployment
- Custom domain
