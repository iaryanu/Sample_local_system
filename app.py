import streamlit as st
from datetime import datetime
from logic import get_best_options, STATIONS_ORDER

st.set_page_config(page_title="SmartRail AI", layout="centered")

st.title("🚆 SmartRail AI")
st.subheader("Find the Best Train & Compartment")

source = st.selectbox("Select Source Station", STATIONS_ORDER)
destination = st.selectbox("Select Destination Station", STATIONS_ORDER)

if "use_current_time" not in st.session_state:
    st.session_state.use_current_time = False

st.subheader("Select Time")

col1, col2 = st.columns(2)

with col1:
    if st.button("Use Current Time ⏰"):
        st.session_state.use_current_time = True

with col2:
    if st.button("Use Manual Time"):
        st.session_state.use_current_time = False


if st.session_state.use_current_time:
    time = datetime.now().hour
    st.success(f"Using Current Time: {time}:00")
else:
    time = st.slider("Select Time (Hour)", 0, 23, 9)

if st.button("Find Best Options"):

    if source == destination:
        st.error("Source and destination cannot be same")
    else:
        results = get_best_options(source, destination, time)

        if results is None:
            st.error("No trains found")
        else:
            st.success("Top 3 Train Recommendations")

            for i, result in enumerate(results, start=1):

                st.markdown(f"### 🚆 Option {i}")
                st.write(f"Train: {result['train_id']} ({result['train_type']})")
                st.write(f"Best Compartment: {result['best_compartment']}")

            
                crowd = result["crowd"]
                if crowd < 0.5:
                    level = "Low"
                    color = "🟢"
                elif crowd < 0.7:
                    level = "Medium"
                    color = "🟡"
                else:
                    level = "High"
                    color = "🔴"

                st.write(f"Crowd: {color} {level} ({round(crowd, 2)})")
                st.write(f"Score: {result['score']}")

                st.write("Compartments (Least → Most Crowded):")

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

                    st.write(f"Coach {comp['compartment']} → {icon} {lvl} ({round(c, 2)})")

                st.divider()