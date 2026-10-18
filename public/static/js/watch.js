/*
============================================================
TSUKOMI STUDYHUB — WATCH TO UNLOCK
============================================================

Baseline behavior:
- Uses a complete YouTube URL stored by Flask.
- YouTube autoplay is OFF.
- Student starts playback manually.
- Real elapsed time is counted only while the player reports PLAYING.
- Pausing stops the counter.
- Forward seeking does not add fake watch time.
- 120 seconds of actual playback unlocks notes.
- Backend heartbeat adds a second server-side layer.
============================================================
*/

let player = null;
let progressTimer = null;
let duration = 0;
let watchedSeconds = 0;
let lastTick = 0;
let completed = false;

const VIDEO = window.TSUKOMI_VIDEO;

const loading = document.getElementById("loading");
const currentTimeEl = document.getElementById("currentTime");
const durationEl = document.getElementById("duration");
const progressFill = document.getElementById("progressFill");
const statusEl = document.getElementById("status");
const unlockBox = document.getElementById("unlockBox");


function extractYouTubeVideoId(url) {
  try {
    const parsed = new URL(url);

    if (parsed.hostname === "youtu.be") {
      return parsed.pathname.substring(1).split("/")[0];
    }

    if (parsed.searchParams.get("v")) {
      return parsed.searchParams.get("v");
    }

    const embedMatch = parsed.pathname.match(/\/embed\/([^/]+)/);
    if (embedMatch) {
      return embedMatch[1];
    }

    const shortsMatch = parsed.pathname.match(/\/shorts\/([^/]+)/);
    if (shortsMatch) {
      return shortsMatch[1];
    }

    return null;
  } catch {
    return null;
  }
}


function formatTime(seconds) {
  seconds = Math.max(0, Math.floor(seconds || 0));

  const minutes = Math.floor(seconds / 60);
  const remaining = seconds % 60;

  return (
    String(minutes).padStart(2, "0") +
    ":" +
    String(remaining).padStart(2, "0")
  );
}


function onYouTubeIframeAPIReady() {

  const videoId =
    VIDEO.youtubeId ||
    extractYouTubeVideoId(VIDEO.youtubeUrl);

  if (!videoId) {
    loading.textContent = "Invalid YouTube URL.";
    statusEl.textContent = "The YouTube URL could not be understood.";
    statusEl.classList.add("warning");
    return;
  }

  player = new YT.Player("player", {
    videoId: videoId,

    playerVars: {
      autoplay: 0,
      playsinline: 1,
      controls: 1,
      rel: 0,
      iv_load_policy: 3,
      enablejsapi: 1,
      origin: window.location.origin
    },

    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange,
      onError: onPlayerError
    }
  });
}


function onPlayerReady(event) {

  loading.classList.add("hidden");

  duration = event.target.getDuration();

  durationEl.textContent = formatTime(duration);

  statusEl.textContent =
    `Lecture ready. Watch ${formatTime(VIDEO.requiredWatchSeconds)} to unlock your notes.`;

  updateProgress();
}


