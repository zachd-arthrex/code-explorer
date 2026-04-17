"""
Migrate index.html from fixed Fn A/B target-tabs approach to
dynamic function system with add/remove and F1/F2 call buttons.
"""
import sys

path = r'C:\Users\ZDominguez\code-explorer\public\index.html'
with open(path, 'r', encoding='utf-8') as f:
    t = f.read()

orig_len = len(t)

# ===== 1. CSS: Replace target-tabs + fn-preview + call-btn styles =====

old_css = """.target-tabs { display: flex; gap: 4px; margin-bottom: 6px; }
  .target-tab {
    flex: 1; padding: 6px 4px; border-radius: 7px; border: 2px solid transparent;
    background: rgba(255,255,255,0.06); color: rgba(255,255,255,0.5);
    font-size: 0.75rem; font-weight: 800; cursor: pointer; text-align: center;
    transition: all 0.15s;
  }
  .target-tab:hover { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.8); }
  .target-tab.active { background: var(--accent); color: #fff; border-color: var(--accent); box-shadow: 0 0 10px color-mix(in srgb, var(--glow) 40%, transparent); }
  .target-tab.tab-fn-a.active { background: linear-gradient(180deg,#fbbf24,#d97706); color: #000; border-color: #f59e0b; box-shadow: 0 0 10px rgba(245,158,11,0.4); }
  .target-tab.tab-fn-b.active { background: linear-gradient(180deg,#22d3ee,#0891b2); color: #000; border-color: #06b6d4; box-shadow: 0 0 10px rgba(6,182,212,0.4); }

  /* Function preview cards */
  .fn-previews { padding: 4px 8px; }
  .fn-preview { padding: 5px 8px; border-radius: 6px; margin-bottom: 4px; }
  .fn-preview.fn-a { background: linear-gradient(135deg, rgba(245,158,11,0.12) 0%, transparent 60%); border: 1px solid rgba(245,158,11,0.25); }
  .fn-preview.fn-b { background: linear-gradient(135deg, rgba(6,182,212,0.12) 0%, transparent 60%); border: 1px solid rgba(6,182,212,0.25); }
  .fn-preview-header { display: flex; align-items: center; gap: 6px; font-size: 0.78rem; }
  .fn-preview-label { font-weight: 800; flex-shrink: 0; }
  .fn-preview.fn-a .fn-preview-label { color: #fcd34d; }
  .fn-preview.fn-b .fn-preview-label { color: #67e8f9; }
  .fn-preview-steps { display: flex; flex-wrap: wrap; gap: 3px; flex: 1; min-height: 18px; align-items: center; }

  /* Call buttons */
  .call-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-top: 6px; }
  .call-btn {
    padding: 8px 4px; border-radius: 8px; border: none; font-size: 0.8rem; font-weight: 800;
    cursor: pointer; text-align: center; position: relative; top: 0; transition: all 0.1s;
  }
  .call-a {
    background: linear-gradient(180deg, #fbbf24 0%, #d97706 100%);
    color: #000; box-shadow: 0 4px 0 #92400e, 0 0 10px rgba(245,158,11,0.3);
  }
  .call-a:hover { filter: brightness(1.1); top: -1px; box-shadow: 0 5px 0 #92400e, 0 0 18px rgba(245,158,11,0.5); }
  .call-a:active { top: 3px; box-shadow: 0 1px 0 #92400e; }
  .call-b {
    background: linear-gradient(180deg, #22d3ee 0%, #0891b2 100%);
    color: #000; box-shadow: 0 4px 0 #164e63, 0 0 10px rgba(6,182,212,0.3);
  }
  .call-b:hover { filter: brightness(1.1); top: -1px; box-shadow: 0 5px 0 #164e63, 0 0 18px rgba(6,182,212,0.5); }
  .call-b:active { top: 3px; box-shadow: 0 1px 0 #164e63; }"""

