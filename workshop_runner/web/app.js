const $ = (selector) => document.querySelector(selector);
const views = ["loginView", "lobbyView", "waitingView", "completeView", "readyView", "reviewView"];

const appState = {
  state: null,
  assignment: null,
  busy: false,
  pollTimer: null,
  clockTimer: null,
  timerExpired: false,
  currentFile: "index.html",
  runClockTimer: null,
  progressTail: null,
};

function requestId() {
  return crypto.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(data.detail || `Request failed (${response.status})`);
    error.status = response.status;
    throw error;
  }
  return data;
}

function showView(id) {
  views.forEach((view) => { $(`#${view}`).hidden = view !== id; });
}

function setOnline(online) {
  const badge = $("#connectionBadge");
  badge.textContent = online ? "Connected" : "Offline";
  badge.classList.toggle("online", online);
}

function setIdentity(participant) {
  const badge = $("#identityBadge");
  const logout = $("#logoutButton");
  if (!participant) {
    badge.hidden = true;
    logout.hidden = true;
    return;
  }
  badge.textContent = `${participant.nickname} · P${participant.slot}`;
  badge.hidden = false;
  logout.hidden = false;
}

function toast(message, error = false) {
  const element = $("#toast");
  element.textContent = message;
  element.classList.toggle("error", error);
  element.hidden = false;
  clearTimeout(element._timer);
  element._timer = setTimeout(() => { element.hidden = true; }, 4200);
}

function terminal(message, className = "") {
  appState.progressTail = null;
  const line = document.createElement("p");
  const time = document.createElement("time");
  const text = document.createElement("span");
  time.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  text.textContent = message;
  if (className) text.className = className;
  line.append(time, text);
  $("#terminalOutput").append(line);
  $("#terminalOutput").scrollTop = $("#terminalOutput").scrollHeight;
}

function renderActivity(activity) {
  const path = activity.path ? ` · ${activity.path}` : "";
  terminal(`${activity.message || activity.type}${path}`, activity.type === "file.changed" ? "path" : "");
}

function terminalStream(text, stream) {
  if (!text) return;
  let tail = appState.progressTail;
  if (!tail || tail.dataset.stream !== stream) {
    const line = document.createElement("p");
    const time = document.createElement("time");
    const output = document.createElement("span");
    time.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    output.className = `stream ${stream === "stderr" ? "failure" : ""}`.trim();
    line.dataset.stream = stream;
    line.append(time, output);
    $("#terminalOutput").append(line);
    appState.progressTail = line;
    tail = line;
  }
  tail.lastElementChild.textContent += text;
  $("#terminalOutput").scrollTop = $("#terminalOutput").scrollHeight;
}

function renderProgressEvent(event) {
  if (["stdout", "stderr"].includes(event.stream)) {
    terminalStream(event.text, event.stream);
  } else if (event.stream === "activity") {
    try {
      const activity = JSON.parse(event.text);
      const file = activity.file ? ` · ${activity.file}` : "";
      const status = activity.status ? ` · ${activity.status}` : "";
      const labels = {
        "session.start": "DCode session started",
        "tool.use": `Calling tool: ${activity.tool || "unknown"}${file}`,
        "tool.result": activity.status === "error"
          ? `Tool attempt failed; DCode may retry: ${activity.tool || "unknown"}${file}`
          : `Tool completed: ${activity.tool || "unknown"}${file}`,
        "tool.error": "DCode tool failed",
        "task.complete": "DCode task completed",
        "session.end": "DCode session ended",
      };
      terminal(labels[activity.event] || activity.event, activity.status === "error" ? "failure" : "");
    } catch (_) {
      terminal(event.text);
    }
  } else {
    appState.progressTail = null;
    terminal(event.text);
  }
}

async function fetchRunProgress(clientRequestId, tracker) {
  const progress = await api(`/api/run-progress/${encodeURIComponent(clientRequestId)}?cursor=${tracker.cursor}`);
  progress.events.forEach(renderProgressEvent);
  if (progress.events.length) tracker.lastEventAt = Date.now();
  tracker.cursor = progress.cursor;
}

async function followRunProgress(clientRequestId, tracker) {
  while (!tracker.done) {
    try {
      await fetchRunProgress(clientRequestId, tracker);
    } catch (_) {
      // The main request reports actionable failures. A transient polling
      // failure should not hide or cancel the agent run.
    }
    const now = Date.now();
    const elapsed = Math.floor((now - tracker.startedAt) / 1000);
    if (
      elapsed >= 15
      && now - tracker.lastEventAt >= 15_000
      && elapsed - tracker.lastHeartbeatAt >= 15
    ) {
      terminal(`Still running (${elapsed}s); Deep Agents Code has not emitted new stdout/stderr.`);
      tracker.lastHeartbeatAt = elapsed;
    }
    if (!tracker.done) await new Promise((resolve) => setTimeout(resolve, 400));
  }
}

function configurePolling(screen) {
  clearTimeout(appState.pollTimer);
  if (["lobby", "waiting"].includes(screen)) {
    appState.pollTimer = setTimeout(loadState, 2000);
  }
}

