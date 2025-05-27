import streamlit as st
import pandas as pd
import os
from datetime import datetime

# App Configuration
st.set_page_config(page_title="🎬 Movie Quiz Registration", page_icon="🍿", layout="centered")

# Constants
DATA_FILE = "participants.csv"
ADMIN_EMAIL = "sridharraju402@gmail.com"
ADMIN_PHONE = "9640416063"

# Style
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; padding: 30px; border-radius: 10px; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.image("https://i.imgur.com/8fKQKcF.png", width=300)
st.title("🍿 Welcome to the Movie Quiz!")
st.markdown("Fill in your details to participate in our fun & exciting movie quiz. 🎥")

# ---- Registration Form ----
with st.form("register"):
    st.subheader("📋 Registration Form")
    name = st.text_input("👤 Full Name").title()
    email = st.text_input("📧 Email Address").strip().lower()
    phone = st.text_input("📱 Phone Number").strip()
    submit = st.form_submit_button("✅ Submit")

    if submit:
        if not name or not email or not phone:
            st.error("Please fill all required fields.")
        else:
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
            else:
                df = pd.DataFrame(columns=["Timestamp", "Name", "Email", "Phone"])

            # Check for duplicate
            if email in df["Email"].astype(str).str.lower().values or phone in df["Phone"].astype(str).values:
                st.warning("⚠️ You have already registered.")
            else:
                new_entry = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Name": name,
                    "Email": email,
                    "Phone": phone
                }
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("🎉 Registration successful!")
                st.balloons()
                st.write("Here’s your registration info:")
                st.json(new_entry)

# ---- Admin Login Section ----
st.markdown("---")
with st.expander("🔒 Admin Login"):
    st.subheader("Admin Access")
    admin_email = st.text_input("Admin Email").strip().lower()
    admin_phone = st.text_input("Admin Phone Number").strip()
    login = st.button("🔓 Login as Admin")

    if login:
        if admin_email == ADMIN_EMAIL or admin_phone == ADMIN_PHONE:
            st.success("✅ Admin access granted!")
            
            # Show Admin Panel
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
                st.markdown("## 📊 Admin Panel")
                st.metric("Total Registrations", len(df))
                st.dataframe(df)
                st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="participants.csv", mime="text/csv")
            else:
                st.info("No registrations yet.")
        else:
            st.error("❌ Invalid admin credentials.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Made with ❤️ for movie lovers • Powered by Streamlit</p>",
    unsafe_allow_html=True
)