new_css = """/* Dynamic function call buttons (F1, F2, ...) */
  .fn-call-btns { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 6px; }
  .fn-call-btn {
    flex: 1; min-width: 55px; padding: 8px 4px; border-radius: 8px; border: none;
    font-size: 0.8rem; font-weight: 800; cursor: pointer; text-align: center;
    position: relative; top: 0; transition: all 0.1s;
    background: linear-gradient(180deg, #a78bfa 0%, #7c3aed 100%);
    color: #fff; box-shadow: 0 4px 0 #4c1d95, 0 0 10px rgba(167,139,250,0.3);
  }
  .fn-call-btn:hover { filter: brightness(1.1); top: -1px; box-shadow: 0 5px 0 #4c1d95, 0 0 18px rgba(167,139,250,0.5); }
  .fn-call-btn:active { top: 3px; box-shadow: 0 1px 0 #4c1d95; }

  /* Add Function button */
  .add-fn-btn {
    width: 100%; padding: 6px; border-radius: 7px; border: 2px dashed rgba(167,139,250,0.4);
    background: transparent; color: rgba(167,139,250,0.7); font-size: 0.78rem; font-weight: 800;
    cursor: pointer; transition: all 0.15s;
  }
  .add-fn-btn:hover { border-color: #a78bfa; color: #a78bfa; background: rgba(167,139,250,0.08); }

  /* List panels (program + function queues) */
  .lists-area { flex: 1; overflow-y: auto; display: flex; flex-direction: column; }
  .list-panel { border-bottom: 1px solid rgba(255,255,255,0.06); }
  .list-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 6px 10px; font-size: 0.82rem; font-weight: 800;
    cursor: pointer; user-select: none; transition: all 0.12s;
    color: rgba(255,255,255,0.5); border-left: 3px solid transparent;
  }
  .list-header:hover { background: rgba(255,255,255,0.04); }
  .list-panel-active > .list-header { color: #fff; }
  .list-panel-active > .list-header-program { background: rgba(99,102,241,0.12); border-left-color: var(--accent); }
  .list-panel-active > .list-header-fn { background: rgba(167,139,250,0.12); border-left-color: #a78bfa; }
  .list-header-fn { color: #c4b5fd; }
  .list-header .fn-remove-btn {
    padding: 1px 6px; border-radius: 4px; border: 1px solid currentColor;
    background: transparent; color: inherit; font-size: 0.65rem; cursor: pointer;
    opacity: 0.5; transition: opacity 0.15s;
  }
  .list-header .fn-remove-btn:hover { opacity: 1; color: var(--danger); border-color: var(--danger); }
  .fn-steps-area { padding: 4px 10px 6px; display: flex; flex-wrap: wrap; gap: 3px; min-height: 22px; }"""

assert old_css in t, "CSS block not found"
t = t.replace(old_css, new_css, 1)

# ===== 2. CSS: Replace call-a-item/call-b-item with fn-call-item =====
old_callcss = """.queue-item.call-a-item { border-color: #f59e0b; background: linear-gradient(180deg, rgba(251,191,36,0.18) 0%, rgba(251,191,36,0.08) 100%); }
  .queue-item.call-b-item { border-color: #06b6d4; background: linear-gradient(180deg, rgba(34,211,238,0.18) 0%, rgba(34,211,238,0.08) 100%); }
  .queue-item.call-a-item.active-step { background: linear-gradient(180deg,#fbbf24,#d97706); color:#000; box-shadow: 0 0 14px rgba(245,158,11,0.6); }
  .queue-item.call-b-item.active-step { background: linear-gradient(180deg,#22d3ee,#0891b2); color:#000; box-shadow: 0 0 14px rgba(6,182,212,0.6); }"""

new_callcss = """.queue-item.fn-call-item { border-color: #a78bfa; background: linear-gradient(180deg, rgba(167,139,250,0.18) 0%, rgba(167,139,250,0.08) 100%); }
  .queue-item.fn-call-item.active-step { background: linear-gradient(180deg,#a78bfa,#7c3aed); color:#fff; box-shadow: 0 0 14px rgba(167,139,250,0.6); }"""

assert old_callcss in t, "Call item CSS not found"
t = t.replace(old_callcss, new_callcss, 1)

# ===== 3. CSS: Replace fn-a/fn-b step chips with single style =====
old_chips = """.fn-a .fn-step-chip { background: linear-gradient(180deg,#fbbf24,#d97706); color:#000; box-shadow: 0 2px 0 #78350f; }
  .fn-b .fn-step-chip { background: linear-gradient(180deg,#22d3ee,#0891b2); color:#000; box-shadow: 0 2px 0 #164e63; }"""

new_chips = """.fn-step-chip { background: linear-gradient(180deg,#a78bfa,#7c3aed); color:#fff; box-shadow: 0 2px 0 #4c1d95; }"""

