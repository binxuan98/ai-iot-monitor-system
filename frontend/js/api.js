const API_BASE_URL = "http://127.0.0.1:5000/api";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.message || "请求失败");
  }
  return result;
}

async function login(username, password) {
  return apiRequest("/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

async function logout() {
  return apiRequest("/logout", { method: "POST" });
}

async function fetchLatestSensor() {
  return apiRequest("/sensors/latest");
}

async function fetchHistory(limit = 30) {
  return apiRequest(`/sensors/history?limit=${limit}`);
}

async function fetchAlerts(limit = 20) {
  return apiRequest(`/alerts?limit=${limit}`);
}

async function fetchAnalysis() {
  return apiRequest("/analysis");
}

async function fetchLogs(limit = 20) {
  return apiRequest(`/logs?limit=${limit}`);
}

async function refreshData() {
  return apiRequest("/refresh", { method: "POST" });
}
