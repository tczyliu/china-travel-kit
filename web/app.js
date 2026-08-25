const categoryLabels = {
  history: "历史", museum: "博物馆", architecture: "建筑", photography: "摄影",
  wildlife: "动物", family: "亲子", nature: "自然", mountain: "山野",
  park: "公园", garden: "园林", walking: "漫步", "world-heritage": "世界遗产",
  food: "美食", nightlife: "夜游", "local-life": "社区生活", literature: "文学",
  archaeology: "考古", teahouse: "茶馆", religion: "宗教文化", culture: "文化",
  art: "艺术", shopping: "购物", "industrial-heritage": "工业遗产", music: "音乐",
  engineering: "工程"
};

const categoryLabelsEn = {
  history: "History", museum: "Museum", architecture: "Architecture", photography: "Photography",
  wildlife: "Wildlife", family: "Family", nature: "Nature", mountain: "Mountain",
  park: "Park", garden: "Garden", walking: "Walking", "world-heritage": "World Heritage",
  food: "Food", nightlife: "Nightlife", "local-life": "Local Life", literature: "Literature",
  archaeology: "Archaeology", teahouse: "Teahouse", religion: "Religion", culture: "Culture",
  art: "Art", shopping: "Shopping", "industrial-heritage": "Industrial Heritage", music: "Music",
  engineering: "Engineering"
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
  "Not suitable for every health condition": "部分健康状况不适合前往",
  "Closed days and hours may change": "闭馆日和开放时间可能变化",
  "Respect residents and keep noise low in residential lanes": "进入居民街巷请降低音量并尊重社区生活",
  "Slippery paths after rain": "雨后道路可能湿滑",
  "Temporary closure reported": "官方页面提示阶段性闭馆",
  "Verify reopening before travel": "出发前必须核验是否恢复开放",
  "Respect active worship and dress expectations": "请尊重宗教活动与着装要求",
  "Event access can change": "活动期间通行安排可能变化",
  "Steep paths": "部分路线坡陡或台阶多",
  "Long transfer from city center": "距离市中心较远",
  "Theme park queues": "主题园区可能长时间排队",
  "Multiple venues and paid experiences": "包含多个独立场馆或付费项目",
  "Insects in warm months": "温暖月份注意蚊虫",
  "Weather-dependent boats": "船班受天气影响",
  "Strong sun exposure": "日照较强"
};

