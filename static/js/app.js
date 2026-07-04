/* ── KrishiMitra AI — Frontend Logic ─────────────────────── */

let lang   = 'en';
let isRec  = false;
let recog  = null;
let selectedImageB64 = null;   // base64 string of selected image
const chatEl = document.getElementById('chat');

/* ── QUICK CHIPS PER LANGUAGE ─────────────────────────── */
const CHIPS = {
  en: [
    ['🍅 Yellow leaves',       'My tomato leaves are turning yellow, what disease could it be?'],
    ['🌾 Wheat fertilizer',    'Best fertilizer schedule for wheat crop'],
    ['🌧️ Cotton irrigation',   'Irrigation schedule for cotton during flowering stage'],
    ['🧅 Onion market price',  'What is the current market price of onion?'],
    ['📋 Govt schemes',        'List all government schemes available for farmers in India'],
    ['🌱 Soil health',         'How to improve soil health and prevent soil erosion?'],
    ['🐛 Pest control',        'Organic pest control methods for vegetable crops'],
    ['🌽 Maize disease',       'Common diseases in maize and how to treat them'],
    ['💧 Drip irrigation',     'Benefits and setup of drip irrigation for small farms'],
    ['🌻 Sunflower farming',   'Complete guide to sunflower farming and harvesting'],
    ['🥜 Groundnut advice',    'Tips for growing groundnut in black soil'],
    ['🌿 Crop rotation',       'Best crop rotation practices to maintain soil fertility'],
    ['🌡️ Heat stress crops',   'How to protect crops from extreme heat and drought?'],
    ['🧪 Soil testing',        'How to do soil testing and what to check for?'],
    ['📦 Storage tips',        'How to store wheat and rice grains after harvest?'],
    ['🐄 Organic farming',     'How to start organic farming and get certification?'],
    ['🚜 Tractor maintenance', 'Daily maintenance checklist for tractors'],
    ['🌦️ Weather forecast',    'How to read weather patterns for upcoming harvest'],
  ],
  hi: [
    ['🍅 पीले पत्ते',    'मेरे टमाटर के पत्ते पीले हो रहे हैं, यह कौन सा रोग हो सकता है?'],
    ['🌾 गेहूं खाद',     'गेहूं की फसल के लिए उर्वरक का सही समय क्या है?'],
    ['📋 सरकारी योजना', 'किसानों के लिए उपलब्ध सरकारी योजनाओं की सूची बताएं'],
    ['🐛 कीट नियंत्रण',  'सब्जियों में कीड़ों को नियंत्रित करने के जैविक उपाय'],
    ['💧 सिंचाई',        'कपास की फसल के फूल आने पर सिंचाई का तरीका'],
    ['🧅 प्याज का भाव',  'आज मंडी में प्याज का क्या भाव चल रहा है?'],
    ['🌱 मिट्टी जांच',   'मिट्टी की उर्वरता बढ़ाने के लिए क्या करना चाहिए?'],
    ['🐄 पशुपालन',       'डेयरी फार्मिंग शुरू करने के लिए महत्वपूर्ण जानकारी'],
    ['🌾 धान की खेती',   'धान की उन्नत किस्में और बुवाई का सही समय क्या है?'],
    ['🍇 अंगूर की खेती', 'अंगूर की बागवानी में खाद और पानी का प्रबंधन कैसे करें?'],
    ['🌿 गन्ने की खेती', 'गन्ने की फसल में वजन बढ़ाने के लिए कौन सी खाद डालें?'],
    ['🥔 आलू के रोग',    'आलू में पिछेता झुलसा रोग (Late Blight) का नियंत्रण कैसे करें?'],
    ['🌽 मक्का की खेती', 'मक्का की फसल में लगने वाले प्रमुख कीट और उनके उपाय'],
    ['🌻 सूरजमुखी',      'सूरजमुखी की खेती के लिए उपयुक्त जलवायु और मिट्टी'],
    ['📉 मौसम और खेती',  'आने वाले दिनों में मौसम कैसा रहेगा और फसलों पर इसका क्या असर होगा?'],
    ['🚜 ट्रैक्टर देखभाल', 'ट्रैक्टर की लंबी उम्र के लिए दैनिक देखभाल के टिप्स'],
    ['🍯 शहद उत्पादन',   'मधुमक्खी पालन कैसे शुरू करें और इसके लिए सरकारी मदद क्या है?'],
    ['🍓 स्ट्रॉबेरी',      'क्या कम तापमान वाले इलाकों में स्ट्रॉबेरी की खेती मुनाफे का सौदा है?'],
  ],
  mr: [
    ['🍅 पिवळी पाने',     'माझ्या टोमॅटोची पाने पिवळी पडत आहेत, हा कोणता रोग असू शकतो?'],
    ['🌾 गव्हाचे खत',     'गव्हाच्या पिकासाठी खतांचे योग्य वेळापत्रक काय आहे?'],
    ['📋 सरकारी योजना',   'शेतकऱ्यांसाठी उपलब्ध सरकारी योजनांची यादी सांगा'],
    ['🐛 कीड नियंत्रण',    'भाज्यांमधील कीड नियंत्रणासाठी जैविक उपाय'],
    ['💧 सिंचन',          'कापूस पिकाला फुले असताना सिंचनाची पद्धत'],
    ['🧅 कांद्याचा भाव',   'आज बाजारात कांद्याचा भाव काय चालू आहे?'],
    ['🌱 माती परीक्षण',    'जमिनीचा कस वाढवण्यासाठी काय करावे?'],
    ['🐄 पशुपालन',        'डेअरी फार्मिंग सुरू करण्यासाठी महत्त्वाची माहिती'],
    ['🍎 सफरचंद बागायत', 'उष्ण हवामानात सफरचंदाची लागवड करणे शक्य आहे का?'],
    ['🌿 सेंद्रिय खते',    'घरच्या घरी गांडूळ खत प्रकल्प कसा सुरू करावा?'],
    ['🌽 मका पीक',        'मका पिकावरील लष्करी अळीचे नियंत्रण कसे करावे?'],
    ['🌻 सूर्यफूल शेती',   'सूर्यफूल लागवडीसाठी सुधारित वाण आणि खत व्यवस्थापन'],
    ['📉 हवामान अंदाज',    'हवामानातील बदलांनुसार पिकांची काळजी कशी घ्यावी?'],
    ['🚜 ट्रॅक्टर देखभाल', 'ट्रॅक्टरच्या इंजिनची काळजी घेण्यासाठी काही महत्त्वाच्या टिप्स सांगा'],
    ['🍯 मधमाशी पालन',    'मधमाशी पालन व्यवसाय कसा सुरू करावा आणि त्यासाठी अनुदान मिळते का?'],
    ['🍓 स्ट्रॉबेरी शेती', 'स्ट्रॉबेरी लागवडीसाठी योग्य वेळ आणि हवामान कोणते?'],
    ['🥜 भुईमूग शेती',     'भुईमूग पिकात शेंगा भरण्यासाठी कोणत्या खतांचा वापर करावा?'],
    ['🥥 नारळ लागवड',      'नारळ झाडांची जोपासना आणि उत्पन्न वाढवण्यासाठी उपाय'],
  ],
};

