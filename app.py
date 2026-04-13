import streamlit as st
from datetime import datetime
from logic import get_best_options, STATIONS_ORDER

st.set_page_config(page_title="SmartRail AI", layout="wide")

st.markdown("""
    <style>
    .card {
        background-color: #111827;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    }
    .title {
        font-size: 22px;
        font-weight: bold;
    }
    .small {
        color: #9ca3af;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚆 SmartRail AI")
st.markdown("### Find the Best Train & Compartment")

col1, col2, col3 = st.columns(3)

with col1:
    source = st.selectbox("Source Station", STATIONS_ORDER)

with col2:
    destination = st.selectbox("Destination Station", STATIONS_ORDER)

with col3:
    if "use_current_time" not in st.session_state:
        st.session_state.use_current_time = False

    if st.button("⏰ Use Current Time"):
        st.session_state.use_current_time = True

    if st.button("🕒 Manual Time"):
        st.session_state.use_current_time = False

    if st.session_state.use_current_time:
        time = datetime.now().hour
        st.success(f"{time}:00")
    else:
        time = st.slider("Hour", 0, 23, 9)

st.markdown("---")

if st.button("🚀 Find Best Options"):

    if source == destination:
        st.error("Source and destination cannot be same")
    else:
        results = get_best_options(source, destination, time)

        if results is None:
            st.error("No trains found")
        else:
            st.markdown("## 🚆 Top 3 Recommendations")

            cols = st.columns(len(results))

            for i, (col, result) in enumerate(zip(cols, results), start=1):

                with col:
                    crowd = result["crowd"]

                    if crowd < 0.5:
                        level = "Low"
                        color = "#10b981"
                    elif crowd < 0.7:
                        level = "Medium"
                        color = "#f59e0b"
                    else:
                        level = "High"
                        color = "#ef4444"

                    st.markdown(f"""
                        <div class="card">
                            <div class="title">🚆 Option {i}</div>
                            <p class="small">Train ID</p>
                            <b>{result['train_id']} ({result['train_type']})</b>
                            <p class="small">Best Compartment</p>
                            <b>{result['best_compartment']}</b>
                            <p class="small">Crowd Level</p>
                            <b style="color:{color}">{level} ({round(crowd,2)})</b>
                            <p class="small">Score</p>
                            <b>{result['score']}</b>
                        </div>
                    """, unsafe_allow_html=True)

                    with st.expander("View Compartments"):
                        for comp in result["full_ranking"]:
                            c = comp["crowd_base"]

                            if c < 0.5:
                                lvl = "Low"
                                icon = "🟢"
                            elif c < 0.7:
                                lvl = "Medium"
                                icon = "🟡"
                            else:
                                lvl = "High"
                                icon = "🔴"

                            st.write(f"{icon} Coach {comp['compartment']} → {lvl} ({round(c,2)})")