const uiTranslations = {
  "跳到查询工具": "Skip to trip planner", "规划旅程": "Plan a trip", "数据承诺": "Data promise", "语言": "Language",
  "选择界面语言": "Choose interface language", "把中国旅行，": "Travel China with", "查清楚再出发。": "clarity and confidence.",
  "为第一次来中国的自由行游客整理城市、景点、路线与出发准备。每条信息保留中文地名、官方来源和核验状态。": "Cities, sights, routes and practical preparation for first-time independent visitors to China. Every record keeps its Chinese name, source and verification status.",
  "开始规划旅程": "Start planning", "正在连接本地数据": "Connecting to local data", "双语": "Bilingual", "中文地名 + English": "Chinese names + English",
  "可追溯": "Traceable", "保留官方来源": "Official sources retained", "不过度承诺": "No false certainty", "动态信息明确待核验": "Live details clearly marked for recheck",
  "项目特点": "Project strengths", "中国旅行色彩主题": "China travel colour themes", "宫墙红": "Palace red", "湖山青": "Landscape green", "琉璃蓝": "Glazed blue", "银杏金": "Ginkgo gold",
  "一张会回答问题的中国旅行图鉴": "A China travel atlas that answers questions", "快速旅行灵感": "Quick trip inspiration", "开源": "OPEN",
  "从一个旅行愿望开始": "Start with a travel wish", "在丽江慢慢走两天": "Two slow days in Lijiang", "古城 · 山野 · 摄影": "Old town · Mountains · Photography",
  "带家人去成都看熊猫": "See pandas with the family in Chengdu", "动物 · 亲子 · 轻松": "Wildlife · Family · Easy pace", "读懂北京的历史建筑": "Explore Beijing's historic architecture", "博物馆 · 建筑 · 摄影": "Museums · Architecture · Photography",
  "个首批城市": "launch cities", "个严谨地点": "curated places", "运行时依赖": "runtime dependencies",
  "从需求到一份可执行的草案": "From your needs to an actionable draft", "当前覆盖 8 城、56 个地点，优先收录一线与重点旅游城市的 5A/4A 景区。价格、预约和实时交通请在出发前再次核验。": "Currently covering 8 cities and 56 places, with priority given to major cities and 5A/4A attractions. Recheck prices, reservations and live transport before departure.",
  "从需求到旅行方案的步骤": "Steps from needs to a trip plan", "告诉我们谁来": "Tell us who's travelling", "选择兴趣与节奏": "Choose interests and pace", "获得可核验方案": "Get a verifiable plan",
  "查询方式": "Search modes", "6 项功能全部可用": "All 6 features are ready", "点击下方任意入口切换功能，查询结果会显示在同一结果区": "Choose any feature below; its output appears in the shared results area", "可用": "READY", "智能匹配方案": "Smart trip match", "查找旅行地点": "Find places", "查询住宿区域": "Find areas to stay", "生成行程草案": "Build itinerary", "出发准备建议": "Trip preparation", "紧急求助信息": "Emergency help",
  "从哪个国家出发": "Country of departure", "几个人": "Travellers", "什么时候来": "Arrival date", "什么时候离开": "Departure date", "没有确定日期时玩几天": "Trip length if dates are flexible", "想去的城市": "Preferred city", "让系统自动匹配": "Let the system match",
  "明确想去的地方": "Must-see places", "旅行节奏": "Travel pace", "轻松 · 每天约 4 小时": "Relaxed · about 4 hours/day", "均衡 · 每天约 6 小时": "Balanced · about 6 hours/day", "充实 · 每天约 8 小时": "Full · about 8 hours/day",
  "预算偏好": "Budget preference", "尽量省钱": "Budget", "适中": "Moderate", "舒适优先": "Comfort first", "步行与行动需求": "Walking and mobility", "普通步行强度": "Standard walking", "需要减少步行或台阶": "Reduce walking or stairs",
  "同行人员": "Travel party", "有儿童同行": "Travelling with children", "想体验什么": "Interests", "历史": "History", "美食": "Food", "动物": "Wildlife", "自然": "Nature", "摄影": "Photography", "文化": "Culture", "购物": "Shopping", "本地生活": "Local life",
  "还有什么具体要求": "Other requirements", "自动查询并生成方案": "Search and build my plan", "想看什么": "What would you like to see?", "目的城市": "Destination city", "全部城市": "All cities", "旅行兴趣": "Travel interest", "全部兴趣": "All interests",
  "历史文化": "History & culture", "博物馆": "Museums", "建筑": "Architecture", "动物生态": "Wildlife", "自然风光": "Nature", "山地": "Mountains", "亲子": "Family", "公园": "Parks", "园林": "Gardens", "城市漫步": "City walks", "世界遗产": "World heritage", "夜游": "Nightlife", "文学": "Literature", "考古": "Archaeology", "茶馆": "Teahouses", "宗教文化": "Religion", "艺术": "Art", "工业遗产": "Industrial heritage", "音乐": "Music", "工程": "Engineering",
  "出行月份": "Travel month", "不限月份": "Any month", "最多游玩时间": "Maximum visit time", "不限时长": "Any duration", "半天内": "Within half a day", "一天内": "Within one day", "只看免费地点": "Free places only", "清空": "Reset", "查询地点": "Search places",
  "区域关键词": "Area keyword", "省份": "Province", "查询区域": "Search areas", "选择城市": "Choose city", "请选择城市": "Select a city", "旅行天数": "Trip length", "偏好的旅行主题": "Preferred themes", "山野": "Mountains", "生成行程": "Build itinerary", "请选择月份": "Select a month", "查看准备建议": "View preparation", "所在城市": "Current city", "查看求助信息": "View emergency help",
  "城市快捷入口": "Quick city links", "快速查看": "Quick view", "正在载入旅行地点": "Loading travel places", "不知道，就明确说不知道。": "If we don't know, we say so.",
  "旅行规则变化很快。项目宁可显示“需要核验”，也不会用一个看似完整、实际过时的数字误导你。": "Travel rules change quickly. We would rather mark an item for verification than mislead you with a complete-looking but outdated number.",
  "来源可追溯": "Traceable sources", "地点卡片保留官方或权威来源，方便出发前复核。": "Place cards retain official or authoritative sources for pre-trip checks.", "核验日期可见": "Verification dates", "未核验和超过期限的数据不会藏在结果里。": "Unverified and stale data is never hidden.", "路线只是草案": "Routes are drafts", "不虚构实时路况、预约余量或精确通勤分钟数。": "We do not invent live traffic, reservation availability or exact transfer times.",
  "开源的中国入境旅行知识工具 · 当前覆盖 8 城 56 个地点": "Open-source China inbound travel toolkit · 8 cities and 56 places", "查看源代码": "View source", "查看源代码 ↗": "View source ↗",
  "例如：Singapore": "e.g. Singapore", "例如：熊猫基地、玉龙雪山；多个地点用逗号分隔": "e.g. Panda Base, Jade Dragon Snow Mountain; separate places with commas", "例如：第一次来中国，想看熊猫、吃当地小吃，不想走太多路": "e.g. First visit to China; pandas and local food; less walking", "例如：古城、熊猫、博物馆": "e.g. old town, pandas, museums", "例如：东城、古城、交通方便": "e.g. Dongcheng, old town, easy transport", "例如：四川": "e.g. Sichuan"
};

const state = {
  language: (() => {
    try { return localStorage.getItem("china-travel-language") === "en" ? "en" : "zh"; }
    catch { return "zh"; }
  })()
};
const API_BASE = window.location.protocol === "file:" ? "http://127.0.0.1:8766" : "";

function copy(zh, en) { return state.language === "en" ? en : zh; }

function translateValue(value) {
  if (state.language !== "en") return value;
  if (uiTranslations[value]) return uiTranslations[value];
  const day = value.match(/^(\d+) 天$/); if (day) return `${day[1]} day${day[1] === "1" ? "" : "s"}`;
  const month = value.match(/^(\d+) 月$/); if (month) return `Month ${month[1]}`;
  const hour = value.match(/^(\d+) 小时内$/); if (hour) return `Within ${hour[1]} hours`;
  return value;
}

function applyInterfaceLanguage() {
  document.documentElement.lang = state.language === "en" ? "en" : "zh-CN";
  document.body.dataset.language = state.language;
  document.querySelectorAll("[data-language]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.language === state.language)));
  if (state.language !== "en") return;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walker.nextNode())) {
    const value = node.nodeValue.trim();
    const translated = translateValue(value);
    if (translated !== value) node.nodeValue = node.nodeValue.replace(value, translated);
  }
  document.querySelectorAll("[placeholder],[aria-label]").forEach(element => {
    ["placeholder", "aria-label"].forEach(attribute => {
      if (element.hasAttribute(attribute)) element.setAttribute(attribute, translateValue(element.getAttribute(attribute)));
    });
  });
}

