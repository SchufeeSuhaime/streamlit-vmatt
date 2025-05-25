import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(
    page_title="VMATT - Vibration Tool",
    layout="centered"
)

# --- Reset trigger control (must be before widgets)
if "reset_trigger" not in st.session_state:
    st.session_state.reset_trigger = False

# --- Perform the reset only BEFORE widgets render
if st.session_state.reset_trigger:
    st.session_state.mass = 0.0
    st.session_state.damping = 0.0
    st.session_state.spring = 0.0
    st.session_state.reset_trigger = False

# --- Initialize input values only once
for key in ["mass", "damping", "spring"]:
    if key not in st.session_state:
        st.session_state[key] = 0.0

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #fdfdfd;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        margin-top: 30px;
        margin-bottom: 10px;
        color: #1a1a1a;
    }

    .stTextInput > div > input {
        border-radius: 10px;
        border: 1px solid #bbb;
        padding: 12px;
        font-size: 16px;
        background-color: #f9f9f9;
    }

    .warning-box {
        background-color: #fff6d9;
        border-left: 6px solid #ffcc00;
        padding: 14px 18px;
        border-radius: 10px;
        margin-top: 20px;
        color: #663c00;
        font-size: 15.5px;
    }

    .footer {
        margin-top: 50px;
        text-align: center;
        color: #999;
        font-size: 13px;
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<div class='main-title'>VIBRATION MAGNIFICATION AND<br>ANGLE TEACHING TOOL (VMATT)</div>", unsafe_allow_html=True)

# --- Name Input ---
name = st.text_input("👤 Enter your name to continue:")

if not name:
    st.markdown("<div class='warning-box'>⚠️ Please enter your name to use VMATT.</div>", unsafe_allow_html=True)
else:
    # --- Description Box ---
    st.markdown("""
    <div style='margin-top: -10px; margin-bottom: 25px; font-size: 16px; text-align: center; color: #444;'>
        <em>VMATT is an interactive tool designed to help students understand vibration behavior through magnification and phase angle analysis. 
        Enter the system parameters below to visualize the dynamic response.</em>
    </div>
    """, unsafe_allow_html=True)

    # --- Input Form ---
    with st.form("vmatt_form"):
        st.markdown("<div style='font-size:22px; font-weight:700; color:#111;'>Input Parameters</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            m = st.number_input("Mass (m) [kg]", min_value=0.0, format="%.3f", key="mass")
        with col2:
            c = st.number_input("Damping Constant (c) [Ns/m]", min_value=0.0, format="%.3f", key="damping")
        with col3:
            k = st.number_input("Spring Constant (k) [N/m]", min_value=0.0, format="%.3f", key="spring")

        col_enter, col_reset = st.columns([1, 1])
        with col_enter:
            enter = st.form_submit_button("ENTER")
        with col_reset:
            reset = st.form_submit_button("RESET")

    # --- Reset Functionality ---
    if reset:
        st.session_state.reset_trigger = True
        st.rerun()

    # --- Enter Processing ---
    if enter:
        if m == 0.0 or c == 0.0 or k == 0.0:
            st.warning("⚠️ Please enter valid non-zero values for Mass (m), Damping Constant (c), and Spring Constant (k).")
        else:
            omega_n = np.sqrt(k / m)
            zeta = c / (2 * np.sqrt(k * m))

            eta = np.linspace(0, 5, 500)
            mag = 1 / np.sqrt((1 - eta**2)**2 + (2 * zeta * eta)**2)
            phi = np.arctan2(2 * zeta * eta, 1 - eta**2) * (180 / np.pi)
            phi = np.where(phi < 0, phi + 180, phi)

            st.subheader("📈 Magnification Factor vs Frequency Ratio")
            fig1, ax1 = plt.subplots()
            ax1.plot(eta, mag, color='royalblue')
            ax1.set_xlabel("Frequency Ratio (r)")
            ax1.set_ylabel("Magnification Factor (M)")
            ax1.grid(True)
            st.pyplot(fig1)

            st.subheader("📈 Phase Angle vs Frequency Ratio")
            fig2, ax2 = plt.subplots()
            ax2.plot(eta, phi, color='firebrick')
            ax2.set_xlabel("Frequency Ratio (r)")
            ax2.set_ylabel("Phase Angle (ϕ) [°]")
            ax2.grid(True)
            st.pyplot(fig2)

            idx = np.abs(eta - 1).argmin()
            M_res = mag[idx]
            phi_res = phi[idx]

            st.success(f"✅ Output at Resonance (r = 1) for {name}")
            colM, colP, colZ = st.columns(3)
            colM.metric("Magnification Factor (M)", f"{M_res:.4f}")
            colP.metric("Phase Angle (ϕ)", f"{phi_res:.2f}°")
            colZ.metric("Damping Ratio (ζ)", f"{zeta:.4f}")

# --- Footer ---
st.markdown("<div class='footer'>Developed by Schufee Suhaime – 2025</div>", unsafe_allow_html=True)
