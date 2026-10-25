from datetime import date

import streamlit as st

st.set_page_config(page_title="VarsityCompass", page_icon="🧭", layout="wide")

# ----------------------------------------------------------------------
# COURSE DATA
# Every number below was checked against the official 2027 documents:
#   - UP  Undergraduate Prospectus 2027
#   - UJ  Undergraduate Prospectus 2027
#   - TUT 2027 First Year Course Information
# "english", "maths" and "phys_sci" are the minimum NSC achievement LEVELS (1-7).
# ----------------------------------------------------------------------
MATHS = "Mathematics"
TECH = "Technical Mathematics"
LIT = "Mathematical Literacy"

UP_CLOSE = date(2026, 6, 30)
UJ_CLOSE = date(2026, 10, 31)   # 12:00 noon
TUT_CLOSE = date(2026, 9, 30)


def course(name, uni, kind, aps, english, maths, closing, source,
           phys_sci=0, aps_lit=None, note=""):
    """Build one programme. 'maths' is a dict like {"Mathematics": 6},
    or None if the programme has no maths requirement."""
    return {
        "name": name, "uni": uni, "kind": kind, "aps": aps, "aps_lit": aps_lit,
        "english": english, "maths": maths, "phys_sci": phys_sci,
        "closing": closing, "source": source, "note": note,
    }


UP_SRC = "UP Undergraduate Prospectus 2027"
UJ_SRC = "UJ Undergraduate Prospectus 2027"
TUT_SRC = "TUT 2027 First Year Course Information (ICT, p.11)"

COURSES = [
    # ---------------- University of Pretoria ----------------
    course("BSc Computer Science", "UP", "Degree", 30, 5, {MATHS: 6}, UP_CLOSE, UP_SRC),
    course("BSc Information Technology (Information and Knowledge Systems)", "UP", "Degree",
           30, 4, {MATHS: 6}, UP_CLOSE, UP_SRC),
    course("Bachelor of Information Technology (Information Systems)", "UP", "Degree",
           30, 5, {MATHS: 5}, UP_CLOSE, UP_SRC),
    course("BCom Information Systems", "UP", "Degree", 30, 5, {MATHS: 5}, UP_CLOSE, UP_SRC),
    course("Bachelor of Information Science (Multimedia)", "UP", "Degree",
           30, 4, {MATHS: 5}, UP_CLOSE, UP_SRC),
    course("Bachelor of Information Science", "UP", "Degree", 28, 4, None, UP_CLOSE, UP_SRC,
           note="If you choose Information Systems as a first-year subject, Mathematics level 5 is required."),
    course("BCom Accounting Sciences", "UP", "Degree", 34, 5, {MATHS: 6}, UP_CLOSE, UP_SRC),
    course("BEng Mechanical Engineering", "UP", "Degree", 35, 5, {MATHS: 6}, UP_CLOSE, UP_SRC,
           phys_sci=6),
    course("BEng Electrical Engineering", "UP", "Degree", 35, 5, {MATHS: 6}, UP_CLOSE, UP_SRC,
           phys_sci=6),

    # ---------------- University of Johannesburg ----------------
    course("BSc Information Technology", "UJ", "Degree", 30, 5, {MATHS: 6},
           UJ_CLOSE, UJ_SRC + ", p.86",
           note="Technical Mathematics and Technical Science are not accepted for Science degrees."),
    course("BSc Computer Science and Informatics", "UJ", "Degree", 30, 5, {MATHS: 6},
           UJ_CLOSE, UJ_SRC + ", p.86",
           note="Technical Mathematics and Technical Science are not accepted for Science degrees."),
    course("BSc Computer Science and Informatics (Artificial Intelligence)", "UJ", "Degree",
           34, 5, {MATHS: 7}, UJ_CLOSE, UJ_SRC + ", p.86",
           note="Technical Mathematics and Technical Science are not accepted for Science degrees."),
    course("BCom Information Systems", "UJ", "Degree", 26, 4, {MATHS: 4, TECH: 4},
           UJ_CLOSE, UJ_SRC + ", p.42"),

    # ---------------- Tshwane University of Technology ----------------
    course("Diploma in Computer Science", "TUT", "Diploma", 26, 4,
           {MATHS: 5, TECH: 5, LIT: 7}, TUT_CLOSE, TUT_SRC, aps_lit=28),
    course("Diploma in Computer Science (Extended, 4 years)", "TUT", "Diploma", 23, 3,
           {MATHS: 4, TECH: 4, LIT: 6}, TUT_CLOSE, TUT_SRC, aps_lit=25),
    course("Diploma in Computer Systems Engineering", "TUT", "Diploma", 26, 4,
           {MATHS: 5, TECH: 5}, TUT_CLOSE, TUT_SRC, phys_sci=4,
           note="Needs Physical Sciences or Technical Sciences."),
    course("Diploma in Informatics", "TUT", "Diploma", 26, 4,
           {MATHS: 5, TECH: 5, LIT: 7}, TUT_CLOSE, TUT_SRC, aps_lit=28),
    course("Diploma in Information Technology", "TUT", "Diploma", 26, 4,
           {MATHS: 5, TECH: 5, LIT: 7}, TUT_CLOSE, TUT_SRC, phys_sci=3, aps_lit=28,
           note="Needs Physical Sciences or Technical Sciences."),
    course("Diploma in Information Technology (Extended, 4 years)", "TUT", "Diploma", 23, 3,
           {MATHS: 4, TECH: 4, LIT: 6}, TUT_CLOSE, TUT_SRC, phys_sci=3, aps_lit=25,
           note="Needs Physical Sciences or Technical Sciences."),
    course("Diploma in Multimedia Computing", "TUT", "Diploma", 26, 4,
           {MATHS: 5, TECH: 5, LIT: 7}, TUT_CLOSE, TUT_SRC, aps_lit=28),
]

