#!/usr/bin/env python3
"""Generate navigable HTML issue pages from markdown source files."""

import os
import re

ISSUES_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(ISSUES_DIR, "html")

# Ordered issue list: (id, filename_stem, short_title, category)
ISSUES = [
    ("1a",  "01a-local-dev-environment",                           "Local dev environment",                            "Foundation"),
    ("1b",  "01b-gcp-production-deployment",                       "GCP production deployment",                        "Foundation"),
    ("2",   "02-authentication-identity",                          "Authentication & identity",                        "Foundation"),
    ("3",   "03-curriculum-structure",                             "Curriculum structure",                             "Foundation"),
    ("4",   "04-coaching-center-enrollment-teacher-assignment",    "CoachingCenter, Enrollment & TeacherAssignment",   "Foundation"),
    ("5",   "05-ncert-corpus-ingestion-rag-service",               "NCERTCorpus ingestion CLI + RAGService",           "AI Content Infrastructure"),
    ("6",   "06-question-bank-generation-sampler",                 "QuestionBank generation CLI + QuestionBankSampler","AI Content Infrastructure"),
    ("7",   "07-explanation-session-backend",                      "ExplanationSession backend",                       "Core Learning Backend"),
    ("8",   "08-teacher-flag-notification-dispatcher",             "TeacherFlag + NotificationDispatcher",             "Core Learning Backend"),
    ("9",   "09-mini-test-backend",                                "MiniTest backend",                                 "Core Learning Backend"),
    ("10",  "10-proficiency-engine-timed-test-backend",            "ProficiencyEngine + TimedTest backend",            "Core Learning Backend"),
    ("11",  "11-daily-concept-revision-session-backend",           "DailyConcept + RevisionSession backend",           "Core Learning Backend"),
    ("12a", "12a-scheduled-test-authoring-window-management",      "ScheduledTest authoring & window management",      "Core Learning Backend"),
    ("12b", "12b-scheduled-test-gatekeeper",                       "ScheduledTestGatekeeper",                          "Core Learning Backend"),
    ("13",  "13-study-note-backend",                               "StudyNote backend",                                "Core Learning Backend"),
    ("14",  "14-performance-report-backend",                       "PerformanceReport backend",                        "Core Learning Backend"),
    ("15",  "15-fcm-push-notifications",                           "FCM push notifications",                           "Core Learning Backend"),
    ("16",  "16-student-app-scaffold-auth-navigation",             "Student app — scaffold + auth + navigation",       "Student App"),
    ("17",  "17-student-app-explanation-session-mini-test-ui",     "Student app — ExplanationSession + MiniTest UI",   "Student App"),
    ("18",  "18-student-app-timed-test-ui",                        "Student app — TimedTest UI",                       "Student App"),
    ("19",  "19-student-app-scheduled-test-ui",                    "Student app — ScheduledTest UI",                   "Student App"),
    ("20",  "20-student-app-daily-concept-revision-session-ui",    "Student app — DailyConcept + RevisionSession UI",  "Student App"),
    ("21",  "21-student-app-performance-report-study-note-ui",     "Student app — PerformanceReport + StudyNote UI",   "Student App"),
    ("22",  "22-teacher-portal-scaffold-auth",                     "TeacherPortal — scaffold + auth",                  "Teacher Portal"),
    ("23",  "23-teacher-portal-daily-concept-study-note-ui",       "TeacherPortal — DailyConcept + StudyNote UI",      "Teacher Portal"),
    ("24",  "24-teacher-portal-scheduled-test-ui",                 "TeacherPortal — ScheduledTest authoring + results","Teacher Portal"),
    ("25",  "25-teacher-portal-teacher-flag-student-monitoring-ui","TeacherPortal — TeacherFlag + student monitoring", "Teacher Portal"),
    ("26",  "26-teacher-portal-center-admin-configuration-ui",     "TeacherPortal — CenterAdmin configuration",        "Teacher Portal"),
]

# Map issue id → (filename_stem, short_title)
ID_MAP = {issue_id: (stem, title) for issue_id, stem, title, _ in ISSUES}

CATEGORY_ORDER = [
    "Foundation",
    "AI Content Infrastructure",
    "Core Learning Backend",
    "Student App",
    "Teacher Portal",
]

