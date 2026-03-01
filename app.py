import requests
import streamlit as st

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE    = "https://movie-rec-466x.onrender.com"
TMDB_IMG    = "https://image.tmdb.org/t/p/w500"
TMDB_ORIG   = "https://image.tmdb.org/t/p/original"

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

# ─────────────────────────────────────────────
# INLINE SVG ICONS  (Lucide-compatible)
# ─────────────────────────────────────────────
def ic(name: str, size: int = 16, color: str = "currentColor") -> str:
    paths = {
        "film":        '<rect x="2" y="2" width="20" height="20" rx="2"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="17" y1="7" x2="22" y2="7"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="2" y1="17" x2="7" y2="17"/>',
        "home":        '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
        "search":      '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
        "star":        '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
        "calendar":    '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
        "clock":       '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        "play":        '<polygon points="5 3 19 12 5 21 5 3"/>',
        "arrow-left":  '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
        "trending-up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
        "award":       '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>',
        "grid":        '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',
        "sparkles":    '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>',
        "info":        '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
        "popcorn":     '<path d="M18 8a2 2 0 0 0 0-4 2 2 0 0 0-4 0 2 2 0 0 0-4 0 2 2 0 0 0-4 0 2 2 0 0 0 0 4"/><path d="m5 8 1 12c.1.7.6 1.2 1.3 1.2h9.4c.7 0 1.2-.5 1.3-1.2L19 8"/>',
        "clapper":     '<path d="M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z"/><path d="m6.2 5.3 3.1 3.9"/><path d="m12.4 3.4 3.1 3.9"/><path d="M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
        "layers":      '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    }
    inner = paths.get(name, "")
    fill = color if name in ("star", "play") else "none"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="{fill}" stroke="{color}" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>'
    )


# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --void:      #07070c;
  --surface:   #0e0e18;
  --card:      #13131f;
  --card2:     #1a1a2a;
  --border:    rgba(255,255,255,0.07);
  --gold:      #d4a84b;
  --gold-lt:   #f0cc80;
  --gold-dim:  #8a6a28;
  --rose:      #c44569;
  --purple:    #7b5ea7;
  --t1:        #f2efe8;
  --t2:        #9996a8;
  --t3:        #5a5770;
  --r:         10px;
}

/* ── RESET ── */
.stApp { background: var(--void) !important; font-family: 'DM Sans', sans-serif !important; color: var(--t1) !important; }
#MainMenu, footer, header { visibility: hidden; }
* { box-sizing: border-box; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: var(--gold-dim); border-radius: 2px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span { color: var(--t2) !important; font-size: 0.82rem !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid var(--border) !important;
  color: var(--t2) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  border-radius: 8px !important;
  padding: 0.45rem 1rem !important;
  transition: all 0.22s ease !important;
  height: auto !important;
}
.stButton > button:hover {
  background: rgba(212,168,75,0.08) !important;
  border-color: rgba(212,168,75,0.3) !important;
  color: var(--gold) !important;
  transform: translateY(-1px) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 50px !important;
  color: var(--t1) !important;
  font-family: 'DM Sans', sans-serif !important;
  padding: 0.7rem 1.4rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--gold-dim) !important;
  box-shadow: 0 0 0 3px rgba(212,168,75,0.07) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--t3) !important; }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--t1) !important;
}

/* ── HR ── */
hr { border-color: var(--border) !important; opacity: 1 !important; margin: 1.5rem 0 !important; }

/* ── ANIMATIONS ── */
@keyframes fadeUp   { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeIn   { from { opacity:0; } to { opacity:1; } }
@keyframes spin     { to { transform:rotate(360deg); } }
@keyframes float    { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-20px,15px)} }

/* ── BACKGROUND ORBS ── */
.orb {
  position: fixed; border-radius: 50%;
  filter: blur(100px); pointer-events: none; z-index: 0;
}
.orb1 { width:500px;height:500px; background:radial-gradient(circle,rgba(123,94,167,.09),transparent 70%); top:-150px;right:-80px; animation:float 22s ease-in-out infinite; }
.orb2 { width:400px;height:400px; background:radial-gradient(circle,rgba(196,69,105,.06),transparent 70%); bottom:50px;left:-60px; animation:float 28s ease-in-out infinite reverse; }
.orb3 { width:300px;height:300px; background:radial-gradient(circle,rgba(212,168,75,.05),transparent 70%); top:45%;left:45%; animation:float 35s ease-in-out infinite; }

