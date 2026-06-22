/**
 * Agy Pomodoro — Premium Focus Timer
 * Core Application Engine
 *
 * Implements:
 * - Anti-drift timing mechanism using Date.now() deltas
 * - Web Audio API chime synthesis (zero external audio files)
 * - State machine control flow with localStorage persistence
 * - Tab-inactivity and sleep/wakeup protection
 * - Fluid HSL state updates and UI interactions
 */

// --- Default Configuration ---
const DEFAULTS = {
  workDuration: 25,       // in minutes
  shortDuration: 5,       // in minutes
  longDuration: 15,       // in minutes
  autoStartBreaks: false,
  autoStartPomodoros: false,
  audioMuted: false
};

// --- Application State Model ---
const state = {
  timerState: 'idle',       // 'idle' | 'running' | 'paused'
  currentMode: 'work',      // 'work' | 'short' | 'long'
  timeLeft: 1500,           // remaining seconds
  totalDuration: 1500,      // base duration of active mode in seconds
  expectedEndTime: null,    // Epoch millisecond target timestamp
  sessionCount: 0,          // Completed focus sessions in the current set (0 to 4)
  settings: { ...DEFAULTS },
  audioMuted: false,
  
  // Historical stats
  stats: {
    totalPomodoros: 0,      // Cumulative lifetime pomodoros
    totalFocusTime: 0       // Cumulative lifetime minutes focused
  }
};

// --- DOM Cache ---
let timerInterval = null;

const DOM = {
  body: document.body,
  
  // Header Actions
  btnMute: document.getElementById('toggle-mute'),
  soundOnIcon: document.getElementById('sound-on-icon'),
  soundOffIcon: document.getElementById('sound-off-icon'),
  btnSettings: document.getElementById('toggle-settings'),
  
  // Tabs
  tabWork: document.getElementById('mode-work'),
  tabShort: document.getElementById('mode-short'),
  tabLong: document.getElementById('mode-long'),
  modeTabs: document.querySelectorAll('.mode-tab'),
  
  // Display
  timerLabel: document.getElementById('timer-label'),
  timerDigits: document.getElementById('timer-digits'),
  timerSublabel: document.getElementById('timer-sublabel'),
  progressCircle: document.querySelector('.timer-ring-progress'),
  
  // Controls
  btnReset: document.getElementById('btn-reset'),
  btnPlayPause: document.getElementById('btn-play-pause'),
  playIcon: document.getElementById('play-icon'),
  pauseIcon: document.getElementById('pause-icon'),
  btnSkip: document.getElementById('btn-skip'),
  
  // Tracker & Stats
  sessionCountText: document.getElementById('session-count-text'),
  capsulesContainer: document.getElementById('capsules-container'),
  statTotalPomodoros: document.getElementById('stat-total-pomodoros'),
  statTotalFocusTime: document.getElementById('stat-total-focus-time'),
  btnResetStats: document.getElementById('btn-reset-stats'),
  
  // Settings Drawer
  drawer: document.getElementById('settings-drawer'),
  drawerOverlay: document.getElementById('drawer-overlay'),
  drawerClose: document.getElementById('close-settings'),
  settingsForm: document.getElementById('settings-form'),
  inputWork: document.getElementById('input-work'),
  inputShort: document.getElementById('input-short'),
  inputLong: document.getElementById('input-long'),
  toggleAutoBreaks: document.getElementById('toggle-auto-breaks'),
  toggleAutoPomodoros: document.getElementById('toggle-auto-pomodoros'),
  btnTestSound: document.getElementById('btn-test-sound'),
  btnRestoreDefaults: document.getElementById('btn-restore-defaults')
};

// --- Sound Synthesis Module (Web Audio API) ---

/**
 * Initializes and synthesizes a focus completed alarm (mellow perfect fifth E5 & B5 chime)
 */
