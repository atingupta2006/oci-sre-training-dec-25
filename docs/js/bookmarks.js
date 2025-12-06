// SPA-AWARE Bookmark System for MkDocs Material
// Works with navigation.instant enabled

const STORAGE_KEY = "mkdocs_bookmarks";

// Load bookmarks
function loadBookmarks() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
}

// Save bookmarks
function saveBookmarks(list) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
}

// Toggle bookmark for the current page
function toggleBookmark() {
    const url = window.location.pathname;
    const title = document.title.replace(" - SRE Concepts", "").trim();

    let bookmarks = loadBookmarks();
    const exists = bookmarks.find(b => b.url === url);

    if (exists) {
        bookmarks = bookmarks.filter(b => b.url !== url);
    } else {
        bookmarks.push({ title, url });
    }

    saveBookmarks(bookmarks);

    updateBookmarkIcon();

    // Update list immediately if on bookmarks page
    if (document.getElementById("bookmark-list")) {
        renderBookmarks();
    }
}

// Update the star icon
function updateBookmarkIcon() {
    const url = window.location.pathname;
    const icon = document.getElementById("bookmark-icon");
    if (!icon) return;

    const bookmarks = loadBookmarks();
    const exists = bookmarks.find(b => b.url === url);

    icon.innerHTML = exists ? "⭐" : "☆";
}

// Render bookmark list
function renderBookmarks() {
    const container = document.getElementById("bookmark-list");
    if (!container) return;

    const bookmarks = loadBookmarks();

    if (bookmarks.length === 0) {
        container.innerHTML = "<p>No bookmarks yet.</p>";
        return;
    }

    let html = "<ul>";
    for (const b of bookmarks) {
        html += `
            <li>
                <a href="${b.url}">${b.title}</a>
                <button onclick="removeBookmark('${b.url}')">Remove</button>
            </li>`;
    }
    html += "</ul>";

    container.innerHTML = html;
}

// Remove bookmark
function removeBookmark(url) {
    let bookmarks = loadBookmarks();
    bookmarks = bookmarks.filter(b => b.url !== url);
    saveBookmarks(bookmarks);
    renderBookmarks();
    updateBookmarkIcon();
}

// ⭐ The MAGIC FIX — Fires on every SPA navigation
document$.subscribe(function () {
    updateBookmarkIcon();
    renderBookmarks();
});