/* ── SIDEBAR LOGO ── */
.sb-logo { display:flex;align-items:center;gap:10px;padding:0 0 1.5rem;margin-bottom:1.5rem;border-bottom:1px solid var(--border); }
.sb-logo-icon { width:34px;height:34px;background:linear-gradient(135deg,var(--gold) 0%,var(--rose) 100%);border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0; }
.sb-logo-name { font-family:'Cormorant Garamond',serif !important;font-size:1.25rem !important;font-weight:700 !important;color:var(--gold) !important;letter-spacing:.04em !important; }
.sb-label { font-size:.62rem !important;font-weight:600 !important;letter-spacing:.16em !important;text-transform:uppercase !important;color:var(--t3) !important;margin:1.2rem 0 .5rem !important;display:block; }

/* ── HERO ── */
.hero { text-align:center;padding:4.5rem 1rem 2.5rem;animation:fadeUp .6s ease both; }
.hero-badge { display:inline-flex;align-items:center;gap:6px;font-size:.68rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);background:rgba(212,168,75,.08);border:1px solid rgba(212,168,75,.18);border-radius:100px;padding:.28rem .9rem;margin-bottom:1.2rem; }
.hero-title { font-family:'Cormorant Garamond',serif;font-size:clamp(2.6rem,5.5vw,4.2rem);font-weight:700;line-height:1.08;color:var(--t1);margin:.1rem 0 .6rem;letter-spacing:-.015em; }
.hero-title em { font-style:italic;background:linear-gradient(120deg,var(--gold) 0%,var(--gold-lt) 50%,var(--rose) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.hero-sub { font-size:.98rem;color:var(--t2);font-weight:300;letter-spacing:.01em; }

/* ── CATEGORY PILLS ── */
.cat-bar { display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap;margin:1.5rem 0 .5rem; }
.cat-pill { display:inline-flex;align-items:center;gap:5px;padding:.3rem .85rem;border-radius:100px;font-size:.75rem;font-weight:500;border:1px solid var(--border);color:var(--t3);background:var(--card);cursor:pointer; }
.cat-pill.on { background:rgba(212,168,75,.1);border-color:rgba(212,168,75,.28);color:var(--gold); }

/* ── SECTION HEADER ── */
.sec-hdr { margin:2.5rem 0 1.2rem;animation:fadeUp .5s ease both; }
.sec-eye { font-size:.62rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-dim); }
.sec-title { font-family:'Cormorant Garamond',serif;font-size:1.7rem;font-weight:700;color:var(--t1);margin:.2rem 0 0; }

/* ── MOVIE CARD ── */
.m-wrap { animation:fadeUp .45s ease both; }
.m-wrap:nth-child(1){animation-delay:.04s}
.m-wrap:nth-child(2){animation-delay:.08s}
.m-wrap:nth-child(3){animation-delay:.12s}
.m-wrap:nth-child(4){animation-delay:.16s}
.m-wrap:nth-child(5){animation-delay:.20s}
.m-wrap:nth-child(6){animation-delay:.24s}

/* Poster image styles */
[data-testid="stImage"] img {
  border-radius: var(--r) !important;
  border: 1px solid var(--border) !important;
  display: block !important;
  transition: transform .28s ease, box-shadow .28s ease, border-color .28s ease !important;
  width: 100% !important;
}
[data-testid="stImage"]:hover img {
  transform: translateY(-4px) scale(1.025) !important;
  box-shadow: 0 16px 40px rgba(0,0,0,.7) !important;
  border-color: rgba(212,168,75,.22) !important;
}

.m-title { font-size:.8rem;font-weight:500;color:var(--t2);margin:.5rem 0 .3rem;line-height:1.3;transition:color .2s; }
.m-wrap:hover .m-title { color:var(--t1); }

/* ── VIEW BUTTON (card) ── */
.vbtn > div > button {
  background: transparent !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  color: var(--t3) !important;
  font-size: .7rem !important;
  padding: .2rem .5rem !important;
  border-radius: 6px !important;
  width: 100% !important;
  margin-top: .1rem !important;
}
.vbtn > div > button:hover {
  background: rgba(212,168,75,.1) !important;
  border-color: rgba(212,168,75,.3) !important;
  color: var(--gold) !important;
  transform: none !important;
}

/* ── PLACEHOLDER POSTER ── */
.no-poster { width:100%;aspect-ratio:2/3;background:var(--card);border-radius:var(--r);border:1px solid var(--border);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.5rem;color:var(--t3);font-size:.72rem; }

/* ─────────────────────────────────────────
   BACKDROP — THE KEY FIX
   Uses a plain <img> inside a positioned
   wrapper. No st.image so CSS fully applies.
   Gradient overlay is absolute inside same div.
───────────────────────────────────────── */
.backdrop-wrap {
  position: relative;
  width: 100%;
  height: 440px;
  overflow: hidden;
  border-radius: 0 0 16px 16px;
  margin-bottom: 2rem;
}
.backdrop-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 25%;
  display: block;
  filter: brightness(.72) saturate(.85);
}
/* Bottom gradient fades into page bg */
.backdrop-wrap::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 65%;
  background: linear-gradient(to bottom, transparent 0%, rgba(7,7,12,.85) 60%, rgba(7,7,12,1) 100%);
  pointer-events: none;
}
/* Left vignette */
.backdrop-wrap::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to right, rgba(7,7,12,.55) 0%, transparent 55%);
  pointer-events: none;
  z-index: 1;
}
.backdrop-title-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 1.5rem 2rem;
  z-index: 2;
  animation: fadeUp .5s ease both;
}

