const categoryLabels = {
  history: "历史", museum: "博物馆", architecture: "建筑", photography: "摄影",
  wildlife: "动物", family: "亲子", nature: "自然", mountain: "山野",
  park: "公园", garden: "园林", walking: "漫步", "world-heritage": "世界遗产"
};

const warningLabels = {
  "Long walking distances": "步行距离较长",
  "Limited shade": "遮阴较少",
  "High holiday crowds": "节假日人流大",
  "Large site": "园区范围较大",
  "Limited shade in some areas": "部分区域遮阴较少",
  "Outdoor heat": "注意户外高温",
  "Animals may be less active later in hot weather": "炎热天气下动物午后可能不活跃",
  "Can be crowded during public holidays": "节假日可能拥挤",
  "Altitude": "注意海拔适应",
  "Uneven and slippery stone lanes": "石板路不平且雨天湿滑",
  "Nighttime noise in busy areas": "繁忙区域夜间可能嘈杂",
  "High altitude": "高海拔",
  "Rapid weather changes": "天气变化快",
  "Ropeways may be suspended": "索道可能停运",
  "Not suitable for every health condition": "部分健康状况不适合前往"
};

const elements = {
  status: document.querySelector("#service-status"),
  searchForm: document.querySelector("#search-form"),
  planForm: document.querySelector("#plan-form"),
  searchCity: document.querySelector("#search-city"),
  planCity: document.querySelector("#plan-city"),
  results: document.querySelector("#results"),
  resultsTitle: document.querySelector("#results-title"),
  resultCount: document.querySelector("#result-count"),
  shortcuts: document.querySelector("#city-shortcut-list")
};

function escapeHtml(value = "") {
  return String(value).replace(/[&<>'"]/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
  })[character]);
}

async function fetchJson(url) {
  const response = await fetch(url);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `请求失败（${response.status}）`);
  return data;
}

function setLoading(title = "正在查找合适的地点") {
  elements.resultsTitle.textContent = title;
  elements.resultCount.textContent = "查询中";
  elements.results.setAttribute("aria-busy", "true");
  elements.results.innerHTML = '<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>';
}

function showError(error) {
  elements.resultsTitle.textContent = "暂时无法完成查询";
  elements.resultCount.textContent = "错误";
  elements.results.setAttribute("aria-busy", "false");
  elements.results.innerHTML = `<div class="error-state"><b>连接没有成功</b><p>${escapeHtml(error.message)}。请确认终端中的服务仍在运行。</p></div>`;
}

function ticketText(ticket) {
  if (ticket?.price_cny === 0) return "免费";
  if (typeof ticket?.price_cny === "number") return `¥${ticket.price_cny}`;
  return "价格需核验";
}

function durationText(hours = []) {
  if (hours.length !== 2) return "时长未知";
  return hours[0] === hours[1] ? `${hours[0]} 小时` : `${hours[0]}–${hours[1]} 小时`;
}

function spotCard(spot, index) {
  const verified = Boolean(spot.last_verified);
  const tags = (spot.categories || []).slice(0, 4).map(tag => `<span>${escapeHtml(categoryLabels[tag] || tag)}</span>`).join("");
  const warnings = (spot.warnings || []).slice(0, 2).map(item => warningLabels[item] || item).join(" · ");
  const source = spot.sources?.[0];
  return `
    <article class="spot-card" style="animation-delay:${index * 45}ms">
      <div class="spot-topline">
        <span class="city-label">${escapeHtml(spot.city?.zh)} · ${escapeHtml(spot.neighborhood)}</span>
        <span class="freshness ${verified ? "" : "unverified"}">${verified ? `已核验 ${escapeHtml(spot.last_verified)}` : "等待核验"}</span>
      </div>
      <h4>${escapeHtml(spot.name?.zh)}</h4>
      <p class="spot-en">${escapeHtml(spot.name?.en)}</p>
      <p class="spot-summary">${escapeHtml(spot.summary?.zh || spot.summary?.en)}</p>
      <div class="spot-tags">${tags}</div>
      <div class="spot-facts">
        <span>建议时长<strong>${escapeHtml(durationText(spot.duration_hours))}</strong></span>
        <span>票务信息<strong>${escapeHtml(ticketText(spot.ticket))}</strong></span>
      </div>
      ${warnings ? `<p class="warning-line">注意：${escapeHtml(warnings)}</p>` : ""}
      <div class="spot-footer">
        <span>${spot.booking?.required === true ? "通常需要预约" : "预约规则请复核"}</span>
        ${source ? `<a href="${escapeHtml(source)}" target="_blank" rel="noreferrer">查看来源 ↗</a>` : ""}
      </div>
    </article>`;
}

function renderSpots(data, context = "全部示例地点") {
  const spots = data.results || [];
  elements.resultsTitle.textContent = context;
  elements.resultCount.textContent = `${spots.length} 个结果`;
  elements.results.setAttribute("aria-busy", "false");
  if (!spots.length) {
    elements.results.innerHTML = '<div class="empty-state"><b>没有找到符合条件的地点</b><p>试试减少筛选条件，或者换一个月份和兴趣。</p></div>';
    return;
  }
  elements.results.innerHTML = spots.map(spotCard).join("");
}

async function searchSpots(params = new URLSearchParams(), context = "全部示例地点") {
  setLoading();
  try {
    const data = await fetchJson(`/search?${params.toString()}`);
    renderSpots(data, context);
  } catch (error) {
    showError(error);
  }
}