/* ── LANGUAGE SWITCH ──────────────────────────────────── */
function setLang(l) {
  lang = l;
  // Sync sidebar language buttons
  document.querySelectorAll('.slb').forEach(b => b.classList.remove('act'));
  const sbBtn = document.getElementById('slb-' + l);
  if (sbBtn) sbBtn.classList.add('act');

  const chips = CHIPS[l] || CHIPS.en;
  const chipsEl = document.getElementById('chips');
  if (chipsEl) {
    chipsEl.innerHTML = chips
      .map(([lbl, q]) =>
        `<div class='chip' onclick='quickAsk("${q.replace(/"/g, '\\"')}")' title="${q.replace(/"/g, '&quot;')}">${lbl}</div>`)
      .join('');
  }

  // Update count badge
  const countEl = document.getElementById('suggCount');
  if (countEl) countEl.textContent = chips.length;
}

function quickAsk(t) {
  document.getElementById('inp').value = t;
  send();
}

/* ── TOGGLE/HIDE SUGGESTIONS PANEL ───────────────────── */
function toggleChips() {
  const drawer = document.getElementById('chipsDrawer');
  const arrow  = document.getElementById('suggArrow');
  if (!drawer) return;
  const isCollapsed = drawer.classList.toggle('collapsed');
  if (arrow) arrow.classList.toggle('collapsed', isCollapsed);
}

function hideChips() {
  const drawer = document.getElementById('chipsDrawer');
  const arrow  = document.getElementById('suggArrow');
  if (drawer && !drawer.classList.contains('collapsed')) {
    drawer.classList.add('collapsed');
    if (arrow) arrow.classList.add('collapsed');
  }
}

/* ── KEYBOARD HANDLER ─────────────────────────────────── */
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
}

