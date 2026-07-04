path = r'c:\Users\sharvil deshmukh\OneDrive\Desktop\Desktop\SHARVIL PROJECT\Kisanmitr\static\js\app.js'
with open(path, encoding='utf-8') as f:
    src = f.read()

# Detect line ending
lf = '\r\n' if '\r\n' in src else '\n'

# ---- PATCH 1: tag user messages in loadHistory ----
# Find forEach line dynamically
import re
m1 = re.search(r'(    data\.history\.forEach\(m =>[^\n]*\n      appendMsg\(m\.user_message, .user., m\.timestamp\);)', src)
if m1:
    old1 = m1.group(0)
    new1 = old1.replace(
        "data.history.forEach(m =>",
        "data.history.forEach((m, i) =>"
    ).replace(
        "appendMsg(m.user_message, 'user', m.timestamp);",
        "appendMsg(m.user_message, 'user', m.timestamp, 'hist-msg-' + i);"
    )
    src = src.replace(old1, new1, 1)
    print('PATCH 1 OK')
else:
    print('PATCH 1 FAIL - trying broader search')
    idx = src.find("data.history.forEach")
    print(repr(src[idx:idx+200]))

# ---- PATCH 2: replace toggleHistory function ----
toggle_start = src.find('async function toggleHistory()')
if toggle_start == -1:
    print('toggleHistory not found!')
else:
    # Find the closing brace of this function
    brace_depth = 0
    i = toggle_start
    in_func = False
    while i < len(src):
        c = src[i]
        if c == '{':
            brace_depth += 1
            in_func = True
        elif c == '}':
            brace_depth -= 1
            if in_func and brace_depth == 0:
                func_end = i + 1
                break
        i += 1
    
    old_func = src[toggle_start:func_end]
    
    new_func = r"""async function toggleHistory() {
  const panel = document.getElementById('historyPanel');
  const isOpen = panel.style.display !== 'none';
  if (isOpen) {
    panel.style.display = 'none';
    document.body.style.overflow = '';
    return;
  }
  panel.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  const listEl = document.getElementById('histList');
  listEl.innerHTML = '<div style="text-align:center;padding:32px;color:rgba(255,255,255,.4)">🔄 Loading history…</div>';
  try {
    const res  = await fetch('/history');
    const data = await res.json();
    if (!data.history || data.history.length === 0) {
      listEl.innerHTML = `<div style="text-align:center;padding:48px;color:rgba(255,255,255,.35)">
        <div style="font-size:2.5rem;margin-bottom:12px">📜</div>
        <div>No chat history yet.</div>
        <div style="font-size:.7rem;margin-top:6px">Start chatting to build your history!</div>
      </div>`;
      return;
    }
    listEl.innerHTML = data.history.map((m, i) => `
      <div class='hist-card' onclick='jumpToHistory(${i})'>
        <div class='hist-q'>👨‍🌾 ${m.user_message}</div>
        <div class='hist-a'>🌾 ${m.bot_response.slice(0, 200)}${m.bot_response.length > 200 ? '…' : ''}</div>
        <div class='hist-ts'>
          <span>${m.timestamp}</span>
          <span class='hist-goto'>🔍 View in chat →</span>
        </div>
      </div>
    `).join('');
  } catch (e) {
    listEl.innerHTML = '<div style="color:#ff7b79;padding:16px">⚠️ Failed to load history.</div>';
  }
}

/* Jump to a specific history message in the chat */
function jumpToHistory(idx) {
  const panel = document.getElementById('historyPanel');
  panel.style.display = 'none';
  document.body.style.overflow = '';
  const target = document.getElementById('hist-msg-' + idx);
  if (!target) return;
  target.scrollIntoView({ behavior: 'smooth', block: 'center' });
  target.classList.add('hist-highlight');
  setTimeout(() => target.classList.remove('hist-highlight'), 2200);
}"""

    src = src.replace(old_func, new_func, 1)
    print('PATCH 2 OK - toggleHistory replaced')

with open(path, 'w', encoding='utf-8') as f:
    f.write(src)
print('File saved successfully.')