assert old_chips in t, "Step chip CSS not found"
t = t.replace(old_chips, new_chips, 1)

# ===== 4. HTML: Replace sidebar from target-tabs through queue-area + actions =====
old_html = """      <div class="sidebar-section">
        <div id="target-tabs" class="target-tabs" style="display:none">
          <button class="target-tab active" data-target="program">Program</button>
          <button class="target-tab tab-fn-a" data-target="a">Fn A</button>
          <button class="target-tab tab-fn-b" data-target="b">Fn B</button>
        </div>
        <div class="sidebar-label" id="cmd-label">Commands</div>
        <div class="cmd-3">
          <button class="cmd-btn" data-cmd="left" title="Turn Left">
            <!-- CCW rotate arrow -->
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1,4 1,10 7,10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-5"/>
            </svg>
            Left
          </button>
          <button class="cmd-btn" data-cmd="forward" title="Go Forward">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="19" x2="12" y2="5"/>
              <polyline points="5,12 12,5 19,12"/>
            </svg>
            Fwd
          </button>
          <button class="cmd-btn" data-cmd="right" title="Turn Right">
            <!-- CW rotate arrow -->
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23,4 23,10 17,10"/>
              <path d="M20.49 15a9 9 0 1 1-.49-5"/>
            </svg>
            Right
          </button>
        </div>
        <div class="cmd-dock" id="cmd-dock-row">
          <button class="cmd-btn dock-btn" data-cmd="dock" title="Dock at station">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="14" width="16" height="6" rx="2"/>
              <line x1="12" y1="3" x2="12" y2="14"/>
              <polyline points="8,10 12,14 16,10"/>
            </svg>
            Dock
          </button>
        </div>
        <div id="call-section" style="display:none">
          <div class="call-btns">
            <button class="call-btn call-a" id="call-a-main">Call A</button>
            <button class="call-btn call-b" id="call-b-main">Call B</button>
          </div>
        </div>
      </div>

      <div id="fn-previews" class="fn-previews" style="display:none">
        <div class="fn-preview fn-a" id="fn-preview-a">
          <div class="fn-preview-header">
            <span class="fn-preview-label">Fn A:</span>
            <span class="fn-preview-steps" id="fn-a-preview-steps"><em class="fn-empty">empty</em></span>
            <button class="fn-clear-btn" data-fn="a">Clear</button>
          </div>
        </div>
        <div class="fn-preview fn-b" id="fn-preview-b">
          <div class="fn-preview-header">
            <span class="fn-preview-label">Fn B:</span>
            <span class="fn-preview-steps" id="fn-b-preview-steps"><em class="fn-empty">empty</em></span>
            <button class="fn-clear-btn" data-fn="b">Clear</button>
          </div>
        </div>
      </div>

      <div class="sidebar-label" style="padding:8px 10px 0;">My Program</div>
      <div class="queue-area" id="queue-area"></div>

      <div class="queue-actions">"""

new_html = """      <div class="sidebar-section">
        <div class="sidebar-label" id="cmd-label">Commands</div>
        <div class="cmd-3">
          <button class="cmd-btn" data-cmd="left" title="Turn Left">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="1,4 1,10 7,10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-5"/>
            </svg>
            Left
          </button>
          <button class="cmd-btn" data-cmd="forward" title="Go Forward">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="19" x2="12" y2="5"/>
              <polyline points="5,12 12,5 19,12"/>
            </svg>
            Fwd
          </button>
          <button class="cmd-btn" data-cmd="right" title="Turn Right">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23,4 23,10 17,10"/>
              <path d="M20.49 15a9 9 0 1 1-.49-5"/>
            </svg>
            Right
          </button>
        </div>
        <div class="cmd-dock" id="cmd-dock-row">
          <button class="cmd-btn dock-btn" data-cmd="dock" title="Dock at station">
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="14" width="16" height="6" rx="2"/>
              <line x1="12" y1="3" x2="12" y2="14"/>
              <polyline points="8,10 12,14 16,10"/>
            </svg>
            Dock
          </button>
        </div>
        <div id="fn-call-btns" class="fn-call-btns" style="display:none"></div>
      </div>

      <div class="lists-area" id="lists-area">
        <div class="list-panel list-panel-active" id="panel-program" data-target="program">
          <div class="list-header list-header-program" data-target="program">
            <span>&#9654; My Program</span>
          </div>
          <div class="queue-area" id="queue-area"></div>
        </div>
        <div id="fn-panels-area"></div>
        <div id="add-fn-row" style="display:none; padding: 4px 8px;">
          <button class="add-fn-btn" id="btn-add-fn">+ Add Function</button>
        </div>
      </div>

      <div class="queue-actions">"""

