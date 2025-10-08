const API_BASE = "http://127.0.0.1:8000";

const els = {
  tabs: document.getElementById("tabs"),
  tabTasks: document.getElementById("tab-tasks"),
  viewAuth: document.getElementById("view-auth"),
  viewTasks: document.getElementById("view-tasks"),
  backToAuth: document.getElementById("back-to-auth"),
  hello: document.getElementById("hello"),

  regForm: document.getElementById("register-form"),
  regUser: document.getElementById("reg-username"),
  regEmail: document.getElementById("reg-email"),
  regPass: document.getElementById("reg-password"),
  regMsg: document.getElementById("register-msg"),

  loginForm: document.getElementById("login-form"),
  loginUser: document.getElementById("login-username"),
  loginPass: document.getElementById("login-password"),
  loginMsg: document.getElementById("login-msg"),

  token: document.getElementById("token"),

  taskForm: document.getElementById("task-form"),
  userId: document.getElementById("user-id"),
  taskTitle: document.getElementById("task-title"),
  taskDesc: document.getElementById("task-desc"),
  loadTasks: document.getElementById("load-tasks"),
  tasks: document.getElementById("tasks"),
};

function setUserId(uid) {
  if (!uid && uid !== 0) return;
  localStorage.setItem("lt_user_id", String(uid));
  els.userId.value = String(uid);
}

function initUserIdFromStorage() {
  const saved = localStorage.getItem("lt_user_id");
  if (saved) {
    els.userId.value = saved;
  }
}

function setMsg(el, text, error = false) {
  el.textContent = text || "";
  el.classList.toggle("error", !!error);
}

function getAuthHeaders() {
  const token = els.token.value.trim();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

function switchTab(name) {
  const buttons = els.tabs.querySelectorAll(".tab");
  buttons.forEach((b) => b.classList.toggle("active", b.dataset.tab === name));
  if (name === "auth") {
    els.viewAuth.classList.remove("hidden");
    els.viewTasks.classList.add("hidden");
  } else {
    els.viewAuth.classList.add("hidden");
    els.viewTasks.classList.remove("hidden");
  }
}

function enableTasksTab(enabled) {
  els.tabTasks.disabled = !enabled;
}

function afterLoginUi() {
  enableTasksTab(true);
  switchTab("tasks");
  const uid = localStorage.getItem("lt_user_id");
  els.hello.textContent = uid ? `Пользователь #${uid}` : "";
  loadTasks();
}

async function register(evt) {
  evt.preventDefault();
  setMsg(els.regMsg, "");
  try {
    const body = {
      username: els.regUser.value.trim(),
      password: els.regPass.value,
      email: els.regEmail.value.trim(),
    };
    const res = await fetch(`${API_BASE}/users/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    setUserId(data.id);
    setMsg(els.regMsg, `OK. ID=${data.id}`);
  } catch (e) {
    setMsg(els.regMsg, e.message || "Ошибка регистрации", true);
  }
}

async function login(evt) {
  evt.preventDefault();
  setMsg(els.loginMsg, "");
  try {
    const body = {
      username: els.loginUser.value.trim(),
      password: els.loginPass.value,
    };
    const res = await fetch(`${API_BASE}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    els.token.value = data.access_token;
    try {
      const payload = JSON.parse(atob(data.access_token.split(".")[1]));
      const sub = payload && payload.sub ? Number(payload.sub) : null;
      if (sub) setUserId(sub);
    } catch (_) {
      // ignore jwt parse
    }
    setMsg(els.loginMsg, "Токен получен");
    afterLoginUi();
  } catch (e) {
    setMsg(els.loginMsg, e.message || "Ошибка логина", true);
  }
}

function logout() {
  els.token.value = "";
  // не очищаем user_id, чтобы удобнее тестировать
}

async function createTask(evt) {
  evt.preventDefault();
  try {
    const uid = Number(els.userId.value);
    const body = {
      title: els.taskTitle.value.trim(),
      description: els.taskDesc.value.trim() || null,
    };
    const res = await fetch(`${API_BASE}/tasks/user/${uid}`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...getAuthHeaders() },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(await res.text());
    await loadTasks();
    els.taskTitle.value = "";
    els.taskDesc.value = "";
  } catch (e) {
    alert(e.message || "Ошибка создания задачи");
  }
}

function taskItem(task, userId) {
  const li = document.createElement("li");
  const title = document.createElement("input");
  title.type = "text";
  title.value = task.title;
  const desc = document.createElement("input");
  desc.type = "text";
  desc.value = task.description || "";
  const save = document.createElement("button");
  save.textContent = "Сохранить";
  const del = document.createElement("button");
  del.textContent = "Удалить";

  save.onclick = async () => {
    try {
      const res = await fetch(`${API_BASE}/tasks/user/${userId}/task/${task.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json", ...getAuthHeaders() },
        body: JSON.stringify({ title: title.value, description: desc.value || null }),
      });
      if (!res.ok) throw new Error(await res.text());
      await loadTasks();
    } catch (e) {
      alert(e.message || "Ошибка обновления");
    }
  };

  del.onclick = async () => {
    try {
      const res = await fetch(`${API_BASE}/tasks/user/${userId}/task/${task.id}`, {
        method: "DELETE",
        headers: { ...getAuthHeaders() },
      });
      if (!res.ok) throw new Error(await res.text());
      await loadTasks();
    } catch (e) {
      alert(e.message || "Ошибка удаления");
    }
  };

  li.append(title, desc, save, del);
  return li;
}

async function loadTasks() {
  els.tasks.innerHTML = "";
  try {
    const uid = Number(els.userId.value);
    const res = await fetch(`${API_BASE}/tasks/user/${uid}`, {
      headers: { ...getAuthHeaders() },
    });
    if (!res.ok) throw new Error(await res.text());
    const items = await res.json();
    items.forEach((t) => els.tasks.appendChild(taskItem(t, uid)));
  } catch (e) {
    alert(e.message || "Ошибка загрузки задач");
  }
}

els.regForm.addEventListener("submit", register);
els.loginForm.addEventListener("submit", login);
els.taskForm.addEventListener("submit", createTask);
els.loadTasks.addEventListener("click", loadTasks);
els.tabs.addEventListener("click", (e) => {
  if (e.target.matches(".tab") && !e.target.disabled) {
    switchTab(e.target.dataset.tab);
  }
});
els.backToAuth.addEventListener("click", () => {
  els.token.value = "";
  enableTasksTab(false);
  switchTab("auth");
});

initUserIdFromStorage();
enableTasksTab(!!els.token.value);
