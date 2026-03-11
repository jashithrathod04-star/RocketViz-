import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="RocketViz AI",layout="wide")





# =========================================================
# DATA SOURCE (DEFAULT CSV + USER UPLOAD)
# =========================================================

st.sidebar.title("📂 Data Source")

uploaded_file = st.sidebar.file_uploader(
    "Upload Mission Dataset (CSV)",
    type=["csv"]
)

# Default dataset path
default_data = pd.read_csv("space_missions_dataset.csv")

if uploaded_file is not None:
    df_data = pd.read_csv(uploaded_file)
    st.sidebar.success("Using Uploaded Dataset")
else:
    df_data = default_data
    st.sidebar.info("Using Default Space Missions Dataset")

df_data.columns = df_data.columns.str.strip()



# Clean column names
df_data.columns = (
    df_data.columns
    .str.strip()        # remove spaces
    .str.lower()        # make lowercase
    .str.replace(" ", "_")
    .str.replace("(", "")
    .str.replace(")", "")
)






missions_df = df_data.rename(columns={
    "distance_from_earth_light-years": "distance",
    "mission_duration_years": "duration",
    "mission_cost_billion_usd": "cost",
    "payload_weight_tons": "payload",
    "fuel_consumption_tons": "fuel",
    "crew_size": "crew",
    "launch_vehicle": "vehicle",
    "scientific_yield_points": "science",
    "mission_success_%": "success"
})



# Convert important columns to numeric
numeric_cols = ["distance","duration","payload","fuel","cost"]

for col in numeric_cols:
    if col in missions_df.columns:
        missions_df[col] = pd.to_numeric(missions_df[col], errors="coerce")
# Remove rows where distance or duration is missing
missions_df = missions_df.dropna(subset=["distance","duration"])

# Ensure required columns exist
required_cols = ["distance","duration","cost","payload","fuel","vehicle","crew","science"]

for col in required_cols:
    if col not in missions_df.columns:
        missions_df[col] = np.nan
















# =========================================================
# DATA CLEANING
# =========================================================

df_data["launch_date"] = pd.to_datetime(df_data["launch_date"])

df_data = df_data.drop_duplicates()

df_data = df_data.fillna(method="ffill")





# Ensure numeric columns are actually numbers
missions_df["distance"] = pd.to_numeric(missions_df["distance"], errors="coerce")
missions_df["duration"] = pd.to_numeric(missions_df["duration"], errors="coerce")
missions_df["payload"] = pd.to_numeric(missions_df["payload"], errors="coerce")
missions_df["fuel"] = pd.to_numeric(missions_df["fuel"], errors="coerce")
missions_df["cost"] = pd.to_numeric(missions_df["cost"], errors="coerce")
# =========================================================
# GLOBAL CSS (GLASSMORPHISM + GLOW)
# =========================================================

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#020617,#020024,#090979,#00d4ff);
color:white;
}

/* GLASS CARDS */

.glass{
backdrop-filter: blur(20px);
background: rgba(255,255,255,0.05);
padding:25px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.1);
box-shadow:0 0 30px rgba(0,255,255,0.4);
transition:0.4s;
}

.glass:hover{
transform:scale(1.05);
box-shadow:0 0 60px rgba(0,255,255,0.9);
}

/* GLOW TEXT */

.glow{
font-size:3rem;
font-weight:700;
background: linear-gradient(90deg,#00e5ff,#00ff9c,#00e5ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
animation:shine 4s linear infinite;
}

@keyframes shine{
0%{background-position:0%}
100%{background-position:200%}
}

/* ===== PARALLAX STARS ===== */

.stApp:before{
content:"";
position:fixed;
width:100%;
height:100%;
background-image:radial-gradient(white 1px, transparent 1px);
background-size:3px 3px;
opacity:0.2;
animation:stars 80s linear infinite;
z-index:-1;
}

@keyframes stars{
from{transform:translateY(0)}
to{transform:translateY(-2000px)}
}

/* ===== GLASS PANELS ===== */

.glass{
backdrop-filter: blur(15px);
background: rgba(255,255,255,0.05);
padding:25px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.2);
box-shadow:0 0 25px rgba(0,255,255,0.5);
transition:0.3s;
}

