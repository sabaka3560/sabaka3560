"""Generate the profile banner and project cards (SVG) in tanmaybohra.com's theme."""
import os, textwrap
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
BG, CARD, BORDER, FG, SOFT, MUTED, ACC = "#0e0e0e", "#141414", "#232323", "#f0ede8", "#b0aba4", "#888888", "#c8ff57"
HEAD = "Syne, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'DM Mono', ui-monospace, 'SFMono-Regular', Consolas, monospace"
BODY = "'DM Sans', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"


def banner():
    lines = ["agentic AI pipelines that cite their reasons",
             "Go &amp; TypeScript APIs built for load",
             "tools that remove manual work inside teams"]
    n = len(lines); cyc = 3.5 * n
    rotors = "".join(
        f'<text class="rot" style="animation-delay:{i*3.5}s" x="64" y="214">{t}</text>' for i, t in enumerate(lines))
    # one slot = 1/n of the cycle: fade in, hold, fade out
    p = 100 / n
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="Tanmay Bohra, full-stack engineer and consultant, Mumbai">
<style>
 .name{{font:800 72px {HEAD};fill:{FG};letter-spacing:-1.5px}}
 .sub{{font:400 22px {MONO};fill:{SOFT}}}
 .rot{{font:400 22px {MONO};fill:{ACC};opacity:0;animation:rot {cyc}s infinite}}
 .lbl{{font:500 15px {MONO};fill:{MUTED};letter-spacing:2px}}
 .dot{{animation:pulse 2s ease-in-out infinite;transform-origin:1085px 64px}}
 .scan{{animation:scan 7s linear infinite}}
 @keyframes rot{{0%{{opacity:0;transform:translateY(8px)}}{p*0.12:.2f}%{{opacity:1;transform:none}}{p*0.85:.2f}%{{opacity:1}}{p:.2f}%,100%{{opacity:0}}}}
 @keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.35;transform:scale(.7)}}}}
 @keyframes scan{{0%{{transform:translateX(-300px)}}100%{{transform:translateX(1500px)}}}}
 @media (prefers-reduced-motion:reduce){{.rot,.dot,.scan{{animation:none}}.rot:first-of-type{{opacity:1}}}}
</style>
<defs>
 <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{BORDER}" stroke-width="1"/></pattern>
 <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity=".2"/><stop offset=".55" stop-color="{BG}" stop-opacity=".85"/><stop offset="1" stop-color="{BG}"/></linearGradient>
 <linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset=".5" stop-color="{ACC}" stop-opacity=".10"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient>
 <clipPath id="c"><rect width="1200" height="300" rx="18"/></clipPath>
</defs>
<g clip-path="url(#c)">
 <rect width="1200" height="300" fill="{BG}"/>
 <rect width="1200" height="300" fill="url(#g)"/>
 <rect width="1200" height="300" fill="url(#fade)" transform="scale(-1,1) translate(-1200,0)"/>
 <rect class="scan" x="0" y="0" width="260" height="300" fill="url(#beam)"/>
 <text class="lbl" x="64" y="70">FULL-STACK ENGINEER &amp; CONSULTANT · MUMBAI</text>
 <text class="name" x="60" y="146">Tanmay Bohra</text>
 <text class="sub" x="64" y="186">I build</text>
 {rotors}
 <rect x="64" y="246" width="56" height="4" rx="2" fill="{ACC}"/>
 <text class="lbl" x="136" y="252">tanmaybohra.com</text>
 <circle class="dot" cx="1085" cy="64" r="7" fill="{ACC}"/>
 <text class="lbl" x="1070" y="70" text-anchor="end">AVAILABLE FOR WORK</text>
