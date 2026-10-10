"""Build the profile's self-contained SVG panels. Run with Python 3, no packages needed."""
from pathlib import Path
import copy
import math
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
BG, FG, MUTED, RED, LINE = "#0d0d10", "#f7f7fb", "#a5a5b3", "#dc2626", "#292930"
SANS = "Inter, system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, monospace"


def el(parent, tag, **attrs):
    return ET.SubElement(parent, f"{{{NS}}}{tag}", {k.replace('_', '-'): str(v) for k, v in attrs.items()})


def text(parent, x, y, value, size=18, color=FG, weight=400, mono=False, **attrs):
    node = el(parent, "text", x=x, y=y, fill=color, font_size=size,
              font_family=MONO if mono else SANS, font_weight=weight, **attrs)
    node.text = value
    return node


def panel(title, description, height, width=390):
    root = ET.Element(f"{{{NS}}}svg", {"width": str(width), "height": str(height),
                                       "viewBox": f"0 0 {width} {height}", "role": "img"})
    el(root, "title").text = title
    el(root, "desc").text = description
    el(root, "rect", width=width, height=height, rx=14, fill=BG)
    el(root, "path", d=f"M{width-48} 22h20v20", stroke=RED, stroke_width=1.5,
       fill="none", opacity="0.7")
    return root


def label(root, value, number=None):
    el(root, "path", d="M26 28h12", stroke=RED, stroke_width=2)
    text(root, 48, 32, value, 12, MUTED, mono=True, letter_spacing="0.7")
    if number:
        text(root, 316, 32, number, 12, RED, mono=True)


def rule(root, y):
    el(root, "path", d=f"M26 {y}H364", stroke=LINE, stroke_width=1)


def save(root, name):
    ET.indent(root, space="  ")
    (ASSETS / name).write_text(ET.tostring(root, encoding="unicode") + "\n")


def logo(root, key, x, y, size=40):
    path = ASSETS / "logos" / f"{key}.svg"
    if path.exists():
        actual_width = size*1.8 if key == "ros" else size
        x -= (actual_width-size)/2
        # Original marks stay untouched; dark marks need a light inset for contrast.
        if key in {"express", "nextjs", "ros"}:
            el(root, "rect", x=x-4, y=y-4, width=actual_width+8, height=size+8, rx=8, fill=FG)
        svg = copy.deepcopy(ET.parse(path).getroot())
        if not svg.get("viewBox"):
            svg.set("viewBox", f"0 0 {svg.get('width')} {svg.get('height')}")
        svg.set("x", str(x)); svg.set("y", str(y))
        svg.set("width", str(actual_width)); svg.set("height", str(size))
        # Scope internal gradient/clip IDs when multiple brands share a panel.
        ids = {node.get("id"): f"{key}-{x}-{y}-{node.get('id')}" for node in svg.iter() if node.get("id")}
        for node in svg.iter():
            for attr, value in list(node.attrib.items()):
                if attr == "id":
                    node.set(attr, ids[value])
                else:
                    for old, new in ids.items():
                        value = value.replace(f"url(#{old})", f"url(#{new})")
                        if value == f"#{old}":
                            value = f"#{new}"
                    node.set(attr, value)
        root.append(svg)
    elif key == "sql":
        group = el(root, "g", transform=f"translate({x} {y}) scale({size/40})",
                   fill="none", stroke="#60a5fa", stroke_width=2)
        el(group, "ellipse", cx=20, cy=7, rx=15, ry=5)
        el(group, "path", d="M5 7v25c0 7 30 7 30 0V7M5 19c0 7 30 7 30 0")
    else:
        raise ValueError(f"Missing authentic logo: {key}")