function playFocusBell() {
  if (state.audioMuted) return;
  
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    
    const osc1 = ctx.createOscillator();
    const osc2 = ctx.createOscillator();
    const gainNode = ctx.createGain();
    
    osc1.connect(gainNode);
    osc2.connect(gainNode);
    gainNode.connect(ctx.destination);
    
    // perfect fifth chime configuration
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(659.25, ctx.currentTime); // E5
    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(987.77, ctx.currentTime); // B5
    
    // Volume Envelope
    gainNode.gain.setValueAtTime(0.001, ctx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.3, ctx.currentTime + 0.05);
    gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.2);
    
    osc1.start();
    osc2.start();
    
    osc1.stop(ctx.currentTime + 1.5);
    osc2.stop(ctx.currentTime + 1.5);
  } catch (err) {
    console.error("Audio synthesis failed:", err);
  }
}

/**
 * Initializes and synthesizes a break completed alarm (uplifting ascending G5 & C6 chime)
 */
function playBreakBell() {
  if (state.audioMuted) return;
  
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    
    const osc1 = ctx.createOscillator();
    const osc2 = ctx.createOscillator();
    const gainNode = ctx.createGain();
    
    osc1.connect(gainNode);
    osc2.connect(gainNode);
    gainNode.connect(ctx.destination);
    
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(783.99, ctx.currentTime); // G5
    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(1046.50, ctx.currentTime); // C6
    
    // Vol Envelope
    gainNode.gain.setValueAtTime(0.001, ctx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.25, ctx.currentTime + 0.03);
    gainNode.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.0);
    
    osc1.start();
    osc2.start();
    
    osc1.stop(ctx.currentTime + 1.2);
    osc2.stop(ctx.currentTime + 1.2);
  } catch (err) {
    console.error("Audio synthesis failed:", err);
  }
}

// --- Local Storage Management ---

function loadStateFromStorage() {
  // Load settings
  const cachedSettings = localStorage.getItem('pomodoro_settings');
  if (cachedSettings) {
    try {
      state.settings = { ...DEFAULTS, ...JSON.parse(cachedSettings) };
    } catch (e) {
      state.settings = { ...DEFAULTS };
    }
  } else {
    state.settings = { ...DEFAULTS };
  }
  
  // Load mute setting
  const cachedMute = localStorage.getItem('pomodoro_audio_muted');
  if (cachedMute !== null) {
    state.audioMuted = cachedMute === 'true';
  } else {
    state.audioMuted = state.settings.audioMuted;
  }
  
  // Load Stats
  const cachedTotalPomodoros = localStorage.getItem('pomodoro_sessions_total');
  const cachedTotalFocusTime = localStorage.getItem('pomodoro_total_focus_time');
  
  state.stats.totalPomodoros = cachedTotalPomodoros ? parseInt(cachedTotalPomodoros, 10) || 0 : 0;
  state.stats.totalFocusTime = cachedTotalFocusTime ? parseInt(cachedTotalFocusTime, 10) || 0 : 0;
}

function saveSettingsToStorage() {
  localStorage.setItem('pomodoro_settings', JSON.stringify(state.settings));
}

function saveMuteToStorage() {
  localStorage.setItem('pomodoro_audio_muted', state.audioMuted.toString());
}

function saveStatsToStorage() {
  localStorage.setItem('pomodoro_sessions_total', state.stats.totalPomodoros.toString());
  localStorage.setItem('pomodoro_total_focus_time', state.stats.totalFocusTime.toString());
}

// --- State Machine Helpers ---

function getDurationForMode(mode) {
  switch (mode) {
    case 'work':
      return state.settings.workDuration * 60;
    case 'short':
      return state.settings.shortDuration * 60;
    case 'long':
      return state.settings.longDuration * 60;
    default:
      return 1500;
  }
}

function setMode(mode) {
  state.currentMode = mode;
  state.totalDuration = getDurationForMode(mode);
  state.timeLeft = state.totalDuration;
  state.expectedEndTime = null;
  
  // Adjust theme variables and update tabs
  DOM.body.className = `mode-${mode}`;
  
  DOM.modeTabs.forEach(tab => {
    if (tab.getAttribute('data-mode') === mode) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  });
  
  // Reset elements
  updateDisplay();
}

