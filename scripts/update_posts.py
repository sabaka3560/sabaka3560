"""Refresh the 'Latest writing' block in README.md from the blog's RSS feed (run by GitHub Actions daily)."""
import re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

FEED = "https://blogs.tanmaybohra.com/rss.xml"
readme = Path(__file__).resolve().parent.parent / "README.md"

req = urllib.request.Request(FEED, headers={"User-Agent": "profile-readme-updater"})
root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
items = root.findall("./channel/item")[:5]
if not items:
    raise SystemExit("feed had no items; leaving README unchanged")
lines = [f"- [{i.findtext('title').strip()}]({i.findtext('link').strip()})" for i in items]
block = "<!-- posts:start -->\n" + "\n".join(lines) + "\n<!-- posts:end -->"

text = readme.read_text(encoding="utf-8")
new = re.sub(r"<!-- posts:start -->.*?<!-- posts:end -->", block, text, flags=re.S)
if new != text:
    readme.write_text(new, encoding="utf-8")
    print("updated")
else:
    print("no change")
