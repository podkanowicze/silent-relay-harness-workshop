const slides = [...document.querySelectorAll(".slide")];
const progressBar = document.querySelector("#progressBar");
const sectionLabel = document.querySelector("#sectionLabel");
const slideNumber = document.querySelector("#slideNumber");
const slideCount = document.querySelector("#slideCount");
const helpDialog = document.querySelector("#helpDialog");
let current = 0;
let touchStartX = 0;

function initialIndex() {
  const value = Number(location.hash.slice(1));
  return Number.isInteger(value) && value >= 1 && value <= slides.length ? value - 1 : 0;
}

function show(index, updateHash = true) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, position) => {
    slide.classList.toggle("active", position === current);
    slide.setAttribute("aria-hidden", position === current ? "false" : "true");
  });
  slideNumber.textContent = current + 1;
  slideCount.textContent = slides.length;
  sectionLabel.textContent = slides[current].dataset.section || "Workshop";
  progressBar.style.width = `${((current + 1) / slides.length) * 100}%`;
  document.title = `${current + 1}/${slides.length} · Silent Relay`;
  if (updateHash) history.replaceState(null, "", `#${current + 1}`);
}

function next() { show(current + 1); }
function previous() { show(current - 1); }

document.querySelector("#previousButton").addEventListener("click", previous);
document.querySelector("#nextButton").addEventListener("click", next);
document.querySelector("#notesButton").addEventListener("click", () => document.body.classList.toggle("show-notes"));
document.querySelector("#fullscreenButton").addEventListener("click", async () => {
  if (document.fullscreenElement) await document.exitFullscreen();
  else await document.documentElement.requestFullscreen();
});
document.querySelector("#helpButton").addEventListener("click", () => helpDialog.showModal());
document.querySelector("#closeHelp").addEventListener("click", () => helpDialog.close());

function toggleVisibleTimer() {
  const widget = slides[current].querySelector(".round-timer");
  if (!widget) return;
  widget.querySelector(widget.dataset.running === "true" ? "[data-action=pause]" : "[data-action=start]").click();
}

document.addEventListener("keydown", (event) => {
  if (event.target.matches("button, input, textarea") || helpDialog.open) return;
  if (["ArrowRight", "PageDown", " "].includes(event.key)) { event.preventDefault(); next(); }
  else if (["ArrowLeft", "PageUp"].includes(event.key)) { event.preventDefault(); previous(); }
  else if (event.key === "Home") show(0);
  else if (event.key === "End") show(slides.length - 1);
  else if (event.key.toLowerCase() === "n") document.body.classList.toggle("show-notes");
  else if (event.key.toLowerCase() === "f") document.querySelector("#fullscreenButton").click();
  else if (event.key.toLowerCase() === "t") toggleVisibleTimer();
  else if (event.key === "?") helpDialog.showModal();
});

window.addEventListener("hashchange", () => show(initialIndex(), false));
document.addEventListener("touchstart", (event) => { touchStartX = event.changedTouches[0].clientX; }, { passive: true });
document.addEventListener("touchend", (event) => {
  const distance = event.changedTouches[0].clientX - touchStartX;
  if (Math.abs(distance) < 60) return;
  if (distance < 0) next(); else previous();
}, { passive: true });

document.querySelectorAll(".round-timer").forEach((widget) => {
  const initialSeconds = Number(widget.dataset.seconds);
  const output = widget.querySelector("output");
  let remaining = initialSeconds;
  let interval = null;

  const render = () => {
    const minutes = String(Math.floor(remaining / 60)).padStart(2, "0");
    const seconds = String(remaining % 60).padStart(2, "0");
    output.textContent = `${minutes}:${seconds}`;
    widget.classList.toggle("expired", remaining === 0);
  };
  const pause = () => {
    clearInterval(interval);
    interval = null;
    widget.dataset.running = "false";
  };
  widget.querySelector("[data-action=start]").addEventListener("click", () => {
    if (interval || remaining === 0) return;
    widget.dataset.running = "true";
    interval = setInterval(() => {
      remaining = Math.max(0, remaining - 1);
      render();
      if (remaining === 0) pause();
    }, 1000);
  });
  widget.querySelector("[data-action=pause]").addEventListener("click", pause);
  widget.querySelector("[data-action=reset]").addEventListener("click", () => {
    pause();
    remaining = initialSeconds;
    render();
  });
  render();
});

const origin = location.protocol.startsWith("http") ? location.origin : "http://<workshop-host>:8001";
document.querySelector("#participantUrl").textContent = `${origin}/`;
show(initialIndex(), false);