const elements = {
  status: document.querySelector("#service-status"),
  recommendForm: document.querySelector("#recommend-form"),
  searchForm: document.querySelector("#search-form"),
  areasForm: document.querySelector("#areas-form"),
  planForm: document.querySelector("#plan-form"),
  prepareForm: document.querySelector("#prepare-form"),
  emergencyForm: document.querySelector("#emergency-form"),
  searchCity: document.querySelector("#search-city"),
  recommendCity: document.querySelector("#recommend-city"),
  planCity: document.querySelector("#plan-city"),
  areasCity: document.querySelector("#areas-city"),
  prepareCity: document.querySelector("#prepare-city"),
  emergencyCity: document.querySelector("#emergency-city"),
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
  const response = await fetch(`${API_BASE}${url}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || copy(`请求失败（${response.status}）`, `Request failed (${response.status})`));
  return data;
}

function setLoading(title = copy("正在查找合适的地点", "Finding suitable places")) {
  elements.resultsTitle.textContent = title;
  elements.resultCount.textContent = copy("查询中", "Searching");
  elements.results.setAttribute("aria-busy", "true");
  elements.results.innerHTML = '<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>';
}

function showError(error) {
  const disconnected = error instanceof TypeError || /failed to fetch/i.test(error.message || "");
  if (window.location.protocol === "file:" && disconnected) {
    elements.status.classList.remove("is-online");
    elements.status.classList.add("is-offline");
    elements.status.innerHTML = `<i></i> ${copy("本地服务未连接", "Local service disconnected")}`;
    showPreviewHelp();
    return;
  }
  if (disconnected) {
    elements.status.classList.remove("is-online");
    elements.status.classList.add("is-offline");
    elements.status.innerHTML = `<i></i> ${copy("本地服务已断开", "Local service disconnected")}`;
  }
  elements.resultsTitle.textContent = copy("暂时无法完成查询", "Unable to complete the search");
  elements.resultCount.textContent = copy("错误", "Error");
  elements.results.setAttribute("aria-busy", "false");
  elements.results.innerHTML = `<div class="error-state"><b>${disconnected ? copy("本地查询服务已经停止", "The local search service has stopped") : copy("输入条件需要调整", "The request needs adjustment")}</b><p>${escapeHtml(error.message)}. ${disconnected ? copy("请双击项目中的“启动华行志.command”，然后点击下方按钮。", "Double-click “启动华行志.command” in the project, then use the button below.") : copy("请检查日期、城市和其他选项。", "Check the dates, city, and other options.")}</p>${disconnected ? `<button class="button button-primary" id="retry-service" type="button">${copy("重新连接查询服务", "Reconnect search service")} →</button>` : ""}</div>`;
  document.querySelector("#retry-service")?.addEventListener("click", () => window.location.reload());
}

function showPreviewHelp({ scroll = true } = {}) {
  elements.resultsTitle.textContent = copy("当前是界面预览模式", "Interface preview mode");
  elements.resultCount.textContent = copy("尚未启动", "Not started");
  elements.results.setAttribute("aria-busy", "false");
  elements.results.innerHTML = `
    <div class="preview-help">
      <span class="preview-help-icon" aria-hidden="true">启</span>
      <div>
        <p class="info-kicker">${copy("需要启动本地查询服务", "LOCAL SERVICE REQUIRED")}</p>
        <h4>${copy("界面已经正常，查询服务还没有启动", "The interface is ready; the search service is not running")}</h4>
        <ol>
          <li>${copy("打开项目文件夹", "Open the project folder")}</li>
          <li>${copy("双击“启动华行志.command”", "Double-click “启动华行志.command”")}</li>
          <li>${copy("等待查询版网页自动打开", "Wait for the searchable site to open automatically")}</li>
        </ol>
      </div>
      <a class="button button-primary" href="http://127.0.0.1:8766/">${copy("服务启动后打开查询版", "Open searchable site after launch")} <span aria-hidden="true">↗</span></a>
    </div>`;
  if (scroll) elements.results.scrollIntoView({ behavior: "smooth", block: "center" });
}

function ticketText(ticket) {
  if (ticket?.price_cny === 0) return copy("免费", "Free");
  if (typeof ticket?.price_cny === "number") return `¥${ticket.price_cny}`;
  return copy("价格需核验", "Verify price");
}

function durationText(hours = []) {
  if (hours.length !== 2) return copy("时长未知", "Duration unknown");
  const unit = state.language === "en" ? "hours" : "小时";
  return hours[0] === hours[1] ? `${hours[0]} ${unit}` : `${hours[0]}–${hours[1]} ${unit}`;
}

function localizedText(value, language = state.language) {
  if (value && typeof value === "object") return value[language] || value.en || value.zh || "";
  return value || "";
}

function bilingualLine(value) {
  const primary = localizedText(value, state.language);
  const secondary = localizedText(value, state.language === "en" ? "zh" : "en");
  return `<b>${escapeHtml(primary)}</b>${secondary && secondary !== primary ? `<small>${escapeHtml(secondary)}</small>` : ""}`;
}

function bilingualList(items = []) {
  return items.map(item => `<li>${bilingualLine(item)}</li>`).join("");
}

function officialPortalList(portals = []) {
  return portals.map(portal => `
    <li>
      <a href="${escapeHtml(portal.url)}" target="_blank" rel="noreferrer">${escapeHtml(localizedText(portal.name))} ↗</a>
      <span>${escapeHtml(localizedText(portal.use_for))}</span>
      <small>${copy("政府入口 · 核验于", "Government portal · verified")} ${escapeHtml(portal.last_verified)}</small>
    </li>`).join("");
}

function spotCard(spot, index) {
  const verified = Boolean(spot.last_verified);
  const rating = spot.tourism_rating?.level;
  const tags = (spot.categories || []).slice(0, 4).map(tag => `<span>${escapeHtml((state.language === "en" ? categoryLabelsEn : categoryLabels)[tag] || tag)}</span>`).join("");
  const warnings = (spot.warnings || []).slice(0, 2).map(item => state.language === "en" ? item : warningLabels[item] || item).join(" · ");
  const source = spot.sources?.[0];
  const tourismPortal = spot.tourism_portals?.[0];
  const name = localizedText(spot.name);
  const secondaryName = localizedText(spot.name, state.language === "en" ? "zh" : "en");
  return `
    <article class="spot-card" style="animation-delay:${index * 45}ms">
      <div class="spot-topline">
        <span class="city-label">${escapeHtml(localizedText(spot.city))} · ${escapeHtml(spot.neighborhood)}${rating ? ` · ${copy(`国家 ${rating} 级`, `National ${rating}`)}` : ""}</span>
        <span class="freshness ${verified ? "" : "unverified"}">${verified ? `${copy("已核验", "Verified")} ${escapeHtml(spot.last_verified)}` : copy("等待核验", "Needs verification")}</span>
      </div>
      <h4>${escapeHtml(name)}</h4>
      <p class="spot-en">${escapeHtml(secondaryName)}</p>
      <p class="spot-summary">${escapeHtml(localizedText(spot.summary))}</p>
      <div class="spot-tags">${tags}</div>
      <div class="spot-facts">
        <span>${copy("建议时长", "Suggested time")}<strong>${escapeHtml(durationText(spot.duration_hours))}</strong></span>
        <span>${copy("票务信息", "Tickets")}<strong>${escapeHtml(ticketText(spot.ticket))}</strong></span>
      </div>
      ${warnings ? `<p class="warning-line">${copy("注意：", "Note: ")}${escapeHtml(warnings)}</p>` : ""}
      <div class="spot-footer">
        <span>${spot.booking?.required === true ? copy("通常需要预约", "Reservation usually required") : copy("预约规则请复核", "Recheck reservation rules")}</span>
        ${source ? `<a href="${escapeHtml(source)}" target="_blank" rel="noreferrer">${copy("查看来源", "View source")} ↗</a>` : ""}
        ${tourismPortal ? `<a href="${escapeHtml(tourismPortal.url)}" target="_blank" rel="noreferrer">${copy("城市文旅官网", "Official city tourism")} ↗</a>` : ""}
      </div>
    </article>`;
}

function renderSpots(data, context = copy("全部示例地点", "All sample places")) {
  const spots = data.results || [];
  elements.resultsTitle.textContent = context;
  elements.resultCount.textContent = copy(`${spots.length} 个结果`, `${spots.length} result${spots.length === 1 ? "" : "s"}`);
  elements.results.setAttribute("aria-busy", "false");
  if (!spots.length) {
    elements.results.innerHTML = `<div class="empty-state"><b>${copy("没有找到符合条件的地点", "No matching places found")}</b><p>${copy("试试减少筛选条件，或者换一个月份和兴趣。", "Try fewer filters, another month or a different interest.")}</p></div>`;
    return;
  }
  elements.results.innerHTML = spots.map(spotCard).join("");
}

async function searchSpots(params = new URLSearchParams(), context = copy("全部示例地点", "All sample places")) {
  setLoading();
  try {
    const data = await fetchJson(`/search?${params.toString()}`);
    renderSpots(data, context);
  } catch (error) {
    showError(error);
  }
}

function renderAreas(data) {
  const areas = data.results || [];
  elements.resultsTitle.textContent = copy("住宿与游览区域", "Areas to stay and explore");
  elements.resultCount.textContent = copy(`${areas.length} 个区域`, `${areas.length} area${areas.length === 1 ? "" : "s"}`);
  elements.results.setAttribute("aria-busy", "false");
  if (!areas.length) {
    elements.results.innerHTML = `<div class="empty-state"><b>${copy("没有找到符合条件的区域", "No matching areas found")}</b><p>${copy("请减少筛选条件或更换城市、省份。", "Try fewer filters or another city or province.")}</p></div>`;
    return;
  }
  elements.results.innerHTML = areas.map((area, index) => {
    const tourismPortal = area.tourism_portals?.[0];
    return `
    <article class="info-card area-card" style="animation-delay:${index * 45}ms">
      <div class="info-kicker">${area.kind === "stay-area" ? copy("住宿区域", "STAY AREA") : copy("景点片区", "SIGHTSEEING AREA")} · ${escapeHtml(localizedText(area.city))}</div>
      <h4>${escapeHtml(localizedText(area.name))}</h4>
      <p class="info-en">${escapeHtml(localizedText(area.name, state.language === "en" ? "zh" : "en"))}</p>
      <p>${escapeHtml(localizedText(area.tradeoff) || copy("当前数据仅提供区域位置线索，住宿条件请另行核验。", "Current data provides location guidance only; verify accommodation details separately."))}</p>
      <div class="area-count"><strong>${escapeHtml(area.indexed_spot_count)}</strong><span>${copy("个已收录地点", "indexed places")}</span></div>
      <small class="coverage-note">${escapeHtml(localizedText(area.coverage_note))}</small>
      ${tourismPortal ? `<a class="area-portal-link" href="${escapeHtml(tourismPortal.url)}" target="_blank" rel="noreferrer">${copy("访问城市文旅官网", "Visit official city tourism")} ↗</a>` : ""}
    </article>`;
  }).join("");
}

async function searchAreas(params) {
  setLoading(copy("正在查找住宿与游览区域", "Finding areas to stay and explore"));
  try {
    renderAreas(await fetchJson(`/areas?${params.toString()}`));
  } catch (error) {
    showError(error);
  }
}

function renderPlan(plan) {
  const days = plan.days || [];
  const dayCards = days.map(day => {
    const stops = day.spots.length
      ? day.spots.map((spot, index) => {
        const nearby = (spot.nearby_spots || []).map(item => `<span>${escapeHtml(localizedText(item.name))} · ${escapeHtml(item.approx_distance_km)} km</span>`).join("");
        const amenities = (spot.amenities_guidance || []).map(item => `<li><b>${escapeHtml(localizedText(item.label))}</b><span>${escapeHtml(localizedText(item.guidance))}</span></li>`).join("");
        return `<div class="day-stop">
          <span>${String(index + 1).padStart(2, "0")}</span>
          <div class="stop-body">
            <b class="stop-title">${escapeHtml(localizedText(spot.name))}</b>
            <small>${escapeHtml(localizedText(spot.neighborhood))} · ${copy("约", "about")} ${escapeHtml(spot.duration_hours)} ${copy("小时", "hours")}</small>
            <div class="stop-context"><strong>${copy("人文导读", "Cultural context")}</strong><p>${escapeHtml(localizedText(spot.cultural_context || spot.summary))}</p></div>
            ${nearby ? `<div class="nearby-spots"><strong>${copy("周边可顺路", "Nearby places")}</strong><div>${nearby}</div><small>${copy("距离为直线估算，实际路线请实时核验", "Straight-line estimates; verify the live route")}</small></div>` : ""}
            <details class="amenities-details"><summary>${copy("查看周边配套核验清单", "View nearby facilities checklist")}</summary><ul>${amenities}</ul></details>
          </div>
        </div>`;
      }).join("")
      : `<div class="day-stop"><span>—</span><div><b>${copy("自由安排", "Free time")}</b><small>${copy("当前样例数据没有更多地点", "No more places in the current sample data")}</small></div></div>`;
    const transfers = (day.transfers || []).map(item => `<li><b>${escapeHtml(localizedText(item.from))} → ${escapeHtml(localizedText(item.to))}</b><span>${item.approx_distance_km !== null ? `${escapeHtml(item.approx_distance_km)} km · ` : ""}${escapeHtml(localizedText(item.guidance))}</span></li>`).join("");
    const arrival = day.arrival_guidance ? `<div class="arrival-guidance"><strong>${copy("从住宿地出发", "From your stay")}</strong><p>${escapeHtml(localizedText(day.arrival_guidance.guidance))}</p></div>` : "";
    const paceException = day.pace_exception ? `<div class="pace-exception"><strong>${copy("本日超过所选轻松节奏", "This day exceeds the selected relaxed pace")}</strong><p>${escapeHtml(localizedText(day.pace_exception))}</p></div>` : "";
    return `<article class="day-card"><div class="day-number"><strong>${copy(`第 ${day.day} 天`, `Day ${day.day}`)}</strong><span>${copy("预计", "Est.")} ${day.estimated_hours} ${copy("小时", "hours")}</span></div>${paceException}${arrival}${stops}${transfers ? `<div class="day-transfers"><strong>${copy("景点间如何乘车", "Transfers between places")}</strong><ul>${transfers}</ul></div>` : ""}</article>`;
  }).join("");

  elements.resultsTitle.textContent = `${localizedText(plan.city)} · ${copy(`${days.length} 日行程草案`, `${days.length}-day itinerary draft`)}`;
  elements.resultCount.textContent = copy(`${days.length} 天`, `${days.length} day${days.length === 1 ? "" : "s"}`);
  elements.results.setAttribute("aria-busy", "false");
  const unavailable = (plan.unavailable_spots || []).map(spot => `
    <li><strong>${escapeHtml(localizedText(spot.name))}</strong><span>${escapeHtml(localizedText(spot.availability?.note) || copy("当前不可用，请在出发前核验。", "Currently unavailable; verify before departure."))}</span></li>`).join("");
  const unassigned = (plan.unassigned_spots || []).map(spot => `
    <li><strong>${escapeHtml(localizedText(spot.name))}</strong><span>${escapeHtml(localizedText(spot.reason) || copy("未排入当前行程。", "Not included in this itinerary."))}</span></li>`).join("");
  const cautions = (plan.caution_spots || []).map(spot => `<li><strong>${escapeHtml(localizedText(spot.name))}</strong><span>${(spot.warnings || []).map(item => escapeHtml(state.language === "en" ? item : warningLabels[item] || item)).join(" · ")}</span></li>`).join("");
  const planNotices = [
    unavailable ? `<section class="plan-notice is-unavailable"><h5>${copy("暂时无法安排", "Currently unavailable")}</h5><p>${copy("以下地点目前闭馆或不可用，没有加入行程：", "These places are closed or unavailable and were not added:")}</p><ul>${unavailable}</ul></section>` : "",
    cautions ? `<section class="plan-notice is-caution"><h5>${copy("行动与环境提醒", "Mobility & environment cautions")}</h5><p>${copy("以下地点与减少步行、台阶或高海拔需求存在冲突，请不要忽略：", "These places may conflict with reduced walking, fewer steps, or altitude needs:")}</p><ul>${cautions}</ul></section>` : "",
    unassigned ? `<section class="plan-notice"><h5>${copy("未排入本次行程", "Not included in this itinerary")}</h5><p>${copy(`受每天约 ${plan.daily_limit_hours} 小时的活动上限影响：`, `Due to the daily activity limit of about ${plan.daily_limit_hours} hours:`)}</p><ul>${unassigned}</ul></section>` : ""
  ].join("");
  const planningNotes = (plan.planning_notes || []).map(note => localizedText(note)).filter(Boolean).join(" ");
  const stayAreas = (plan.recommended_stay_areas || []).map(area => `<li><b>${escapeHtml(localizedText(area.name))}</b><span>${escapeHtml(localizedText(area.tradeoff))}</span><small>${copy("覆盖本行程", "Covers")} ${escapeHtml(area.planned_spot_count)} ${copy("个景点", "planned places")}</small></li>`).join("");
  const transportModes = (plan.transport?.local || []).map(item => `<span>${escapeHtml(localizedText(item))}</span>`).join("");
  const transportNotes = (plan.transport?.notes || []).map(item => `<li>${escapeHtml(localizedText(item))}</li>`).join("");
  const weather = plan.weather || {};
  const weatherCard = weather.forecast_url ? `<article class="support-card weather-support"><p class="info-kicker">LIVE WEATHER</p><h5>${copy("当地实时天气与预警", "Live local weather & alerts")}</h5><p>${escapeHtml(localizedText(weather.note))}</p><div class="support-links"><a href="${escapeHtml(weather.forecast_url)}" target="_blank" rel="noreferrer">${copy("查看当地实时天气", "Live local forecast")} ↗</a><a href="${escapeHtml(weather.warnings_url)}" target="_blank" rel="noreferrer">${copy("查看气象预警", "Weather alerts")} ↗</a></div><small>${copy("入口核验于", "Links verified")} ${escapeHtml(weather.last_verified)}</small></article>` : "";
  const tourismPortals = officialPortalList(plan.tourism_portals);
  const tourismPortalCard = tourismPortals ? `<article class="support-card tourism-portal-support"><p class="info-kicker">OFFICIAL CITY TOURISM</p><h5>${copy("城市文旅官网", "Official city tourism")}</h5><ul class="official-portal-list">${tourismPortals}</ul></article>` : "";

  elements.results.innerHTML = `
    <div class="plan-result">
      <div class="plan-summary"><div><h4>${copy(`${escapeHtml(plan.city?.zh)}旅行草案`, `${escapeHtml(plan.city?.en)} itinerary draft`)}</h4><p>${escapeHtml(state.language === "en" ? plan.city?.zh : plan.city?.en)} · RULE-BASED ITINERARY</p></div><span class="stamp">${copy("行程", "PLAN")}</span></div>
      <div class="plan-days">${dayCards}</div>
      <div class="trip-support-grid">
        ${stayAreas ? `<article class="support-card"><p class="info-kicker">STAY</p><h5>${copy("住在哪里更顺路", "Where to stay")}</h5><ul class="stay-recommendations">${stayAreas}</ul></article>` : ""}
        <article class="support-card"><p class="info-kicker">GETTING AROUND</p><h5>${copy("市内乘车原则", "Getting around")}</h5><div class="transport-mode-tags">${transportModes}</div><ul class="transport-notes">${transportNotes}</ul><p class="live-note">${copy("不保存实时线路、票价和末班车时间；每天出发前请用地图与官方交通渠道复核。", "Live routes, fares, and last services are not stored; recheck with a map and official transport channel each day.")}</p></article>
        ${weatherCard}
        ${tourismPortalCard}
      </div>
      ${planNotices}
      <p class="plan-caveat">${escapeHtml(planningNotes || copy("这是基于地点时长与兴趣排序生成的草案，不是实时导航。出发前请核验开放时间、预约、交通和天气。", "This draft is based on visit duration and interests, not live navigation. Verify opening hours, reservations, transport and weather before departure."))}</p>
    </div>`;
}

async function generatePlan(city, days = 2, interests = []) {
  setLoading(copy("正在整理每日行程", "Building your daily itinerary"));
  const params = new URLSearchParams({ city, days: String(days) });
  if (interests.length) params.set("interests", interests.join(","));
  try {
    renderPlan(await fetchJson(`/plan?${params.toString()}`));
  } catch (error) {
    showError(error);
  }
}

function renderRecommendation(data) {
  renderPlan(data.itinerary);
  const planResult = elements.results.querySelector(".plan-result");
  const recommended = data.recommended_city;
  const requirements = data.normalized_requirements;
  const reasons = (recommended.reasons || []).map(reason => `<li>${bilingualLine(reason)}</li>`).join("");
  const rankings = (data.ranked_cities || []).map((city, index) => `<li><span>${index + 1}</span><b>${escapeHtml(localizedText(city.name))}</b><small>${copy("匹配分", "Score")} ${escapeHtml(city.score)} · ${escapeHtml(city.indexed_spot_count)} ${copy("个地点", "places")}</small></li>`).join("");
  const stayAreas = (data.city_guide?.stay_areas || []).slice(0, 2).map(area => `<li>${bilingualLine(area.name)}<span>${escapeHtml(localizedText(area.tradeoff))}</span></li>`).join("");
  const foods = (data.city_guide?.foods || []).map(food => `<li>${bilingualLine(food.name)}</li>`).join("");
  const liveChecks = (data.live_checks_required || []).map(item => {
    const links = (item.sources || []).map((source, index) => `<a href="${escapeHtml(source)}" target="_blank" rel="noreferrer">${copy("官方核验入口", "Official verification")} ${index + 1} ↗</a>`).join("");
    return `<li>${bilingualLine(item)}${links}</li>`;
  }).join("");
  const unmet = (data.unmet_requirements || []).map(item => `<li>${bilingualLine(item)}</li>`).join("");
  const seasonal = data.preparation?.seasonal_advice?.[0];
  const preparation = seasonal ? `
    <article class="recommend-detail"><h5>${copy(`${escapeHtml(requirements.month)} 月准备`, `Month ${escapeHtml(requirements.month)} preparation`)}</h5><p>${bilingualLine(seasonal.clothing)}</p><div class="detail-tags">${(seasonal.gear || []).map(item => `<span>${escapeHtml(localizedText(item))}</span>`).join("")}</div></article>` : "";
  const dateText = requirements.start_date
    ? `${requirements.start_date}${requirements.end_date ? ` 至 ${requirements.end_date}` : ""}`
    : copy(`暂未确定日期 · ${requirements.days} 天`, `Dates flexible · ${requirements.days} days`);

  planResult.insertAdjacentHTML("afterbegin", `
    <section class="recommendation-hero">
      <div><p>BEST MATCH · ${escapeHtml(recommended.confidence.toUpperCase())}</p><h4>${copy("最佳匹配：", "Best match: ")}${escapeHtml(localizedText(recommended.name))}</h4><small>${escapeHtml(localizedText(recommended.name, state.language === "en" ? "zh" : "en"))} · ${escapeHtml(localizedText(recommended.overview))}</small></div>
      <div class="match-score"><strong>${escapeHtml(recommended.score)}</strong><span>${copy("匹配分", "MATCH")}</span></div>
    </section>
    <div class="requirement-bar"><span>${escapeHtml(requirements.traveler_count)} ${copy("人", "travellers")}</span><span>${escapeHtml(dateText)}</span><span>${copy("每天约", "About")} ${escapeHtml(data.itinerary.daily_limit_hours)} ${copy("小时", "hours/day")}</span><span>${requirements.children ? copy("有儿童同行", "With children") : copy("成人/未注明儿童", "Adults / children not specified")}</span></div>
    <div class="recommend-grid">
      <article class="recommend-detail"><h5>${copy("为什么推荐", "Why this match")}</h5><ul class="bilingual-list">${reasons}</ul></article>
      <article class="recommend-detail"><h5>${copy("城市匹配顺序", "City ranking")}</h5><ol class="ranking-list">${rankings}</ol></article>
      <article class="recommend-detail"><h5>${copy("住宿区域建议", "Where to stay")}</h5><ul class="bilingual-list food-list">${stayAreas}</ul></article>
      <article class="recommend-detail"><h5>${copy("当地特色小吃", "Local food")}</h5><ul class="bilingual-list">${foods}</ul></article>
      ${preparation}
    </div>`);
  planResult.insertAdjacentHTML("beforeend", `
    ${unmet ? `<section class="plan-notice is-unavailable"><h5>${copy("尚未满足的要求", "Unmet requirements")}</h5><ul class="bilingual-list">${unmet}</ul></section>` : ""}
    <section class="live-checks"><h5>${copy("出发前自动方案仍需核验", "Checks still required before departure")}</h5><ul class="bilingual-list">${liveChecks}</ul></section>`);
  elements.resultsTitle.textContent = `${localizedText(recommended.name)} · ${copy("智能匹配方案", "Smart trip match")}`;
  elements.resultCount.textContent = copy(`${requirements.days} 天方案`, `${requirements.days}-day plan`);
}

async function generateRecommendation(params) {
  setLoading(copy("正在匹配城市、景点和旅行要求", "Matching cities, places and travel needs"));
  try {
    renderRecommendation(await fetchJson(`/recommend?${params.toString()}`));
  } catch (error) {
    showError(error);
  }
}

function renderPreparation(data) {
  const seasonal = data.seasonal_advice || [];
  const seasonCards = seasonal.length ? seasonal.map(item => `
    <article class="info-card">
      <div class="info-kicker">${copy(`${escapeHtml(data.month)} 月穿衣与装备`, `MONTH ${escapeHtml(data.month)} · CLOTHING & GEAR`)}</div>
      <h4>${copy("当月准备建议", "Monthly preparation")}</h4>
      <ul class="bilingual-list"><li>${bilingualLine(item.clothing)}</li></ul>
      <h5>${copy("随身装备", "What to pack")}</h5><ul class="bilingual-list">${bilingualList(item.gear)}</ul>
      <h5>${copy("主要风险", "Key risks")}</h5><ul class="bilingual-list">${bilingualList(item.risks)}</ul>
    </article>`).join("") : `<article class="info-card"><h4>${copy("暂无当月建议", "No monthly advice yet")}</h4><p>${copy("请在出发前查询当地实时天气与预警。", "Check the local forecast and alerts before departure.")}</p></article>`;
  const gateways = bilingualList(data.transport?.international_gateways);
  const localTransport = bilingualList(data.transport?.local);
  const culture = bilingualList(data.culture);
  const foods = (data.foods || []).map(food => `<li>${bilingualLine(food.name)}<span>${(food.dietary_notes || []).map(note => escapeHtml(localizedText(note))).join(" · ")}</span></li>`).join("");
  const weather = data.weather || {};
  const liveWeather = weather.forecast_url ? `<article class="info-card weather-info-card"><div class="info-kicker">LIVE WEATHER</div><h4>${copy("实时天气与预警入口", "Live weather & alerts")}</h4><p>${escapeHtml(localizedText(weather.note))}</p><div class="support-links"><a href="${escapeHtml(weather.forecast_url)}" target="_blank" rel="noreferrer">${copy("当地实时天气", "Live local forecast")} ↗</a><a href="${escapeHtml(weather.warnings_url)}" target="_blank" rel="noreferrer">${copy("中央气象台预警", "NMC alerts")} ↗</a></div><small>${copy("入口核验于", "Links verified")} ${escapeHtml(weather.last_verified)}</small></article>` : "";
  const tourismPortals = officialPortalList(data.tourism_portals);
  const tourismPortalCard = tourismPortals ? `<article class="info-card tourism-portal-info"><div class="info-kicker">OFFICIAL CITY TOURISM</div><h4>${copy("城市文旅官网", "Official city tourism")}</h4><p>${copy("查看当地文旅动态、景区公告、公共服务和节庆活动。", "Check local tourism news, attraction notices, public services and events.")}</p><ul class="official-portal-list">${tourismPortals}</ul></article>` : "";

  elements.resultsTitle.textContent = `${localizedText(data.city)} · ${copy(`${data.month} 月出发准备`, `Month ${data.month} preparation`)}`;
  elements.resultCount.textContent = copy("准备清单", "Checklist");
  elements.results.setAttribute("aria-busy", "false");
  elements.results.innerHTML = `
    ${seasonCards}
    ${liveWeather}
    ${tourismPortalCard}
    <article class="info-card"><div class="info-kicker">TRANSPORT</div><h4>${copy("抵达与市内交通", "Arrival & local transport")}</h4><h5>${copy("主要抵达门户", "Main gateways")}</h5><ul class="bilingual-list">${gateways}</ul><h5>${copy("市内交通", "Getting around")}</h5><ul class="bilingual-list">${localTransport}</ul><p>${escapeHtml(localizedText(data.transport?.notes?.[0]))}</p></article>
    <article class="info-card"><div class="info-kicker">LOCAL CULTURE & FOOD</div><h4>${copy("文化与特色小吃", "Culture & local food")}</h4><h5>${copy("文化体验", "Cultural experiences")}</h5><ul class="bilingual-list">${culture}</ul><h5>${copy("特色小吃", "Local specialities")}</h5><ul class="bilingual-list food-list">${foods}</ul></article>
    <p class="result-caveat">${escapeHtml(localizedText(data.limitations))}</p>`;
}

async function loadPreparation(city, month) {
  setLoading(copy("正在整理出发准备清单", "Building your preparation checklist"));
  try {
    renderPreparation(await fetchJson(`/prepare?city=${encodeURIComponent(city)}&month=${encodeURIComponent(month)}`));
  } catch (error) {
    showError(error);
  }
}

function renderEmergency(data) {
  const services = data.services || [];
  elements.resultsTitle.textContent = `${localizedText(data.city)} · ${copy("紧急求助信息", "Emergency help")}`;
  elements.resultCount.textContent = copy(`${services.length} 个号码`, `${services.length} numbers`);
  elements.results.setAttribute("aria-busy", "false");
  elements.results.innerHTML = `
    <div class="emergency-instruction"><strong>${copy("遇到危险时", "In an emergency")}</strong><p>${escapeHtml(localizedText(data.instructions))}</p></div>
    ${services.map(service => `<article class="info-card emergency-card"><div class="info-kicker">${escapeHtml(service.scope)}</div><h4>${escapeHtml(localizedText(service.service))}</h4><p class="info-en">${escapeHtml(localizedText(service.service, state.language === "en" ? "zh" : "en"))}</p><a class="phone-number" href="tel:${escapeHtml(service.phone)}">${escapeHtml(service.phone)}</a><div class="source-line"><span>${copy("核验于", "Verified")} ${escapeHtml(service.last_verified)}</span><a href="${escapeHtml(service.source)}" target="_blank" rel="noreferrer">${copy("官方来源", "Official source")} ↗</a></div></article>`).join("")}
    <p class="result-caveat">${escapeHtml(localizedText(data.limitations))}</p>`;
}

async function loadEmergency(city) {
  setLoading(copy("正在载入紧急求助信息", "Loading emergency help"));
  try {
    renderEmergency(await fetchJson(`/emergency?city=${encodeURIComponent(city)}`));
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
    if (health.status !== "ok") throw new Error(copy("服务状态异常", "Service status error"));
    elements.status.classList.add("is-online");
    elements.status.innerHTML = `<i></i> ${copy("本地数据已连接", "Local data connected")}`;
    document.querySelector("#city-count").textContent = cities.length;

    cities.forEach(city => {
      const label = state.language === "en" ? `${city.name.en} · ${city.name.zh}` : `${city.name.zh} · ${city.name.en}`;
      elements.searchCity.add(new Option(label, city.id));
      elements.planCity.add(new Option(label, city.id));
      elements.recommendCity.add(new Option(label, city.id));
      [elements.areasCity, elements.prepareCity, elements.emergencyCity].forEach(select => select.add(new Option(label, city.id)));
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.city = city.id;
      button.textContent = localizedText(city.name);
      elements.shortcuts.append(button);
    });
    setLoading();
    const initialData = await fetchJson("/search");
    document.querySelector("#spot-count").textContent = initialData.count;
    renderSpots(initialData);
  } catch (error) {
    elements.status.classList.add("is-offline");
    elements.status.innerHTML = `<i></i> ${copy("本地服务未连接", "Local service disconnected")}`;
    showError(error);
  }
}

applyInterfaceLanguage();

document.querySelectorAll("[data-language]").forEach(button => button.addEventListener("click", () => {
  if (button.dataset.language === state.language) return;
  try { localStorage.setItem("china-travel-language", button.dataset.language); } catch { /* The page still reloads with the default language. */ }
  window.location.reload();
}));

document.querySelectorAll(".tab").forEach(tab => tab.addEventListener("click", () => activateTab(tab.dataset.tab)));

elements.recommendForm.addEventListener("submit", event => {
  event.preventDefault();
  const form = new FormData(elements.recommendForm);
  const params = new URLSearchParams();
  ["traveler_count", "start_date", "end_date", "days", "city", "pace", "budget", "mobility", "origin_country", "requirements"].forEach(key => {
    const value = form.get(key);
    if (value) params.set(key, value);
  });
  const desiredPlaces = String(form.get("desired_places") || "").split(/[，,]/).map(value => value.trim()).filter(Boolean);
  if (desiredPlaces.length) params.set("desired_places", desiredPlaces.join(","));
  const interests = form.getAll("interests");
  if (interests.length) params.set("interests", interests.join(","));
  if (form.get("children")) params.set("children", "true");
  generateRecommendation(params);
});

elements.searchForm.addEventListener("submit", event => {
  event.preventDefault();
  const form = new FormData(elements.searchForm);
  const params = new URLSearchParams();
  [["q", form.get("keyword")], ["city", form.get("city")], ["category", form.get("category")], ["month", form.get("month")], ["max_hours", form.get("max_hours")]].forEach(([key, value]) => {
    if (value) params.set(key, value);
  });
  if (form.get("free")) params.set("free", "true");
  const cityLabel = elements.searchCity.selectedOptions[0]?.text.split(" · ")[0];
  searchSpots(params, cityLabel && form.get("city") ? `${cityLabel} · ${copy("查询结果", "Results")}` : copy("旅行地点查询结果", "Travel place results"));
});

elements.areasForm.addEventListener("submit", event => {
  event.preventDefault();
  const form = new FormData(elements.areasForm);
  const params = new URLSearchParams();
  [["q", form.get("keyword")], ["city", form.get("city")], ["province", form.get("province")]].forEach(([key, value]) => {
    if (value) params.set(key, value);
  });
  searchAreas(params);
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

elements.prepareForm.addEventListener("submit", event => {
  event.preventDefault();
  const form = new FormData(elements.prepareForm);
  loadPreparation(form.get("city"), form.get("month"));
});

elements.emergencyForm.addEventListener("submit", event => {
  event.preventDefault();
  loadEmergency(new FormData(elements.emergencyForm).get("city"));
});

elements.shortcuts.addEventListener("click", event => {
  const button = event.target.closest("button[data-city]");
  if (!button) return;
  activateTab("search");
  elements.searchCity.value = button.dataset.city;
  const params = new URLSearchParams({ city: button.dataset.city });
  searchSpots(params, `${button.textContent} · ${copy("全部示例地点", "All sample places")}`);
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
    searchSpots(new URLSearchParams({ city: button.dataset.city, category: button.dataset.category }), copy("旅行灵感查询结果", "Travel inspiration results"));
  }
}));

initialize();
