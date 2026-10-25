# TSUKOMI StudyHub

TSUKOMI StudyHub is an exam-focused learning platform created for **TSUKOMI PADHAYEGA**. It brings RGPV B.Tech lectures, revision material, and study notes into one focused experience for students preparing for university examinations.

## About the project

The platform gives students a simple way to discover relevant lectures by year, semester, and subject. Subject videos are listed together in unit order, starting from Unit 1. Each lecture has its own dedicated page with an embedded YouTube video, learning information, and related content. After students complete the required watch duration, they can open the notes attached to that lecture.

The project also has a protected admin workspace, making it possible to manage the full lecture library without changing website code for every new video. An administrator can add a YouTube link, attach notes, choose academic details, publish content, and review engagement analytics.

## Curriculum browser

The study browser starts with year cards, then shows that year's two semesters, followed by grouped subject cards. Semesters 1 and 2 show Group A and Group B separately; later semesters organize subjects into core, elective, lab, and project groups. Selecting a subject shows all its videos together, ordered by unit, instead of requiring a separate unit selection. Selecting a year, semester, or subject updates the browser without a full-page reload, shows immediate loading feedback, and can prefetch hovered or keyboard-focused cards. Browser Back/Forward and direct links continue to work. Subjects without published lectures show “Content coming soon.” These are curriculum placeholders only and do not create fake video records or links; published video counts continue to come from MongoDB.

## How it helps students

- Keeps exam-focused lecture content in one organized study hub
- Makes it easier to find content by subject, semester, and unit
- Supports revision with YouTube lectures and accompanying notes
- Encourages learners to engage with a lecture before opening its notes
- Helps students quickly explore related lectures from the same subject

## How it was built

TSUKOMI StudyHub was built as a full-stack web application using Python and Flask for the backend, MongoDB for content and analytics storage, and HTML, CSS, JavaScript, and Jinja templates for the user interface. YouTube is integrated through the YouTube IFrame API, while Google Drive links are used to provide lecture notes.

The project includes a responsive public StudyHub, search and academic filters, dynamic video pages, a secure admin dashboard, watch-progress handling, and analytics for video activity and notes-link clicks.

## Skills demonstrated

Building this project has helped develop practical skills in:

- Full-stack web development with Flask
- Designing responsive, student-focused user interfaces
- MongoDB data modelling and database integration
- Authentication, session handling, CSRF protection, and rate limiting
- CRUD operations for a real content-management workflow
- Third-party platform integration with YouTube and Google Drive
- Search, filtering, pagination, analytics, and SEO fundamentals
- Version control and project documentation with Git and GitHub

## Impact

TSUKOMI StudyHub turns scattered learning resources into a structured academic platform. It is designed to make exam preparation easier for students while giving the creator a practical system for publishing, organizing, and improving educational content over time.

## Deploy to Vercel

The Flask app runs on Vercel as a Python function. Before deploying:

1. Push this repository to GitHub and import it as a project in Vercel. The included `vercel.json` routes requests to the Flask function and includes the templates and static assets.
2. Create a MongoDB database (for example, with MongoDB Atlas) and allow connections from your Vercel deployment. Use a database user with a strong password.
3. In **Vercel → Project Settings → Environment Variables**, set:
   - `MONGO_URI` — the MongoDB connection string for the database.
   - `SECRET_KEY` — a long, random value used to sign session cookies. Generate one locally with `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
4. Set `ADMIN_USERNAME` to your chosen admin username and `ADMIN_PASSWORD_HASH` to a Werkzeug password hash. Generate the hash locally; the command prompts for the password without echoing it:
   `python -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('New admin password: ')))"`
   Add the same variables to your local `.env` file for local development. Do not share or commit the password or its hash.
5. Optionally set `DB_NAME` (defaults to `tsukomi_studyhub`), `REQUIRED_WATCH_SECONDS` (defaults to `40`), and `SESSION_COOKIE_SECURE` (defaults to enabled on Vercel).
6. Redeploy after adding or changing Vercel environment variables. Open `/admin` to reach the protected admin login.

Do not commit `.env` or put production secrets in the repository. On successful MongoDB connections, the app ensures its indexes, imports the bundled initial video records if the videos collection is empty, and applies idempotent metadata migrations such as simplified video titles.

## License

Private project for TSUKOMI PADHAYEGA.