// --- UI Rendering Module ---

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function updateDisplay() {
  // Update numbers
  DOM.timerDigits.textContent = formatTime(state.timeLeft);
  
  // Update mode labels & dynamic messages
  switch (state.currentMode) {
    case 'work':
      DOM.timerLabel.textContent = "FOCUS";
      if (state.timerState === 'running') {
        DOM.timerSublabel.textContent = "Stay focused on your objective";
      } else if (state.timerState === 'paused') {
        DOM.timerSublabel.textContent = "Timer is paused";
      } else {
        DOM.timerSublabel.textContent = "Flow state active";
      }
      break;
    case 'short':
      DOM.timerLabel.textContent = "SHORT BREAK";
      if (state.timerState === 'running') {
        DOM.timerSublabel.textContent = "Breathe and relax your body";
      } else if (state.timerState === 'paused') {
        DOM.timerSublabel.textContent = "Timer is paused";
      } else {
        DOM.timerSublabel.textContent = "Take a moment";
      }
      break;
    case 'long':
      DOM.timerLabel.textContent = "LONG BREAK";
      if (state.timerState === 'running') {
        DOM.timerSublabel.textContent = "Recharge completely. Well done";
      } else if (state.timerState === 'paused') {
        DOM.timerSublabel.textContent = "Timer is paused";
      } else {
        DOM.timerSublabel.textContent = "Unwind and refresh";
      }
      break;
  }
  
  // Update play/pause button state icons
  if (state.timerState === 'running') {
    DOM.playIcon.classList.add('hidden');
    DOM.pauseIcon.classList.remove('hidden');
    DOM.btnPlayPause.setAttribute('aria-label', 'Pause Timer');
    DOM.btnPlayPause.setAttribute('title', 'Pause');
  } else {
    DOM.playIcon.classList.remove('hidden');
    DOM.pauseIcon.classList.add('hidden');
    DOM.btnPlayPause.setAttribute('aria-label', 'Start Timer');
    DOM.btnPlayPause.setAttribute('title', 'Start Focus');
  }
  
  // Update progress circle
  updateProgressRing();
  
  // Update dynamic Tab titles
  updateDocumentTitle();
  
  // Update Capsules Progress tracker
  updateCapsulesUI();
  
  // Update Lifetime Stats Displays
  DOM.statTotalPomodoros.textContent = state.stats.totalPomodoros;
  DOM.statTotalFocusTime.textContent = `${state.stats.totalFocusTime}m`;
}

function updateProgressRing() {
  const percentLeft = state.totalDuration > 0 ? (state.timeLeft / state.totalDuration) : 0;
  // Circumference of our r=150 circle is exactly 2 * PI * 150 = 942.48.
  const circumference = 942.48;
  const offset = circumference - (percentLeft * circumference);
  
  DOM.progressCircle.style.strokeDashoffset = offset;
}

function updateDocumentTitle() {
  if (state.timerState === 'running') {
    const formatted = formatTime(state.timeLeft);
    const modeLabel = state.currentMode === 'work' ? 'Focus' : 'Break';
    document.title = `(${formatted}) ${modeLabel} — Agy Pomodoro`;
  } else if (state.timerState === 'paused') {
    const formatted = formatTime(state.timeLeft);
    document.title = `[Paused] ${formatted} — Agy Pomodoro`;
  } else {
    document.title = "Agy Pomodoro — Flow into Deep Focus";
  }
}

function updateCapsulesUI() {
  DOM.capsulesContainer.innerHTML = '';
  
  for (let i = 0; i < 4; i++) {
    const capsule = document.createElement('div');
    capsule.className = 'capsule';
    capsule.setAttribute('data-index', i);
    
    if (i < state.sessionCount) {
      capsule.classList.add('completed');
    } else if (i === state.sessionCount && state.timerState === 'running' && state.currentMode === 'work') {
      capsule.classList.add('active');
    }
    
    DOM.capsulesContainer.appendChild(capsule);
  }
  
  DOM.sessionCountText.textContent = `${state.sessionCount} / 4 completed`;
}

function updateMuteButtonUI() {
  if (state.audioMuted) {
    DOM.soundOnIcon.classList.add('hidden');
    DOM.soundOffIcon.classList.remove('hidden');
    DOM.btnMute.setAttribute('aria-label', 'Unmute Sound');
  } else {
    DOM.soundOnIcon.classList.remove('hidden');
    DOM.soundOffIcon.classList.add('hidden');
    DOM.btnMute.setAttribute('aria-label', 'Mute Sound');
  }
}

// --- Core Countdown Timer Engine ---

