import streamlit as st
import re
import random
import string
import pyperclip  # Clipboard ke liye

st.set_page_config(page_title="🔒 STRONG PASSWORD GENERATOR")

st.title("🔒 STRONG PASSWORD GENERATOR")

value = st.slider(
    "Password Length", 
    min_value=1, 
    max_value=30, 
    value=8  # Default value
)

st.write("Selected Length:", value)

if value > 5:
    manage_password_1 = st.radio(
        "Select Case",
        ["Uppercase", "Lowercase"],
    )

    manage_password_2 = st.radio(
        "Select Character Type",
        ["Easy to say", "Easy to read", "All characters"]
    )

    def generate_password(length, char_type):
        if char_type == "Easy to say":
            characters = string.ascii_letters + string.digits  # No special characters
        elif char_type == "Easy to read":
            characters = "".join(set(string.ascii_letters + string.digits) - {"I", "l", "O", "0"})  # Remove confusing characters
        else:
            characters = string.ascii_letters + string.digits + string.punctuation  # All characters
        
        return ''.join(random.choice(characters) for _ in range(length))

    def is_valid_password(password):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]?)[A-Za-z\d@$!%*?&]{8,}$"
        return bool(re.match(pattern, password))
    
    if st.button("🔑 Generate Password"):
        while True:
            password = generate_password(value, manage_password_2)
            if is_valid_password(password):
                if manage_password_1 == "Uppercase":
                    password = password.upper()
                elif manage_password_1 == "Lowercase":
                    password = password.lower()

                # Save password in session state
                st.session_state.generated_password = password
                break

    # **Show Password After Generation**
    if "generated_password" in st.session_state:
        generated_password = st.session_state.generated_password
        st.text_input("Generated Password", generated_password, key="password_display")

        # **Copy Button**
        if st.button("📋 Copy to Clipboard"):
            pyperclip.copy(generated_password)
            st.success("✅ Password copied to clipboard!")

else:
    st.warning("⚠️ Please select a password length greater than 5.")


