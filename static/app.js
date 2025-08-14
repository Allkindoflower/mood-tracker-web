document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("mood-form");
  const input = document.getElementById("mood-input");
  const list = document.getElementById("mood-list");
  const count = document.getElementById("mood-count");

  const confirmPopup = document.getElementById("confirm-popup");
  const confirmYes = document.getElementById("confirm-yes");
  const confirmNo = document.getElementById("confirm-no");

  const helpPopup = document.getElementById("help-popup");
  const helpButton = document.getElementById("help-button");
  const helpClose = document.getElementById("help-close");

  let moodToDelete = null;

  function polarityToColor(polarity) {
    const red = polarity < 0 ? 255 : Math.floor(255 * (1 - polarity));
    const green = polarity > 0 ? 255 : Math.floor(255 * (1 + polarity));
    const blue = 0;
    return `rgb(${red}, ${green}, ${blue})`;
  }

  const openPopup = (popup) => {
    popup.classList.remove("hidden");
    popup.querySelector(".popup-content").focus();
  };

  const closePopup = (popup) => {
    popup.classList.add("hidden");
  };

  const renderMoods = async () => {
    try {
      const res = await fetch("/logged-moods");
      const data = await res.json();

      list.innerHTML = "";

      if (!data.moods || data.moods.length === 0) return;

      data.moods.forEach(({ mood_id, time, mood, polarity }) => {
        if (!mood_id) return;
        const li = document.createElement("li");

        li.innerHTML = `
          <span>${time} — ${mood}</span>
          <button class="delete-button" data-id="${mood_id}" aria-label="Delete mood">✖</button>
        `;

        if (polarity !== undefined) {
          li.style.backgroundColor = polarityToColor(polarity);
        }

        list.appendChild(li);
      });
    } catch (err) {
      console.error("Failed to load moods:", err);
      list.innerHTML = "<li>Failed to load moods.</li>";
    }
  };

  const updateCount = async () => {
    try {
      const res = await fetch("/mood-count");
      const data = await res.json();
      count.textContent = data.message || "No mood count available.";
    } catch (err) {
      console.error("Failed to load mood count:", err);
      count.textContent = "Failed to load mood count.";
    }
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const mood = input.value.trim();
    if (!mood) return;

    try {
      const res = await fetch("/mood", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood }),
      });
      if (!res.ok) throw new Error("Failed to log mood");

      input.value = "";
      await renderMoods();
      await updateCount();
    } catch (err) {
      console.error(err);
      alert("Failed to log mood. Try again.");
    }
  });

  list.addEventListener("click", (e) => {
    if (e.target.classList.contains("delete-button")) {
      moodToDelete = e.target.dataset.id;
      openPopup(confirmPopup);
    }
  });

  confirmYes.addEventListener("click", async () => {
    if (!moodToDelete) return;

    try {
      const res = await fetch(`/mood/delete/${moodToDelete}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete mood");

      await renderMoods();
      await updateCount();
    } catch (err) {
      console.error(err);
      alert("Failed to delete mood. Try again.");
    } finally {
      moodToDelete = null;
      closePopup(confirmPopup);
    }
  });

  confirmNo.addEventListener("click", () => {
    moodToDelete = null;
    closePopup(confirmPopup);
  });

  confirmPopup.addEventListener("click", (e) => {
    if (e.target === confirmPopup) closePopup(confirmPopup);
  });

  helpButton.addEventListener("click", () => openPopup(helpPopup));
  helpClose.addEventListener("click", () => closePopup(helpPopup));
  helpPopup.addEventListener("click", (e) => {
    if (e.target === helpPopup) closePopup(helpPopup);
  });

  renderMoods();
  updateCount();
});
