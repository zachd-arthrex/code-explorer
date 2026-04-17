path = r'C:\Users\ZDominguez\code-explorer\public\index.html'
t = open(path, encoding='utf-8').read()

s = t.index('function renderQueue()')
e = t.index('function updateStepCounter()')

new_fn = r"""function renderQueue() {
  const area = document.getElementById('queue-area');
  area.innerHTML = '';
  area.classList.remove('insert-end');
  if (state.queue.length === 0) {
    area.innerHTML = '<div style="opacity:0.4;font-size:0.8rem;text-align:center;padding:12px;">Add commands above</div>';
    return;
  }

  let dragSrcIdx = null;

  function clearMarkers() {
    area.querySelectorAll('.insert-before').forEach(el => el.classList.remove('insert-before'));
    area.classList.remove('insert-end');
  }

  function markInsert(clientY) {
    clearMarkers();
    const items = [...area.querySelectorAll('.queue-item')];
    for (const item of items) {
      const rect = item.getBoundingClientRect();
      if (clientY < rect.top + rect.height / 2) {
        item.classList.add('insert-before');
        return;
      }
    }
    // Past all items — insert at end
    area.classList.add('insert-end');
  }

  function getDropIdx(clientY) {
    const items = [...area.querySelectorAll('.queue-item')];
    for (const item of items) {
      const rect = item.getBoundingClientRect();
      if (clientY < rect.top + rect.height / 2) return parseInt(item.dataset.qidx);
    }
    return state.queue.length;
  }

  state.queue.forEach((item, idx) => {
    const div = document.createElement('div');
    div.dataset.qidx = idx;
    div.draggable = true;

    const grip = '<span class="drag-grip">\u2630</span>';
    if (item.type === 'call') {
      div.className = `queue-item call-${item.fn}-item`;
      const preview = state.fnDefs[item.fn].map(cmdShort).join('') || '\u2026';
      div.innerHTML = `${grip}<span style="flex:1">\u26A1 <b>Call ${item.fn.toUpperCase()}</b> <span class="queue-call-preview">${preview}</span></span><span class="del-btn">\u2715</span>`;
    } else {
      div.className = 'queue-item';
      div.innerHTML = `${grip}<span style="flex:1">${cmdLabel(item.cmd)}</span><span class="del-btn">\u2715</span>`;
    }

    div.querySelector('.del-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      state.queue.splice(idx, 1);
      renderQueue();
      updateStepCounter();
    });

    div.addEventListener('dragstart', (e) => {
      if (state.running) { e.preventDefault(); return; }
      dragSrcIdx = idx;
      setTimeout(() => div.classList.add('dragging'), 0);
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', String(idx));
    });
    div.addEventListener('dragend', () => {
      div.classList.remove('dragging');
      clearMarkers();
      dragSrcIdx = null;
    });

    area.appendChild(div);
  });

  // Single container-level listeners only — no per-item dragover
  area.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    markInsert(e.clientY);
  });

  area.addEventListener('dragleave', (e) => {
    if (!area.contains(e.relatedTarget)) clearMarkers();
  });

  area.addEventListener('drop', (e) => {
    e.preventDefault();
    clearMarkers();
    const src = parseInt(e.dataTransfer.getData('text/plain'), 10);
    if (isNaN(src)) return;
    let dst = getDropIdx(e.clientY);
    if (src === dst || src + 1 === dst) return;
    const moved = state.queue.splice(src, 1)[0];
    if (src < dst) dst -= 1;
    state.queue.splice(dst, 0, moved);
    renderQueue();
    updateStepCounter();
  });
}

"""

t = t[:s] + new_fn + t[e:]
open(path, 'w', encoding='utf-8', newline='\n').write(t)
print('OK')
