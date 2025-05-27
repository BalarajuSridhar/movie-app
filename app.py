import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 🚀 Must be the first Streamlit command
st.set_page_config(page_title="🎬 Movie Quiz Registration", page_icon="🍿", layout="centered")

# 📁 Constants
DATA_FILE = "participants.csv"

# 🛡️ Ensure CSV file exists with correct headers
if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
    pd.DataFrame(columns=["Timestamp", "Name", "Email", "Phone"]).to_csv(DATA_FILE, index=False)

# 🎨 Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 🖼️ Header
st.image("gjft.jpg", width=100)
st.title("🍿 Welcome to the Movie Quiz!")
st.markdown("Fill in your details to participate in our fun & exciting movie quiz. 🎥")

# 📝 Registration Form
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
            df = pd.read_csv(DATA_FILE)

            # Duplicate check
            if email in df["Email"].astype(str).str.lower().values or phone in df["Phone"].astype(str).values:
                st.warning("⚠️ You have already registered with this email or phone number.")
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

# 🛠️ Admin Panel
with st.expander("📊 Admin View (Total Registrations & Download Data)"):
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            st.metric("Total Registrations", len(df))
            st.dataframe(df)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="participants.csv", mime="text/csv")
        except pd.errors.EmptyDataError:
            st.warning("⚠️ The file exists but is empty. No data to show.")
    else:
        st.info("No registrations yet.")

# 💬 Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Made with ❤️ for movie lovers • Powered by Streamlit</p>",
    unsafe_allow_html=True
)