def flow(root, items, y):
    width = 100
    for i, item in enumerate(items):
        x = 26 + i * 119
        el(root, "rect", x=x, y=y, width=width, height=29, rx=5, fill="#16161c", stroke=LINE)
        text(root, x+width/2, y+19, item, 12, MUTED, mono=True, text_anchor="middle")
        if i < len(items)-1:
            el(root, "path", d=f"M{x+width+4} {y+14}h11m-4-4 4 4-4 4", fill="none", stroke=RED)


def overview():
    root = panel("AI, vision and robotics", "AI undergraduate at UTS; Computer Vision and Robotics research assistant at IVS; co-founder at Odylytics. Perception and navigation for robots and UAVs, with LiDAR, mapping and geometric reasoning.", 270)
    label(root, "PROFILE / HO CHI MINH CITY")
    text(root, 26, 76, "AI, vision & robotics.", 29, weight=650)
    for y, role in zip([111, 137, 163], ["AI undergraduate · UTS", "Research assistant · IVS", "Co-founder · Odylytics"]):
        el(root, "circle", cx=30, cy=y-6, r=3, fill=RED)
        text(root, 44, y, role, 17)
    rule(root, 182)
    for y, line in zip([208, 230, 252], ["Perception and navigation for robots", "and UAVs, with LiDAR, mapping", "and geometric reasoning."]):
        text(root, 26, y, line, 17, MUTED)
    save(root, "about.svg")

    root = panel("Current focus", "Building reliable backend services for AI-enabled applications and reproducible research experiments with clear evaluation and documentation.", 270)
    label(root, "CURRENT FOCUS")
    text(root, 26, 76, "Research → software.", 29, weight=650)
    for y, line in zip([112, 136, 180, 204], ["Reliable backend services for", "AI-enabled applications.", "Reproducible research experiments,", "with evaluation and documentation."]):
        text(root, 26, y, line, 17, MUTED)
    flow(root, ["Experiment", "Evaluate", "Build"], 224)
    save(root, "focus.svg")


def project(name, title, subtitle, lines, nodes, technologies, description, number):
    root = panel(title, description, 340)
    label(root, "SELECTED WORK", number)
    text(root, 26, 76, title, 30, weight=650)
    text(root, 26, 104, subtitle, 16, MUTED)
    for i, line in enumerate(lines):
        text(root, 26, 142+i*23, line, 17)
    rule(root, 228)
    flow(root, nodes, 243)
    for i, (key, display) in enumerate(technologies):
        x = 76 + i * 179 if len(technologies) == 2 else 30 + i * 119
        logo(root, key, x, 295, 22)
        text(root, x+30, 312, display, 12, MUTED)
    save(root, name)