assert old_html in t, "HTML block not found"
t = t.replace(old_html, new_html, 1)

# ===== 5. State: Replace fnDefs =====
t = t.replace("fnDefs: { a: [], b: [] },", "fnDefs: {},  // dynamic: { f1: [], f2: [], ... }", 1)

# ===== 6. startLevel: Replace fn visibility =====
old_start = """// Function UI
  document.getElementById('target-tabs').style.display  = lvl.functionsUnlocked ? '' : 'none';
  document.getElementById('fn-previews').style.display  = lvl.functionsUnlocked ? '' : 'none';
  cmdTarget = 'program';
  setTarget('program');"""

new_start = """// Function UI
  document.getElementById('add-fn-row').style.display = lvl.functionsUnlocked ? '' : 'none';
  document.getElementById('fn-call-btns').style.display = 'none';
  document.getElementById('fn-panels-area').innerHTML = '';
  state.fnDefs = {};
  fnCounter = 0;
  cmdTarget = 'program';
  setTarget('program');"""

assert old_start in t, "startLevel fn block not found"
t = t.replace(old_start, new_start, 1)

# ===== 7. renderFnDefs: Replace entirely =====
old_render_fn = """function renderFnDefs() {
  ['a','b'].forEach(fn => {
    const steps = document.getElementById(`fn-${fn}-preview-steps`);
    if (!steps) return;
    steps.innerHTML = '';
    if (state.fnDefs[fn].length === 0) {
      steps.innerHTML = '<em class="fn-empty">empty</em>';
    } else {
      state.fnDefs[fn].forEach((cmd, ci) => {
        const chip = document.createElement('span');
        chip.className = 'fn-step-chip';
        chip.title = 'Click to remove';
        chip.textContent = cmdShort(cmd);
        chip.style.cursor = 'pointer';
        chip.addEventListener('click', () => {
          state.fnDefs[fn].splice(ci, 1);
          renderFnDefs();
          renderQueue();
          updateStepCounter();
        });
        steps.appendChild(chip);
      });
    }
  });
}"""

new_render_fn = """function renderFnDefs() {
  // no-op: fn panels rendered by renderFnPanels
}"""

assert old_render_fn in t, "renderFnDefs function not found"
t = t.replace(old_render_fn, new_render_fn, 1)

# ===== 8. JS: Replace COMMAND TARGET through Clear handler =====
old_js = """// =============================================
//  COMMAND TARGET + BUTTONS
// =============================================
let cmdTarget = 'program'; // 'program' | 'a' | 'b'

function setTarget(target) {
  cmdTarget = target;
  document.querySelectorAll('.target-tab').forEach(t => t.classList.toggle('active', t.dataset.target === target));
  // Show dock & call buttons only in program mode
  document.getElementById('cmd-dock-row').style.display = target === 'program' ? '' : 'none';
  document.getElementById('call-section').style.display =
    (target === 'program' && state.currentLevel && state.currentLevel.functionsUnlocked) ? '' : 'none';
  document.getElementById('cmd-label').textContent = target === 'program' ? 'Commands' : `Add to Fn ${target.toUpperCase()}`;
}

document.querySelectorAll('.target-tab').forEach(tab => {
  tab.addEventListener('click', () => setTarget(tab.dataset.target));
});

document.querySelectorAll('.cmd-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (state.running) return;
    if (cmdTarget === 'program') {
      state.queue.push({ type: 'cmd', cmd: btn.dataset.cmd });
      renderQueue();
    } else {
      state.fnDefs[cmdTarget].push(btn.dataset.cmd);
      renderFnDefs();
      renderQueue(); // update call previews
    }
    updateStepCounter();
  });
});

// Function clear buttons
document.querySelectorAll('.fn-clear-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    state.fnDefs[btn.dataset.fn] = [];
    renderFnDefs();
    renderQueue();
    updateStepCounter();
  });
});

// Call A / Call B buttons
document.getElementById('call-a-main').addEventListener('click', () => {
  if (state.running) return;
  state.queue.push({ type: 'call', fn: 'a' });
  renderQueue();
  updateStepCounter();
});
document.getElementById('call-b-main').addEventListener('click', () => {
  if (state.running) return;
  state.queue.push({ type: 'call', fn: 'b' });
  renderQueue();
  updateStepCounter();
});
// Clear
document.getElementById('btn-clear').addEventListener('click', () => {
  if (state.running) return;
  state.queue = [];
  state.fnDefs = { a: [], b: [] };
  state.facing = state.currentLevel.startDir;
  state.playerPos = [...state.currentLevel.player];
  state.collectedSet = new Set();
  state.collectAnims = [];
  setTarget('program');
  renderGrid();
  renderQueue();
  renderFnDefs();
  updateStepCounter();
});"""