/* ── MARKDOWN → HTML ──────────────────────────────────── */
function mdToHtml(t) {
  return t
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
}

/* ── APPEND MESSAGE ───────────────────────────────────── */
function appendMsg(text, type, ts, elemId) {
  const w  = document.createElement('div');
  w.className = 'msg ' + type;
  if (elemId) w.id = elemId;                    // tag for scroll-jump
  const id = 'msg' + Date.now() + Math.random().toString(36).slice(2);
  if (type === 'bot') {
    w.innerHTML = `
      <div class='avatar bavatar'>🌾</div>
      <div style='flex:1'>
        <div class='bubble bbub'>
          <div id='${id}'>${mdToHtml(text)}</div>
          ${ts ? `<div style='font-size:.6rem;color:#999;margin-top:4px'>${ts}</div>` : ''}
          <button class='ttsb' onclick='speak("${id}")'>🔊 Listen</button>
        </div>
      </div>`;
  } else {
    w.innerHTML = `
      <div style='flex:1;text-align:right'>
        <div class='bubble ubub'>${text}${ts ? `<div style='font-size:.6rem;opacity:.6;margin-top:4px'>${ts}</div>` : ''}</div>
      </div>
      <div class='avatar uavatar'>👨‍🌾</div>`;
  }
  chatEl.appendChild(w);
  chatEl.scrollTop = chatEl.scrollHeight;
  return w;  // return the element for reference
}

/* ── CHAT SEPARATOR ───────────────────────────────────── */
function appendSep(label) {
  const s = document.createElement('div');
  s.className = 'chat-sep';
  s.textContent = label;
  chatEl.appendChild(s);
}

/* ── TYPING INDICATOR ─────────────────────────────────── */
function showTyping() {
  const w = document.createElement('div');
  w.className = 'msg bot';
  w.id = 'typing';
  w.innerHTML = `
    <div class='avatar bavatar'>🌾</div>
    <div class='typing'>
      <div class='tdot'></div>
      <div class='tdot'></div>
      <div class='tdot'></div>
    </div>`;
  chatEl.appendChild(w);
  chatEl.scrollTop = chatEl.scrollHeight;
}

const historyMsgIds = [];

async function loadHistory() {
  try {
    const res  = await fetch('/history');
    const data = await res.json();
    if (!data.history || data.history.length === 0) {
      appendMsg(
        'Namaste! I am KrishiMitra AI — your farming assistant.\n' +
        'Ask about crops, diseases, fertilizers, market prices, or government schemes!',
        'bot'
      );
      return;
    }
    appendSep('── Previous conversations ──');
    data.history.forEach((m, idx) => {
      const userElemId = 'hist-user-' + idx;
      appendMsg(m.user_message, 'user', m.timestamp, userElemId);
      appendMsg(m.bot_response, 'bot',  m.timestamp);
      historyMsgIds.push({ elemId: userElemId, question: m.user_message, ts: m.timestamp });
    });
    appendSep('── New conversation ──');
  } catch (e) {
    appendMsg(
      'Namaste! I am KrishiMitra AI — your farming assistant.\n' +
      'Ask about crops, diseases, fertilizers, market prices, or government schemes!',
      'bot'
    );
  }
}
async function toggleHistory() {
  const panel = document.getElementById('historyPanel');
  const isOpen = panel.style.display !== 'none';
  if (isOpen) { panel.style.display = 'none'; return; }

  panel.style.display = 'flex';
  await refreshHistoryPanel();
}