/* ── DETAIL CONTENT ── */
.det-wrap { animation:fadeUp .55s ease both;animation-delay:.1s; }
.rating-badge {
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(212,168,75,.1);border:1px solid rgba(212,168,75,.22);
  border-radius:100px;padding:.25rem .85rem;font-size:.88rem;
  font-weight:700;color:var(--gold);margin-bottom:.7rem;
}
.det-title { font-family:'Cormorant Garamond',serif;font-size:clamp(1.9rem,4vw,3rem);font-weight:700;line-height:1.08;color:#fff;margin:.2rem 0 .8rem;letter-spacing:-.015em; }
.meta-pills { display:flex;flex-wrap:wrap;gap:.45rem;margin:.8rem 0; }
.mpill { display:inline-flex;align-items:center;gap:5px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);border-radius:100px;padding:.22rem .75rem;font-size:.73rem;font-weight:500;color:var(--t2); }
.mpill.genre { background:rgba(123,94,167,.12);border-color:rgba(123,94,167,.28);color:#c4b5fd; }
.ov-label { display:flex;align-items:center;gap:6px;font-size:.62rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-dim);margin:1.5rem 0 .5rem; }
.ov-text { font-size:.97rem;line-height:1.78;color:var(--t2);font-weight:300;border-left:2px solid rgba(212,168,75,.2);padding-left:1rem;margin:0; }

/* ── DETAIL POSTER ── */
.det-poster [data-testid="stImage"] img {
  border-radius: var(--r) !important;
  border: 1px solid rgba(255,255,255,.1) !important;
  box-shadow: 0 24px 60px rgba(0,0,0,.8) !important;
  transform: none !important;
}
.det-poster [data-testid="stImage"]:hover img {
  transform: none !important;
}

/* ── BACK BUTTON ── */
.back-btn > div > button {
  background: rgba(255,255,255,.03) !important;
  border: 1px solid var(--border) !important;
  color: var(--t2) !important;
  width: 100% !important;
  margin-top: 1rem !important;
}
.back-btn > div > button:hover {
  background: rgba(123,94,167,.1) !important;
  border-color: rgba(123,94,167,.35) !important;
  color: #c4b5fd !important;
  transform: none !important;
}

/* ── RECS DIVIDER ── */
.recs-div { display:flex;align-items:center;gap:1rem;margin:3rem 0 2rem; }
.recs-div-line { flex:1;height:1px;background:linear-gradient(to right,transparent,var(--border),transparent); }
.recs-div-txt { font-size:.62rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--t3);white-space:nowrap; }

/* ── SPINNER ── */
.spinner-wrap { display:flex;flex-direction:column;align-items:center;gap:1rem;padding:3rem;color:var(--t3);font-size:.83rem; }
.spin-ring { width:32px;height:32px;border:2px solid var(--border);border-top-color:var(--gold);border-radius:50%;animation:spin .75s linear infinite; }

/* ── EMPTY STATE ── */
.empty { text-align:center;padding:4rem 2rem;color:var(--t3);animation:fadeIn .5s ease; }
.empty-icon { margin-bottom:.8rem;opacity:.35; }