new_js = """// =============================================
//  DYNAMIC FUNCTIONS + COMMAND ROUTING
// =============================================
let cmdTarget = 'program';
let fnCounter = 0;

function setTarget(target) {
  cmdTarget = target;
  document.getElementById('cmd-dock-row').style.display = target === 'program' ? '' : 'none';
  document.getElementById('cmd-label').textContent = target === 'program' ? 'Commands' : 'Add to ' + target.toUpperCase();
  document.querySelectorAll('.list-panel').forEach(function(p) {
    p.classList.toggle('list-panel-active', p.dataset.target === target);
  });
}

function addFunction() {
  fnCounter++;
  var fnId = 'f' + fnCounter;
  state.fnDefs[fnId] = [];
  renderFnPanels();
  renderFnCallBtns();
  setTarget(fnId);
}

function removeFunction(fnId) {
  delete state.fnDefs[fnId];
  state.queue = state.queue.filter(function(item) { return !(item.type === 'call' && item.fn === fnId); });
  if (cmdTarget === fnId) setTarget('program');
  renderFnPanels();
  renderFnCallBtns();
  renderQueue();
  updateStepCounter();
}

function renderFnPanels() {
  var area = document.getElementById('fn-panels-area');
  area.innerHTML = '';
  var fnIds = Object.keys(state.fnDefs);
  fnIds.forEach(function(fnId) {
    var panel = document.createElement('div');
    panel.className = 'list-panel' + (cmdTarget === fnId ? ' list-panel-active' : '');
    panel.dataset.target = fnId;

    var header = document.createElement('div');
    header.className = 'list-header list-header-fn';
    header.dataset.target = fnId;
    var label = fnId.toUpperCase();
    header.innerHTML = '<span>\\u0192 ' + label + '</span><button class="fn-remove-btn" data-fn="' + fnId + '">\\u2715 Remove</button>';
    header.addEventListener('click', function(e) {
      if (e.target.classList.contains('fn-remove-btn')) return;
      setTarget(fnId);
    });
    header.querySelector('.fn-remove-btn').addEventListener('click', function() { removeFunction(fnId); });
    panel.appendChild(header);

    var stepsArea = document.createElement('div');
    stepsArea.className = 'fn-steps-area';
    if (state.fnDefs[fnId].length === 0) {
      stepsArea.innerHTML = '<em class="fn-empty">empty \\u2014 select ' + label + ' then add commands</em>';
    } else {
      state.fnDefs[fnId].forEach(function(cmd, ci) {
        var chip = document.createElement('span');
        chip.className = 'fn-step-chip';
        chip.title = 'Click to remove';
        chip.textContent = cmdShort(cmd);
        chip.style.cursor = 'pointer';
        chip.addEventListener('click', function() {
          state.fnDefs[fnId].splice(ci, 1);
          renderFnPanels();
          renderQueue();
          updateStepCounter();
        });
        stepsArea.appendChild(chip);
      });
    }
    panel.appendChild(stepsArea);
    area.appendChild(panel);
  });
}

function renderFnCallBtns() {
  var area = document.getElementById('fn-call-btns');
  area.innerHTML = '';
  var fnIds = Object.keys(state.fnDefs);
  if (fnIds.length === 0) { area.style.display = 'none'; return; }
  area.style.display = '';
  fnIds.forEach(function(fnId) {
    var btn = document.createElement('button');
    btn.className = 'fn-call-btn';
    btn.textContent = fnId.toUpperCase();
    btn.title = 'Insert ' + fnId.toUpperCase() + ' call into program';
    btn.addEventListener('click', function() {
      if (state.running) return;
      setTarget('program');
      state.queue.push({ type: 'call', fn: fnId });
      renderQueue();
      updateStepCounter();
    });
    area.appendChild(btn);
  });
}

document.getElementById('panel-program').querySelector('.list-header').addEventListener('click', function() {
  setTarget('program');
});

document.getElementById('btn-add-fn').addEventListener('click', function() {
  if (state.running) return;
  addFunction();
});

document.querySelectorAll('.cmd-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    if (state.running) return;
    if (cmdTarget === 'program') {
      state.queue.push({ type: 'cmd', cmd: btn.dataset.cmd });
      renderQueue();
    } else {
      if (!state.fnDefs[cmdTarget]) return;
      state.fnDefs[cmdTarget].push(btn.dataset.cmd);
      renderFnPanels();
      renderQueue();
    }
    updateStepCounter();
  });
});

// Clear
document.getElementById('btn-clear').addEventListener('click', function() {
  if (state.running) return;
  state.queue = [];
  state.fnDefs = {};
  fnCounter = 0;
  state.facing = state.currentLevel.startDir;
  state.playerPos = [...state.currentLevel.player];
  state.collectedSet = new Set();
  state.collectAnims = [];
  cmdTarget = 'program';
  setTarget('program');
  document.getElementById('fn-panels-area').innerHTML = '';
  document.getElementById('fn-call-btns').innerHTML = '';
  document.getElementById('fn-call-btns').style.display = 'none';
  renderGrid();
  renderQueue();
  updateStepCounter();
});"""