async function refreshHistoryPanel() {
  const listEl = document.getElementById('histList');
  if (!listEl) return;
  const panel = document.getElementById('historyPanel');
  const isVisible = panel && panel.style.display !== 'none';
  if (!isVisible) return;   // don't refresh if panel is closed
  listEl.innerHTML = '<div style="color:rgba(255,255,255,.5);font-size:.75rem;text-align:center;padding:12px">Loading…</div>';
  try {
    const res  = await fetch('/history');
    const data = await res.json();
    if (!data.history || data.history.length === 0) {
      listEl.innerHTML = '<div style="color:rgba(255,255,255,.4);font-size:.72rem;text-align:center;padding:20px">🌱 No history yet.<br>Start chatting!</div>';
      return;
    }
    // Show newest first in the panel
    const reversed = [...data.history].reverse();
    listEl.innerHTML = reversed.map((m, idx) => {
      const origIdx = data.history.length - 1 - idx;
      const elemId  = 'hist-user-' + origIdx;
      const preview = m.bot_response.slice(0, 130) + (m.bot_response.length > 130 ? '…' : '');
      const badge   = m.intent && m.intent !== 'general'
        ? `<span style="font-size:.58rem;padding:2px 7px;background:rgba(138,208,68,.12);border:1px solid rgba(138,208,68,.25);border-radius:10px;color:var(--g6);margin-left:6px">${escHtml(m.intent)}</span>`
        : '';
      return `
        <div class='hist-card' onclick='jumpToHistory("${elemId}")'>
          <div class='hist-q'>👨‍🌾 ${escHtml(m.user_message)}${badge}</div>
          <div class='hist-a'>🌾 ${escHtml(preview)}</div>
          <div class='hist-ts'>
            <span>🕐 ${escHtml(m.timestamp || '')}</span>
            <span class='hist-goto'>↗️ Go to chat</span>
          </div>
        </div>`;
    }).join('');
  } catch (e) {
    listEl.innerHTML = '<div style="color:#ff7b79;text-align:center;padding:12px">⚠️ Failed to load history.</div>';
  }
}

function escHtml(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function jumpToHistory(elemId) {
  // Close the history panel
  document.getElementById('historyPanel').style.display = 'none';
  // Find the element and scroll to it
  const el = document.getElementById(elemId);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    // Highlight briefly
    el.style.outline = '2px solid rgba(138,208,68,0.8)';
    el.style.borderRadius = '8px';
    setTimeout(() => { el.style.outline = ''; el.style.borderRadius = ''; }, 2000);
  }
}

/* ── SEND MESSAGE ─────────────────────────────────────── */
async function send() {
  const inp  = document.getElementById('inp');
  const text = inp.value.trim();
  const hasImg = !!selectedImageB64;
  if (!text && !hasImg) return;

  // Show user bubble — with thumbnail if image attached
  const displayText = hasImg
    ? (text || '📷 Analyzing crop image… BY KrishiMitra AI')
    : text;
  if (hasImg) {
    appendMsgWithImage(displayText, selectedImageB64);
  } else {
    appendMsg(text, 'user');
  }
  inp.value = '';
  hideChips();   // hide suggestions once user starts chatting
  showTyping();

  const payload = { message: displayText, language: lang };
  if (hasImg) payload.image = selectedImageB64;
  clearImage();   // reset after attaching to payload

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.status === 401) { window.location.href = '/login'; return; }
    const data = await res.json();
    const t = document.getElementById('typing');
    if (t) t.remove();
    appendMsg(data.response, 'bot', data.timestamp);
    // Auto-refresh history panel silently
    refreshHistoryPanel();
  } catch (e) {
    const t = document.getElementById('typing');
    if (t) t.remove();
    appendMsg('Error connecting to server. Is app.py running?', 'bot');
  }
}

/* ── IMAGE CAPTURE / UPLOAD ───────────────────────────── */
function handleImageSelect(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    // Store raw base64 (strip data URL prefix)
    const dataUrl = e.target.result;
    selectedImageB64 = dataUrl.split(',')[1];
    // Show preview
    document.getElementById('imgPreview').src = dataUrl;
    document.getElementById('imgPreviewWrap').style.display = 'block';
    document.getElementById('camBtn').classList.add('has-img');
    // Hint user
    const inp = document.getElementById('inp');
    if (!inp.value.trim()) inp.placeholder = 'Add a question about this image (optional)…';
  };
  reader.readAsDataURL(file);
  // Reset input so same file can be re-selected
  event.target.value = '';
}

function clearImage() {
  selectedImageB64 = null;
  document.getElementById('imgPreviewWrap').style.display = 'none';
  document.getElementById('imgPreview').src = '';
  document.getElementById('camBtn').classList.remove('has-img');
  document.getElementById('inp').placeholder = 'Ask about crops, diseases, market prices...';
}

function appendMsgWithImage(text, b64) {
  const w = document.createElement('div');
  w.className = 'msg user';
  w.innerHTML = `
    <div style='flex:1;text-align:right'>
      <div class='bubble ubub'>
        <img src="data:image/jpeg;base64,${b64}"
          style="max-width:180px;max-height:140px;border-radius:9px;display:block;margin-bottom:5px;margin-left:auto">
        ${text}
      </div>
    </div>
    <div class='avatar uavatar'>👨‍🌾</div>`;
  chatEl.appendChild(w);
  chatEl.scrollTop = chatEl.scrollHeight;
}