.glass:hover{
transform:scale(1.03);
box-shadow:0 0 60px cyan;
}

/* ===== GLOW TITLE ===== */

.glow{
font-size:3rem;
font-weight:800;
background:linear-gradient(90deg,#00e5ff,#00ff9c,#ff00ff,#00e5ff);
background-size:400%;
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
animation:glowmove 8s linear infinite;
}

@keyframes glowmove{
0%{background-position:0%}
100%{background-position:400%}
}













/* BUTTON */

.stButton>button{
background:linear-gradient(90deg,#00e5ff,#00ff9c);
border:none;
border-radius:30px;
padding:12px 30px;
font-size:16px;
box-shadow:0 0 20px #00e5ff;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.1);
box-shadow:0 0 40px #00ff9c;
}

/* SIDEBAR */

[data-testid="stSidebar"]{
background:rgba(255,255,255,0.04);
backdrop-filter: blur(20px);
border-right:1px solid rgba(255,255,255,0.1);
box-shadow:0 0 20px rgba(0,255,255,0.4);
}



.stTabs [data-baseweb="tab"]{
font-size:18px;
color:white;
padding:12px;
border-radius:15px;
transition:0.3s;
}

.stTabs [aria-selected="true"]{
background:linear-gradient(90deg,#00e5ff,#00ff9c);
color:black;
box-shadow:0 0 20px #00e5ff;
}

</style>
""",unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page="splash"


# =========================================================
# =========================================================
# SPLASH SCREEN
# =========================================================

if st.session_state.page == "splash":

    splash_html = """
    <html>
    <style>

    body{
    margin:0;
    background:black;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    color:white;
    font-family:sans-serif;
    overflow:hidden;
    }

    .title{
    font-size:3.5rem;
    font-weight:700;
    background:linear-gradient(90deg,#00e5ff,#00ff9c);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation:glow 2s infinite alternate;
    }

    @keyframes glow{
    from{ text-shadow:0 0 10px #00e5ff}
    to{ text-shadow:0 0 40px #00ff9c}
    }

    .rocket{
    font-size:5rem;
    animation:fly 2s infinite;
    }

    @keyframes fly{
    0%{transform:translateY(0)}
    50%{transform:translateY(-30px)}
    100%{transform:translateY(0)}
    }

    </style>

    <body>

    <div style="text-align:center">

    <div class="rocket">🚀</div>

    <div class="title">RocketViz AI</div>

    <p>Rocket Launch Simulation & Mission Analytics</p>

    </div>

    </body>
    </html>
    """

    components.html(splash_html, height=800)

    if "splash_shown" not in st.session_state:
        time.sleep(3)
        st.session_state.splash_shown = True
        st.session_state.page = "landing"
        st.rerun()


# =========================================================
# LANDING PAGE
# =========================================================

elif st.session_state.page=="landing":

    st.markdown("<div class='glow'>RocketViz AI</div>",unsafe_allow_html=True)

    st.write("")

    st.markdown("""
<div class="glass">

### 🚀 Explore the Universe of Rocket Science

Simulate rocket launches using real physics principles and explore space missions through interactive analytics.

Features:

• Rocket launch simulation  
• Mission dataset analytics  
• Interactive charts  
• Payload vs fuel insights  
• Mission success exploration  

</div>
""",unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 Launch App"):
        st.session_state.page="signup"



# =========================================================
# SIGNUP PAGE
# =========================================================

elif st.session_state.page=="signup":

    st.markdown("""
    <style>
    
    .signup-box{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    border-radius:20px;
    padding:40px;
    border:1px solid rgba(255,255,255,0.2);
    box-shadow:0 0 30px rgba(0,255,255,0.6);
    transition:0.4s;
    margin-top:20px;
    }
    
    .signup-box:hover{
    transform: translateY(-10px) scale(1.02);
    box-shadow:0 0 70px rgba(0,255,255,1);
    }
    
    .signup-title{
    font-size:36px;
    font-weight:800;
    text-align:center;
    
    background: linear-gradient(90deg,#00f7ff,#ff00ff,#00ff9d,#00f7ff);
    background-size:400%;
    
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    
    animation: glowText 6s linear infinite;
    
    margin-bottom:25px;
    }
    
    @keyframes glowText{
    0%{background-position:0%}
    50%{background-position:200%}
    100%{background-position:0%}
    }
    
    </style>
    """, unsafe_allow_html=True)
   
    
    st.markdown('<div class="signup-box">', unsafe_allow_html=True)

    st.markdown('<div class="signup-title">🚀 Create Mission Profile</div>', unsafe_allow_html=True)

    st.image("https://api.dicebear.com/7.x/bottts/svg?seed=rocket",width=120)
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("👨‍🚀 Commander Name")
        email = st.text_input("📧 Email Address")
        password = st.text_input("🔑 Password", type="password")
    
    with col2:
        confirm_password = st.text_input("🔒 Confirm Password", type="password")
        mission_name = st.text_input("🛰 Mission Name")
        launch_vehicle = st.selectbox(
            "🚀 Launch Vehicle",
            ["Falcon 9", "Atlas V", "Soyuz", "SLS", "Starship"]
        )
    
    experience = st.slider("🧑‍🚀 Crew Experience Level",1,10)
    
    create = st.button("🚀 Create Mission")
    
    if create:
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            st.success("Mission Profile Created Successfully")
            st.session_state.page="dashboard"
    
    st.markdown('</div>', unsafe_allow_html=True)




   




# =========================================================
# DASHBOARD
elif st.session_state.page=="dashboard":

    st.markdown("""
    <style>
    
    .dashboard-box{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border-radius:20px;
    padding:40px;
    text-align:center;
    margin-bottom:30px;
    
    border:1px solid rgba(255,255,255,0.2);
    
    box-shadow:0 0 30px rgba(0,255,255,0.5);
    
    transition:0.4s;
    }
    
    .dashboard-box:hover{
    transform:translateY(-10px) scale(1.02);
    box-shadow:0 0 80px rgba(0,255,255,1);
    }
    
    .app-title{
    font-size:50px;
    font-weight:800;
    
    background: linear-gradient(90deg,#00f7ff,#ff00ff,#00ff9d,#00f7ff);
    background-size:400%;
    
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    
    animation: glowText 6s linear infinite;
    }
    
    .subtitle{
    font-size:22px;
    margin-top:10px;
    color:white;
    letter-spacing:2px;
    }
    
    @keyframes glowText{
    0%{background-position:0%}
    50%{background-position:200%}
    100%{background-position:0%}
    }
    
    </style>
    
    <div class="dashboard-box">
    
    <div class="app-title">
    🚀 Space Mission Control
    </div>
    
    <div class="subtitle">
    Mission Control Dashboard
    </div>
    
    </div>
    
    """, unsafe_allow_html=True)

    # ===============================
    # TOP DASHBOARD CARDS
    # ===============================

    col1,col2,col3,col4,col5 = st.columns(5)

    total_missions = len(missions_df)
    avg_payload = int(missions_df["payload"].mean())
    avg_fuel = int(missions_df["fuel"].mean())
    success_rate = round(missions_df["success"].mean(),2)
    avg_cost = round(missions_df["cost"].mean(),2)
    
    with col1:
        st.markdown(f"""
        <div class="glass">
        <h3>🚀 Missions</h3>
        <h2>{total_missions}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="glass">
        <h3>🛰 Payload Avg</h3>
        <h2>{avg_payload} tons</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="glass">
        <h3>⛽ Fuel Avg</h3>
        <h2>{avg_fuel} tons</h2>
        </div>
        """, unsafe_allow_html=True)



    with col4:
        st.markdown(f"""
        <div class="glass">
        <h3>🎯 Success Rate</h3>
        <h2>{success_rate}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="glass">
        <h3>💰 Avg Cost</h3>
        <h2>{avg_cost} B USD</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ===============================


    









    
    # FEATURE TABS
    # ===============================

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Home",
        "📊 Mission Data Explorer",
        "🚀 Rocket Physics Simulation",
        "📈 Mission Analytics",
        "🔍 Comparative Insights",
        "ℹ️ About Project"
        
    ])

    # ==========================================
    # TAB 1 : ROCKET SIMULATION
    # ==========================================

   

    # ==========================================
    # TAB 2 : ANALYTICS
    # ==========================================

    



    with tab1: 

        st.markdown("<div class='glow'>RocketLab AI Dashboard</div>",unsafe_allow_html=True)

        st.write("""
        Interactive rocket launch simulator and mission analytics platform.
        
        This application explores rocket physics and real mission data
        to understand how thrust, fuel, payload, and cost influence
        space missions.
        """)
        
        st.image("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa",use_column_width=True)
        
        st.info("Use the tabs above to explore mission data, simulate rocket launches, and discover insights.")
        st.markdown("### 🚀 Rocket Physics Concepts")

        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="glass">
            <h3>⚖ Newton's 2nd Law</h3>
            <p>Force = Mass × Acceleration.  
            Rocket acceleration depends on thrust minus gravity and drag divided by total mass.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="glass">
            <h3>🔥 Thrust</h3>
            <p>Thrust is the force produced by rocket engines pushing gases downward,
            propelling the rocket upward against gravity.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="glass">
            <h3>🌬 Drag</h3>
            <p>Drag is air resistance acting opposite to motion.
            Higher drag slows rockets and reduces acceleration.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="glass">
            <h3>🛰 Payload</h3>
            <p>Payload is the cargo carried by the rocket such as satellites,
            instruments, or astronauts.</p>
            </div>
            """, unsafe_allow_html=True)


    


    with tab2:

        st.markdown("<div class='glow'>Mission Data Explorer</div>", unsafe_allow_html=True)
    
        vehicle = st.selectbox(
            "Launch Vehicle",
            missions_df["vehicle"].unique()
        )
    
        cost_range = st.slider(
            "Mission Cost Range",
            float(missions_df["cost"].min()),
            float(missions_df["cost"].max()),
            (float(missions_df["cost"].min()), float(missions_df["cost"].max()))
        )
    
        filtered = missions_df[
            (missions_df["vehicle"] == vehicle) &
            (missions_df["cost"] >= cost_range[0]) &
            (missions_df["cost"] <= cost_range[1])
        ]
    
        st.dataframe(filtered)



    with tab3:


        

        st.markdown("<div class='glow'>Rocket Physics Simulation</div>",unsafe_allow_html=True)

        payload=st.slider("Payload Weight",100,10000,2000,key="payload_slider")

        fuel=st.slider("Fuel Amount",500,20000,5000,key="fuel_slider")
        
        thrust=st.slider("Thrust",10000,200000,60000,key="thrust_slider")
        
        drag_coeff=st.slider("Drag Coefficient",0.01,0.2,0.05,key="drag_slider")
        
        g=9.81
        mass=payload+fuel+5000
        
        velocity=0
        altitude=0
        fuel_left=fuel
        
        data=[]
        
        for t in range(200):
        
            drag=drag_coeff*(velocity**2)
        
            accel=(thrust-(mass*g)-drag)/mass
        
            velocity+=accel
            altitude+=velocity
        
            fuel_left-=5
            mass-=5
        
            data.append([t,velocity,altitude,fuel_left])
        
        df_sim=pd.DataFrame(data,columns=["Time","Velocity","Altitude","Fuel"])
        
        fig1=px.line(df_sim,x="Time",y="Altitude",title="Altitude vs Time")
        st.plotly_chart(fig1,use_container_width=True)
        
        fig2=px.line(df_sim,x="Time",y="Velocity",title="Velocity vs Time")
        st.plotly_chart(fig2,use_container_width=True)
        
        fig3=px.line(df_sim,x="Time",y="Fuel",title="Fuel Remaining")
        st.plotly_chart(fig3,use_container_width=True)






    with tab4:

        st.markdown("<div class='glow'>Mission Analytics</div>", unsafe_allow_html=True)
    
        # ===============================
        # GRAPH SELECT DROPDOWN
        # ===============================
    
        graph_option = st.selectbox(
            "📊 Select Graph",
            [
                "Payload vs Fuel",
                "Mission Cost by Launch Vehicle",
                "Mission Duration vs Distance",
                "Crew Size Distribution",
                "Correlation Heatmap",
                "Mission Success vs Payload",
                "Mission Cost vs Mission Success"
            ]
        )
    
        # ===============================
        # GRAPH 1
        # ===============================
    
        if graph_option == "Payload vs Fuel":
    
            fig = px.scatter(
                missions_df,
                x="payload",
                y="fuel",
                color="vehicle",
                title="Payload vs Fuel Consumption"
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        # ===============================
        # GRAPH 2
        # ===============================
    
        elif graph_option == "Mission Cost by Launch Vehicle":
    
            fig = px.bar(
                missions_df,
                x="vehicle",
                y="cost",
                title="Mission Cost by Launch Vehicle"
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        # ===============================
        # GRAPH 3
        # ===============================
    
        elif graph_option == "Mission Duration vs Distance":
    
            fig = px.scatter(
                missions_df,
                x="distance",
                y="duration",
                color="vehicle",
                size="payload",
                title="Mission Duration vs Distance from Earth",
                labels={
                    "distance":"Distance from Earth (light years)",
                    "duration":"Mission Duration (years)"
                }
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        # ===============================
        # GRAPH 4
        # ===============================
    
        elif graph_option == "Crew Size Distribution":
    
            fig = px.box(
                missions_df,
                y="crew",
                title="Crew Size Distribution"
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        # ===============================
        # GRAPH 5
        # ===============================
    
        elif graph_option == "Correlation Heatmap":
    
            corr = missions_df[["payload","fuel","cost","distance","duration","science","crew"]].corr()
    
            fig = px.imshow(
                corr,
                text_auto=True,
                title="Correlation Heatmap"
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        # ===============================
        # GRAPH 6
        # ===============================
    
        elif graph_option == "Mission Success vs Payload":
    
            fig = px.scatter(
                missions_df,
                x="payload",
                y="fuel",
                color="success",
                size="cost",
                title="Mission Success vs Payload and Fuel"
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        # ===============================
        # GRAPH 7
        # ===============================
    
        elif graph_option == "Mission Cost vs Mission Success":
    
            cost_success = missions_df.dropna(subset=["cost","success"])
    
            fig = px.box(
                cost_success,
                x="success",
                y="cost",
                color="success",
                title="Mission Cost for Successful vs Unsuccessful Missions",
                labels={
                    "success":"Mission Outcome",
                    "cost":"Mission Cost (Billion USD)"
                }
            )
    
            st.plotly_chart(fig, use_container_width=True)


    

          
    with tab5:

        st.markdown("<div class='glow'>Comparative Insights</div>", unsafe_allow_html=True)
    
        avg_payload = missions_df["payload"].mean()
    
        comparison = pd.DataFrame({
            "Type": ["Real Missions", "Simulation"],
            "Payload": [avg_payload, payload]
        })
    
        fig = px.bar(
            comparison,
            x="Type",
            y="Payload",
            title="Simulation vs Real Mission Payload"
        )
    
        st.plotly_chart(fig, use_container_width=True)


    with tab6:



        st.markdown("<div class='glow'>About This Project</div>",unsafe_allow_html=True)

        st.write("""
        
        RocketViz AI is an interactive platform that explores
        rocket launch physics and mission analytics.
        
        Technologies Used:
        
        • Python  
        • Streamlit  
        • Pandas  
        • Plotly  
        
        This project demonstrates how mathematical modelling
        and data science can be used to analyse space missions
        and simulate rocket launches.
        
        Developed for CRS Artificial Intelligence course.
        
        """)
        questions = [
        "🚀 What is RocketViz AI?",
        "⚙ How does the rocket simulation calculate altitude?",
        "📦 How does adding more payload affect altitude?",
        "🔥 How does increasing thrust affect launch success?",
        "🌬 Does lower drag at higher altitudes improve speed?",
        "🛰 How long would it take a rocket to reach orbit?",
        "📊 Can I compare simulation values to real mission data?",
        "⛽ How does fuel consumption affect rocket performance?",
        "📉 What factors cause rocket launch failure in the simulator?",
        "🔬 How can this simulator help understand real rocket missions?"
        ]
        selected = st.selectbox("Select a Question", questions)

       
        answers = {

        "🚀 What is RocketViz AI?":
        "RocketViz AI is an interactive platform that combines rocket launch simulation with space mission data analytics. It allows users to explore how physics variables such as thrust, fuel, drag, and payload influence rocket performance.",
        
        "⚙ How does the rocket simulation calculate altitude?":
        "The simulator calculates altitude using physics principles. Thrust provides upward force while gravity and drag oppose motion. The resulting acceleration changes velocity, which is then integrated over time to estimate altitude.",
        
        "📦 How does adding more payload affect altitude?":
        "Increasing payload increases the rocket's total mass. A heavier rocket requires more thrust to achieve the same acceleration. If thrust remains constant, higher payload reduces maximum altitude and may even prevent successful launch.",
        
        "🔥 How does increasing thrust affect launch success?":
        "Greater thrust increases upward force and improves acceleration. If thrust is significantly higher than the combined effects of gravity and drag, the rocket launches more efficiently and reaches higher altitude.",
        
        "🌬 Does lower drag at higher altitudes improve speed?":
        "Yes. As rockets climb higher, air density decreases, which reduces aerodynamic drag. Lower drag allows rockets to accelerate more efficiently and maintain higher speeds.",
        
        "🛰 How long would it take a rocket to reach orbit?":
        "Typical rockets take around 8–10 minutes to reach Low Earth Orbit (LEO). The exact time depends on thrust, payload mass, fuel efficiency, and aerodynamic drag.",
        
        "📊 Can I compare simulation values to real mission data?":
        "Yes. The dashboard includes real mission datasets containing payload weight, fuel consumption, mission cost, and success rates. These can be compared with simulation results to understand how real missions behave.",
        
        "⛽ How does fuel consumption affect rocket performance?":
        "As fuel burns, rocket mass decreases, which improves acceleration. However, once fuel is depleted, thrust stops and the rocket can no longer accelerate.",
        
        "📉 What factors cause rocket launch failure in the simulator?":
        "Launch failure may occur if thrust is too low compared to rocket mass, payload is too heavy, or drag is too high. These factors prevent the rocket from overcoming gravitational forces.",
        
        "🔬 How can this simulator help understand real rocket missions?":
        "The simulator helps visualize how physical variables interact during launch. By adjusting thrust, payload, fuel, and drag, users can explore scenarios similar to real rocket engineering challenges."
        }
    
        st.markdown(f"""
        <div class="glass">
        <h3>{selected}</h3>
        <p style="font-size:18px">{answers[selected]}</p>
        </div>
        """,unsafe_allow_html=True)




    



    









        
