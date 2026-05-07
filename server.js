const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.json());

const MAX_LEVEL = 21;
const STATE_FILE = path.join(__dirname, 'state.json');

// --- State persistence ---
function saveState() {
  try {
    const data = { levelLocks: state.levelLocks, teams: state.teams, challengeSets: state.challengeSets };
    fs.writeFileSync(STATE_FILE, JSON.stringify(data), 'utf8');
  } catch (e) { /* ignore write errors */ }
}

function loadState() {
  try {
    if (fs.existsSync(STATE_FILE)) {
      const data = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
      if (data.levelLocks) state.levelLocks = data.levelLocks;
      if (data.teams) {
        state.teams = data.teams;
        // Mark all teams as disconnected on load (they'll reconnect via WS)
        Object.values(state.teams).forEach(t => { t.connected = false; });
      }
      if (data.challengeSets) state.challengeSets = data.challengeSets;
      return true;
    }
  } catch (e) { /* ignore read errors, use defaults */ }
  return false;
}

// --- In-memory state ---
let state = {
  levelLocks: {},
  teams: {},
  challengeSets: [
    { id: 1, name: 'Challenge 1', levels: [4, 5], active: false },
    { id: 2, name: 'Challenge 2', levels: [7, 8, 9], active: false },
    { id: 3, name: 'Challenge 3', levels: [12,13,14,15,16,17,18,19,20,21], active: false },
  ],
};

// Initialize default locks
for (let i = 1; i <= MAX_LEVEL; i++) {
  state.levelLocks[i] = false;
}

// Try to restore saved state
loadState();

// Compute which levels are unlocked (individual locks + active challenge sets)
function getUnlockedLevels() {
  const unlocked = {};
  for (let i = 1; i <= MAX_LEVEL; i++) {
    unlocked[i] = !!state.levelLocks[i];
  }
  state.challengeSets.forEach(cs => {
    if (cs.active) {
      cs.levels.forEach(id => { unlocked[id] = true; });
    }
  });
  return unlocked;
}

// --- Broadcast helpers ---
function broadcast(data) {
  const msg = JSON.stringify(data);
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) client.send(msg);
  });
}

function broadcastState() {
  broadcast({ type: 'state:unlock', unlockedLevels: getUnlockedLevels(), challengeSets: state.challengeSets });
  saveState();
}

// --- REST API for teacher dashboard ---
app.get('/api/state', (req, res) => {
  res.json({
    levelLocks: state.levelLocks,
    teams: state.teams,
    challengeSets: state.challengeSets,
    unlockedLevels: getUnlockedLevels(),
  });
});

app.post('/api/levels/lock', (req, res) => {
  const { level, locked } = req.body;
  const lvl = parseInt(level, 10);
  if (lvl >= 1 && lvl <= MAX_LEVEL) {
    state.levelLocks[lvl] = !locked;
    broadcastState();
  }
  res.json({ levelLocks: state.levelLocks, unlockedLevels: getUnlockedLevels() });
});

app.post('/api/levels/unlock-range', (req, res) => {
  const { from, to } = req.body;
  for (let i = parseInt(from, 10); i <= parseInt(to, 10); i++) {
    if (i >= 1 && i <= MAX_LEVEL) state.levelLocks[i] = true;
  }
  broadcastState();
  res.json({ levelLocks: state.levelLocks, unlockedLevels: getUnlockedLevels() });
});

app.post('/api/levels/lock-range', (req, res) => {
  const { from, to } = req.body;
  for (let i = parseInt(from, 10); i <= parseInt(to, 10); i++) {
    if (i >= 1 && i <= MAX_LEVEL) state.levelLocks[i] = false;
  }
  broadcastState();
  res.json({ levelLocks: state.levelLocks, unlockedLevels: getUnlockedLevels() });
});

// Toggle all levels in a challenge set (lock or unlock as a group)
app.post('/api/challenge/toggle-lock', (req, res) => {
  const { id, unlock } = req.body;
  const cs = state.challengeSets.find(c => c.id === id);
  if (!cs) return res.status(404).json({ error: 'not found' });
  cs.levels.forEach(lvl => { if (lvl >= 1 && lvl <= MAX_LEVEL) state.levelLocks[lvl] = !!unlock; });
  broadcastState();
  res.json({ levelLocks: state.levelLocks, unlockedLevels: getUnlockedLevels() });
});

app.post('/api/reset', (req, res) => {
  state.teams = {};
  for (let i = 1; i <= MAX_LEVEL; i++) state.levelLocks[i] = false;
  state.challengeSets.forEach(cs => { cs.active = false; });
  broadcast({ type: 'state:reset' });
  saveState();
  res.json({ ok: true });
});