/* ── TEXT-TO-SPEECH ───────────────────────────────────── */
function speak(elId) {
  const el = document.getElementById(elId);
  if (!el) return;
  window.speechSynthesis.cancel();
  const utt  = new SpeechSynthesisUtterance(el.innerText.slice(0, 400));
  utt.lang   = { en: 'en-IN', hi: 'hi-IN', mr: 'mr-IN' }[lang] || 'en-IN';
  utt.rate   = 0.9;
  window.speechSynthesis.speak(utt);
}

/* ── VOICE INPUT ──────────────────────────────────────── */
function toggleVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    document.getElementById('vstatus').textContent =
      'Voice not supported. Use Chrome browser.';
    return;
  }
  if (isRec) { stopVoice(); return; }
  const r = new SR();
  recog   = r;
  r.lang  = { en: 'en-IN', hi: 'hi-IN', mr: 'mr-IN' }[lang] || 'en-IN';
  r.onstart  = () => {
    isRec = true;
    document.getElementById('micBtn').classList.add('rec');
    document.getElementById('vstatus').textContent = '🎤 Listening...';
  };
  r.onresult = (e) => {
    const t = Array.from(e.results).map(r => r[0].transcript).join('');
    document.getElementById('inp').value = t;
    if (e.results[e.results.length - 1].isFinal) { stopVoice(); send(); }
  };
  r.onerror = () => stopVoice();
  r.onend   = () => stopVoice();
  r.start();
}

function stopVoice() {
  isRec = false;
  document.getElementById('micBtn').classList.remove('rec');
  document.getElementById('vstatus').textContent = '';
  try { recog && recog.stop(); } catch (e) {}
}

/* ── SIDEBAR ───────────────────────────────────────── */
function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  const bd = document.getElementById('sbBackdrop');
  const hb = document.getElementById('hambtn');
  const open = sb.classList.contains('open');
  sb.classList.toggle('open', !open);
  bd.classList.toggle('open', !open);
  hb.classList.toggle('open', !open);
}
function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sbBackdrop').classList.remove('open');
  document.getElementById('hambtn').classList.remove('open');
}

/* Set language from sidebar — syncs langbar too */
function setSbLang(l, btn) {
  closeSidebar();
  setLang(l);
}
function openHistorySb() {
  closeSidebar();
  const panel = document.getElementById('historyPanel');
  // Always show the panel and refresh content with latest data
  panel.style.display = 'flex';
  refreshHistoryPanel();
}
function openWeatherSb() {
  closeSidebar();
  const panel = document.getElementById('weatherPanel');
  const isOpen = panel.style.display !== 'none';
  if (isOpen) { closeWeatherSb(); return; }
  panel.style.display = 'flex';
  fetchWeather();
}
function closeWeatherSb() {
  document.getElementById('weatherPanel').style.display = 'none';
}

/* ── WEATHER & CROP ADVISOR ─────────────────────────── */
const WMO_DESC = {
  0:'Clear sky',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',
  45:'Foggy',48:'Icy fog',51:'Light drizzle',53:'Moderate drizzle',55:'Heavy drizzle',
  61:'Light rain',63:'Moderate rain',65:'Heavy rain',
  71:'Light snow',73:'Moderate snow',75:'Heavy snow',
  80:'Light showers',81:'Moderate showers',82:'Heavy showers',
  95:'Thunderstorm',96:'Thunderstorm + hail',99:'Thunderstorm + heavy hail',
};
const WMO_ICON = {
  0:'☀️',1:'🌤️',2:'⛅',3:'☁️',45:'🌫️',48:'🌫️',
  51:'🌦️',53:'🌦️',55:'🌧️',61:'🌧️',63:'🌧️',65:'⛈️',
  71:'🌨️',73:'❄️',75:'❄️',80:'🌦️',81:'🌧️',82:'⛈️',
  95:'⛈️',96:'⛈️',99:'⛈️',
};