assert old_js in t, "COMMAND TARGET JS block not found"
t = t.replace(old_js, new_js, 1)

# ===== 9. renderQueue: Replace call-a/b-item with fn-call-item =====
old_rq = """    if (item.type === 'call') {
      div.className = `queue-item call-${item.fn}-item`;
      const preview = state.fnDefs[item.fn].map(cmdShort).join('') || '\\u2026';
      div.innerHTML = `${grip}<span style="flex:1">\\u26A1 <b>Call ${item.fn.toUpperCase()}</b> <span class="queue-call-preview">${preview}</span></span><span class="del-btn">\\u2715</span>`;"""

new_rq = """    if (item.type === 'call') {
      div.className = 'queue-item fn-call-item';
      var preview = (state.fnDefs[item.fn] || []).map(cmdShort).join('') || '\\u2026';
      div.innerHTML = grip + '<span style="flex:1">\\u0192 <b>' + item.fn.toUpperCase() + '</b> <span class="queue-call-preview">' + preview + '</span></span><span class="del-btn">\\u2715</span>';"""

assert old_rq in t, "renderQueue call block not found"
t = t.replace(old_rq, new_rq, 1)

# ===== 10. Execution: Update fn expansion =====
t = t.replace(
    "state.fnDefs[item.fn].forEach(cmd => moves.push(cmd));",
    "(state.fnDefs[item.fn] || []).forEach(cmd => moves.push(cmd));"
)

# ===== 11. countSteps: Update =====
t = t.replace(
    "if (item.type === 'call') return sum + Math.max(state.fnDefs[item.fn].length, 1);",
    "if (item.type === 'call') return sum + Math.max((state.fnDefs[item.fn] || []).length, 1);"
)

# ===== 12. highlightStep: Update =====
t = t.replace(
    "const steps = item.type === 'call' ? Math.max(state.fnDefs[item.fn].length, 1) : 1;",
    "const steps = item.type === 'call' ? Math.max((state.fnDefs[item.fn] || []).length, 1) : 1;"
)

# Safety: write to temp file first, verify, then move
import shutil, os
tmp = path + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
    f.write(t)

# Verify temp file
with open(tmp, 'r', encoding='utf-8') as f:
    verify = f.read()
assert len(verify) > 50000, f"Temp file too small: {len(verify)} chars"
assert '<html' in verify, "Missing <html tag"
assert 'renderFnPanels' in verify, "Missing renderFnPanels function"
assert 'addFunction' in verify, "Missing addFunction function"

# Now safe to replace
shutil.move(tmp, path)
print(f"Migration complete. {orig_len} -> {len(t)} chars")
