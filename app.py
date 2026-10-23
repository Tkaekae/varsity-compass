import streamlit as st

COURSES = [
    {"name": "Placeholder Course A", "uni": "Uni 1", "min_aps": 30, "deadline": "TBC"},
    {"name": "Placeholder Course B", "uni": "Uni 2", "min_aps": 26, "deadline": "TBC"},
]

st.title("VarsityCompass")
aps = st.number_input("Your APS score", 0, 50, 25)

for c in COURSES:
    gap = c["min_aps"] - aps
    if gap <= 0:
        st.success(f"{c['name']} ({c['uni']}): you qualify. Deadline: {c['deadline']}")
    else:
        st.warning(f"{c['name']} ({c['uni']}): you're {gap} points short")
   