function getCropRecommendations(maxTemp, minTemp, rainMm, month) {
  const avg = (maxTemp + minTemp) / 2;
  // Seasons: Kharif Jun-Oct, Rabi Nov-Feb, Zaid Mar-May
  const season = (month >= 5 && month <= 9) ? 'kharif'
               : (month >= 10 || month <= 1) ? 'rabi'
               : 'zaid';
  let crops;
  if (season === 'kharif') {
    if (avg >= 28 && rainMm > 3)
      crops = ['🌾 Rice','🌽 Maize','🪘 Soybean','🌱 Cotton','🌿 Tur/Arhar'];
    else if (avg >= 28)
      crops = ['🌾 Bajra (Millet)','🌿 Jowar (Sorghum)','🥜 Groundnut','🌱 Cotton'];
    else
      crops = ['🪘 Moong','🌿 Urad','🌽 Maize','🌻 Sunflower'];
  } else if (season === 'rabi') {
    if (avg < 20)
      crops = ['🌾 Wheat','🪘 Chickpea (Gram)','🧅 Mustard','🥔 Potato','🧅 Peas'];
    else
      crops = ['🧅 Onion','🧄 Garlic','🌿 Coriander','🌻 Sunflower','🪘 Lentil'];
  } else {
    crops = ['🍉 Watermelon','🍈 Muskmelon','🥒 Cucumber','🌿 Summer Veg','🪘 Summer Moong'];
  }
  if (rainMm > 20) {
    crops = crops.filter(c => !['Potato','Onion'].some(x => c.includes(x)));
    if (!crops.some(c => c.includes('Rice'))) crops.unshift('🌾 Rice');
  }
  const seasonLabel = { kharif:'🌧️ Kharif', rabi:'❄️ Rabi', zaid:'☀️ Zaid' }[season];
  return { crops, seasonLabel };
}

async function fetchWeather() {
  const body = document.getElementById('weatherBody');
  body.innerHTML = '<div style="text-align:center;padding:24px;color:rgba(255,255,255,.45)">📍 Detecting your location…</div>';
  if (!navigator.geolocation) {
    body.innerHTML = '<div style="color:#ff7b79;padding:16px">❌ Geolocation not supported in this browser.</div>';
    return;
  }
  navigator.geolocation.getCurrentPosition(async pos => {
    const { latitude: lat, longitude: lon } = pos.coords;
    try {
      const [wRes, gRes] = await Promise.all([
        fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,weathercode,windspeed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=auto&forecast_days=2`),
        fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`),
      ]);
      const weather = await wRes.json();
      const geo     = await gRes.json();
      const place   = geo.address?.city || geo.address?.town || geo.address?.village || geo.address?.county || 'Your Location';
      renderWeather(weather, place);
    } catch(e) {
      body.innerHTML = '<div style="color:#ff7b79;padding:16px">⚠️ Could not load weather data. Check your internet.</div>';
    }
  }, () => {
    body.innerHTML = '<div style="color:rgba(255,255,255,.45);padding:16px;text-align:center">📍 Location access denied.<br><small>Allow location to see live weather.</small></div>';
  });
}

function renderWeather(data, place) {
  const body  = document.getElementById('weatherBody');
  const curr  = data.current;
  const daily = data.daily;
  const month = new Date().getMonth();
  const { crops, seasonLabel } = getCropRecommendations(
    daily.temperature_2m_max[0], daily.temperature_2m_min[0],
    daily.precipitation_sum[0] || 0, month
  );
  body.innerHTML = `
    <div class="w-location">📍 ${place}</div>
    <div class="w-current">
      <span style="font-size:2.8rem">${WMO_ICON[curr.weathercode] || '🌡️'}</span>
      <div>
        <div class="w-temp">${Math.round(curr.temperature_2m)}°C</div>
        <div class="w-desc">${WMO_DESC[curr.weathercode] || 'Unknown'}</div>
        <div class="w-meta">💧 ${curr.relative_humidity_2m}% &nbsp;💨 ${curr.windspeed_10m} km/h</div>
      </div>
    </div>
    <div class="w-forecast">
      ${['Today','Tomorrow'].map((lbl, i) => `
        <div class="w-day">
          <div class="w-day-lbl">${lbl}</div>
          <div class="w-day-icon">${WMO_ICON[daily.weathercode[i]] || '🌡️'}</div>
          <div class="w-day-temps">${Math.round(daily.temperature_2m_max[i])}° / ${Math.round(daily.temperature_2m_min[i])}°</div>
          <div class="w-day-rain">🌧️ ${(daily.precipitation_sum[i] || 0).toFixed(1)} mm</div>
        </div>`).join('')}
    </div>
    <div class="w-crops-section">
      <div class="w-crops-title">🌱 Recommended Crops — ${seasonLabel} Season</div>
      <div class="w-crops-grid">${crops.map(c => `<span class="w-crop-tag">${c}</span>`).join('')}</div>
      <div class="w-crops-note">Based on today's temperature, rainfall & season</div>
    </div>`;
}

/* ── INITIALISE ───────────────────────────────────────── */
setLang('en');      // load default English chips
loadHistory();     // load previous conversations from server
