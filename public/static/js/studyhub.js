(() => {
  let navigationRequestId = 0;

  async function showBrowsePage(url, addHistoryEntry) {
    const requestId = ++navigationRequestId;

    try {
      const response = await fetch(url, {
        headers: { "X-Requested-With": "StudyHub-Navigation" }
      });
      if (!response.ok) {
        throw new Error(`StudyHub navigation failed with status ${response.status}.`);
      }

      const page = new DOMParser().parseFromString(await response.text(), "text/html");
      if (requestId !== navigationRequestId) {
        return;
      }

      const nextSelector = page.querySelector("#study-selector");
      const currentSelector = document.querySelector("#study-selector");
      if (!nextSelector || !currentSelector) {
        throw new Error("StudyHub navigation response did not include the study selector.");
      }

      currentSelector.replaceWith(nextSelector);

      const currentLectures = document.querySelector("#lectures");
      const nextLectures = page.querySelector("#lectures");
      if (currentLectures && nextLectures) {
        currentLectures.replaceWith(nextLectures);
      } else if (currentLectures) {
        currentLectures.remove();
      } else if (nextLectures) {
        document.querySelector("#study-selector").after(nextLectures);
      }

      if (addHistoryEntry) {
        window.history.pushState({}, "", url);
      }

      const heading = document.querySelector("#browser-title");
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
      }
    } catch (error) {
      if (requestId !== navigationRequestId) {
        return;
      }
      console.error("Could not update the StudyHub browser without reloading.", error);
      window.location.assign(url);
    }
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest(
      "#study-selector a[href], #lectures .pagination a[href]"
    );
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
    showBrowsePage(url, true);
  });

  window.addEventListener("popstate", () => {
    showBrowsePage(window.location.href, false);
  });
})();