def projects():
    project("project-aquaguard.svg", "AquaGuard", "Flood alerts & rescue coordination",
            ["Flood maps, GPS-based SOS and", "live rescue tracking connect", "citizens, rescuers and admins.", "Includes family safety updates."],
            ["Flood map", "SOS", "Rescue"], [("react", "React"), ("nodejs", "Node.js"), ("postgresql", "Postgres")],
            "AquaGuard is a team project for flood maps, GPS SOS requests, live rescue tracking and family safety updates. React, Node.js, Express, PostgreSQL and Firebase.", "01")
    project("project-ant.svg", "VirtualDouble / ANT", "Focus companion · Hackathon project",
            ["Optional on-device vision and", "supportive check-ins, with task", "breakdown, a floating focus window", "and a recovery workspace."],
            ["Local vision", "Check-in", "Focus"], [("nextjs", "Next.js"), ("typescript", "TS"), ("mediapipe", "MediaPipe")],
            "VirtualDouble / ANT uses optional browser-side face landmarks, supportive check-ins, task breakdown, a floating focus window and a recovery workspace. Camera frames stay on device. Next.js, TypeScript, MediaPipe and Web Audio.", "02")
    project("project-uav.svg", "UAV Localization", "Research prototype · In progress",
            ["Vision-based localization in forests", "where GNSS is unreliable. Testing", "canopy features and geometric", "matching to estimate position."],
            ["Canopy", "Geometry", "Position"], [("cplusplus", "C++"), ("python", "Python")],
            "In-progress UAV localization research prototype exploring canopy features and geometric matching to estimate position in forests where GNSS is unavailable or unreliable. C++, Python, computer vision and geometry.", "03")

    root = panel("Pothole surface reconstruction", "Research presented at CTMIA 2026: pothole surface reconstruction.", 340)
    label(root, "RESEARCH / CTMIA 2026")
    text(root, 26, 76, "Surface reconstruction", 26, weight=650)
    text(root, 26, 104, "Pothole analysis", 17, MUTED)
    # A wireframe surface illustrates the research topic, rather than a claimed result.
    for r in range(6):
        pts = []
        for c in range(9):
            x = 37+c*34+r*3
            depth = max(0, 1-((c-4)/3)**2-((r-2.5)/2.5)**2) * 24
            y = 142+r*13+depth
            pts.append(f"{x},{y:.1f}")
        el(root, "polyline", points=" ".join(pts), fill="none", stroke=RED, stroke_width=1, opacity="0.7")
    for c in range(9):
        pts = []
        for r in range(6):
            depth = max(0, 1-((c-4)/3)**2-((r-2.5)/2.5)**2)*24
            pts.append(f"{37+c*34+r*3},{142+r*13+depth:.1f}")
        el(root, "polyline", points=" ".join(pts), fill="none", stroke="#626270", stroke_width=1)
    rule(root, 228)
    text(root, 26, 267, "Presented at CTMIA 2026.", 18)
    text(root, 26, 311, "COMPUTER VISION / GEOMETRY", 12, MUTED, mono=True)
    save(root, "research.svg")


def section(name, number, title, suffix, width=800):
    root = panel(title, f"Section {number}: {title}", 64, width)
    text(root, 24, 40, number, 16, RED, mono=True)
    text(root, 68, 41, title, 26, weight=600, mono=True)
    # Keep metadata secondary and out of the title's reading path.
    if width == 800:
        text(root, 737, 39, suffix, 12, MUTED, mono=True, text_anchor="end")
    el(root, "path", d=f"M24 57H{width-24}", stroke=LINE, stroke_width=1)
    el(root, "path", d="M24 57H122", stroke=RED, stroke_width=2)
    save(root, name)


def mobile_frames():
    # Derive the narrow hero from the user's original artwork.
    root = ET.parse(ASSETS / "header.svg").getroot()
    root.set("width", "390"); root.set("height", "180"); root.set("viewBox", "0 0 390 180")
    for node in root.iter():
        cls = node.get("class")
        if node.get("transform") == "translate(800 0) scale(-1 1)":
            node.set("transform", "translate(390 0) scale(-1 1)")
        if cls == "name":
            node.set("x", "195"); node.set("y", "84"); node.set("font-size", "34")
            node.set("letter-spacing", "-1")
        elif cls == "meta":
            node.set("x", "195"); node.set("y", "141"); node.set("font-size", "10")
            node.set("letter-spacing", "0.7")
        elif cls == "underline":
            node.set("x", "72"); node.set("y", "108"); node.set("width", "246")
        if cls == "corner":
            for rect in node:
                rect.set("x", "24"); rect.set("y", "26")
    save(root, "header-mobile.svg")

    root = ET.Element(f"{{{NS}}}svg", {"width": "390", "height": "130", "viewBox": "0 0 390 130", "role": "img"})
    el(root, "title").text = "Made with heart by Tran Tuan Nghia"
    el(root, "rect", width=390, height=130, rx=14, fill=BG)
    for offset, opacity in [(0, ".45"), (20, ".16")]:
        pts = " ".join(f"{x},{65+math.sin((x+offset)/26)*8:.2f}" for x in range(0,391,4))
        el(root, "polyline", points=pts, fill="none", stroke=RED, stroke_width=1, opacity=opacity)
    node = text(root, 195, 54, "made with ", 14, weight=500, text_anchor="middle")
    heart = el(node, "tspan", fill=RED); heart.text = "♥"; heart.tail = " by Tran Tuan Nghia"
    text(root, 195, 85, "github.com/tuannghia2457", 12, MUTED, mono=True, text_anchor="middle")
    text(root, 374, 116, "made with ryme.md", 8, MUTED, text_anchor="end", opacity=".4", mono=True)
    save(root, "footer-mobile.svg")