function tick() {
  if (state.timerState !== 'running') {
    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }
    return;
  }
  
  const now = Date.now();
  const remainingMs = state.expectedEndTime - now;
  
  if (remainingMs <= 0) {
    // End of timer session reached!
    state.timeLeft = 0;
    updateDisplay();
    
    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }
    
    handleSessionExpiration();
  } else {
    // Accurate time left estimation
    const currentSecondLeft = Math.ceil(remainingMs / 1000);
    if (currentSecondLeft !== state.timeLeft) {
      state.timeLeft = currentSecondLeft;
      updateDisplay();
    }
  }
}

function startTimer() {
  state.timerState = 'running';
  state.expectedEndTime = Date.now() + (state.timeLeft * 1000);
  
  // Force clean existing timer loop
  if (timerInterval) {
    clearInterval(timerInterval);
  }
  
  // Ticking every 100ms prevents drift and is highly responsive
  timerInterval = setInterval(tick, 100);
  
  updateDisplay();
}

function pauseTimer() {
  state.timerState = 'paused';
  
  // Capture precisely how many seconds are left based on target timestamp
  if (state.expectedEndTime) {
    const diff = state.expectedEndTime - Date.now();
    state.timeLeft = Math.max(0, Math.ceil(diff / 1000));
  }
  
  state.expectedEndTime = null;
  
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  
  updateDisplay();
}

function resetTimer() {
  state.timerState = 'idle';
  state.expectedEndTime = null;
  
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  
  state.timeLeft = getDurationForMode(state.currentMode);
  updateDisplay();
}

function skipTimer() {
  // Gracefully transition to next logical state
  transitionNextMode(true); // pass skipped=true
}

function handleSessionExpiration() {
  // Trigger sound bells first
  if (state.currentMode === 'work') {
    playFocusBell();
    
    // Accumulate Stats
    state.sessionCount++;
    state.stats.totalPomodoros++;
    state.stats.totalFocusTime += state.settings.workDuration;
    saveStatsToStorage();
  } else {
    playBreakBell();
    
    // If we completed a long break, reset set counter
    if (state.currentMode === 'long') {
      state.sessionCount = 0;
    }
  }
  
  // Switch phases
  transitionNextMode(false); // natural completion
}

function transitionNextMode(isSkipped = false) {
  // Logical flow transitions:
  // Work (1) -> Short Break -> Work (2) -> Short Break -> Work (3) -> Short Break -> Work (4) -> Long Break -> Work (1)
  
  let nextMode = 'work';
  let shouldTriggerAutomation = false;
  
  if (state.currentMode === 'work') {
    if (!isSkipped && state.sessionCount >= 4) {
      nextMode = 'long';
    } else {
      nextMode = 'short';
    }
    shouldTriggerAutomation = state.settings.autoStartBreaks;
  } else {
    // Both short and long break return to work
    nextMode = 'work';
    shouldTriggerAutomation = state.settings.autoStartPomodoros;
  }
  
  // Set the timer state
  state.timerState = 'idle';
  state.expectedEndTime = null;
  
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  
  // Apply mode transition changes
  setMode(nextMode);
  
  // Automate next state starts if configured and not skipped manually
  if (!isSkipped && shouldTriggerAutomation) {
    startTimer();
  } else {
    updateDisplay();
  }
}

// --- Settings Form Dialog Actions ---

function openSettings() {
  // Pull current settings values into inputs
  DOM.inputWork.value = state.settings.workDuration;
  DOM.inputShort.value = state.settings.shortDuration;
  DOM.inputLong.value = state.settings.longDuration;
  DOM.toggleAutoBreaks.checked = state.settings.autoStartBreaks;
  DOM.toggleAutoPomodoros.checked = state.settings.autoStartPomodoros;
  
  DOM.drawer.setAttribute('aria-hidden', 'false');
  // Add body lock/blur helper if desired, drawer overlay holds transition smoothly
}

function closeSettings() {
  DOM.drawer.setAttribute('aria-hidden', 'true');
}