// Delete a team entirely
app.post('/api/team/delete', (req, res) => {
  const name = (req.body.name || '').trim();
  if (!name || !state.teams[name]) return res.status(404).json({ error: 'Team not found' });
  // Disconnect their websocket if active
  wss.clients.forEach(client => {
    if (client.teamName === name && client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({ type: 'state:reset' }));
      client.teamName = null;
    }
  });
  delete state.teams[name];
  broadcastState();
  res.json({ ok: true });
});

// Reset a team's progress (keep connection, clear stats)
app.post('/api/team/reset', (req, res) => {
  const name = (req.body.name || '').trim();
  if (!name || !state.teams[name]) return res.status(404).json({ error: 'Team not found' });
  state.teams[name].completedLevels = [];
  state.teams[name].levelStats = {};
  state.teams[name].currentLevel = 1;
  // Tell their client to reload state
  wss.clients.forEach(client => {
    if (client.teamName === name && client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({
        type: 'team:registered',
        team: state.teams[name],
        unlockedLevels: getUnlockedLevels(),
      }));
    }
  });
  broadcastState();
  res.json({ ok: true });
});

// --- WebSocket ---
wss.on('connection', (ws) => {
  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw); } catch { return; }

    switch (msg.type) {
      case 'team:register': {
        const name = (msg.name || '').trim().substring(0, 32);
        if (!name) return;
        const rejoin = !!msg.rejoin;

        if (rejoin) {
          // Rejoin: team must already exist
          if (!state.teams[name]) {
            ws.send(JSON.stringify({ type: 'team:register:fail', reason: 'No team found with that name. Use "New Team" to create one.' }));
            return;
          }
          // Kick any old sessions with this name
          wss.clients.forEach(client => {
            if (client !== ws && client.readyState === WebSocket.OPEN && client.teamName === name) {
              client.send(JSON.stringify({ type: 'team:kicked', reason: 'Your team logged in from another device.' }));
              client.teamName = null;
            }
          });
        } else {
          // New team: name must NOT already exist
          if (state.teams[name]) {
            ws.send(JSON.stringify({ type: 'team:register:fail', reason: 'That team name already exists. Use "Rejoin" to reconnect, or pick a different name.' }));
            return;
          }
          state.teams[name] = {
            completedLevels: [],
            currentLevel: 1,
            levelStats: {},
            lastSeen: Date.now(),
            connected: true,
          };
        }

        state.teams[name].lastSeen = Date.now();
        state.teams[name].connected = true;
        ws.teamName = name;
        ws.send(JSON.stringify({
          type: 'team:registered',
          team: state.teams[name],
          unlockedLevels: getUnlockedLevels(),
          challengeSets: state.challengeSets,
        }));
        saveState();
        break;
      }

      case 'team:progress': {
        if (!ws.teamName || !state.teams[ws.teamName]) return;
        const team = state.teams[ws.teamName];
        team.lastSeen = Date.now();
        if (typeof msg.level === 'number') team.currentLevel = msg.level;
        if (Array.isArray(msg.completedLevels)) team.completedLevels = msg.completedLevels;
        // Per-level stats: { levelId: { runsToFirstSolve, bestCommands, runs, commands } }
        if (msg.levelStats) {
          Object.keys(msg.levelStats).forEach(id => {
            const incoming = msg.levelStats[id];
            const existing = team.levelStats[id];
            if (!existing) {
              team.levelStats[id] = {
                runsToFirstSolve: incoming.runsToFirstSolve || incoming.runs || 0,
                bestCommands: incoming.bestCommands || incoming.commands || 0,
                runsToBest: incoming.runsToBest || incoming.runs || 0,
                runs: incoming.runs || 0,
                commands: incoming.commands || 0,
                firstCompleted: Date.now(),
              };
            } else {
              if (incoming.bestCommands && incoming.bestCommands < existing.bestCommands) {
                existing.bestCommands = incoming.bestCommands;
                existing.runsToBest = incoming.runsToBest || incoming.runs || existing.runsToBest;
              }
              existing.runs = incoming.runs || existing.runs;
              existing.commands = incoming.commands || existing.commands;
            }
          });
        }
        saveState();
        break;
      }

      case 'team:ping': {
        ws.send(JSON.stringify({ type: 'state:unlock', unlockedLevels: getUnlockedLevels(), challengeSets: state.challengeSets }));
        break;
      }
    }
  });

  ws.on('close', () => {
    if (ws.teamName && state.teams[ws.teamName]) {
      state.teams[ws.teamName].connected = false;
    }
  });

  // Send current state on connect
  ws.send(JSON.stringify({ type: 'state:unlock', unlockedLevels: getUnlockedLevels(), challengeSets: state.challengeSets }));
});

// --- Static files ---
app.use(express.static(path.join(__dirname, 'public')));
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.get('/teacher', (req, res) => res.sendFile(path.join(__dirname, 'public', 'teacher.html')));

const PORT = process.env.PORT || 3000;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`Code Explorer running on port ${PORT} — accessible on all network interfaces`);
});
