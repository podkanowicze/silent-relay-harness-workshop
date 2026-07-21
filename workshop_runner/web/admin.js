const ADMIN_STORAGE_KEY = "contextTelephoneAdminCode";
let adminCode = sessionStorage.getItem(ADMIN_STORAGE_KEY) || "";
let adminState = null;
let pollTimer = null;

const element = (selector) => document.querySelector(selector);

async function adminApi(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Workshop-Admin": adminCode,
      ...(options.headers || {}),
    },
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail || `Request failed (${response.status})`);
  return payload;
}

function setConnected(connected) {
  const badge = element("#adminConnection");
  badge.textContent = connected ? "Connected" : "Not connected";
  badge.classList.toggle("online", connected);
}

function renderAdmin(state) {
  adminState = state;
  element("#adminLogin").hidden = true;
  element("#adminDashboard").hidden = false;
  element("#adminStateBadge").textContent = state.state;
  element("#adminCount").textContent = `${state.registered_count} / ${state.capacity}`;

  const roster = element("#adminRoster");
  roster.replaceChildren();
  state.participants.forEach((participant) => {
    const item = document.createElement("li");
    const slot = document.createElement("span");
    const nickname = document.createElement("strong");
    slot.textContent = `P${participant.slot}`;
    nickname.textContent = participant.nickname;
    item.append(slot, nickname);
    roster.append(item);
  });
  element("#adminEmpty").hidden = state.participants.length > 0;

  const startButton = element("#adminStartButton");
  if (state.state === "lobby") {
    const missing = Math.max(0, state.minimum_participants - state.registered_count);
    element("#adminActionTitle").textContent = "Start when the room is ready";
    element("#adminActionCopy").textContent = missing
      ? `Waiting for ${missing} more participant${missing === 1 ? "" : "s"}. Capacity is ${state.capacity}.`
      : `Start with the current ${state.registered_count}-person roster. One exercise will be assigned per participant.`;
    startButton.disabled = missing > 0 || state.registered_count > state.exercise_count;
    startButton.textContent = `Start with ${state.registered_count}`;
  } else {
    element("#adminActionTitle").textContent = state.state === "complete" ? "Workshop complete" : "Workshop running";
    element("#adminActionCopy").textContent = `${state.active_participant_count} participants are locked into the active roster.`;
    startButton.disabled = true;
    startButton.textContent = "Roster locked";
  }
}

async function loadAdminState() {
  clearTimeout(pollTimer);
  if (!adminCode) return;
  try {
    const state = await adminApi("/api/admin/state");
    setConnected(true);
    renderAdmin(state);
    pollTimer = setTimeout(loadAdminState, 1500);
  } catch (error) {
    setConnected(false);
    sessionStorage.removeItem(ADMIN_STORAGE_KEY);
    adminCode = "";
    element("#adminDashboard").hidden = true;
    element("#adminLogin").hidden = false;
    element("#adminLoginError").textContent = error.message;
  }
}

element("#adminLoginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  adminCode = element("#adminCode").value;
  element("#adminLoginError").textContent = "";
  sessionStorage.setItem(ADMIN_STORAGE_KEY, adminCode);
  await loadAdminState();
});

element("#adminStartButton").addEventListener("click", async () => {
  if (!adminState || adminState.state !== "lobby") return;
  const count = adminState.registered_count;
  if (!window.confirm(`Start the workshop with ${count} participants? The roster will be locked.`)) return;
  const button = element("#adminStartButton");
  button.disabled = true;
  button.textContent = "Starting…";
  element("#adminActionError").textContent = "";
  try {
    renderAdmin(await adminApi("/api/admin/start", { method: "POST", body: "{}" }));
  } catch (error) {
    element("#adminActionError").textContent = error.message;
    await loadAdminState();
  }
});

if (adminCode) loadAdminState();