function renderPlan(plan) {
  const days = plan.days || [];
  const dayCards = days.map(day => {
    const stops = day.spots.length
      ? day.spots.map((spot, index) => `<div class="day-stop"><span>${String(index + 1).padStart(2, "0")}</span><div><b>${escapeHtml(spot.name?.zh)}</b><small>${escapeHtml(spot.neighborhood)} · 约 ${escapeHtml(spot.duration_hours)} 小时</small></div></div>`).join("")
      : '<div class="day-stop"><span>—</span><div><b>自由安排</b><small>当前样例数据没有更多地点</small></div></div>';
    return `<article class="day-card"><div class="day-number"><strong>第 ${day.day} 天</strong><span>预计 ${day.estimated_hours} 小时</span></div>${stops}</article>`;
  }).join("");

  elements.resultsTitle.textContent = `${plan.city?.zh} · ${days.length} 日行程草案`;
  elements.resultCount.textContent = `${days.length} 天`;
  elements.results.setAttribute("aria-busy", "false");
  elements.results.innerHTML = `
    <div class="plan-result">
      <div class="plan-summary"><div><h4>${escapeHtml(plan.city?.zh)}旅行草案</h4><p>${escapeHtml(plan.city?.en)} · RULE-BASED ITINERARY</p></div><span class="stamp">行程</span></div>
      <div class="plan-days">${dayCards}</div>
      <p class="plan-caveat">这是基于地点时长与兴趣排序生成的草案，不是实时导航。出发前请核验开放时间、预约、交通和天气。</p>
    </div>`;
}

async function generatePlan(city, days = 2, interests = []) {
  setLoading("正在整理每日行程");
  const params = new URLSearchParams({ city, days: String(days) });
  if (interests.length) params.set("interests", interests.join(","));
  try {
    renderPlan(await fetchJson(`/plan?${params.toString()}`));
  } catch (error) {
    showError(error);
  }
}

function activateTab(name) {
  document.querySelectorAll(".tab").forEach(tab => {
    const active = tab.dataset.tab === name;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-selected", String(active));
  });
  document.querySelectorAll(".panel").forEach(panel => {
    const active = panel.id === `${name}-panel`;
    panel.classList.toggle("is-active", active);
    panel.hidden = !active;
  });
}

async function initialize() {
  try {
    const [health, cities] = await Promise.all([fetchJson("/health"), fetchJson("/cities")]);
    if (health.status !== "ok") throw new Error("服务状态异常");
    elements.status.classList.add("is-online");
    elements.status.innerHTML = "<i></i> 本地数据已连接";
    document.querySelector("#city-count").textContent = cities.length;

    cities.forEach(city => {
      const label = `${city.name.zh} · ${city.name.en}`;
      elements.searchCity.add(new Option(label, city.id));
      elements.planCity.add(new Option(label, city.id));
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.city = city.id;
      button.textContent = city.name.zh;
      elements.shortcuts.append(button);
    });
    setLoading();
    const initialData = await fetchJson("/search");
    document.querySelector("#spot-count").textContent = initialData.count;
    renderSpots(initialData);
  } catch (error) {
    elements.status.classList.add("is-offline");
    elements.status.innerHTML = "<i></i> 本地服务未连接";
    showError(error);
  }
}

document.querySelectorAll(".tab").forEach(tab => tab.addEventListener("click", () => activateTab(tab.dataset.tab)));

elements.searchForm.addEventListener("submit", event => {
  event.preventDefault();
  const form = new FormData(elements.searchForm);
  const params = new URLSearchParams();
  [["q", form.get("keyword")], ["city", form.get("city")], ["category", form.get("category")], ["month", form.get("month")], ["max_hours", form.get("max_hours")]].forEach(([key, value]) => {
    if (value) params.set(key, value);
  });
  if (form.get("free")) params.set("free", "true");
  const cityLabel = elements.searchCity.selectedOptions[0]?.text.split(" · ")[0];
  searchSpots(params, cityLabel && form.get("city") ? `${cityLabel} · 查询结果` : "旅行地点查询结果");
});

document.querySelector("#reset-search").addEventListener("click", () => {
  elements.searchForm.reset();
  searchSpots();
});

elements.planForm.addEventListener("submit", event => {
  event.preventDefault();
  const form = new FormData(elements.planForm);
  generatePlan(form.get("city"), Number(form.get("days")), form.getAll("interests"));
});

elements.shortcuts.addEventListener("click", event => {
  const button = event.target.closest("button[data-city]");
  if (!button) return;
  activateTab("search");
  elements.searchCity.value = button.dataset.city;
  const params = new URLSearchParams({ city: button.dataset.city });
  searchSpots(params, `${button.textContent} · 全部示例地点`);
});

document.querySelectorAll(".inspiration").forEach(button => button.addEventListener("click", () => {
  document.querySelector("#query-studio").scrollIntoView({ behavior: "smooth" });
  if (button.dataset.mode === "plan") {
    activateTab("plan");
    elements.planCity.value = button.dataset.city.toLowerCase();
    document.querySelector('#plan-form input[value="mountain"]').checked = true;
    document.querySelector('#plan-form input[value="photography"]').checked = true;
    generatePlan(button.dataset.city, 2, ["mountain", "photography"]);
  } else {
    activateTab("search");
    elements.searchCity.value = button.dataset.city.toLowerCase();
    document.querySelector("#category").value = button.dataset.category;
    searchSpots(new URLSearchParams({ city: button.dataset.city, category: button.dataset.category }), "旅行灵感查询结果");
  }
}));

initialize();