function validateAndSaveSettings(e) {
  e.preventDefault();
  
  // Fetch form values
  const work = parseInt(DOM.inputWork.value, 10);
  const short = parseInt(DOM.inputShort.value, 10);
  const long = parseInt(DOM.inputLong.value, 10);
  
  // Validation constraints fallback checks
  const validatedWork = (!isNaN(work) && work >= 1 && work <= 120) ? work : DEFAULTS.workDuration;
  const validatedShort = (!isNaN(short) && short >= 1 && short <= 60) ? short : DEFAULTS.shortDuration;
  const validatedLong = (!isNaN(long) && long >= 1 && long <= 60) ? long : DEFAULTS.longDuration;
  
  // Save settings values
  state.settings.workDuration = validatedWork;
  state.settings.shortDuration = validatedShort;
  state.settings.longDuration = validatedLong;
  state.settings.autoStartBreaks = DOM.toggleAutoBreaks.checked;
  state.settings.autoStartPomodoros = DOM.toggleAutoPomodoros.checked;
  
  saveSettingsToStorage();
  closeSettings();
  
  // If timer is inactive, immediately apply the updated active mode duration
  if (state.timerState === 'idle') {
    setMode(state.currentMode);
  } else {
    // If running, we only recalculate total duration to prevent jumping progress ring glitches
    state.totalDuration = getDurationForMode(state.currentMode);
    updateDisplay();
  }
}

function restoreDefaultSettings() {
  DOM.inputWork.value = DEFAULTS.workDuration;
  DOM.inputShort.value = DEFAULTS.shortDuration;
  DOM.inputLong.value = DEFAULTS.longDuration;
  DOM.toggleAutoBreaks.checked = DEFAULTS.autoStartBreaks;
  DOM.toggleAutoPomodoros.checked = DEFAULTS.autoStartPomodoros;
}

// --- Event Registrations ---

function registerEventListeners() {
  // Play/Pause Action
  DOM.btnPlayPause.addEventListener('click', () => {
    if (state.timerState === 'running') {
      pauseTimer();
    } else {
      startTimer();
    }
  });
  
  // Reset Action
  DOM.btnReset.addEventListener('click', resetTimer);
  
  // Skip Action
  DOM.btnSkip.addEventListener('click', skipTimer);
  
  // Mode tabs clicks
  DOM.modeTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const selectedMode = tab.getAttribute('data-mode');
      if (selectedMode !== state.currentMode) {
        if (state.timerState === 'running' || state.timerState === 'paused') {
          const confirmSwitch = confirm("An active session is running. Would you like to transition and reset the timer?");
          if (!confirmSwitch) return;
        }
        setMode(selectedMode);
        state.timerState = 'idle';
        if (timerInterval) {
          clearInterval(timerInterval);
          timerInterval = null;
        }
        updateDisplay();
      }
    });
  });
  
  // Header Volume toggle
  DOM.btnMute.addEventListener('click', () => {
    state.audioMuted = !state.audioMuted;
    saveMuteToStorage();
    updateMuteButtonUI();
  });
  
  // Settings Dialog Open/Close
  DOM.btnSettings.addEventListener('click', openSettings);
  DOM.drawerClose.addEventListener('click', closeSettings);
  DOM.drawerOverlay.addEventListener('click', closeSettings);
  
  // Drawer Actions
  DOM.settingsForm.addEventListener('submit', validateAndSaveSettings);
  DOM.btnRestoreDefaults.addEventListener('click', restoreDefaultSettings);
  
  // Test synthesized tone
  DOM.btnTestSound.addEventListener('click', () => {
    if (state.currentMode === 'work') {
      playFocusBell();
    } else {
      playBreakBell();
    }
  });
  
  // Lifetime Stats Wipe
  DOM.btnResetStats.addEventListener('click', () => {
    const confirmReset = confirm("Are you sure you want to permanently clear all completed statistics?");
    if (confirmReset) {
      state.stats.totalPomodoros = 0;
      state.stats.totalFocusTime = 0;
      state.sessionCount = 0;
      saveStatsToStorage();
      updateDisplay();
    }
  });
  
  // Tab visibility changes anti-drift listener
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
      // Re-evaluate remaining target time accurately if active
      if (state.timerState === 'running') {
        tick();
      }
    }
  });
}

// --- Initialization Entry Point ---

function init() {
  loadStateFromStorage();
  updateMuteButtonUI();
  setMode('work'); // Default Focus mode starts
  registerEventListeners();
}

// Fire up the flow engine
document.addEventListener('DOMContentLoaded', init);
