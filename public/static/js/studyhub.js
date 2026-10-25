(() => {
  let navigationRequestId = 0;
  const pageCache = new Map();
  const maxCachedPages = 6;

  function requestPage(url) {
    const key = url.toString();
    if (pageCache.has(key)) {
      const cachedPage = pageCache.get(key);
      pageCache.delete(key);
      pageCache.set(key, cachedPage);
      return cachedPage;
    }

    const pageRequest = fetch(key, {
      headers: { "X-Requested-With": "StudyHub-Navigation" }
    }).then((response) => {
      if (!response.ok) {
        throw new Error(`StudyHub navigation failed with status ${response.status}.`);
      }
      return response.text();
    }).catch((error) => {
      pageCache.delete(key);
      throw error;
    });

    pageCache.set(key, pageRequest);
    if (pageCache.size > maxCachedPages) {
      pageCache.delete(pageCache.keys().next().value);
    }
    return pageRequest;
  }

  function getNavigationUi() {
    let progress = document.querySelector(".study-navigation-progress");
    let status = document.querySelector(".study-navigation-status");

    if (!progress) {
      progress = document.createElement("div");
      progress.className = "study-navigation-progress";
      progress.setAttribute("role", "progressbar");
      progress.setAttribute("aria-label", "Loading StudyHub content");
      progress.setAttribute("aria-valuetext", "Loading");
      progress.innerHTML = "<span></span>";
      document.body.append(progress);
    }

    if (!status) {
      status = document.createElement("div");
      status.className = "study-navigation-status";
      status.setAttribute("role", "status");
      status.setAttribute("aria-live", "polite");
      status.innerHTML = '<span class="study-navigation-spinner" aria-hidden="true"></span><span></span>';
      document.body.append(status);
    }

    return { progress, status };
  }

  function setLoading(isLoading, label = "") {
    const { progress, status } = getNavigationUi();
    document.body.classList.toggle("study-navigation-loading", isLoading);
    progress.classList.toggle("active", isLoading);
    status.classList.toggle("active", isLoading);
    status.lastElementChild.textContent = isLoading
      ? `Loading ${label || "StudyHub"}…`
      : "";

    document.querySelectorAll("#study-selector, #lectures").forEach((section) => {
      if (isLoading) {
        section.setAttribute("aria-busy", "true");
      } else {
        section.removeAttribute("aria-busy");
      }
    });
  }

  function linkLabel(link) {
    const title = link.querySelector("strong, h3");
    return title?.textContent.trim() || link.textContent.trim().replace(/\s+/g, " ");
  }

  async function showBrowsePage(url, addHistoryEntry, label = "") {
    const requestId = ++navigationRequestId;
    setLoading(true, label);

    try {
      const responseText = await requestPage(url);
      const page = new DOMParser().parseFromString(responseText, "text/html");
      if (requestId !== navigationRequestId) {
        return;
      }

      const nextSelector = page.querySelector("#study-selector");
      const currentSelector = document.querySelector("#study-selector");
      if (!nextSelector || !currentSelector) {
        throw new Error("StudyHub navigation response did not include the study selector.");
      }

      nextSelector.classList.add("study-page-enter");
      currentSelector.replaceWith(nextSelector);

      const currentLectures = document.querySelector("#lectures");
      const nextLectures = page.querySelector("#lectures");
      if (currentLectures && nextLectures) {
        nextLectures.classList.add("study-page-enter");
        currentLectures.replaceWith(nextLectures);
      } else if (currentLectures) {
        currentLectures.remove();
      } else if (nextLectures) {
        nextLectures.classList.add("study-page-enter");
        document.querySelector("#study-selector").after(nextLectures);
      }

      if (addHistoryEntry) {
        window.history.pushState({}, "", url);
      }

      setLoading(false);
      const heading = document.querySelector("#browser-title");
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
      }
    } catch (error) {
      if (requestId !== navigationRequestId) {
        return;
      }
      setLoading(false);
      console.error("Could not update the StudyHub browser without reloading.", error);
      window.location.assign(url);
    }
  }

  function navigationLink(target) {
    return target.closest("#study-selector a[href], #lectures .pagination a[href]");
  }

  function prefetchPage(link) {
    if (!link || navigator.connection?.saveData) {
      return;
    }
    const url = new URL(link.href, window.location.href);
    if (url.origin === window.location.origin && url.pathname === window.location.pathname) {
      requestPage(url).catch((error) => {
        console.debug("StudyHub page prefetch failed; it will be requested on click.", error);
      });
    }
  }

  document.addEventListener("pointerover", (event) => {
    prefetchPage(navigationLink(event.target));
  });

  document.addEventListener("focusin", (event) => {
    prefetchPage(navigationLink(event.target));
  });

  document.addEventListener("click", (event) => {
    const link = navigationLink(event.target);
    if (
      !link ||
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }

    const url = new URL(link.href, window.location.href);
    if (url.origin !== window.location.origin || url.pathname !== window.location.pathname) {
      return;
    }

    event.preventDefault();
    showBrowsePage(url, true, linkLabel(link));
  });

  window.addEventListener("popstate", () => {
    showBrowsePage(window.location.href, false);
  });
})();
