import os
import re
import uuid
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps

from bson import ObjectId
from dotenv import load_dotenv
from flask import (
    Flask, abort, flash, jsonify, redirect, render_template,
    request, session, url_for, Response,
)
from pymongo import MongoClient
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__, static_folder="public/static")
secret_key = os.getenv("SECRET_KEY")
if os.getenv("VERCEL") and not secret_key:
    raise RuntimeError("Set the SECRET_KEY environment variable in your Vercel project.")
app.secret_key = secret_key or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv(
        "SESSION_COOKIE_SECURE",
        "1" if os.getenv("VERCEL") else "0",
    ) == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
)

from migrations import ensure_mongodb_initialized

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "tsukomi_studyhub")
REQUIRED_WATCH_SECONDS = int(os.getenv("REQUIRED_WATCH_SECONDS", "40"))
LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 15 * 60
_login_attempts = {}


def now():
    return datetime.now(timezone.utc)


def _client_ip():
    """Use proxy forwarding only when the deployment proxy has set it."""
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    return forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr


def _login_is_limited(ip_address):
    cutoff = now().timestamp() - LOGIN_WINDOW_SECONDS
    recent = [stamp for stamp in _login_attempts.get(ip_address, []) if stamp > cutoff]
    _login_attempts[ip_address] = recent
    return len(recent) >= LOGIN_MAX_ATTEMPTS


def _record_failed_login(ip_address):
    _login_attempts.setdefault(ip_address, []).append(now().timestamp())


def _is_safe_local_url(target):
    return bool(target) and target.startswith("/") and not target.startswith("//")


@app.context_processor
def inject_csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf_token"] = token
    return {"csrf_token": token}


@app.before_request
def protect_admin_posts():
    """Require a per-session token for every state-changing admin request."""
    if request.path.startswith("/admin/") and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        submitted_token = request.form.get("csrf_token", "")
        expected_token = session.get("csrf_token", "")
        if not expected_token or not hmac.compare_digest(submitted_token, expected_token):
            abort(400, description="Invalid or missing CSRF token.")


client = None
db = None

if MONGO_URI:
    try:
        test_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        test_client.admin.command("ping")
        client = test_client
        db = client[DB_NAME]
        print(f"[Database] Connected successfully to MongoDB ({DB_NAME}).")
        ensure_mongodb_initialized(db)
    except Exception as err:
        print(f"[Database] MongoDB remote connection error ({err}).")
        try:
            import mongomock
            print("[Database] Using local mongomock database instance.")
            client = mongomock.MongoClient()
            db = client[DB_NAME]
            ensure_mongodb_initialized(db)
        except ImportError:
            client = None
            db = None


def require_db():
    if db is None:
        abort(503, description="MongoDB is not configured or reachable. Check MONGO_URI in .env.")


def record_analytics_event(event, video=None, watched_seconds=0):
    """Store one analytics event using the same field names used by the dashboard."""
    if db is None:
        return

    analytics_session_id = session.get("analytics_session_id")
    if not analytics_session_id:
        analytics_session_id = str(uuid.uuid4())
        session["analytics_session_id"] = analytics_session_id
        session.modified = True

    document = {
        "event": event,
        "analytics_session_id": analytics_session_id,
        "created_at": now(),
        "watched_seconds": float(watched_seconds or 0),
    }

    if video:
        document.update({
            "video_id": str(video["_id"]),
            "video_title": video.get("title", ""),
            "subject": video.get("subject", ""),
            "unit": video.get("unit", ""),
            "year": video.get("year", ""),
            "semester": video.get("semester", ""),
            "slug": video.get("slug", ""),
        })

    db.analytics_events.insert_one(document)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper


def slugify(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s-]+", "-", value).strip("-")
    return value


def extract_youtube_id(url):
    """Accept common YouTube URL formats and return the video ID."""
    if not url:
        return None

    patterns = [
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def _semester_label(number):
    if number % 100 in {11, 12, 13}:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix} Semester"


def _semester_filter(value):
    """Match common stored labels for a semester number."""
    match = re.search(r"\d+", value or "")
    if not match:
        return {"semester": value}

    number = int(match.group())
    ordinal = _semester_label(number).split(" ", 1)[0]
    alternatives = (
        rf"^{ordinal}\s+semester$",
        rf"^semester\s+{number}$",
        rf"^{number}$",
    )
    return {
        "semester": {
            "$regex": "(?:" + "|".join(alternatives) + ")",
            "$options": "i",
        }
    }