function renderTimer(deadline) {
  clearInterval(appState.clockTimer);
  const timer = $("#timer");
  const update = () => {
    const remaining = Math.max(0, Math.floor((new Date(deadline).getTime() - Date.now()) / 1000));
    const minutes = String(Math.floor(remaining / 60)).padStart(2, "0");
    const seconds = String(remaining % 60).padStart(2, "0");
    timer.textContent = `${minutes}:${seconds}`;
    timer.classList.toggle("expired", remaining === 0);
    appState.timerExpired = remaining === 0;
    timer.title = remaining === 0
      ? "Suggested time ended. You may continue; the moderator controls the round."
      : "Advisory round timer";
    $("#promptHint").textContent = remaining === 0
      ? "Suggested time ended. You may continue; the moderator decides when to pass."
      : "Give useful context, but request exactly one feature. The task card and previous reply are not injected automatically.";
    $("#runButton").disabled = appState.busy;
  };
  update();
  appState.clockTimer = setInterval(update, 1000);
}

function renderState(state) {
  appState.state = state;
  appState.assignment = state.assignment || null;
  setIdentity(state.participant);
  configurePolling(state.screen);

  if (state.screen === "lobby") {
    showView("lobbyView");
    $("#lobbyCount").textContent = `${state.workshop.registered_count} of ${state.workshop.participant_count} participants have joined. Waiting for the moderator to start.`;
    return;
  }
  if (state.screen === "waiting") {
    showView("waitingView");
    $("#queueMessage").textContent = state.queued_count
      ? `${state.queued_count} application${state.queued_count === 1 ? " is" : "s are"} queued for you.`
      : "No application is queued for you yet.";
    return;
  }
  if (state.screen === "complete") {
    showView("completeView");
    return;
  }
  if (state.screen === "review") {
    renderReview(state.assignment);
    return;
  }
  renderReady(state);
}

function renderReady(state) {
  showView("readyView");
  const assignment = state.assignment;
  $("#stationLabel").textContent = `${assignment.station} · participant ${state.participant.slot}`;
  $("#roundTitle").textContent = `DELTA-${assignment.stage}`;
  $("#deltaLabel").textContent = `DELTA-${assignment.stage}`;
  $("#deltaText").textContent = assignment.delta.text;
  $("#routingBadge").textContent = state.workshop.routing_mode.replace("_", " ");
  $("#agentModeBadge").textContent = "fresh session";
  $("#latestReply").textContent = assignment.latest_agent_reply || "No previous reply. You are starting this application.";
  $("#replyState").textContent = assignment.has_successful_run ? "Current" : "Incoming";
  $("#passButton").disabled = !assignment.has_successful_run || appState.busy;
  $("#interpretationCard").hidden = assignment.stage !== 12;
  $("#specCard").hidden = !assignment.spec0_image_url;
  if (assignment.spec0_image_url) {
    $("#specImage").src = `${assignment.spec0_image_url}?v=${assignment.revision}`;
    $("#specDialogImage").src = $("#specImage").src;
  }
  $("#previewFrame").src = `${assignment.preview_url}?embed=1&v=${assignment.project_revision}`;
  $("#openPreviewLink").href = assignment.preview_url;
  renderTimer(assignment.deadline_at);
}

function appendDefinitionList(list, label, value) {
  const wrapper = document.createElement("div");
  const term = document.createElement("dt");
  const description = document.createElement("dd");
  term.textContent = label;
  description.textContent = value || "—";
  wrapper.append(term, description);
  list.append(wrapper);
}

function renderReview(assignment) {
  showView("reviewView");
  $("#reviewTitle").textContent = assignment.exercise_title;
  $("#reviewSpec").textContent = assignment.spec0;
  const list = $("#reviewInterpretation");
  list.replaceChildren();
  const interpretation = assignment.interpretation || {};
  appendDefinitionList(list, "This application is for", interpretation.application_for);
  appendDefinitionList(list, "Its primary user is", interpretation.primary_user);
  appendDefinitionList(list, "Its final action causes", interpretation.final_action_causes);
  $("#reviewPreviewFrame").src = assignment.preview_url;
  $("#reviewPreviewLink").href = assignment.preview_url;
}

async function loadState() {
  try {
    const state = await api("/api/state");
    setOnline(true);
    renderState(state);
  } catch (error) {
    setOnline(false);
    if (error.status === 401) {
      setOnline(true);
      setIdentity(null);
      showView("loginView");
      $("#nicknameInput").value = localStorage.getItem("workshopNickname") || "";
      return;
    }
    toast(error.message, true);
    configurePolling("waiting");
  }
}

function setBusy(busy) {
  appState.busy = busy;
  clearInterval(appState.runClockTimer);
  $("#runButton").disabled = busy;
  $("#promptInput").disabled = busy;
  $("#passButton").disabled = busy || !appState.assignment?.has_successful_run;
  if (busy) {
    const started = Date.now();
    const update = () => {
      const seconds = Math.floor((Date.now() - started) / 1000);
      $("#runButton").textContent = `Agent running · ${seconds}s`;
    };
    update();
    appState.runClockTimer = setInterval(update, 1000);
  } else {
    $("#runButton").textContent = "Run prompt";
  }
}

