const loginSection = document.getElementById("loginSection");
const dashboardSection = document.getElementById("dashboardSection");
const loginMessage = document.getElementById("loginMessage");
const userInfo = document.getElementById("userInfo");
const analysisText = document.getElementById("analysisText");

const lineChart = echarts.init(document.getElementById("lineChart"));
const barChart = echarts.init(document.getElementById("barChart"));
const gaugeChart = echarts.init(document.getElementById("gaugeChart"));

function setKpiValue(id, value) {
  document.getElementById(id).textContent = value;
}

function renderAlertsTable(rows) {
  const table = document.getElementById("alertsTable");
  table.innerHTML = rows
    .map(
      (item) =>
        `<tr><td>${item.timestamp}</td><td>${item.level}</td><td>${item.metric}</td><td>${item.value}</td><td>${item.message}</td></tr>`
    )
    .join("");
}

function renderLogsTable(rows) {
  const table = document.getElementById("logsTable");
  table.innerHTML = rows
    .map((item) => `<tr><td>${item.timestamp}</td><td>${item.event_type}</td><td>${item.detail}</td></tr>`)
    .join("");
}

function renderCharts(history, score) {
  const labels = history.map((item) => item.timestamp.slice(11));
  const temperatures = history.map((item) => item.temperature);
  const humidities = history.map((item) => item.humidity);
  const pm25List = history.map((item) => item.pm25);

  lineChart.setOption({
    tooltip: { trigger: "axis" },
    legend: { data: ["温度", "湿度", "PM2.5"] },
    xAxis: { type: "category", data: labels },
    yAxis: { type: "value" },
    series: [
      { name: "温度", type: "line", data: temperatures, smooth: true },
      { name: "湿度", type: "line", data: humidities, smooth: true },
      { name: "PM2.5", type: "line", data: pm25List, smooth: true },
    ],
  });

  const latest = history[history.length - 1] || {};
  barChart.setOption({
    tooltip: {},
    xAxis: { type: "category", data: ["温度", "湿度", "PM2.5", "光照", "CO2"] },
    yAxis: { type: "value" },
    series: [
      {
        type: "bar",
        data: [
          latest.temperature || 0,
          latest.humidity || 0,
          latest.pm25 || 0,
          latest.light || 0,
          latest.co2 || 0,
        ],
      },
    ],
  });

  gaugeChart.setOption({
    series: [
      {
        type: "gauge",
        min: 0,
        max: 100,
        detail: { formatter: "{value} 分" },
        data: [{ value: score, name: "环境评分" }],
      },
    ],
  });
}

async function refreshDashboard() {
  const latestRes = await fetchLatestSensor();
  const historyRes = await fetchHistory(30);
  const alertRes = await fetchAlerts(20);
  const analysisRes = await fetchAnalysis();
  const logsRes = await fetchLogs(20);

  const latest = latestRes.data;
  setKpiValue("temperatureValue", latest.temperature.toFixed(1));
  setKpiValue("humidityValue", latest.humidity.toFixed(1));
  setKpiValue("pm25Value", latest.pm25.toFixed(1));
  setKpiValue("lightValue", latest.light.toFixed(1));
  setKpiValue("co2Value", latest.co2.toFixed(1));
  setKpiValue("scoreValue", analysisRes.data.score);
  analysisText.textContent = `${analysisRes.data.status}（${analysisRes.data.detail}）`;

  renderCharts(historyRes.data, analysisRes.data.score);
  renderAlertsTable(alertRes.data);
  renderLogsTable(logsRes.data);
}

document.getElementById("loginBtn").addEventListener("click", async () => {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  try {
    const result = await login(username, password);
    loginMessage.textContent = "";
    userInfo.textContent = `当前用户：${result.data.username}（${result.data.role}）`;
    loginSection.classList.add("hidden");
    dashboardSection.classList.remove("hidden");
    await refreshDashboard();
  } catch (error) {
    loginMessage.textContent = error.message;
  }
});

document.getElementById("logoutBtn").addEventListener("click", async () => {
  await logout();
  dashboardSection.classList.add("hidden");
  loginSection.classList.remove("hidden");
});

document.getElementById("refreshBtn").addEventListener("click", async () => {
  await refreshData();
  await refreshDashboard();
});

setInterval(async () => {
  if (!dashboardSection.classList.contains("hidden")) {
    await refreshDashboard();
  }
}, 15000);

window.addEventListener("resize", () => {
  lineChart.resize();
  barChart.resize();
  gaugeChart.resize();
});