def _stored_semester_matches(stored_value, semester_label):
    semester_query = _semester_filter(semester_label)["semester"]
    if isinstance(semester_query, dict):
        return re.fullmatch(
            semester_query["$regex"],
            str(stored_value),
            re.IGNORECASE,
        ) is not None
    return stored_value == semester_query


def _video_unit_sort_key(video):
    unit_match = re.search(r"\d+", video.get("unit") or "")
    return (
        0 if unit_match else 1,
        int(unit_match.group()) if unit_match else 0,
    )


CURRICULUM_SUBJECT_ALIASES = {
    "Computer Organization & Architecture (COA)": (
        "Computer Organization & Architecture",
        "Computer Organization & Architecture (COA)",
    ),
}


CURRICULUM = {
    1: [
        ("Group A", [
            ("BT-101 / BT-201", "Engineering Chemistry"),
            ("BT-102 / BT-202", "Mathematics-I"),
            ("BT-103 / BT-203", "English for Communication"),
            ("BT-104 / BT-204", "Basic Electrical & Electronics Engineering"),
            ("BT-105 / BT-205", "Engineering Graphics"),
            ("BT-106 / BT-206", "Manufacturing Practices"),
        ]),
        ("Group B", [
            ("BT-201 / BT-101", "Engineering Physics"),
            ("BT-202 / BT-102", "Mathematics-II"),
            ("BT-203 / BT-103", "Basic Mechanical Engineering"),
            ("BT-204 / BT-104", "Basic Civil Engineering & Mechanics"),
            ("BT-205 / BT-105", "Basic Computer Engineering"),
            ("BT-206 / BT-106", "Language Lab & Seminars"),
        ]),
    ],
    2: [
        ("Group A", [
            ("BT-101 / BT-201", "Engineering Chemistry"),
            ("BT-102 / BT-202", "Mathematics-I"),
            ("BT-103 / BT-203", "English for Communication"),
            ("BT-104 / BT-204", "Basic Electrical & Electronics Engineering"),
            ("BT-105 / BT-205", "Engineering Graphics"),
            ("BT-106 / BT-206", "Manufacturing Practices"),
        ]),
        ("Group B", [
            ("BT-201 / BT-101", "Engineering Physics"),
            ("BT-202 / BT-102", "Mathematics-II"),
            ("BT-203 / BT-103", "Basic Mechanical Engineering"),
            ("BT-204 / BT-104", "Basic Civil Engineering & Mechanics"),
            ("BT-205 / BT-105", "Basic Computer Engineering"),
            ("BT-206 / BT-106", "Language Lab & Seminars"),
        ]),
    ],
    3: [
        ("Core Subjects", [
            ("ES-301", "Energy & Environmental Engineering"),
            ("CS-302", "Discrete Structure (Discrete Mathematics)"),
            ("CS-303", "Data Structure"),
            ("CS-304", "Digital Systems"),
            ("CS-305", "Object Oriented Programming & Methodology"),
        ]),
        ("Practical", [("CS-306", "Computer Workshop")]),
    ],
    4: [
        ("Core Subjects", [
            ("BT-401", "Mathematics-III"),
            ("CS-402", "Analysis & Design of Algorithm (ADA)"),
            ("CS-403", "Software Engineering"),
            ("CS-404", "Computer Organization & Architecture (COA)"),
            ("CS-405", "Operating Systems"),
        ]),
    ],
    5: [
        ("Core Subjects", [
            ("CS-501", "Theory of Computation (TOC)"),
            ("CS-502", "Database Management Systems (DBMS)"),
        ]),
        ("Electives", [
            ("CS-503", "Departmental Elective (e.g., Data Analytics, Pattern Recognition, Cyber Security)"),
            ("CS-504", "Open Elective (e.g., Internet and Web Technology, Introduction to DBMS)"),
        ]),
        ("Labs & Project", [
            ("CS-505", "Linux Lab"),
            ("CS-506", "Python Lab"),
            ("CS-508", "Minor Project-I"),
        ]),
    ],
    6: [
        ("Core Subjects", [
            ("CS-601", "Machine Learning"),
            ("CS-602", "Computer Networks"),
        ]),
        ("Electives", [
            ("CS-603", "Departmental Elective (e.g., Advanced Computer Architecture, Compiler Design, Computer Graphics)"),
            ("CS-604", "Open Elective (e.g., Knowledge Management, Project Management)"),
        ]),
        ("Labs & Project", [
            ("CS-605", "Data Analytics Lab"),
            ("CS-606", "Skill Development Lab"),
            ("CS-608", "Minor Project-II"),
        ]),
    ],
    7: [
        ("Core Subjects", [("CS-701", "Software Architectures")]),
        ("Electives", [
            ("CS-702", "Departmental Elective (e.g., Computational Intelligence, Cloud Computing, Big Data)"),
            ("CS-703", "Open Elective (e.g., Cryptography & Information Security, Data Mining)"),
        ]),
        ("Practical & Project", [
            ("CS-704", "Departmental Elective Lab"),
            ("CS-706", "Major Project-I"),
            ("CS-707", "Industrial Training / Internship Evaluation"),
        ]),
    ],
    8: [
        ("Core Subjects", [("CS-801", "Internet of Things (IoT)")]),
        ("Electives", [
            ("CS-802", "Departmental Elective (e.g., Blockchain Technologies, High Performance Computing)"),
            ("CS-803", "Open Elective / Managing Innovation & Entrepreneurship"),
        ]),
        ("Project", [("CS-804", "Major Project-II")]),
    ],
}