</g>
<rect x=".5" y=".5" width="1199" height="299" rx="18" fill="none" stroke="{BORDER}"/>
</svg>'''
    # "I build" sits on y=186, rotating line just below it
    open(os.path.join(OUT, "banner.svg"), "w", encoding="utf-8").write(svg)


CARDS = [
    # slug, title, kind, desc, tags
    ("arova", "Arova", "LIVE", "Agentic accounting for Indian fund managers: TDS and GST decisions with citable reasons, journals posted to Tally or ERPNext.", ["AI agents", "Python", "Accounting"]),
    ("zupabilling", "ZupaBilling · Countersign", "LIVE", "Checks a seller with live Google evidence and signs the exact cart before an AI agent can pay. Paytm × Etriq AI Hackathon Finals.", ["Agent payments", "Ed25519", "MCP"]),
    ("auditflow", "AuditFlow", "LIVE", "Define audit checks, upload documents; an AI agent runs the workflow and returns a compliance report.", ["AI workflow", "Compliance"]),
    ("travel-refund", "Travel Refund Assurance", "CODE", "Reconstructs the airline refund a passenger was owed under the fare rules in force, with evidence behind every rupee. No LLM in the math.", ["Python", "FastAPI", "Deterministic"]),
    ("procurement", "Procurement Agent · Zinc &amp; Steel", "CODE", "Live market data, tariff resolution and landed cost, turned into buy / when / where recommendations with probabilities.", ["Python", "Forecasting", "Agents"]),
    ("salonflow", "SalonFlow", "CODE", "Mobile-first field sales CRM for salon distributors: leads, demos, purchase orders and dispatch with role-based access.", ["React 19", "TanStack", "Supabase"]),
    ("nekomachi", "Nekomachi", "PLAY", "A 3D rooftop cat runner in the browser. Installable, works offline, world leaderboard.", ["Three.js", "PWA", "Game"]),
    ("space-local", "Space Local", "PLAY", "A pixel-art Mumbai Local endless runner, in space. One self-contained HTML file.", ["Canvas", "Pixel art", "Game"]),
]


def card(slug, title, kind, desc, tags):
    W, H = 600, 190
    desc_lines = textwrap.wrap(desc.replace("&amp;", "&"), 70)[:3]
    dl = "".join(f'<tspan x="28" dy="{0 if i == 0 else 21}">{escape(l)}</tspan>' for i, l in enumerate(desc_lines))
    x = 28; chips = ""
    for t in tags:
        w = 16 + 7.6 * len(t)
        chips += f'<rect x="{x}" y="152" width="{w:.0f}" height="22" rx="11" fill="none" stroke="{BORDER}"/><text class="chip" x="{x + w/2:.0f}" y="167" text-anchor="middle">{escape(t)}</text>'
        x += w + 8
    bw = 66
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<style>
 .t{{font:700 22px {HEAD};fill:{FG}}}
 .d{{font:400 14.5px {BODY};fill:{SOFT}}}
 .chip{{font:400 12px {MONO};fill:{MUTED}}}
 .b{{font:500 12px {MONO};fill:{BG};letter-spacing:1px}}
 .edge{{animation:e 10s ease-in-out infinite}}
 @keyframes e{{0%,80%,100%{{opacity:0}}88%{{opacity:1}}}}
 @media (prefers-reduced-motion:reduce){{.edge{{animation:none}}}}
</style>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{CARD}" stroke="{BORDER}"/>
<rect class="edge" x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{ACC}" stroke-opacity=".55"/>
<text class="t" x="28" y="44">{title}</text>
<rect x="{W-28-bw}" y="26" width="{bw}" height="22" rx="11" fill="{ACC}"/>
<text class="b" x="{W-28-bw/2}" y="41" text-anchor="middle">{kind} ↗</text>
<text class="d" x="28" y="78">{dl}</text>
{chips}
</svg>'''
    open(os.path.join(OUT, f"card-{slug}.svg"), "w", encoding="utf-8").write(svg)


if __name__ == "__main__":
    banner()
    for i, c in enumerate(CARDS):
        card(*c)
    print("ok", sorted(os.listdir(OUT)))