async function startWatchSession() {

  try {
    await fetch(`/api/watch/${VIDEO.dbId}/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
  } catch (error) {
    console.warn("Watch session could not be started.", error);
  }
}


function onPlayerStateChange(event) {

  if (!player) return;

  if (event.data === YT.PlayerState.PLAYING) {

    startWatchSession();

    statusEl.textContent =
      `▶ Playing. Actual watch time: ${formatTime(watchedSeconds)} / ${formatTime(VIDEO.requiredWatchSeconds)}`;

    statusEl.classList.remove("warning");

    lastTick = performance.now();

    startProgressMonitor();
  }

  else if (event.data === YT.PlayerState.PAUSED) {

    stopProgressMonitor();

    statusEl.textContent =
      `⏸ Paused. Actual watch time: ${formatTime(watchedSeconds)} / ${formatTime(VIDEO.requiredWatchSeconds)}`;
  }

  else if (event.data === YT.PlayerState.ENDED) {

    stopProgressMonitor();

    updateProgress();

    if (watchedSeconds >= VIDEO.requiredWatchSeconds) {
      unlockNotes();
    } else {
      statusEl.textContent =
        `Lecture ended. You still need ${formatTime(VIDEO.requiredWatchSeconds - watchedSeconds)} of actual playback.`;
      statusEl.classList.add("warning");
    }
  }
}


function startProgressMonitor() {

  if (progressTimer) return;

  lastTick = performance.now();

  progressTimer = setInterval(trackPlayback, 250);
}


function stopProgressMonitor() {

  if (!progressTimer) return;

  clearInterval(progressTimer);
  progressTimer = null;
}


async function trackPlayback() {

  if (!player || completed) return;

  if (player.getPlayerState() !== YT.PlayerState.PLAYING) {
    return;
  }

  const now = performance.now();
  const realElapsed = (now - lastTick) / 1000;

  /*
    Count only normal short intervals.
    A huge browser freeze/tab suspension cannot create
    a giant fake watch-time jump.
  */
  if (realElapsed > 0 && realElapsed <= 1) {
    watchedSeconds += realElapsed;
  }

  lastTick = now;

  watchedSeconds = Math.min(watchedSeconds, duration);

  updateProgress();

  await sendProgressHeartbeat();

  if (watchedSeconds >= VIDEO.requiredWatchSeconds) {
    unlockNotes();
  }
}


async function sendProgressHeartbeat() {

  try {

    const response = await fetch(
      `/api/watch/${VIDEO.dbId}/progress`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          watched_seconds: Math.floor(watchedSeconds)
        })
      }
    );

    if (!response.ok) {
      return;
    }

    const data = await response.json();

    if (data.unlocked) {
      unlockNotes();
    }

  } catch (error) {
    console.warn("Progress heartbeat failed.", error);
  }
}


function updateProgress() {

  if (!duration) return;

  const percentage =
    Math.min(
      100,
      (watchedSeconds / duration) * 100
    );

  progressFill.style.width = percentage + "%";

  currentTimeEl.textContent = formatTime(watchedSeconds);
  durationEl.textContent = formatTime(duration);

  if (!completed) {

    statusEl.textContent =
      `Watch ${formatTime(VIDEO.requiredWatchSeconds)} of this lecture to unlock your notes. ` +
      `Actual watch time: ${formatTime(watchedSeconds)}`;
  }
}


async function unlockNotes() {

  if (completed) return;

  try {

    const response = await fetch(
      `/api/watch/${VIDEO.dbId}/unlock`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        }
      }
    );

    if (!response.ok) {
      return;
    }

    const data = await response.json();

    if (!data.unlocked) {
      return;
    }

    completed = true;

    watchedSeconds =
      Math.max(watchedSeconds, VIDEO.requiredWatchSeconds);

    updateProgress();

    if (data.has_drive_link || VIDEO.notesUrl) {
      statusEl.textContent =
        "✅ Required watch time completed. Your notes are unlocked.";
      statusEl.classList.add("success");
      const dlBtn = document.getElementById("downloadButton");
      if (dlBtn) {
        dlBtn.href = VIDEO.notesUrl;
        dlBtn.style.display = "inline-flex";
      }
      unlockBox.classList.add("show");
    } else {
      statusEl.textContent =
        "✅ Required watch time completed! (No notes link was attached to this video description).";
      statusEl.classList.add("success");
      const dlBtn = document.getElementById("downloadButton");
      if (dlBtn) dlBtn.style.display = "none";
      unlockBox.classList.add("show");
    }

  } catch (error) {
    console.warn("Unlock request failed.", error);
  }
}


function onPlayerError(event) {

  loading.classList.remove("hidden");

  loading.textContent =
    "This YouTube video could not be loaded.";

  statusEl.textContent =
    "YouTube player error: " + event.data;

  statusEl.classList.add("warning");
}