CATEGORY_COLORS = {
    "Foundation":               "#4f46e5",
    "AI Content Infrastructure":"#0891b2",
    "Core Learning Backend":    "#059669",
    "Student App":              "#d97706",
    "Teacher Portal":           "#dc2626",
}

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f8fafc;
    color: #1e293b;
    line-height: 1.6;
    font-size: 15px;
}

a { color: #4f46e5; text-decoration: none; }
a:hover { text-decoration: underline; }

.topbar {
    background: #1e293b;
    color: #f1f5f9;
    padding: 12px 32px;
    display: flex;
    align-items: center;
    gap: 16px;
    font-size: 13px;
    position: sticky;
    top: 0;
    z-index: 100;
}
.topbar a { color: #94a3b8; }
.topbar a:hover { color: #f1f5f9; text-decoration: none; }
.topbar .sep { color: #475569; }
.topbar .current { color: #f1f5f9; font-weight: 600; }

.container {
    max-width: 860px;
    margin: 40px auto;
    padding: 0 24px 80px;
}

.issue-header {
    margin-bottom: 32px;
}
.issue-id {
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 4px;
    margin-bottom: 10px;
    color: white;
}
.issue-header h1 {
    font-size: 26px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.3;
}

.section {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.section h2 {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748b;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid #f1f5f9;
}
.section p {
    color: #334155;
    margin-bottom: 12px;
}
.section p:last-child { margin-bottom: 0; }

.section ul, .section ol {
    padding-left: 20px;
    color: #334155;
}
.section li { margin-bottom: 6px; }
.section code {
    background: #f1f5f9;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 13px;
    color: #0f172a;
}

.checklist { list-style: none; padding-left: 0; }
.checklist li {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 6px 0;
    border-bottom: 1px solid #f8fafc;
    color: #334155;
}
.checklist li:last-child { border-bottom: none; }
.checklist input[type=checkbox] {
    margin-top: 3px;
    flex-shrink: 0;
    width: 15px;
    height: 15px;
    accent-color: #4f46e5;
    cursor: pointer;
}

.blocker-list { list-style: none; padding-left: 0; }
.blocker-list li {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid #f8fafc;
}
.blocker-list li:last-child { border-bottom: none; }
.blocker-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    color: white;
    flex-shrink: 0;
}
.blocker-list a { font-weight: 500; color: #4f46e5; }

.none-tag {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
}

.nav-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 32px;
    gap: 12px;
}
.nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 9px 18px;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    color: #475569;
    font-size: 13px;
    font-weight: 500;
    transition: background 0.15s;
}
.nav-btn:hover { background: #f1f5f9; text-decoration: none; color: #1e293b; }
.nav-btn.disabled { opacity: 0.35; pointer-events: none; }

/* Index styles */
.index-hero {
    text-align: center;
    padding: 48px 0 36px;
}
.index-hero h1 {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
}
.index-hero p {
    color: #64748b;
    font-size: 15px;
}

.category-section { margin-bottom: 40px; }
.category-title {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 6px 14px;
    border-radius: 6px;
    display: inline-block;
    color: white;
    margin-bottom: 14px;
}
.issue-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.issue-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: box-shadow 0.15s, border-color 0.15s;
}
.issue-card:hover {
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border-color: #c7d2fe;
    text-decoration: none;
}
.issue-card .card-id {
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    color: white;
    flex-shrink: 0;
    min-width: 42px;
    text-align: center;
}
.issue-card .card-title {
    font-weight: 600;
    color: #0f172a;
    font-size: 14px;
}
.issue-card .card-blockers {
    margin-left: auto;
    font-size: 12px;
    color: #94a3b8;
    flex-shrink: 0;
}
"""


def html_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def parse_markdown(md_text):
    """
    Returns dict with keys: title, what_to_build, acceptance_criteria, blocked_by_raw
    """
    sections = {}
    current_section = None
    lines = md_text.strip().splitlines()
    buf = []

    for line in lines:
        if line.startswith("## "):
            if current_section is not None:
                sections[current_section] = "\n".join(buf).strip()
            current_section = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current_section:
        sections[current_section] = "\n".join(buf).strip()

    return sections


def render_body_text(text):
    """Convert simple markdown body (paragraphs, bullet lists, code) to HTML."""
    lines = text.splitlines()
    html_parts = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("- ") or stripped.startswith("* "):
            # Collect list items
            items = []
            while i < len(lines) and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(lines[i].strip()[2:])
                i += 1
            html_parts.append("<ul>")
            for item in items:
                html_parts.append(f"  <li>{inline_md(item)}</li>")
            html_parts.append("</ul>")
            continue

        elif stripped == "":
            i += 1
            continue

        else:
            # Collect paragraph lines
            para_lines = []
            while i < len(lines) and lines[i].strip() != "" and not lines[i].strip().startswith("- ") and not lines[i].strip().startswith("* ") and not lines[i].startswith("#"):
                para_lines.append(lines[i].strip())
                i += 1
            if para_lines:
                html_parts.append(f"<p>{inline_md(' '.join(para_lines))}</p>")
            continue

        i += 1

    return "\n".join(html_parts)


def inline_md(text):
    """Convert inline markdown (bold, code, links) to HTML."""
    # code
    text = re.sub(r'`([^`]+)`', lambda m: f'<code>{html_escape(m.group(1))}</code>', text)
    # bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text


def render_acceptance_criteria(text):
    """Render - [ ] checklist items as HTML checkboxes."""
    lines = text.strip().splitlines()
    items = []
    for line in lines:
        m = re.match(r'\s*-\s*\[\s*\]\s*(.*)', line)
        if m:
            items.append(m.group(1).strip())
    if not items:
        return f"<p>{html_escape(text)}</p>"
    parts = ['<ul class="checklist">']
    for item in items:
        parts.append(f'  <li><input type="checkbox"> <span>{inline_md(item)}</span></li>')
    parts.append("</ul>")
    return "\n".join(parts)


def render_blocked_by(text):
    """Render blocked-by section, converting #Nx references to links."""
    stripped = text.strip()

    if "None" in stripped and len(stripped) < 60:
        return '<span class="none-tag">None — can start immediately</span>'

    lines = stripped.splitlines()
    items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Strip leading "- "
        if line.startswith("- "):
            line = line[2:]
        items.append(line)

    if not items:
        return f"<p>{html_escape(stripped)}</p>"

    parts = ['<ul class="blocker-list">']
    for item in items:
        # Find issue reference like #1a, #12b, #7 etc.
        m = re.search(r'#(\w+)', item)
        if m:
            ref_id = m.group(1)
            if ref_id in ID_MAP:
                stem, title = ID_MAP[ref_id]
                _, _, _, cat = next(i for i in ISSUES if i[0] == ref_id)
                color = CATEGORY_COLORS.get(cat, "#64748b")
                desc = re.sub(r'#\w+\s*', '', item).strip()
                desc_html = f" — {html_escape(desc)}" if desc else ""
                parts.append(
                    f'  <li>'
                    f'<span class="blocker-badge" style="background:{color}">#{ref_id}</span>'
                    f'<a href="{stem}.html">{html_escape(title)}</a>'
                    f'{desc_html}'
                    f'</li>'
                )
            else:
                parts.append(f'  <li>{html_escape(item)}</li>')
        else:
            parts.append(f'  <li>{html_escape(item)}</li>')

    parts.append("</ul>")
    return "\n".join(parts)


def make_issue_page(issue_id, stem, title, category, prev_issue, next_issue, sections):
    color = CATEGORY_COLORS.get(category, "#64748b")

    what_html = render_body_text(sections.get("What to build", ""))
    criteria_html = render_acceptance_criteria(sections.get("Acceptance criteria", ""))
    blocked_html = render_blocked_by(sections.get("Blocked by", "None"))

    prev_btn = ""
    if prev_issue:
        prev_stem = prev_issue[1]
        prev_title = prev_issue[2]
        prev_btn = f'<a class="nav-btn" href="{prev_stem}.html">&#8592; {html_escape(prev_title)}</a>'
    else:
        prev_btn = '<span class="nav-btn disabled">&#8592; Previous</span>'

    next_btn = ""
    if next_issue:
        next_stem = next_issue[1]
        next_title = next_issue[2]
        next_btn = f'<a class="nav-btn" href="{next_stem}.html">{html_escape(next_title)} &#8594;</a>'
    else:
        next_btn = '<span class="nav-btn disabled">Next &#8594;</span>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>#{issue_id} {html_escape(title)} — Vidyasaarthi</title>
  <style>{CSS}</style>
</head>
<body>

<div class="topbar">
  <a href="index.html">Vidyasaarthi Issues</a>
  <span class="sep">›</span>
  <span class="current">#{issue_id} {html_escape(title)}</span>
</div>

<div class="container">

  <div class="issue-header">
    <div class="issue-id" style="background:{color}">#{issue_id} · {html_escape(category)}</div>
    <h1>{html_escape(title)}</h1>
  </div>

  <div class="section">
    <h2>What to build</h2>
    {what_html}
  </div>

  <div class="section">
    <h2>Acceptance criteria</h2>
    {criteria_html}
  </div>

  <div class="section">
    <h2>Blocked by</h2>
    {blocked_html}
  </div>

  <div class="nav-row">
    {prev_btn}
    <a class="nav-btn" href="index.html">&#8617; All issues</a>
    {next_btn}
  </div>

</div>
</body>
</html>"""


def make_index_page(issues_by_category):
    total = sum(len(v) for v in issues_by_category.values())

    category_blocks = []
    for cat in CATEGORY_ORDER:
        if cat not in issues_by_category:
            continue
        color = CATEGORY_COLORS.get(cat, "#64748b")
        cards = []
        for issue_id, stem, title, _ in issues_by_category[cat]:
            # Count blockers
            md_path = os.path.join(ISSUES_DIR, f"{stem}.md")
            blocker_count = 0
            if os.path.exists(md_path):
                with open(md_path) as f:
                    content = f.read()
                blockers_section = re.search(r'## Blocked by\s*(.*?)(?=##|\Z)', content, re.DOTALL)
                if blockers_section:
                    refs = re.findall(r'#\w+', blockers_section.group(1))
                    blocker_count = len(refs)

            blocker_text = ""
            if blocker_count == 0:
                blocker_text = '<span style="color:#22c55e;font-weight:600;">No blockers</span>'
            else:
                blocker_text = f'{blocker_count} blocker{"s" if blocker_count > 1 else ""}'

            cards.append(f"""    <a class="issue-card" href="{stem}.html">
      <span class="card-id" style="background:{color}">#{issue_id}</span>
      <span class="card-title">{html_escape(title)}</span>
      <span class="card-blockers">{blocker_text}</span>
    </a>""")

        category_blocks.append(f"""  <div class="category-section">
    <div class="category-title" style="background:{color}">{html_escape(cat)}</div>
    <div class="issue-grid">
{chr(10).join(cards)}
    </div>
  </div>""")

    blocks_html = "\n".join(category_blocks)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vidyasaarthi — Issues</title>
  <style>{CSS}</style>
</head>
<body>

<div class="topbar">
  <span class="current">Vidyasaarthi Issues</span>
</div>

<div class="container">

  <div class="index-hero">
    <h1>Vidyasaarthi</h1>
    <p>{total} issues &nbsp;·&nbsp; {len(CATEGORY_ORDER)} categories</p>
  </div>

{blocks_html}

</div>
</body>
</html>"""


def main():
    issues_by_category = {}
    for issue in ISSUES:
        cat = issue[3]
        issues_by_category.setdefault(cat, []).append(issue)

    # Generate individual issue pages
    for idx, (issue_id, stem, title, category) in enumerate(ISSUES):
        md_path = os.path.join(ISSUES_DIR, f"{stem}.md")
        if not os.path.exists(md_path):
            print(f"  SKIP (not found): {md_path}")
            continue

        with open(md_path) as f:
            md_text = f.read()

        sections = parse_markdown(md_text)

        prev_issue = ISSUES[idx - 1] if idx > 0 else None
        next_issue = ISSUES[idx + 1] if idx < len(ISSUES) - 1 else None

        html = make_issue_page(issue_id, stem, title, category, prev_issue, next_issue, sections)

        out_path = os.path.join(HTML_DIR, f"{stem}.html")
        with open(out_path, "w") as f:
            f.write(html)
        print(f"  OK: {stem}.html")

    # Generate index
    index_html = make_index_page(issues_by_category)
    index_path = os.path.join(HTML_DIR, "index.html")
    with open(index_path, "w") as f:
        f.write(index_html)
    print(f"  OK: index.html")
    print(f"\nDone. Open: {index_path}")


if __name__ == "__main__":
    main()