# ----------------------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------------------


def mark_to_level(mark):
    """Turn a percentage into an NSC level (same scale at UP, UJ and TUT).
    0 means 'not taken'."""
    if mark <= 0:
        return 0
    if mark >= 80:
        return 7
    if mark >= 70:
        return 6
    if mark >= 60:
        return 5
    if mark >= 50:
        return 4
    if mark >= 40:
        return 3
    if mark >= 30:
        return 2
    return 1


def calc_aps(levels, uni):
    """APS = sum of your best 6 subjects. Life Orientation is never counted.
    TUT also ignores any subject where you only got level 1."""
    counted = [lv for lv in levels if lv > 0]
    if uni == "TUT":
        counted = [lv for lv in counted if lv > 1]
    counted.sort(reverse=True)
    return sum(counted[:6])


def deadline_text(closing):
    days = (closing - date.today()).days
    pretty = closing.strftime("%d %B %Y")
    if days < 0:
        return False, f"Applications closed on {pretty}. Check the university's website for late applications or next year's intake."
    if days == 0:
        return True, f"Applications close TODAY ({pretty})."
    return True, f"Applications close on {pretty}: {days} day(s) left."


def check_course(c, me):
    """Compare the student (me) with one programme.
    Returns (status, messages, levels_needed)."""
    messages = []
    subject_gap = 0
    hard_block = False  # something marks alone can't fix (e.g. wrong maths subject)

    # English
    if me["english"] < c["english"]:
        subject_gap += c["english"] - me["english"]
        messages.append(f"English: you're at level {me['english']}, need level {c['english']}")

    # Maths
    if c["maths"]:
        accepted = c["maths"]
        if me["maths_type"] not in accepted:
            hard_block = True
            messages.append(f"{me['maths_type']} is not accepted here (needs {' or '.join(accepted)})")
        elif me["maths_level"] < accepted[me["maths_type"]]:
            need = accepted[me["maths_type"]]
            subject_gap += need - me["maths_level"]
            messages.append(f"{me['maths_type']}: you're at level {me['maths_level']}, need level {need}")

    # Physical Sciences
    if c["phys_sci"]:
        if me["phys_level"] == 0:
            hard_block = True
            messages.append("This programme needs Physical Sciences")
        elif me["phys_level"] < c["phys_sci"]:
            subject_gap += c["phys_sci"] - me["phys_level"]
            messages.append(f"Physical Sciences: you're at level {me['phys_level']}, need level {c['phys_sci']}")

    # APS (some TUT programmes ask for more points if you take Maths Literacy)
    needed_aps = c["aps"]
    if me["maths_type"] == LIT and c["aps_lit"]:
        needed_aps = c["aps_lit"]
    my_aps = calc_aps(me["levels"], c["uni"])
    aps_gap = max(0, needed_aps - my_aps)
    if aps_gap > 0:
        messages.append(f"APS: you have {my_aps}, need {needed_aps} ({aps_gap} short)")

    # One level up in a subject adds 1 APS point, so the effort overlaps.
    levels_needed = max(aps_gap, subject_gap)

    if not messages:
        return "qualify", [], 0
    if not hard_block and levels_needed <= 3:
        return "close", messages, levels_needed
    return "not_yet", messages, levels_needed

def best_moves(me, courses):
    """Try raising each subject by ONE level. Count the programmes that would newly open up."""
    names = ["English", me["maths_type"], "Physical Sciences",
             "Other subject 1", "Other subject 2", "Other subject 3", "Other subject 4"]
    moves = []
    for i, name in enumerate(names):
        level = me["levels"][i]
        if level == 0 or level >= 7:   # not taken, or already at the top
            continue
        better = dict(me)
        better["levels"] = list(me["levels"])
        better["levels"][i] = level + 1
        if i == 0:
            better["english"] = level + 1
        elif i == 1:
            better["maths_level"] = level + 1
        elif i == 2:
            better["phys_level"] = level + 1
        unlocked = [c for c in courses
                    if check_course(c, me)[0] != "qualify" and check_course(c, better)[0] == "qualify"]
        if unlocked:
            moves.append((len(unlocked), name, level, unlocked))
    moves.sort(key=lambda m: m[0], reverse=True)
    return moves