$("#loginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const nickname = $("#nicknameInput").value.trim();
  $("#loginError").textContent = "";
  try {
    const result = await api("/api/login", { method: "POST", body: JSON.stringify({ nickname, client: "browser" }) });
    localStorage.setItem("workshopNickname", nickname);
    setOnline(true);
    renderState(result.state);
  } catch (error) {
    $("#loginError").textContent = error.message;
  }
});

$("#logoutButton").addEventListener("click", async () => {
  await api("/api/logout", { method: "POST", body: "{}" }).catch(() => {});
  setIdentity(null);
  showView("loginView");
});

$("#promptForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const prompt = $("#promptInput").value.trim();
  if (!prompt || !appState.assignment) return;
  const clientRequestId = requestId();
  const tracker = {
    cursor: 0,
    done: false,
    startedAt: Date.now(),
    lastEventAt: Date.now(),
    lastHeartbeatAt: 0,
  };
  setBusy(true);
  appState.progressTail = null;
  terminal("Opening a completely fresh agent session…");
  terminal("Mounting only index.html, styles.css, and app.js…");
  const progressFollower = followRunProgress(clientRequestId, tracker);
  try {
    const result = await api("/api/run", {
      method: "POST",
      body: JSON.stringify({
        assignment_id: appState.assignment.id,
        prompt,
        client_request_id: clientRequestId,
      }),
    });
    result.activities.forEach(renderActivity);
    terminal(`Committed ${result.changed_files.length} changed file(s).`, "success");
    $("#promptInput").value = "";
    await loadState();
    toast("Agent run committed. You can prompt again or pass onward.");
  } catch (error) {
    terminal(error.message, "failure");
    toast(error.message, true);
  } finally {
    await fetchRunProgress(clientRequestId, tracker).catch(() => {});
    tracker.done = true;
    await progressFollower;
    setBusy(false);
  }
});

$("#passButton").addEventListener("click", async () => {
  if (!appState.assignment || appState.busy) return;
  let interpretation = null;
  if (appState.assignment.stage === 12) {
    interpretation = {
      application_for: $("#applicationFor").value.trim(),
      primary_user: $("#primaryUser").value.trim(),
      final_action_causes: $("#finalAction").value.trim(),
    };
    if (Object.values(interpretation).some((value) => !value)) {
      toast("Complete all three interpretation fields before passing.", true);
      return;
    }
  }
  setBusy(true);
  try {
    const state = await api("/api/pass", {
      method: "POST",
      body: JSON.stringify({
        assignment_id: appState.assignment.id,
        request_key: requestId(),
        interpretation,
      }),
    });
    terminal("Handoff committed.", "success");
    renderState(state);
  } catch (error) {
    toast(error.message, true);
  } finally {
    setBusy(false);
  }
});

$("#completeReviewButton").addEventListener("click", async () => {
  if (!appState.assignment) return;
  try {
    const state = await api("/api/review", {
      method: "POST",
      body: JSON.stringify({ assignment_id: appState.assignment.id, notes: $("#reviewNotes").value }),
    });
    renderState(state);
  } catch (error) {
    toast(error.message, true);
  }
});

$("#refreshPreviewButton").addEventListener("click", () => {
  if (appState.assignment) $("#previewFrame").src = `${appState.assignment.preview_url}?v=${Date.now()}`;
});

$("#clearTerminalButton").addEventListener("click", () => {
  appState.progressTail = null;
  $("#terminalOutput").replaceChildren();
});

async function loadCode(filename) {
  if (!appState.assignment) return;
  appState.currentFile = filename;
  document.querySelectorAll(".code-tabs button").forEach((button) => button.classList.toggle("active", button.dataset.file === filename));
  $("#codeOutput").textContent = "Loading…";
  try {
    const response = await fetch(`/api/files/${appState.assignment.id}/${filename}`, { credentials: "same-origin" });
    if (!response.ok) throw new Error("Could not load file");
    $("#codeOutput").textContent = await response.text() || "(empty file)";
  } catch (error) {
    $("#codeOutput").textContent = error.message;
  }
}

$("#viewCodeButton").addEventListener("click", () => { $("#codeDialog").showModal(); loadCode("index.html"); });
$("#closeCodeButton").addEventListener("click", () => $("#codeDialog").close());
document.querySelectorAll(".code-tabs button").forEach((button) => button.addEventListener("click", () => loadCode(button.dataset.file)));
$("#specExpandButton").addEventListener("click", () => $("#specDialog").showModal());
$("#closeSpecButton").addEventListener("click", () => $("#specDialog").close());

window.addEventListener("online", () => { setOnline(true); loadState(); });
window.addEventListener("offline", () => setOnline(false));

$("#nicknameInput").value = localStorage.getItem("workshopNickname") || "";
loadState();