/* ── COLUMN SPACING ── */
[data-testid="column"] { padding: 0 0.35rem !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CATEGORY CONFIG
# ─────────────────────────────────────────────
CATS = {
    "trending":    ("Trending",    "trending-up"),
    "popular":     ("Popular",     "star"),
    "top_rated":   ("Top Rated",   "award"),
    "upcoming":    ("Upcoming",    "clock"),
    "now_playing": ("Now Playing", "play"),
}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "view"      not in st.session_state: st.session_state.view      = "home"
if "tmdb_id"   not in st.session_state: st.session_state.tmdb_id   = None
if "cols"      not in st.session_state: st.session_state.cols      = 6
if "category"  not in st.session_state: st.session_state.category  = "trending"

def goto_home():
    st.session_state.view    = "home"
    st.session_state.tmdb_id = None
    st.rerun()

def goto_detail(tid: int):
    st.session_state.view    = "details"
    st.session_state.tmdb_id = int(tid)
    st.rerun()

# ─────────────────────────────────────────────
# API
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def api(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=20)
        return r.json(), None
    except Exception as e:
        return None, str(e)

# ─────────────────────────────────────────────
# POSTER GRID
# ─────────────────────────────────────────────
def poster_grid(cards, cols=6, prefix="g"):
    if not cards:
        st.markdown(
            f'<div class="empty"><div class="empty-icon">{ic("popcorn",40,"#5a5770")}</div>'
            f'<p>No titles found.</p></div>',
            unsafe_allow_html=True,
        )
        return
    idx = 0
    for _ in range((len(cards) + cols - 1) // cols):
        colset = st.columns(cols, gap="small")
        for c in range(cols):
            if idx >= len(cards): break
            m      = cards[idx]
            tid    = m.get("tmdb_id") or m.get("id")
            title  = m.get("title") or "Untitled"
            poster = m.get("poster_url") or (f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None)
            with colset[c]:
                st.markdown('<div class="m-wrap">', unsafe_allow_html=True)
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.markdown(
                        f'<div class="no-poster">{ic("film",28,"#3a3755")}<span>No Image</span></div>',
                        unsafe_allow_html=True,
                    )
                st.markdown(f'<p class="m-title">{title}</p>', unsafe_allow_html=True)
                st.markdown('<div class="vbtn">', unsafe_allow_html=True)
                if st.button("▶ View", key=f"{prefix}_{idx}_{tid}"):
                    goto_detail(tid)
                st.markdown('</div></div>', unsafe_allow_html=True)
            idx += 1


# ═══════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════
with st.sidebar:
    st.markdown(
        f'<div class="sb-logo">'
        f'  <div class="sb-logo-icon">{ic("clapper",18,"#07070c")}</div>'
        f'  <span class="sb-logo-name">CineMatch</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    if st.button("⌂  Home", use_container_width=True, key="sb_home"):
        goto_home()

    st.markdown('<span class="sb-label">Browse</span>', unsafe_allow_html=True)
    cat_key = st.selectbox(
        "cat",
        list(CATS.keys()),
        format_func=lambda k: CATS[k][0],
        index=list(CATS.keys()).index(st.session_state.category),
        label_visibility="collapsed",
        key="cat_select",
    )
    if cat_key != st.session_state.category:
        st.session_state.category = cat_key

    st.markdown('<span class="sb-label">Display</span>', unsafe_allow_html=True)
    new_cols = st.slider("cols", 3, 8, st.session_state.cols, label_visibility="collapsed")
    if new_cols != st.session_state.cols:
        st.session_state.cols = new_cols
    st.markdown(
        f'<p style="font-size:.68rem;color:var(--t3);text-align:center;margin-top:.3rem">'
        f'{ic("grid",11,"#5a5770")}  {st.session_state.cols} columns</p>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════
# BACKGROUND ORBS
# ═══════════════════════════════════════════
st.markdown(
    '<div class="orb orb1"></div><div class="orb orb2"></div><div class="orb orb3"></div>',
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════
# HOME VIEW
# ═══════════════════════════════════════════════════════════
if st.session_state.view == "home":
    cat_label, cat_icon = CATS[st.session_state.category]

    st.markdown(
        f'<div class="hero">'
        f'  <div class="hero-badge">{ic("sparkles",11,"#d4a84b")} Your Cinema Guide</div>'
        f'  <h1 class="hero-title">Discover your next<br><em>favourite film</em></h1>'
        f'  <p class="hero-sub">Trending picks · Top rated · Hidden gems</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Search bar
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        q = st.text_input("search", placeholder="Search for a movie…", label_visibility="collapsed")

    # Category pills (visual indicator)
    pills = '<div class="cat-bar">'
    for k, (lbl, ico) in CATS.items():
        cls = "on" if k == st.session_state.category else ""
        pills += f'<span class="cat-pill {cls}">{ic(ico,12)} {lbl}</span>'
    pills += '</div>'
    st.markdown(pills, unsafe_allow_html=True)

    # Results
    if q:
        st.markdown(
            f'<div class="sec-hdr"><div class="sec-eye">{ic("search",10)} Results</div>'
            f'<div class="sec-title">"{q}"</div></div>',
            unsafe_allow_html=True,
        )
        data, _ = api("/tmdb/search", {"query": q})
        if data:
            poster_grid(data.get("results", []), st.session_state.cols, "srch")
        else:
            st.markdown('<div class="spinner-wrap"><div class="spin-ring"></div><span>Searching…</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="sec-hdr"><div class="sec-eye">{ic(cat_icon,10)} Now Showing</div>'
            f'<div class="sec-title">{cat_label}</div></div>',
            unsafe_allow_html=True,
        )
        data, _ = api("/home", {"category": st.session_state.category, "limit": 24})
        if data:
            poster_grid(data, st.session_state.cols, "home")
        else:
            st.markdown('<div class="spinner-wrap"><div class="spin-ring"></div><span>Loading titles…</span></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# DETAIL VIEW
# ═══════════════════════════════════════════════════════════
elif st.session_state.view == "details":
    data, err = api(f"/movie/id/{st.session_state.tmdb_id}")

    if not data:
        st.markdown(
            '<div class="empty" style="padding-top:5rem">'
            '<div class="empty-icon">🎬</div>'
            "<p>Couldn't load this movie. Please go back.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Parse data
    backdrop = data.get("backdrop_url") or ""
    poster   = data.get("poster_url") or ""
    title    = data.get("title", "Untitled")
    overview = data.get("overview") or "No description available."
    rating   = data.get("vote_average", 0)
    release  = data.get("release_date", "")
    year     = release[:4] if release else "N/A"
    runtime  = data.get("runtime")
    genres   = data.get("genres", [])

    # ── BACKDROP ─────────────────────────────────────────────
    # Using raw <img> inside a div — NOT st.image — gives us
    # full CSS control: object-fit, pseudo-element overlays, etc.
    if backdrop:
        st.markdown(
            f'<div class="backdrop-wrap">'
            f'  <img src="{backdrop}" alt="{title} backdrop" />'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        # Fallback gradient bar when no backdrop exists
        st.markdown(
            '<div style="height:180px;background:linear-gradient(180deg,#1a1a2a 0%,#07070c 100%);'
            'border-radius:0 0 16px 16px;margin-bottom:2rem"></div>',
            unsafe_allow_html=True,
        )

    # ── MAIN COLUMNS ─────────────────────────────────────────
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown('<div class="det-poster">', unsafe_allow_html=True)
        if poster:
            st.image(poster, use_container_width=True)
        else:
            st.markdown(
                f'<div class="no-poster" style="min-height:360px">'
                f'{ic("film",44,"#3a3755")}<span>No Poster</span></div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back to Home", key="back", use_container_width=True):
            goto_home()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="det-wrap">', unsafe_allow_html=True)

        # Rating badge
        st.markdown(
            f'<div class="rating-badge">{ic("star",14,"#d4a84b")} {rating:.1f} / 10</div>',
            unsafe_allow_html=True,
        )

        # Title
        st.markdown(f'<h1 class="det-title">{title}</h1>', unsafe_allow_html=True)

        # Meta pills
        pills = '<div class="meta-pills">'
        pills += f'<span class="mpill">{ic("calendar",12)} {year}</span>'
        if runtime:
            h, m = divmod(runtime, 60)
            pills += f'<span class="mpill">{ic("clock",12)} {h}h {m}m</span>'
        for g in genres:
            pills += f'<span class="mpill genre">{g["name"]}</span>'
        pills += '</div>'
        st.markdown(pills, unsafe_allow_html=True)

        # Overview
        st.markdown(
            f'<div class="ov-label">{ic("info",11,"#8a6a28")} Overview</div>'
            f'<p class="ov-text">{overview}</p>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RECOMMENDATIONS ──────────────────────────────────────
    st.markdown(
        f'<div class="recs-div">'
        f'  <div class="recs-div-line"></div>'
        f'  <span class="recs-div-txt">{ic("sparkles",10)} More Like This</span>'
        f'  <div class="recs-div-line"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sec-hdr">'
        f'  <div class="sec-eye">{ic("layers",10)} Personalized</div>'
        f'  <div class="sec-title">You Might Also Love</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    rec, _ = api("/recommend/genre", {"tmdb_id": st.session_state.tmdb_id, "limit": 12})
    if rec:
        poster_grid(rec, st.session_state.cols, "rec")
    else:
        st.markdown(
            '<div class="spinner-wrap"><div class="spin-ring"></div>'
            '<span>Finding similar titles…</span></div>',
            unsafe_allow_html=True,
        )