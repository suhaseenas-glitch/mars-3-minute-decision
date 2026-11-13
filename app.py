"""The 3-Minute Decision — a mobile-friendly educational Mars rover game.

Run: streamlit run app.py
No logins, school details, tracking, or external APIs are required.
The scenario outcomes are fictional teaching simulations, not NASA operational advice.
"""

from __future__ import annotations

import csv
import html
import io
import time
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"
DECISION_SECONDS = 180
NAV = ["🏠 Home", "🎮 Play", "📊 Report", "📘 Guide"]
STARTING_RESOURCES = {"Safety": 70, "Energy": 72, "Science": 45}

st.set_page_config(
    page_title="The 3-Minute Decision | Mars Rover Mission",
    page_icon=str(ASSETS / "app_icon.png") if (ASSETS / "app_icon.png").exists() else "🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# The visual system uses equal-height, full-width buttons and mobile-friendly cards.
st.markdown(
    """
<style>
    :root { --sky:#0B1120; --panel:#172239; --stroke:#304260;
            --soft:#BAC8DC; --white:#F8FBFF; --mars:#FF996B; --mint:#64DCCE; }
    html, body { font-family: 'Segoe UI', Inter, system-ui, sans-serif; }
    .stApp { background: radial-gradient(ellipse at 75% 0%, #233653 0%, #101A2D 38%, #0B1120 77%); }
    .block-container { max-width: 960px; padding-top: 1.2rem; padding-bottom: 4rem; }
    h1,h2,h3,p,li {overflow-wrap: anywhere;}
    h1,h2,h3 { letter-spacing: -.025em; }
    .brandline {display:flex; align-items:center; gap:12px; padding:5px 0 12px;}
    .brand-mark {width:42px;height:42px;border-radius:14px;background:linear-gradient(135deg,#fa8e59,#ac4734);
          display:flex;align-items:center;justify-content:center;font-size:23px;flex:none;box-shadow:0 4px 20px #ff87462b;}
    .brand-title {font-size:17px;font-weight:900;line-height:1.12;color:var(--white);}
    .brand-caption {color:#ACBDD4;font-size:11px;letter-spacing:1.7px;font-weight:800;margin-top:4px;}
    .eyebrow {font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#7CE2D8;font-weight:900;margin:11px 0 9px;}
    .big-title {font-size:clamp(2rem, 5.4vw, 3.6rem);font-weight:950;line-height:1.10;color:#fff;margin:2px 0 10px;letter-spacing:-.05em;}
    .lead {font-size:clamp(15px,2.1vw,19px);color:#C9D5E8;line-height:1.55;max-width:770px;}
    .panel {background:linear-gradient(145deg,#1D2A42,#152035);border:1px solid #344660;
           border-radius:20px;padding:18px 19px;margin:12px 0;box-shadow:0 14px 28px #050a1830;}
    .panel-title {font-size:17px;font-weight:900;color:#fff;margin:0 0 8px;}
    .muted {color:#C0CCDC;font-size:14px;line-height:1.55;}
    .small-note {font-size:12px;color:#9FB3CD;line-height:1.5;}
    .pill-tag {display:inline-flex;align-items:center;gap:7px;background:#173C45;color:#9DF1E4;
        border:1px solid #34717C;border-radius:50px;padding:6px 11px;font-size:12px;font-weight:850;}
    .mission-number {color:#FFE1CF;font-size:12px;font-weight:850;letter-spacing:1.4px;text-transform:uppercase;}
    .status-grid {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:13px 0 16px;}
    .stat-card {border:1px solid #34435b;background:#16233a;border-radius:16px;padding:14px 12px;min-width:0;}
    .stat-icon {font-size:19px;display:block;margin-bottom:7px;}
    .stat-value {color:#fff;font-size:clamp(20px,4.1vw,30px);line-height:1;font-weight:900;}
    .stat-label {color:#A8BAD2;font-size:12px;margin-top:6px;}
    .info-card {display:flex;align-items:center;gap:14px;background:#17273d;border:1px solid #334a63;
           padding:15px;border-radius:17px;margin:10px 0;min-height:80px;}
    .info-icon {width:48px;height:48px;border-radius:14px;background:#263A54;display:flex;align-items:center;
          justify-content:center;font-size:24px;flex:0 0 48px;}
    .info-copy {flex:1;min-width:0;}
    .info-label {font-size:12px;color:#A9BBD3;font-weight:700;letter-spacing:.4px;}
    .info-value {font-size:16px;color:#F4F8FF;font-weight:800;line-height:1.35;margin-top:3px;}
    .choice-card {display:flex;gap:14px;align-items:flex-start;padding:17px 17px 16px;border-radius:18px;
        border:1px solid #32435C;background:linear-gradient(115deg,#1C2B42,#152035);margin:14px 0 7px;}
    .choice-icon {background:#303F53;color:#fff;width:47px;height:47px;border-radius:14px;
        font-size:22px;display:flex;align-items:center;justify-content:center;flex:0 0 47px;}
    .choice-copy {flex:1;min-width:0;}
    .choice-title {font-size:16px;font-weight:900;color:#F5F9FF;line-height:1.35;}
    .choice-subtitle {color:#B9C9DE;font-size:13px;line-height:1.45;margin-top:5px;}
    .choice-meta {color:#87DBD4;font-size:12px;font-weight:750;margin-top:7px;}
    .timer-card {padding:16px 20px;border-radius:18px;border:1px solid #4A5B71;
          background:linear-gradient(110deg,#253448,#172339);margin:9px 0 10px;
          display:flex;align-items:center;justify-content:space-between;gap:12px;}
    .timer-caption {font-size:13px;font-weight:800;color:#C8D8E8;}
    .timer-value {font-size:clamp(27px,5vw,38px);font-weight:950;font-variant-numeric:tabular-nums;
          letter-spacing:1px;color:#FDAB79;}
    .feedback {border-radius:20px;border:1px solid #467068;background:#173530;padding:18px 20px;margin:15px 0;}
    .feedback-title {font-weight:900;font-size:19px;color:#BEF7E6;margin-bottom:9px;}
    .result-item {border-radius:16px;background:#172338;border:1px solid #37465b;padding:16px;margin:12px 0;}
    .result-head {font-weight:900;color:white;font-size:16px;margin-bottom:5px;}
    .result-choose {color:#8DE0D5;font-weight:800;font-size:14px;}
    .stButton > button, div[data-testid="stDownloadButton"] > button {
         border-radius:13px !important; min-height:52px !important; width:100% !important;
         font-size:15px !important; font-weight:850 !important; letter-spacing:.1px;
         line-height:1.2 !important; padding:10px 16px !important;
         justify-content:center !important; align-items:center !important; text-align:center !important;
         border:1px solid #3c536d;
    }
    .stButton > button[kind="primary"] {
         color:#111d2e !important;background:linear-gradient(100deg,#FFB37F,#FF8E65) !important;
         border:1px solid #ffb587 !important;box-shadow:0 7px 20px #d6613428;
    }
    .stButton > button[kind="secondary"] {background:#1C2E46;color:#F3F7FF;}
    .stButton > button:hover {border-color:#67DDD1 !important;}
    div[data-testid="stSegmentedControl"] { width:100%; }
    div[data-testid="stSegmentedControl"] > div {flex-wrap:wrap !important; gap:6px !important;}
    div[data-testid="stSegmentedControl"] button { border-radius:13px !important; font-weight:800; min-height:40px;}
    div[data-testid="stProgress"] {margin-top:-3px;margin-bottom:9px;}
    div[data-testid="stProgress"] > div > div > div {background:linear-gradient(90deg,#65d6cb,#ffc17e);}
    div[data-testid="stTextArea"] textarea {background:#111c30;color:#F8FBFF;border-radius:13px;}
    div[data-testid="stExpander"] {border:1px solid #364861;background:#152238;border-radius:14px;}
    .credit {font-size:11px;color:#90A6C2;text-align:center;line-height:1.55;margin-top:34px;}
    @media (max-width: 650px) {
       .block-container {padding-left:.78rem; padding-right:.78rem; padding-top:.6rem;}
       .brand-title {font-size:15px;} .brand-mark {width:38px;height:38px;border-radius:12px;}
       .panel {padding:14px 14px;border-radius:15px;}
       .choice-card {padding:13px;gap:11px;}
       .choice-title {font-size:15px;} .choice-subtitle {font-size:12.5px;}
       .choice-icon {width:40px;height:40px;flex-basis:40px;font-size:19px;}
       .info-card {padding:11px;gap:10px;}
       .info-icon {width:39px;height:39px;flex-basis:39px;font-size:20px;}
       .info-value {font-size:14px;}
       .stat-card {padding:11px 9px;}
       .stat-label {font-size:10px;}
       div[data-testid="stSegmentedControl"] button {font-size:12px !important;}
       .timer-card {padding:13px 15px;}
    }
</style>
""",
    unsafe_allow_html=True,
)


# All outcomes are hypothetical and intended to illustrate trade-offs.
SCENARIOS = [
    {
        "icon": "🛞", "title": "A dangerous shortcut", "sector": "Jezero-like rocky terrain",
        "alert": "Your rover approaches a promising outcrop. The shortest route crosses unstable sand, and Earth cannot respond in time.",
        "objective": "Reach the science target without trapping the wheels.",
        "data": [
            ("📐", "Slope", "18° along the shortcut"),
            ("🛞", "Wheel slip", "26% on the left side"),
            ("🧭", "Alternative", "A safer path adds 12 m"),
        ],
        "notes": "High wheel slip can mean loose terrain. A shorter route is not always the safest route. Review the slope and slip before deciding.",
        "options": [
            {"icon": "🧭", "title": "Map a safer route", "desc": "Use onboard navigation to go around the soft ground.",
             "tradeoff": "Less risk · more time and energy", "delta": (12, -8, 4), "points": 10,
             "outcome": "The rover detours around the sand. It uses extra energy but arrives with its wheels protected.",
             "lesson": "Combining several signals — not just distance — supports a safer route."},
            {"icon": "⚡", "title": "Push straight ahead", "desc": "Take the shortest path before conditions change.",
             "tradeoff": "Fast progress · high wheel risk", "delta": (-22, -12, 5), "points": 2,
             "outcome": "The wheels begin to spin in soft sand. The rover makes little progress and loses energy.",
             "lesson": "Ignoring a strong warning signal can turn a short route into a costly obstacle."},
            {"icon": "🛑", "title": "Stop and wait for Earth", "desc": "Park and request a later route review.",
             "tradeoff": "Low immediate risk · delayed science", "delta": (9, -4, -7), "points": 6,
             "outcome": "The rover remains safe, but it misses a useful chance to gather data during the planned activity window.",
             "lesson": "Waiting can protect equipment, but autonomy sometimes allows a safe alternative."},
        ],
    },
    {
        "icon": "🌪️", "title": "Dust on the horizon", "sector": "Atmospheric monitoring zone",
        "alert": "A dust cloud reduces visibility and sunlight. A planned camera survey would consume considerable power.",
        "objective": "Protect the rover while preserving useful atmospheric observations.",
        "data": [
            ("☀️", "Solar input", "32% below forecast"),
            ("🔋", "Energy reserve", "62% remaining"),
            ("📷", "Survey", "Long camera sequence queued"),
        ],
        "notes": "This is a fictional solar-powered training rover. Real Mars rovers use different power systems; Perseverance uses a radioisotope power system. In this scenario, reduced solar input matters.",
        "options": [
            {"icon": "🛡️", "title": "Enter power-saving mode", "desc": "Cancel the long survey and preserve the most important data.",
             "tradeoff": "Better reserve · fewer new images", "delta": (10, 13, -5), "points": 10,
             "outcome": "The rover safely rides out the dusty period while conserving its energy reserve.",
             "lesson": "Resource protection may matter more than completing a lower-priority science task."},
            {"icon": "📸", "title": "Run the full camera survey", "desc": "Collect as many images as possible despite dim conditions.",
             "tradeoff": "More images · large power cost", "delta": (-8, -24, 11), "points": 3,
             "outcome": "The rover gets extra photographs, but energy drains rapidly as the dust thickens.",
             "lesson": "More data is not always worth the added system risk."},
            {"icon": "🔬", "title": "Capture a brief dust sample", "desc": "Run a quick scan, then shut down nonessential instruments.",
             "tradeoff": "Balanced data · moderate power cost", "delta": (3, -8, 8), "points": 8,
             "outcome": "A short scan records valuable dust conditions, and the rover retains enough energy to pause safely.",
             "lesson": "A limited test can balance scientific value with energy conservation."},
        ],
    },
    {
        "icon": "🔋", "title": "The energy alert", "sector": "Nightfall preparation",
        "alert": "The rover's energy reserve is running low. Important observations are stored onboard, but some have not been protected.",
        "objective": "Keep essential records secure and prepare for the next cycle.",
        "data": [
            ("🔋", "Reserve", "36% before nightfall"),
            ("💾", "Science records", "3 priority files unchecked"),
            ("🌡️", "Temperature", "Expected to fall overnight"),
        ],
        "notes": "A rover has to budget energy for computing, communications, instruments and maintaining safe conditions. This training scenario uses simplified resources.",
        "options": [
            {"icon": "💾", "title": "Protect data and sleep", "desc": "Save essential results and activate a low-power state.",
             "tradeoff": "Strong protection · slower progress", "delta": (8, 12, 4), "points": 10,
             "outcome": "The priority data is secured, and the rover reaches the next cycle with a safer energy margin.",
             "lesson": "Protecting irreplaceable results can be more valuable than taking one more measurement."},
            {"icon": "📡", "title": "Transmit all files immediately", "desc": "Attempt a large data transfer now.",
             "tradeoff": "Data delivery · significant energy use", "delta": (-5, -20, 7), "points": 4,
             "outcome": "Some files are sent, but the power draw leaves little margin for nighttime protection.",
             "lesson": "Communication plans should be balanced with power and survival requirements."},
            {"icon": "🧪", "title": "Run one more science test", "desc": "Keep instruments active and collect a final reading.",
             "tradeoff": "More science · low safety margin", "delta": (-14, -18, 12), "points": 2,
             "outcome": "The science reading is interesting, but the rover must cut other functions to stay operational.",
             "lesson": "A productive action can still be a poor choice when the remaining energy is critically low."},
        ],
    },
    {
        "icon": "📷", "title": "A camera goes blurry", "sector": "Rock field traversal",
        "alert": "The navigation camera suddenly produces uncertain depth readings while the rover is driving toward the next waypoint.",
        "objective": "Decide whether the rover has enough reliable information to keep moving.",
        "data": [
            ("📷", "Depth confidence", "58% for the next 10 m"),
            ("🪨", "Detected obstacles", "Multiple rocks ahead"),
            ("🛣️", "Current speed", "Slow exploratory drive"),
        ],
        "notes": "Navigation cameras provide evidence for obstacle detection. A system should be able to respond to uncertainty, not treat every reading as correct.",
        "options": [
            {"icon": "🧰", "title": "Stop, clean and recalibrate", "desc": "Pause navigation and validate fresh camera measurements.",
             "tradeoff": "Reduced risk · a few minutes lost", "delta": (12, -6, -2), "points": 10,
             "outcome": "The rover corrects its sensor issue and resumes travel with more trustworthy distance estimates.",
             "lesson": "When evidence quality is poor, verification is often the strongest decision."},
            {"icon": "🐢", "title": "Use backup readings slowly", "desc": "Drive cautiously using the remaining working sensors.",
             "tradeoff": "Some progress · residual uncertainty", "delta": (-3, -9, 6), "points": 7,
             "outcome": "The rover advances slowly, but it has to stop twice to avoid possible obstacles.",
             "lesson": "Redundancy can help, but uncertain measurements still demand caution."},
            {"icon": "🏎️", "title": "Continue at the same pace", "desc": "Trust the original route and avoid delays.",
             "tradeoff": "Quick action · significant damage risk", "delta": (-20, -10, 8), "points": 2,
             "outcome": "The rover hits an unseen stone and must suspend science activities for a mechanical check.",
             "lesson": "Unreliable measurements should not be treated as reliable just because a schedule is tight."},
        ],
    },
    {
        "icon": "🪨", "title": "A promising rock", "sector": "Ancient riverbed study",
        "alert": "A layered rock contains intriguing mineral patterns. It could reveal clues about Mars's ancient environment, but drilling carries a risk.",
        "objective": "Gather useful evidence before spending energy on an irreversible action.",
        "data": [
            ("🧪", "Mineral pattern", "Interesting, not yet confirmed"),
            ("🌡️", "Drill temperature", "Above ideal starting level"),
            ("⚡", "Sampling cost", "High power requirement"),
        ],
        "notes": "Interesting minerals alone are not proof of life. Scientists consider many independent measurements before drawing conclusions.",
        "options": [
            {"icon": "🔍", "title": "Scan the rock first", "desc": "Take lower-risk images and a short spectral measurement.",
             "tradeoff": "Better evidence · modest energy use", "delta": (5, -7, 10), "points": 10,
             "outcome": "The scan narrows down where a later sample would be most useful, while avoiding an overheated drill.",
             "lesson": "Collecting evidence before committing equipment can improve both science and safety."},
            {"icon": "🛠️", "title": "Drill immediately", "desc": "Try to collect a sample before leaving the site.",
             "tradeoff": "Potential sample · high equipment risk", "delta": (-16, -21, 14), "points": 4,
             "outcome": "The rover retrieves material, but the hot drill strains its mechanisms and uses much of its reserve.",
             "lesson": "A high scientific reward may not justify a poorly controlled mechanical risk."},
            {"icon": "📍", "title": "Mark the location and leave", "desc": "Record coordinates for a possible future visit.",
             "tradeoff": "Safer equipment · missed data now", "delta": (7, 4, -8), "points": 6,
             "outcome": "The rover stays in good condition, but it collects little new information about the unusual rock.",
             "lesson": "Avoiding risk is useful, yet choosing no measurement at all also has a cost."},
        ],
    },
    {
        "icon": "📡", "title": "Out of contact", "sector": "Communication relay window",
        "alert": "An orbiter relay opportunity is delayed. Onboard storage is filling up, and the team must choose what data to keep.",
        "objective": "Preserve high-value science without overloading the rover.",
        "data": [
            ("💾", "Storage", "90% occupied"),
            ("📶", "Next relay", "Not yet available"),
            ("📋", "Data priority", "Critical logs are flagged"),
        ],
        "notes": "Mars missions often transmit data through relay orbiters. Data prioritization and limited communication opportunities are realistic engineering concerns; the numbers here are fictional.",
        "options": [
            {"icon": "🗂️", "title": "Prioritize and compress", "desc": "Keep critical records and compress less urgent data.",
             "tradeoff": "Protects key science · some processing cost", "delta": (8, -7, 6), "points": 10,
             "outcome": "The most valuable science remains intact and the rover creates room for essential telemetry.",
             "lesson": "A prioritized plan is better than treating every file as equally important."},
            {"icon": "🗑️", "title": "Delete older science files", "desc": "Free space immediately by removing several stored observations.",
             "tradeoff": "Fast storage recovery · lost science", "delta": (2, 5, -19), "points": 3,
             "outcome": "Storage pressure disappears, but some irreplaceable evidence is permanently lost.",
             "lesson": "A solution that fixes one metric can seriously damage another mission goal."},
            {"icon": "📷", "title": "Keep collecting new images", "desc": "Ignore the storage alert to continue the planned observations.",
             "tradeoff": "Short-term data gain · higher system risk", "delta": (-14, -12, 10), "points": 4,
             "outcome": "The rover captures more images, then reaches its storage limit and cannot save a critical diagnostic file.",
             "lesson": "Capacity limits must be part of the decision, even when new data is exciting."},
        ],
    },
]


def esc(text: object) -> str:
    return html.escape(str(text), quote=True)


def clamp(value: int) -> int:
    return max(0, min(100, int(value)))


def initialize() -> None:
    s = st.session_state
    defaults = {
        "view": NAV[0], "phase": "welcome", "index": 0,
        "deadline": None, "resources": STARTING_RESOURCES.copy(),
        "log": [], "score": 0,
    }
    for key, value in defaults.items():
        if key not in s:
            s[key] = value


def go_to(page: str) -> None:
    st.session_state.view = page


def start_game() -> None:
    s = st.session_state
    s.phase = "playing"
    s.index = 0
    s.resources = STARTING_RESOURCES.copy()
    s.log = []
    s.score = 0
    s.deadline = time.time() + DECISION_SECONDS
    s.view = NAV[1]
    for i in range(len(SCENARIOS)):
        s.pop(f"reason_{i}", None)


def record_decision(option_index: int | None) -> None:
    s = st.session_state
    if s.phase != "playing":
        return
    scenario = SCENARIOS[s.index]
    remaining = max(0, int(s.deadline - time.time()))
    # The server checks the deadline, not only the display's countdown.
    expired = remaining <= 0 or option_index is None
    if expired:
        choice_title = "Automatic safe hold (time expired)"
        delta = (4, -5, -6)
        outcome = "The rover enters a conservative hold state. It stays relatively safe, but the team misses the decision window and some science opportunity."
        lesson = "Evidence-based decisions are valuable, but teams also need a clear response before the deadline."
        points = 0
        reasoning = ""
        risk = "Timeout"
    else:
        choice = scenario["options"][option_index]
        choice_title = choice["title"]
        delta = choice["delta"]
        outcome = choice["outcome"]
        lesson = choice["lesson"]
        reasoning = s.get(f"reason_{s.index}", "").strip()[:240]
        points = choice["points"] + (1 if len(reasoning) >= 15 else 0)
        risk = choice["tradeoff"]
    for name, value in zip(("Safety", "Energy", "Science"), delta):
        s.resources[name] = clamp(s.resources[name] + value)
    s.score += points
    s.log.append({
        "round": s.index + 1,
        "scenario": scenario["title"],
        "choice": choice_title,
        "outcome": outcome,
        "lesson": lesson,
        "tradeoff": risk,
        "reason": reasoning,
        "points": points,
        "remaining": 0 if expired else remaining,
        "delta": delta,
    })
    s.phase = "feedback"


def next_round() -> None:
    s = st.session_state
    if s.phase != "feedback":
        return
    if s.index < len(SCENARIOS) - 1:
        s.index += 1
        s.phase = "playing"
        s.deadline = time.time() + DECISION_SECONDS
        s.view = NAV[1]
    else:
        s.phase = "finished"
        s.deadline = None
        s.view = NAV[2]


def resources_ui() -> None:
    r = st.session_state.resources
    st.markdown(
        '<div class="status-grid">'
        + ''.join(
            f'<div class="stat-card"><span class="stat-icon">{icon}</span>'
            f'<div class="stat-value">{r[name]}<span style="font-size:12px;color:#9DAFC5;">/100</span></div>'
            f'<div class="stat-label">{name} reserve</div></div>'
            for name, icon in (("Safety", "🛡️"), ("Energy", "🔋"), ("Science", "🔬"))
        )
        + '</div>',
        unsafe_allow_html=True,
    )


@st.fragment(run_every="1s")
def live_countdown() -> None:
    s = st.session_state
    if s.phase != "playing" or s.deadline is None:
        return
    remaining = max(0, int(s.deadline - time.time() + 0.999))
    if remaining <= 0:
        record_decision(None)
        st.rerun()
    minutes, seconds = divmod(remaining, 60)
    warning = remaining <= 30
    st.markdown(
        f'<div class="timer-card"><div><div class="timer-caption">⏱️ DECISION WINDOW</div>'
        f'<div class="small-note">Think carefully; one choice per emergency.</div></div>'
        f'<div class="timer-value" style="color:{"#FF7777" if warning else "#FFBA8B"}">'
        f'{minutes:02d}:{seconds:02d}</div></div>',
        unsafe_allow_html=True,
    )
    st.progress(remaining / DECISION_SECONDS)
    if warning:
        st.caption("⚠️ Less than 30 seconds. Choose an action before the rover enters safe hold.")


def brand() -> None:
    st.markdown(
        '<div class="brandline"><div class="brand-mark">🪐</div><div>'
        '<div class="brand-title">THE 3-MINUTE DECISION</div>'
        '<div class="brand-caption">MARS ROVER • MISSION SIMULATION</div></div></div>',
        unsafe_allow_html=True,
    )


def hero() -> None:
    st.markdown('<div class="eyebrow">Mission briefing • Mars</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-title">3 minutes. One decision.<br>Millions of kilometres away.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="lead">A rover faces an unexpected problem, and Earth cannot reply in time. '
        'Study the evidence, weigh the risks, and choose the rover’s next move.</p>',
        unsafe_allow_html=True,
    )
    if (ASSETS / "mars_hero.png").exists():
        st.image(str(ASSETS / "mars_hero.png"), width="stretch")


def home() -> None:
    hero()
    st.markdown(
        '<div class="status-grid">'
        '<div class="stat-card"><span class="stat-icon">🧩</span><div class="stat-value">6</div><div class="stat-label">Challenges</div></div>'
        '<div class="stat-card"><span class="stat-icon">⏱️</span><div class="stat-value">03:00</div><div class="stat-label">Per decision</div></div>'
        '<div class="stat-card"><span class="stat-icon">🔍</span><div class="stat-value">3</div><div class="stat-label">Choices each</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.button("🚀  Launch Mars mission", on_click=start_game, type="primary", width="stretch")
    if st.session_state.phase in ("playing", "feedback"):
        st.button("↩  Continue current mission", on_click=go_to, args=(NAV[1],), width="stretch")
    elif st.session_state.phase == "finished":
        st.button("📊  View your last report", on_click=go_to, args=(NAV[2],), width="stretch")

    st.markdown('<div class="eyebrow">What you will do</div>', unsafe_allow_html=True)
    for icon, title, subtitle in [
        ("📡", "Respond without instant help", "Radio signals take minutes to travel between Earth and Mars."),
        ("🔎", "Read rover telemetry", "Use clues about terrain, cameras, power and science goals."),
        ("⚖️", "Balance three mission needs", "Protect safety, conserve energy and still collect meaningful science."),
        ("📝", "Defend your decision", "Write a short mission note and compare it with the outcome."),
    ]:
        st.markdown(
            f'<div class="info-card"><div class="info-icon">{icon}</div><div class="info-copy">'
            f'<div class="info-value">{esc(title)}</div><div class="muted">{esc(subtitle)}</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="panel"><div class="panel-title">🛰️ How realistic is it?</div>'
        '<div class="muted">This is a fictional training game inspired by NASA Mars rover engineering. '
        'The decisions, scores and emergencies are simplified for learning. '
        'NASA describes one-way Earth–Mars communication delays of roughly 4–24 minutes, depending on distance. '
        'The three-minute timer is the game rule, not the real signal delay.</div></div>',
        unsafe_allow_html=True,
    )


def telemetry_card(icon: str, label: str, value: str) -> None:
    st.markdown(
        f'<div class="info-card"><div class="info-icon">{esc(icon)}</div>'
        f'<div class="info-copy"><div class="info-label">{esc(label)}</div>'
        f'<div class="info-value">{esc(value)}</div></div></div>',
        unsafe_allow_html=True,
    )


def play() -> None:
    s = st.session_state
    if s.phase == "welcome":
        st.markdown('<div class="big-title">Your mission begins here.</div>', unsafe_allow_html=True)
        st.markdown('<p class="lead">Six emergencies. Three choices each. Three minutes per decision.</p>', unsafe_allow_html=True)
        st.button("🚀  Start challenge", type="primary", width="stretch", on_click=start_game)
        return
    if s.phase == "finished":
        st.markdown('<div class="big-title">Mission complete!</div>', unsafe_allow_html=True)
        st.button("📊  Open mission report", type="primary", width="stretch", on_click=go_to, args=(NAV[2],))
        return

    scenario = SCENARIOS[s.index]
    if s.phase == "playing" and time.time() >= s.deadline:
        record_decision(None)

    st.markdown(
        f'<div class="mission-number">CASE {s.index+1:02d} OF {len(SCENARIOS):02d} · {esc(scenario["sector"])}</div>'
        f'<div class="big-title">{scenario["icon"]} {esc(scenario["title"])}</div>',
        unsafe_allow_html=True,
    )
    resources_ui()
    if s.phase == "feedback":
        outcome_screen()
        return

    live_countdown()
    st.markdown(
        f'<div class="panel"><span class="pill-tag">🚨 INCOMING ROVER ALERT</span>'
        f'<p style="font-size:17px;color:#F2F6FF;line-height:1.52;font-weight:700;margin:14px 0 9px;">'
        f'{esc(scenario["alert"])}</p>'
        f'<div class="small-note">🎯 Mission goal: {esc(scenario["objective"])}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="eyebrow">📟 Live telemetry — review the evidence</div>', unsafe_allow_html=True)
    for icon, label, value in scenario["data"]:
        telemetry_card(icon, label, value)
    with st.expander("🔎 Engineering notes — inspect before deciding"):
        st.write(scenario["notes"])

    st.markdown('<div class="eyebrow">🧠 Your mission note</div>', unsafe_allow_html=True)
    st.text_area(
        "What information matters most, and why? (Optional — earn +1 point for a note)",
        max_chars=240,
        height=94,
        placeholder="I choose this because the telemetry shows…",
        key=f"reason_{s.index}",
    )
    st.markdown('<div class="eyebrow">Choose one action</div>', unsafe_allow_html=True)
    for i, choice in enumerate(scenario["options"]):
        st.markdown(
            f'<div class="choice-card"><div class="choice-icon">{choice["icon"]}</div><div class="choice-copy">'
            f'<div class="choice-title">{esc(choice["title"])}</div>'
            f'<div class="choice-subtitle">{esc(choice["desc"])}</div>'
            f'<div class="choice-meta">{esc(choice["tradeoff"])}</div></div></div>',
            unsafe_allow_html=True,
        )
        st.button(
            f"Choose action {chr(65+i)}  ·  {choice['title']}",
            key=f"choose_{s.index}_{i}",
            type="primary" if i == 0 else "secondary",
            width="stretch",
            on_click=record_decision,
            args=(i,),
        )
    st.caption("Each choice produces a different consequence. The timer continues even if you switch tabs.")


def outcome_screen() -> None:
    s = st.session_state
    record = s.log[-1]
    st.markdown('<div class="eyebrow">Decision registered</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="feedback"><div class="feedback-title">'
        + ("⏳ Time expired — safe hold" if record["tradeoff"] == "Timeout" else "✅ Decision received")
        + '</div><div class="info-value">' + esc(record["choice"]) + '</div>'
        + '<p class="muted">' + esc(record["outcome"]) + '</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="status-grid">'
        f'<div class="stat-card"><span class="stat-icon">🛡️</span><div class="stat-value">{record["delta"][0]:+d}</div><div class="stat-label">Safety change</div></div>'
        f'<div class="stat-card"><span class="stat-icon">🔋</span><div class="stat-value">{record["delta"][1]:+d}</div><div class="stat-label">Energy change</div></div>'
        f'<div class="stat-card"><span class="stat-icon">🔬</span><div class="stat-value">{record["delta"][2]:+d}</div><div class="stat-label">Science change</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="panel"><div class="panel-title">💡 Why this matters</div>'
        f'<div class="muted">{esc(record["lesson"])}</div>'
        f'<div class="small-note" style="margin-top:8px;">+{record["points"]} decision points earned in this case</div></div>',
        unsafe_allow_html=True,
    )
    if record["reason"]:
        st.markdown(
            f'<div class="panel"><div class="panel-title">📝 Your reasoning</div>'
            f'<div class="muted">{esc(record["reason"])}</div></div>',
            unsafe_allow_html=True,
        )
    label = "➡️  Next rover emergency" if s.index < len(SCENARIOS) - 1 else "🏁  View final mission report"
    st.button(label, type="primary", width="stretch", on_click=next_round)


def report_csv() -> str:
    s = st.session_state
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Case", "Emergency", "Chosen action", "Points", "Seconds left", "Reasoning", "Outcome"])
    for record in s.log:
        writer.writerow([record["round"], record["scenario"], record["choice"],
                         record["points"], record["remaining"], record["reason"], record["outcome"]])
    return output.getvalue()


def report() -> None:
    s = st.session_state
    st.markdown('<div class="eyebrow">Mission dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-title">📊 Mission report</div>', unsafe_allow_html=True)
    if not s.log:
        st.markdown('<p class="lead">No decisions recorded yet. Launch the game to create your report.</p>', unsafe_allow_html=True)
        st.button("🚀  Start new mission", type="primary", width="stretch", on_click=start_game)
        return

    maximum = len(SCENARIOS) * 11
    if s.phase == "finished":
        rating = "🏆 Mission Strategist" if s.score >= 51 else "🧭 Adaptive Explorer" if s.score >= 35 else "🛠️ Rover Team Trainee"
        st.markdown(
            f'<div class="panel"><span class="pill-tag">{rating}</span>'
            f'<div class="big-title" style="margin-top:14px;">{s.score} <span style="font-size:18px;color:#C2CAD9;">/ {maximum} pts</span></div>'
            '<div class="muted">Your decisions affected rover safety, energy and science. There is often a trade-off, even when one action is strongest.</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f'<p class="lead">Progress: {len(s.log)} / {len(SCENARIOS)} decisions complete. Current points: <b>{s.score}</b>.</p>', unsafe_allow_html=True)
        st.button("🎮  Return to active mission", on_click=go_to, args=(NAV[1],), width="stretch", type="primary")
    resources_ui()
    st.markdown('<div class="eyebrow">Your decision history</div>', unsafe_allow_html=True)
    for record in s.log:
        st.markdown(
            '<div class="result-item">'
            f'<div class="small-note">CASE {record["round"]:02d} · +{record["points"]} points · {record["remaining"]} seconds left</div>'
            f'<div class="result-head">{esc(record["scenario"])}</div>'
            f'<div class="result-choose">{esc(record["choice"])}</div>'
            f'<div class="muted" style="margin-top:6px;">{esc(record["outcome"])}</div>'
            '</div>', unsafe_allow_html=True,
        )
    st.download_button("⬇️  Download decision log (CSV)", report_csv(),
                       file_name="mars_rover_decision_log.csv", mime="text/csv", width="stretch")
    if s.phase == "finished":
        st.button("🔄  Play again with different choices", on_click=start_game, type="primary", width="stretch")


def guide() -> None:
    st.markdown('<div class="eyebrow">Flight manual</div>', unsafe_allow_html=True)
    st.markdown('<div class="big-title">📘 How to play</div>', unsafe_allow_html=True)
    for icon, title, desc in [
        ("1️⃣", "Read the emergency", "Each case starts with a rover problem and a specific mission goal."),
        ("2️⃣", "Check three data points", "Compare the measurements, and open the engineering notes for extra clues."),
        ("3️⃣", "Decide within three minutes", "Choose one of the three actions. The clock does not pause when you navigate away."),
        ("4️⃣", "Explain your choice", "Optionally write a short reason. A mission note of 15+ characters earns one participation point."),
        ("5️⃣", "See the consequence", "Each action changes safety, energy and science. Learn from the outcome."),
        ("6️⃣", "Finish and reflect", "After six cases, view your score and download a report of your choices."),
    ]:
        telemetry_card(icon, title, desc)
    st.markdown(
        '<div class="panel"><div class="panel-title">🔬 NASA research that inspired the game</div>'
        '<div class="muted">NASA explains that Earth–Mars signals can take about 4–24 minutes one way. '
        'Perseverance uses autonomous navigation technology to identify obstacles and plan safe routes. '
        'The game presents made-up rover telemetry and outcomes so players can practise reasoning and risk assessment.</div>'
        '<div class="small-note" style="margin-top:9px;">'
        'Learn more: <a style="color:#9BE8E0" href="https://www.nasa.gov/centers-and-facilities/goddard/space-communications-7-things-you-need-to-know/" target="_blank">NASA space communication</a>'
        ' · <a style="color:#9BE8E0" href="https://science.nasa.gov/resource/how-perseverance-drives-on-mars/" target="_blank">NASA rover navigation</a>'
        ' · <a style="color:#9BE8E0" href="https://science.nasa.gov/mission/mars-2020-perseverance/rover-components/" target="_blank">Rover systems</a>'
        '</div></div>', unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="panel"><div class="panel-title">🔒 Privacy and credits</div>'
        '<div class="muted">No name, email, school details or login is requested. Your mission choices stay in your current Streamlit session; '
        'you can optionally download your own report. Original Mars artwork is included with this app. '
        'This is an independent educational simulation, not a NASA product or an official NASA mission.</div></div>',
        unsafe_allow_html=True,
    )
    st.button("🚀  Begin the challenge", type="primary", width="stretch", on_click=start_game)


initialize()
brand()
st.segmented_control("Navigate", NAV, key="view", required=True, label_visibility="collapsed", width="stretch")

page = st.session_state.view
if page == NAV[0]:
    home()
elif page == NAV[1]:
    play()
elif page == NAV[2]:
    report()
else:
    guide()

st.markdown(
    '<div class="credit">THE 3-MINUTE DECISION · INDEPENDENT EDUCATIONAL GAME<br>'
    'Fictional scenarios inspired by NASA Mars exploration research · Not affiliated with NASA</div>',
    unsafe_allow_html=True,
)