# ----------------------------------------------------------------------
# PAGE
# ----------------------------------------------------------------------
st.title("🧭 VarsityCompass")
st.write("Enter your matric marks and see which programmes you qualify for, how far you are from the "
         "ones you don't, and whether applications are still open.")

# ----- Sidebar: the student's marks -----
st.sidebar.header("Your marks (%)")
english_mark = st.sidebar.number_input("English (Home Language or First Additional)", 0, 100, 65)
maths_type = st.sidebar.radio("Which maths subject do you take?", [MATHS, TECH, LIT])
maths_mark = st.sidebar.number_input(f"{maths_type} mark", 0, 100, 62)
phys_mark = st.sidebar.number_input("Physical Sciences (put 0 if you don't take it)", 0, 100, 55)
st.sidebar.caption("Other subjects (not Life Orientation). Put 0 if you don't have one.")
other1 = st.sidebar.number_input("Other subject 1", 0, 100, 70)
other2 = st.sidebar.number_input("Other subject 2", 0, 100, 65)
other3 = st.sidebar.number_input("Other subject 3", 0, 100, 60)
other4 = st.sidebar.number_input("Other subject 4", 0, 100, 58)

me = {
    "english": mark_to_level(english_mark),
    "maths_type": maths_type,
    "maths_level": mark_to_level(maths_mark),
    "phys_level": mark_to_level(phys_mark),
}
me["levels"] = [
    me["english"], me["maths_level"], me["phys_level"],
    mark_to_level(other1), mark_to_level(other2), mark_to_level(other3), mark_to_level(other4),
]

# ----- Filters -----
col1, col2 = st.columns([2, 1])
with col1:
    chosen_unis = st.multiselect("Universities", ["UP", "UJ", "TUT"], default=["UP", "UJ", "TUT"])
with col2:
    only_open = st.checkbox("Only show programmes still open for applications")

st.info(f"Your APS (best 6 subjects, no Life Orientation): **{calc_aps(me['levels'], 'UP')}**  |  "
        f"English level {me['english']}  |  {maths_type} level {me['maths_level']}")

# ----- Work out every result -----
results = {"qualify": [], "close": [], "not_yet": []}
for c in COURSES:
    if c["uni"] not in chosen_unis:
        continue
    is_open, deadline = deadline_text(c["closing"])
    if only_open and not is_open:
        continue
    status, messages, levels_needed = check_course(c, me)
    results[status].append((c, messages, levels_needed, is_open, deadline))
results["close"].sort(key=lambda r: r[2])  # closest first


def show(items, icon):
    for c, messages, levels_needed, is_open, deadline in items:
        with st.container(border=True):
            st.markdown(f"**{icon} {c['name']}**  \n{c['uni']} · {c['kind']}")
            need = f"APS {c['aps']}" + (f" ({c['aps_lit']} with Maths Literacy)" if c["aps_lit"] else "")
            need += f" · English level {c['english']}"
            if c["maths"]:
                need += " · " + " / ".join(f"{k} {v}" for k, v in c["maths"].items())
            if c["phys_sci"]:
                need += f" · Physical Sciences level {c['phys_sci']}"
            st.caption("Needs: " + need)
            for m in messages:
                st.write("• " + m)
            if messages and levels_needed > 0 and icon == "🟡":
                st.write(f"💡 You're about **{levels_needed} level(s)** away. One level is roughly +10% in one subject.")
            if is_open:
                st.write("📅 " + deadline)
            else:
                st.write("⛔ " + deadline)
            if c["note"]:
                st.caption("Note: " + c["note"])
            st.caption("Source: " + c["source"])

moves = best_moves(me, [c for c in COURSES if c["uni"] in chosen_unis])
if moves:
    count, name, level, unlocked = moves[0]
    with st.container(border=True):
        st.markdown("### 🚀 Your best move")
        st.write(f"Raise **{name}** from level {level} to level {level + 1} and you unlock "
                 f"**{count}** more programme(s):")
        for c in unlocked:
            tag = "" if deadline_text(c["closing"])[0] else " (2027 applications already closed)"
            st.write(f"• {c['name']} ({c['uni']}){tag}")

st.subheader(f"✅ You qualify ({len(results['qualify'])})")
show(results["qualify"], "✅")
st.subheader(f"🟡 Almost there ({len(results['close'])})")
show(results["close"], "🟡")
st.subheader(f"❌ Not yet ({len(results['not_yet'])})")
show(results["not_yet"], "❌")

# ----- Funding -----
st.divider()
st.subheader("💰 Funding")
nsfas_days = (date(2026, 11, 28) - date.today()).days
if nsfas_days >= 0:
    nsfas_line = f"NSFAS applications for 2027 registration close on 28 November 2026 ({nsfas_days} day(s) left)."
else:
    nsfas_line = "NSFAS applications for 2027 registration closed on 28 November 2026."
st.write(nsfas_line + " Apply at nsfas.org.za. Grants depend on family income "
         "(source: UJ Undergraduate Prospectus 2027).")

st.caption("Data comes from the official 2027 prospectuses. Meeting the minimum requirements does not "
           "guarantee admission. Always confirm on the university's website before you apply.")
