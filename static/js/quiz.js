(function () {
  const root = document.getElementById("quiz-root");
  if (!root) return;

  const csrfToken =
    document.querySelector('meta[name="csrf-token"]')?.getAttribute("content") ||
    "";

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }

  const token = csrfToken || getCookie("csrftoken");

  const playUrl = root.dataset.playUrl;
  const resultUrl = root.dataset.resultUrl;

  let elapsed = 0;
  let locked = false;
  let timerId = null;

  const elTimer = document.getElementById("timer-display");
  const buttons = Array.from(document.querySelectorAll("[data-choice]"));

  function stopTimer() {
    if (timerId) clearInterval(timerId);
    timerId = null;
  }

  function finishFeedback() {
    locked = true;
    stopTimer();
  }

  function highlight(correctAnswer, selected) {
    buttons.forEach((btn) => {
      const val = parseInt(btn.getAttribute("data-choice"), 10);
      btn.disabled = true;
      if (val === correctAnswer) btn.classList.add("correct");
      else if (selected && val === selected) btn.classList.add("wrong");
    });
  }

  async function postAnswer(payload) {
    const res = await fetch(playUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": token,
      },
      body: JSON.stringify(payload),
      credentials: "same-origin",
    });
    if (!res.ok) throw new Error("Request failed");
    return res.json();
  }

  function scheduleNext(data) {
    setTimeout(() => {
      if (data.done) {
        window.location.href = data.redirect || resultUrl;
      } else {
        window.location.href = playUrl;
      }
    }, 1400);
  }

  async function onPick(choice) {
    if (locked) return;
    finishFeedback();
    try {
      const data = await postAnswer({ choice, timed_out: false });
      highlight(data.correct_answer, choice);
      scheduleNext(data);
    } catch (e) {
      window.location.reload();
    }
  }

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const choice = parseInt(btn.getAttribute("data-choice"), 10);
      onPick(choice);
    });
  });

  timerId = setInterval(() => {
    if (locked) return;
    elapsed += 1;
    if (elTimer) elTimer.textContent = String(elapsed);
  }, 1000);
})();
