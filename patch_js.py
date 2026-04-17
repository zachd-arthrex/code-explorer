with open(r'C:\Users\ZDominguez\code-explorer\public\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire COMMAND TARGET + BUTTONS section through the Clear button handler
old_js = '''// =============================================
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
});'''

new_js = '''// =============================================
//  DYNAMIC FUNCTIONS + COMMAND ROUTING
// =============================================
let cmdTarget = 'program'; // 'program' | 'f1' | 'f2' ...
let fnCounter = 0;         // increments for unique fn IDs

function setTarget(target) {
  cmdTarget = target;
  // Show dock only in program mode
  document.getElementById('cmd-dock-row').style.display = target === 'program' ? '' : 'none';
  document.getElementById('cmd-label').textContent = target === 'program' ? 'Commands' : `Add to ${target.toUpperCase()}`;
  // Highlight active panel
  document.querySelectorAll('.list-panel').forEach(p => {
    p.classList.toggle('list-panel-active', p.dataset.target === target);
  });
}

function addFunction() {
  fnCounter++;
  const fnId = 'f' + fnCounter;
  state.fnDefs[fnId] = [];
  renderFnPanels();
  renderFnCallBtns();
  setTarget(fnId);
}

function removeFunction(fnId) {
  delete state.fnDefs[fnId];
  // Remove any calls to this fn from queue
  state.queue = state.queue.filter(item => !(item.type === 'call' && item.fn === fnId));
  if (cmdTarget === fnId) setTarget('program');
  renderFnPanels();
  renderFnCallBtns();
  renderQueue();
  updateStepCounter();
}

function renderFnPanels() {
  const area = document.getElementById('fn-panels-area');
  area.innerHTML = '';
  const fnIds = Object.keys(state.fnDefs);
  fnIds.forEach(fnId => {
    const panel = document.createElement('div');
    panel.className = 'list-panel' + (cmdTarget === fnId ? ' list-panel-active' : '');
    panel.dataset.target = fnId;

    const header = document.createElement('div');
    header.className = 'list-header list-header-fn';
    header.dataset.target = fnId;
    const label = fnId.toUpperCase();
    header.innerHTML = `<span>\\u0192 ${label}</span><button class="fn-remove-btn" data-fn="${fnId}">\\u2715 Remove</button>`;
    header.addEventListener('click', (e) => {
      if (e.target.classList.contains('fn-remove-btn')) return;
      setTarget(fnId);
    });
    header.querySelector('.fn-remove-btn').addEventListener('click', () => removeFunction(fnId));
    panel.appendChild(header);

    // Function steps area
    const stepsArea = document.createElement('div');
    stepsArea.className = 'fn-steps-area';
    stepsArea.style.cssText = 'padding: 4px 10px 6px; display: flex; flex-wrap: wrap; gap: 3px; min-height: 22px;';
    if (state.fnDefs[fnId].length === 0) {
      stepsArea.innerHTML = '<em class="fn-empty">empty — select ' + label + ' above then add commands</em>';
    } else {
      state.fnDefs[fnId].forEach((cmd, ci) => {
        const chip = document.createElement('span');
        chip.className = 'fn-step-chip';
        chip.title = 'Click to remove';
        chip.textContent = cmdShort(cmd);
        chip.style.cursor = 'pointer';
        chip.addEventListener('click', () => {
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
  const area = document.getElementById('fn-call-btns');
  area.innerHTML = '';
  const fnIds = Object.keys(state.fnDefs);
  if (fnIds.length === 0) { area.style.display = 'none'; return; }
  area.style.display = '';
  fnIds.forEach(fnId => {
    const btn = document.createElement('button');
    btn.className = 'fn-call-btn';
    btn.textContent = fnId.toUpperCase();
    btn.title = `Insert ${fnId.toUpperCase()} call into program`;
    btn.addEventListener('click', () => {
      if (state.running) return;
      state.queue.push({ type: 'call', fn: fnId });
      renderQueue();
      updateStepCounter();
    });
    area.appendChild(btn);
  });
}

// Program header click → target program
document.getElementById('panel-program').querySelector('.list-header').addEventListener('click', () => {
  setTarget('program');
});

// Add Function button
document.getElementById('btn-add-fn').addEventListener('click', () => {
  if (state.running) return;
  addFunction();
});

// Command buttons route to active target
document.querySelectorAll('.cmd-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (state.running) return;
    if (cmdTarget === 'program') {
      state.queue.push({ type: 'cmd', cmd: btn.dataset.cmd });
      renderQueue();
    } else {
      state.fnDefs[cmdTarget].push(btn.dataset.cmd);
      renderFnPanels();
      renderQueue();
    }
    updateStepCounter();
  });
});

// Clear
document.getElementById('btn-clear').addEventListener('click', () => {
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
  renderFnPanels();
  renderFnCallBtns();
  renderGrid();
  renderQueue();
  updateStepCounter();
});'''

assert old_js in content, "Could not find old JS block"
content = content.replace(old_js, new_js)

with open(r'C:\Users\ZDominguez\code-explorer\public\index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("JS replacement OK")