def stack(name, title, items, subtitle):
    columns = 2 if len(items) == 4 else 3
    rows = (len(items)+columns-1)//columns
    height = 86 + rows*88 + 32
    root = panel(title, subtitle + ": " + ", ".join(display for _, display in items), height)
    label(root, "TECH STACK")
    text(root, 26, 69, title, 24, weight=600)
    for i, (key, display) in enumerate(items):
        col, row = i % columns, i // columns
        cx = 111+col*167 if columns == 2 else 76+col*119
        y = 92+row*88
        logo(root, key, cx-20, y, 40)
        text(root, cx, y+65, display, 15, MUTED, text_anchor="middle")
    rule(root, height-35)
    text(root, 26, height-14, subtitle, 11, MUTED, mono=True)
    save(root, name)


def stacks():
    stack("skills.svg", "Languages", [("python", "Python"), ("cplusplus", "C++"), ("typescript", "TypeScript"), ("javascript", "JavaScript"), ("java", "Java"), ("sql", "SQL")], "SYSTEMS / APPLICATIONS / DATA")
    stack("stack-vision.svg", "Vision & robotics", [("pytorch", "PyTorch"), ("opencv", "OpenCV"), ("mediapipe", "MediaPipe"), ("ros", "ROS 2"), ("gazebo", "Gazebo"), ("nav2", "Nav2")], "ROS 2 TOOLCHAIN / NAV2 / RVIZ")
    stack("stack-web.svg", "Web & backend", [("react", "React"), ("nextjs", "Next.js"), ("nodejs", "Node.js"), ("express", "Express"), ("postgresql", "PostgreSQL"), ("firebase", "Firebase")], "INTERFACES / SERVICES / STORAGE")
    stack("stack-tools.svg", "Development", [("git", "Git"), ("linux", "Linux"), ("docker", "Docker"), ("playwright", "Playwright")], "VERSION CONTROL / RUNTIME / TESTING")


def milestones():
    cards = [("milestones-projects.svg", [("1st Place", "EPICS Season 8 · AquaGuard"), ("First Runner-Up", "Bach Khoa Innovation · AquaGuard")]),
             ("milestones-academic.svg", [("Dean's List", "UTS · Academic achievement"), ("Finalist", "InnoStars & Leave a Nest · AquaGuard")])]
    for name, items in cards:
        desc = "; ".join(award+" — "+event+" (2026)" for award, event in items)
        root = panel("Recognition in 2026", desc, 200)
        label(root, "RECOGNITION / 2026")
        for i, (award, event) in enumerate(items):
            y = 76 + i*83
            text(root, 26, y, award, 27, weight=600)
            text(root, 26, y+25, event, 16, MUTED)
        rule(root, 119)
        save(root, name)


if __name__ == "__main__":
    overview()
    projects()
    stacks()
    milestones()
    for name, number, title, suffix in [
        ("section-work.svg", "01", "Selected work", "BUILD / RESEARCH"),
        ("section-stack.svg", "02", "Tech stack", "LANGUAGES / TOOLS"),
        ("section-recognition.svg", "03", "Recognition", "2026"),
        ("gh-stats.svg", "04", "Coding activity", "GITHUB / LEETCODE"),
    ]:
        section(name, number, title, suffix)
        section(name.replace(".svg", "-mobile.svg"), number, title, suffix, 390)
    mobile_frames()
    print("Built self-contained profile panels.")