@app.route("/")
def home():
    require_db()
    query = request.args.get("q", "").strip()
    selected_subject = request.args.get("subject", "").strip()
    selected_year = request.args.get("year", "").strip()
    selected_academic_year = request.args.get("academic_year", "").strip()
    selected_semester = request.args.get("semester", "").strip()
    selected_unit = request.args.get("unit", "").strip()
    selected_unit_label = (
        "Uncategorized"
        if selected_unit == "__uncategorized__"
        else selected_unit
    )
    selected_semester_number = re.search(r"\d+", selected_semester or "")
    selected_semester_number = (
        int(selected_semester_number.group())
        if selected_semester_number else None
    )
    selected_semester_label = (
        _semester_label(selected_semester_number)
        if selected_semester_number else selected_semester
    )
    try:
        page = max(1, int(request.args.get("page", "1")))
    except ValueError:
        page = 1

    filters = {"published": True}
    if selected_year:
        filters["year"] = selected_year
    if selected_semester:
        filters.update(_semester_filter(selected_semester))
    if selected_subject:
        filters["subject"] = {
            "$in": CURRICULUM_SUBJECT_ALIASES.get(
                selected_subject,
                (selected_subject,),
            )
        }
    if selected_unit:
        if selected_unit == "__uncategorized__":
            filters["$and"] = [{
                "$or": [
                    {"unit": ""},
                    {"unit": None},
                    {"unit": {"$exists": False}},
                ]
            }]
        else:
            filters["unit"] = selected_unit

    if query:
        safe_query = re.escape(query)
        filters.setdefault("$and", []).append({"$or": [
            {"title": {"$regex": safe_query, "$options": "i"}},
            {"subject": {"$regex": safe_query, "$options": "i"}},
            {"unit": {"$regex": safe_query, "$options": "i"}},
            {"description": {"$regex": safe_query, "$options": "i"}},
        ]})

    browse_filters = {"published": True}
    if selected_semester:
        browse_filters.update(_semester_filter(selected_semester))

    catalog_rows = []
    if not selected_subject and (not query or selected_semester):
        catalog_pipeline = [{"$match": browse_filters}]
        catalog_pipeline.append({
            "$group": {
                "_id": {
                    "semester": "$semester",
                    "subject": "$subject",
                },
                "video_count": {"$sum": 1},
            }
        })
        catalog_rows = list(db.videos.aggregate(catalog_pipeline))

    semester_video_counts = {number: 0 for number in range(1, 9)}
    subject_video_counts = {number: {} for number in range(1, 9)}
    stored_semester_counts = {}
    for row in catalog_rows:
        stored_semester = row["_id"].get("semester")
        subject = row["_id"].get("subject")
        video_count = row["video_count"]
        if stored_semester:
            stored_semester_counts[stored_semester] = (
                stored_semester_counts.get(stored_semester, 0) + video_count
            )
            for semester_number in semester_video_counts:
                if _stored_semester_matches(
                    stored_semester,
                    _semester_label(semester_number),
                ):
                    semester_video_counts[semester_number] += video_count
                    if subject:
                        counts = subject_video_counts[semester_number]
                        counts[subject] = counts.get(subject, 0) + video_count

    semester_catalog = []
    for semester_number in range(1, 9):
        label = _semester_label(semester_number)
        semester_catalog.append({
            "label": label,
            "number": semester_number,
            "video_count": semester_video_counts[semester_number],
            "subject_count": sum(
                len(subjects) for _, subjects in CURRICULUM.get(semester_number, [])
            ),
        })

    known_semester_numbers = {item["number"] for item in semester_catalog}
    for stored_semester, video_count in stored_semester_counts.items():
        if not stored_semester:
            continue
        number_match = re.search(r"\d+", str(stored_semester))
        if number_match and int(number_match.group()) in known_semester_numbers:
            continue
        semester_catalog.append({
            "label": str(stored_semester),
            "number": int(number_match.group()) if number_match else 99,
            "video_count": video_count,
        })
    semester_catalog.sort(key=lambda item: (item["number"], item["label"].casefold()))
    academic_years = [
        {"label": _semester_label(year).replace("Semester", "Year"), "number": year}
        for year in range(1, 5)
    ]
    if any(semester["number"] not in range(1, 9) for semester in semester_catalog):
        academic_years.append({"label": "Other Semesters", "number": None})
    if selected_academic_year not in {year["label"] for year in academic_years}:
        selected_academic_year = ""
    for academic_year in academic_years:
        if academic_year["number"] is None:
            academic_year["semester_count"] = sum(
                semester["number"] not in range(1, 9)
                for semester in semester_catalog
            )
            continue
        first_semester = (academic_year["number"] - 1) * 2 + 1
        academic_year["semester_count"] = sum(
            first_semester <= semester["number"] <= first_semester + 1
            for semester in semester_catalog
        )

    semester_subject_groups = []
    subject_video_count = 0
    if selected_semester and not selected_subject:
        catalog_groups = CURRICULUM.get(selected_semester_number, [])
        catalog_names = {
            alias.casefold()
            for _, subjects in catalog_groups
            for _, name in subjects
            for alias in CURRICULUM_SUBJECT_ALIASES.get(name, (name,))
        }
        for group_name, subjects in catalog_groups:
            group_subjects = []
            for code, name in subjects:
                aliases = CURRICULUM_SUBJECT_ALIASES.get(name, (name,))
                video_count = sum(
                    subject_video_counts.get(selected_semester_number, {}).get(alias, 0)
                    for alias in aliases
                )
                group_subjects.append({
                    "code": code,
                    "name": name,
                    "video_count": video_count,
                })
            semester_subject_groups.append({
                "name": group_name,
                "subjects": group_subjects,
            })

        extra_subjects = []
        semester_subject_counts = subject_video_counts.get(
            selected_semester_number,
            {},
        )
        for subject in sorted(semester_subject_counts, key=str.casefold):
            if subject.casefold() in catalog_names:
                continue
            extra_subjects.append({
                "name": subject,
                "video_count": semester_subject_counts[subject],
            })
        if extra_subjects:
            semester_subject_groups.append({
                "name": "Other Published Subjects",
                "subjects": extra_subjects,
            })
    elif selected_semester and selected_subject:
        subject_video_count = 0
    else:
        subject_video_count = 0

    show_videos = bool(query or selected_subject)
    total_videos = 0
    matching_videos = []
    if show_videos:
        if selected_subject:
            matching_videos = list(db.videos.find(filters).sort("created_at", -1))
            matching_videos.sort(key=_video_unit_sort_key)
            total_videos = len(matching_videos)
            subject_video_count = total_videos
        else:
            total_videos = db.videos.count_documents(filters)
    page_size = max(12, total_videos) if selected_subject else 12
    total_pages = max(1, (total_videos + page_size - 1) // page_size)
    page = min(page, total_pages)
    if selected_subject:
        start = (page - 1) * page_size
        videos = matching_videos[start:start + page_size]
    elif query:
        videos = list(
            db.videos.find(filters)
            .sort("created_at", -1)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )
    else:
        videos = []
    return render_template(
        "index.html",
        videos=videos,
        query=query,
        selected_subject=selected_subject,
        selected_year=selected_year,
        selected_academic_year=selected_academic_year,
        selected_semester=selected_semester,
        selected_unit=selected_unit,
        selected_unit_label=selected_unit_label,
        selected_semester_label=selected_semester_label,
        semester_catalog=semester_catalog,
        academic_years=academic_years,
        semester_subject_groups=semester_subject_groups,
        subject_video_count=subject_video_count,
        show_videos=show_videos,
        page=page,
        total_pages=total_pages,
        total_videos=total_videos,
    )


@app.route("/robots.txt")
def robots():
    return Response(
        "User-agent: *\nAllow: /\nDisallow: /admin\nDisallow: /api/\nSitemap: "
        + url_for("sitemap", _external=True) + "\n",
        mimetype="text/plain",
    )


@app.route("/sitemap.xml")
def sitemap():
    require_db()
    pages = [url_for("home", _external=True)]
    pages.extend(
        url_for("watch", slug=video["slug"], _external=True)
        for video in db.videos.find({"published": True}, {"slug": 1})
    )
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.extend(f"<url><loc>{page}</loc></url>" for page in pages)
    xml.append("</urlset>")
    return Response("".join(xml), mimetype="application/xml")


@app.route("/watch/<slug>")
def watch(slug):
    require_db()
    video = db.videos.find_one({"slug": slug, "published": True})
    if not video:
        abort(404)

    related_filter = {
        "published": True,
        "_id": {"$ne": video["_id"]},
    }
    if video.get("subject"):
        related_filter["subject"] = video["subject"]
    related_videos = list(
        db.videos.find(related_filter).sort("created_at", -1).limit(3)
    )

    return render_template(
        "watch.html",
        video=video,
        related_videos=related_videos,
        required_watch_seconds=REQUIRED_WATCH_SECONDS,
    )


@app.route("/api/watch/<video_id>/start", methods=["POST"])
def watch_start(video_id):
    require_db()

    try:
        video = db.videos.find_one({
            "_id": ObjectId(video_id),
            "published": True,
        })
    except Exception:
        abort(404)

    if not video:
        abort(404)

    session["watch_video_id"] = str(video["_id"])
    session["watch_started_at"] = now().isoformat()
    session["watch_seconds"] = 0
    session["analytics_last_progress"] = 0
    session["analytics_unlock_recorded"] = False
    session.modified = True

    record_analytics_event("video_start", video, 0)

    return jsonify({
        "ok": True,
        "required_seconds": REQUIRED_WATCH_SECONDS,
    })


@app.route("/api/watch/<video_id>/progress", methods=["POST"])
def watch_progress(video_id):
    require_db()

    if session.get("watch_video_id") != video_id:
        return jsonify({
            "ok": False,
            "error": "Watch session not started.",
        }), 400

    data = request.get_json(silent=True) or {}

    try:
        client_seconds = float(data.get("watched_seconds", 0))
    except (TypeError, ValueError):
        client_seconds = 0

    previous = float(session.get("watch_seconds", 0))

    if data.get("video_ended"):
        client_seconds = max(previous, float(REQUIRED_WATCH_SECONDS))
    else:
        if client_seconds < previous:
            client_seconds = previous
        # Prevent a large artificial jump from the browser.
        client_seconds = min(client_seconds, previous + 3)

    session["watch_seconds"] = client_seconds
    session.modified = True

    # Fetch the video only when we need to write an analytics event.
    last_recorded = float(session.get("analytics_last_progress", 0))

    # Store progress approximately every 5 seconds instead of every heartbeat.
    if client_seconds >= last_recorded + 5:
        try:
            video = db.videos.find_one({
                "_id": ObjectId(video_id),
                "published": True,
            })
        except Exception:
            video = None

        if video:
            record_analytics_event(
                "watch_progress",
                video,
                client_seconds,
            )
            session["analytics_last_progress"] = client_seconds
            session.modified = True

    unlocked = client_seconds >= REQUIRED_WATCH_SECONDS

    return jsonify({
        "ok": True,
        "watched_seconds": client_seconds,
        "required_seconds": REQUIRED_WATCH_SECONDS,
        "unlocked": unlocked,
    })


@app.route("/api/watch/<video_id>/unlock", methods=["POST"])
def unlock(video_id):
    require_db()

    if session.get("watch_video_id") != video_id:
        return jsonify({
            "ok": False,
            "error": "Invalid watch session.",
        }), 400

    data = request.get_json(silent=True) or {}
    watched = float(session.get("watch_seconds", 0))

    if data.get("video_ended"):
        watched = max(watched, float(REQUIRED_WATCH_SECONDS))
        session["watch_seconds"] = watched
        session.modified = True

    if watched < REQUIRED_WATCH_SECONDS:
        return jsonify({
            "ok": False,
            "unlocked": False,
            "watched_seconds": watched,
            "required_seconds": REQUIRED_WATCH_SECONDS,
        }), 403

    try:
        video = db.videos.find_one({
            "_id": ObjectId(video_id),
            "published": True,
        })
    except Exception:
        abort(404)

    if not video:
        abort(404)

    session["unlocked_video_id"] = video_id

    # Count one completion per watch session.
    if not session.get("analytics_unlock_recorded", False):
        record_analytics_event(
            "notes_unlock",
            video,
            watched,
        )
        session["analytics_unlock_recorded"] = True
        session.modified = True

    notes_url = (video.get("notes_url") or "").strip()
    has_valid_drive_link = bool(notes_url and ("drive.google.com" in notes_url or notes_url.startswith(("http://", "https://"))))

    return jsonify({
        "ok": True,
        "unlocked": True,
        "notes_url_allowed": True,
        "has_drive_link": has_valid_drive_link,
        "download_url": url_for("download_redirect", video_id=video_id),
    })


@app.route("/api/watch/<video_id>/download", methods=["GET"])
def download_redirect(video_id):
    require_db()

    # Student must have unlocked the notes first
    if session.get("unlocked_video_id") != video_id:
        flash("Please finish watching to unlock your notes.", "warning")
        return redirect(
            url_for(
                "watch",
                slug=_slug_for_video(video_id)
            )
        )

    try:
        video = db.videos.find_one({
            "_id": ObjectId(video_id),
            "published": True
        })
    except Exception:
        abort(404)

    if not video:
        abort(404)

    notes_url = (video.get("notes_url") or "").strip()

    # Gracefully handle missing or broken links
    if not notes_url or not notes_url.startswith(("http://", "https://")):
        flash("Notes for this lecture are not available in its description yet.", "warning")
        return redirect(url_for("watch", slug=_slug_for_video(video_id)))

    # Record the notes download BEFORE redirecting
    record_analytics_event(
        "notes_download",
        video,
        watched_seconds=session.get("watch_seconds", 0)
    )

    # Send student directly to that specific video's Google Drive link
    return redirect(notes_url)


def _slug_for_video(video_id):
    try:
        video = db.videos.find_one({"_id": ObjectId(video_id)})
        return video["slug"] if video else ""
    except Exception:
        return ""


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        ip_address = _client_ip()

        if _login_is_limited(ip_address):
            flash("Too many login attempts. Please try again in 15 minutes.", "error")
            return render_template("admin_login.html"), 429

        configured_username = os.getenv("ADMIN_USERNAME", "")
        password_hash = os.getenv("ADMIN_PASSWORD_HASH", "")
        legacy_password = os.getenv("ADMIN_PASSWORD", "")
        password_valid = (
            check_password_hash(password_hash, password)
            if password_hash else hmac.compare_digest(password, legacy_password)
        )

        if (
            configured_username
            and hmac.compare_digest(username, configured_username)
            and password_valid
        ):
            # Prevent session fixation and expire the elevated session quickly.
            session.clear()
            session["admin"] = True
            session.permanent = True
            session["csrf_token"] = secrets.token_urlsafe(32)
            _login_attempts.pop(ip_address, None)
            target = request.args.get("next", "")
            return redirect(target if _is_safe_local_url(target) else url_for("admin_dashboard"))

        _record_failed_login(ip_address)
        flash("Invalid credentials.", "error")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    require_db()

    videos = list(db.videos.find().sort("created_at", -1))
    total_videos = db.videos.count_documents({})
    published = db.videos.count_documents({"published": True})
    drafts = db.videos.count_documents({
        "published": False,
        "status": "draft",
    })
    disabled = db.videos.count_documents({
        "published": False,
        "status": {"$ne": "draft"},
    })

    return render_template(
        "admin.html",
        videos=videos,
        total_videos=total_videos,
        published=published,
        drafts=drafts,
        disabled=disabled,
        required_watch_seconds=REQUIRED_WATCH_SECONDS,
    )


# ============================================================
# ADMIN CONTENT LIBRARY
# ============================================================

@app.route("/admin/content")
@admin_required
def admin_content():
    require_db()

    videos = list(db.videos.find().sort("created_at", -1))
    total_videos = db.videos.count_documents({})
    published = db.videos.count_documents({"published": True})
    drafts = db.videos.count_documents({
        "published": False,
        "status": "draft",
    })
    disabled = db.videos.count_documents({
        "published": False,
        "status": {"$ne": "draft"},
    })

    return render_template(
        "admin_content.html",
        videos=videos,
        total_videos=total_videos,
        published=published,
        drafts=drafts,
        disabled=disabled,
        required_watch_seconds=REQUIRED_WATCH_SECONDS,
    )


@app.route("/admin/videos/new", methods=["POST"])
@admin_required
def create_video():
    require_db()

    title = request.form.get("title", "").strip()
    year = request.form.get("year", "").strip()
    semester = request.form.get("semester", "").strip()
    slug = slugify(request.form.get("slug", "").strip() or title)
    subject = request.form.get("subject", "").strip()
    unit = request.form.get("unit", "").strip()
    description = request.form.get("description", "").strip()
    youtube_url = request.form.get("youtube_url", "").strip()
    notes_url = request.form.get("notes_url", "").strip()
    status = request.form.get("status", "published").strip().lower()

    youtube_id = extract_youtube_id(youtube_url)

    if status not in {"published", "draft"}:
        status = "published"

    if not title or not slug or not youtube_id or not notes_url:
        flash(
            "Title, valid YouTube URL and notes URL are required.",
            "error",
        )
        return redirect(url_for("admin_dashboard"))

    if db.videos.find_one({"slug": slug}):
        flash("That slug already exists. Choose another.", "error")
        return redirect(url_for("admin_dashboard"))

    video = {
        "title": title,
        "slug": slug,
        "year": year,
        "semester": semester,
        "subject": subject,
        "unit": unit,
        "description": description,
        "youtube_url": youtube_url,
        "youtube_id": youtube_id,
        "notes_url": notes_url,
        "status": status,
        "published": status == "published",
        "created_at": now(),
        "updated_at": now(),
    }

    db.videos.insert_one(video)

    if status == "draft":
        flash("Video saved as draft.", "success")
    else:
        flash("Video published successfully.", "success")

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/videos/<video_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_video(video_id):
    require_db()

    try:
        video = db.videos.find_one({"_id": ObjectId(video_id)})
    except Exception:
        abort(404)

    if not video:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        slug = slugify(request.form.get("slug", "").strip() or title)
        year = request.form.get("year", "").strip()
        semester = request.form.get("semester", "").strip()
        subject = request.form.get("subject", "").strip()
        unit = request.form.get("unit", "").strip()
        description = request.form.get("description", "").strip()
        youtube_url = request.form.get("youtube_url", "").strip()
        notes_url = request.form.get("notes_url", "").strip()
        status = request.form.get("status", "published").strip().lower()
        youtube_id = extract_youtube_id(youtube_url)

        if status not in {"published", "draft"}:
            status = "published"

        if not title or not slug or not youtube_id or not notes_url:
            flash("Please fill all required fields correctly.", "error")
            return redirect(url_for("edit_video", video_id=video_id))

        duplicate = db.videos.find_one({
            "slug": slug,
            "_id": {"$ne": video["_id"]},
        })

        if duplicate:
            flash(
                "That slug is already being used by another video.",
                "error",
            )
            return redirect(url_for("edit_video", video_id=video_id))

        db.videos.update_one(
            {"_id": video["_id"]},
            {"$set": {
                "title": title,
                "slug": slug,
                "year": year,
                "semester": semester,
                "subject": subject,
                "unit": unit,
                "description": description,
                "youtube_url": youtube_url,
                "youtube_id": youtube_id,
                "notes_url": notes_url,
                "status": status,
                "published": status == "published",
                "updated_at": now(),
            }},
        )

        flash("Video updated successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_video.html", video=video)


@app.route("/admin/videos/<video_id>/delete", methods=["POST"])
@admin_required
def delete_video(video_id):
    require_db()

    try:
        video = db.videos.find_one({"_id": ObjectId(video_id)})
    except Exception:
        abort(404)

    if not video:
        abort(404)

    db.videos.delete_one({"_id": video["_id"]})
    flash(f'Video "{video["title"]}" deleted.', "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/videos/<video_id>/toggle", methods=["POST"])
@admin_required
def toggle_video(video_id):
    require_db()

    try:
        video = db.videos.find_one({"_id": ObjectId(video_id)})
    except Exception:
        abort(404)

    if not video:
        abort(404)

    db.videos.update_one(
        {"_id": video["_id"]},
        {"$set": {
            "published": not video.get("published", True),
            "updated_at": now(),
        }},
    )

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/videos/sync-youtube", methods=["POST"])
@admin_required
def sync_youtube():
    require_db()
    try:
        import yt_dlp
        channel_url = request.form.get("channel_url", "").strip() or "https://www.youtube.com/@TSUKOMI_PADHAYEGA/videos"
        ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
        entries = info.get('entries', []) or []
        added_count = 0
        updated_count = 0

        detail_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(detail_opts) as detail_ydl:
            for e in entries:
                vid_id = e.get('id')
                if not vid_id:
                    continue
                try:
                    vinfo = detail_ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
                    desc = vinfo.get('description', '') or ''
                    title = vinfo.get('title') or e.get('title') or ''
                except Exception:
                    desc = ''
                    title = e.get('title') or ''

                drive_links = re.findall(r'(https?://(?:drive|docs)\.google\.com/[^\s\n\)\"\'<>]+)', desc)
                notes_link = drive_links[0] if drive_links else ""

                title_lower = title.lower()
                if 'coa' in title_lower or 'computer organization' in title_lower:
                    subject = "Computer Organization & Architecture"
                elif 'operating system' in title_lower or 'os ' in title_lower or 'os unit' in title_lower:
                    subject = "Operating Systems"
                elif 'software engineering' in title_lower:
                    subject = "Software Engineering"
                else:
                    subject = "Engineering"

                unit = "All Units"
                unit_match = re.search(r'unit\s*([0-9])', title_lower)
                if unit_match:
                    unit = f"Unit {unit_match.group(1)}"
                elif 'top 15' in title_lower or 'important' in title_lower:
                    unit = "Important Questions"
                elif 'last moment' in title_lower:
                    unit = "Last Moment Revision"
                elif 'one shot' in title_lower:
                    unit = "Complete Revision"

                slug = slugify(title)
                existing = db.videos.find_one({"$or": [{"youtube_id": vid_id}, {"slug": slug}]})

                if not existing:
                    if db.videos.find_one({"slug": slug}):
                        slug = f"{slug}-{vid_id[:4]}"
                    db.videos.insert_one({
                        "title": title,
                        "slug": slug,
                        "year": "2nd Year",
                        "semester": "4th Semester",
                        "subject": subject,
                        "unit": unit,
                        "description": desc or f"Study lecture and notes for {subject} - {unit}.",
                        "youtube_url": f"https://www.youtube.com/watch?v={vid_id}",
                        "youtube_id": vid_id,
                        "notes_url": notes_link,
                        "status": "published",
                        "published": True,
                        "created_at": now(),
                        "updated_at": now(),
                    })
                    added_count += 1
                else:
                    db.videos.update_one(
                        {"_id": existing["_id"]},
                        {"$set": {
                            "title": title,
                            "subject": subject,
                            "unit": unit,
                            "description": desc or existing.get("description", ""),
                            "notes_url": notes_link if notes_link else existing.get("notes_url", ""),
                            "updated_at": now(),
                        }}
                    )
                    updated_count += 1

        flash(f"YouTube Sync Complete: {added_count} new videos added, {updated_count} updated.", "success")
    except Exception as exc:
        flash(f"Sync failed: {exc}", "error")

    return redirect(request.referrer or url_for("admin_dashboard"))


# ============================================================
# ADMIN ANALYTICS
# ============================================================

@app.route("/admin/analytics")
@admin_required
def admin_analytics():
    require_db()

    events = db.analytics_events

    total_views = events.count_documents({"event": "video_start"})
    notes_downloads = events.count_documents({"event": "notes_download"})
    completions = events.count_documents({"event": "notes_unlock"})

    unique_learners = len(
        events.distinct("analytics_session_id")
    )

    completion_rate = (
        round((completions / total_views) * 100, 1)
        if total_views > 0 else 0
    )

    # One maximum progress value per learner/video, then sum those values.
    watch_pipeline = [
        {"$match": {"event": "watch_progress"}},
        {"$group": {
            "_id": {
                "session": "$analytics_session_id",
                "video": "$video_id",
            },
            "max_watched": {"$max": "$watched_seconds"},
        }},
        {"$group": {
            "_id": None,
            "total_seconds": {"$sum": "$max_watched"},
        }},
    ]

    watch_result = list(events.aggregate(watch_pipeline))
    total_watch_seconds = (
        watch_result[0].get("total_seconds", 0)
        if watch_result else 0
    )
    total_watch_minutes = round(total_watch_seconds / 60, 1)

    subject_pipeline = [
        {"$match": {
            "event": "video_start",
            "subject": {"$nin": [None, ""]},
        }},
        {"$group": {
            "_id": "$subject",
            "views": {"$sum": 1},
        }},
        {"$sort": {"views": -1}},
        {"$limit": 10},
    ]

    subject_stats = list(events.aggregate(subject_pipeline))

    lecture_pipeline = [
        {"$match": {"event": "video_start"}},
        {"$group": {
            "_id": {
                "video_id": "$video_id",
                "title": "$video_title",
            },
            "views": {"$sum": 1},
        }},
        {"$sort": {"views": -1}},
        {"$limit": 10},
    ]

    lecture_stats = list(events.aggregate(lecture_pipeline))

    return render_template(
        "admin_analytics.html",
        total_views=total_views,
        unique_learners=unique_learners,
        total_watch_minutes=total_watch_minutes,
        notes_downloads=notes_downloads,
        completion_rate=completion_rate,
        subject_stats=subject_stats,
        lecture_stats=lecture_stats,
    )


@app.errorhandler(503)
def service_unavailable(error):
    return render_template(
        "error.html",
        code=503,
        message=error.description,
    ), 503


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "1") == "1",
    )
