import streamlit as st
import google.generativeai as genai
import re
import random
import string
import pyperclip

st.set_page_config(page_title="🔒 STRONG PASSWORD GENERATOR")
st.title("🔒 STRONG PASSWORD GENERATOR")

# **Session state me lists initialize karein**
if "save_password_manual" not in st.session_state:
    st.session_state.save_password_manual = []  # is ky andar manual password save ho rahy hai
if "save_password_ai" not in st.session_state:
    st.session_state.save_password_ai = []  # is ky andar Ai password save ho rahy hai

# is ky zayeye user range selete kary ga
value = st.slider("Password Length", min_value=1, max_value=30, value=8)
st.write("Selected Length:", value)

if value > 5:  # agar user ny 5 length sy com selete ki to ye false ho jaye ga
    manage_password_1 = st.radio("Select Case", ["Uppercase", "Lowercase"])
    manage_password_2 = st.radio("Select Character Type", ["Easy to say", "Easy to read", "All characters"])


    col1, col2 = st.columns(2)

    with col1:  # ye manual password wala section
        with st.form("manual_password_form"):
            if st.form_submit_button("🔑 Manual Generate Password"):

                # is ky nadar manual password generate ho rahy hai
                def generate_password(length, char_type):  # ek ky andar length arahe hai or dosary main manage_password_2 ki value arahe hai
                    if char_type == "Easy to say":
                        characters = string.ascii_letters + string.digits
                    elif char_type == "Easy to read":
                        characters = "".join(set(string.ascii_letters + string.digits) - {"I", "l", "O", "0"})
                    else:
                        characters = string.ascii_letters + string.digits + string.punctuation
                    return ''.join(random.choice(characters) for _ in range(length))

                # is ky andar password valify ho raha hai
                def is_valid_password(password):
                    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]?)[A-Za-z\d@$!%*?&]{8,}$"
                    return bool(re.match(pattern, password))

                while True:
                    password = generate_password(value, manage_password_2)  # ek ky andar length jarahe hai or dosary main manage_password_2 ki value jarahe hai
                    if is_valid_password(password):
                        if manage_password_1 == "Uppercase":
                            password = password.upper()
                        elif manage_password_1 == "Lowercase":
                            password = password.lower()

                        st.session_state.generated_password = password
                        break

            if "generated_password" in st.session_state:
                manual_password = st.text_input("Generated Password", st.session_state.generated_password, key="password_manual_display")
                # is ky zayeye user manual password ko copy karry ga
                if st.form_submit_button("📋 Copy"):
                    pyperclip.copy(manual_password)
                    st.success("✅ Copy Password Successfully")

                # Manual password history save karein
                if manual_password and manual_password not in st.session_state.save_password_manual:
                    st.session_state.save_password_manual.append(manual_password)  # is ky zayeye save_password_manual ky andar paasword jaraha hai

    with col2:  # ye AI wala section hai
        with st.form("ai_password_form"):
            if st.form_submit_button("🔑 AI Generate Password"):
                with st.spinner("Generating password... Please wait"): # jab tak bata nhi aye ga to ye chaly ga
                    API_KEY_TOKEN = st.secrets["API_KEY"]
                    genai.configure(api_key=API_KEY_TOKEN)
                    model = genai.GenerativeModel("gemini-1.5-pro")

                    # is ky andar AI ko trian karaha ho
                    prompt = f"""
                    You are a password generator AI. Your task is to generate a strong password.
                    Don't give explanations, just output a random, secure password with at least:
                    - {value} characters
                    - {manage_password_1} case
                    - {manage_password_2} type
                    - No spaces or unnecessary text
                    Now, generate the password:
                    """

                    response = model.generate_content(prompt)

                if response and response.text:
                    ai_generate = response.text.strip()  # response.text AI ka generate kiya hua poora text return karega or .strip()  Agar text ke start ya end me extra spaces ya new lines hain to unko hata dyga.
                    st.session_state.ai_generated_password = ai_generate

            if "ai_generated_password" in st.session_state:
                ai_generate = st.text_input("Generated Password", st.session_state.ai_generated_password, key="password_ai_display")
                # is ky zayeye user AI password ko copy karry ga
                if st.form_submit_button("📋 Copy"):
                    pyperclip.copy(ai_generate)
                    st.success("✅ Copy Password Successfully")

                # AI password history save karein
                if ai_generate and ai_generate not in st.session_state.save_password_ai:
                    st.session_state.save_password_ai.append(ai_generate)  # is ky zayeye save_password_ai ky andar password jaraha hai

    if st.button("History"):  # user jitny bhi password generate kary ga wo is main show hoye gy
        # is ky andar manual password show hoye gy
        st.write("### 🔑 Manual Password History")
        for index, getvalue in enumerate(st.session_state.save_password_manual, start=1):
            st.write(f"{index}. {getvalue}")

        # is ky andar AI password show hoye gy
        st.write("### 🤖 AI Generated Password History")
        for index, getvalue in enumerate(st.session_state.save_password_ai, start=1):
            st.write(f"{index}. {getvalue}")

else:
    st.warning("⚠️ Please select a password length greater than 5.")