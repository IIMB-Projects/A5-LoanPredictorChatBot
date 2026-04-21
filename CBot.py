import streamlit as st
import time
from datetime import date

# -------------------------------
# INIT STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "warning_level" not in st.session_state:
    st.session_state.warning_level = 0

def add_message(role, text):
    st.session_state.messages.append({
        "role": role,
        "text": text
    })

def get_prediction(payload):
    """
    API placeholder function.
    Teammate will replace this with actual API integration.
    """

# -------------------------------
# FUTURE API INTEGRATION
# -------------------------------
    # Example (to be implemented by teammate):
    #
    # import requests
    # API_URL = "http://<your-api-endpoint>/predict"
    # response = requests.post(API_URL, json=payload)
    # return response.json()
    #
# -------------------------------

    # Temporary mock response (for UI testing)
    return {"decision": "Approved"}




st.set_page_config(page_title="Loan Approval Chatbot")
st.title("💬 Loan Approval Chatbot")

# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "bot":
        st.write(f"🤖 {msg['text']}")
    else:
        st.write(f"👤 {msg['text']}")


# -------------------------------
# TIMEOUT HANDLER
# -------------------------------
def handle_timeout(first=15, later=10):
    elapsed = time.time() - st.session_state.start_time

    thresholds = [first, first + later, first + 2 * later]

    if st.session_state.warning_level == 0 and elapsed > thresholds[0]:
        st.warning("We need this information to evaluate your eligibility. Please provide the required input.")
        st.session_state.warning_level = 1

    elif st.session_state.warning_level == 1 and elapsed > thresholds[1]:
        st.error("Without this information, your application cannot be processed.")
        st.session_state.warning_level = 2

    elif st.session_state.warning_level == 2 and elapsed > thresholds[2]:
        st.error("We are unable to process your application right now. Thanks for considering ABC Credit.")
        st.stop()

# -------------------------------
# NAVIGATION
# -------------------------------
def next_step():
    st.session_state.step += 1
    st.session_state.start_time = time.time()
    st.session_state.warning_level = 0
    st.rerun()

def prev_step():
    st.session_state.step -= 1
    st.session_state.start_time = time.time()
    st.session_state.warning_level = 0
    st.rerun()

# -------------------------------
# COMMON UI
# -------------------------------
def show_back():
    if st.session_state.step > 0:
        if st.button("⬅ Back"):
            prev_step()

def number_input_clean(label, key):
    return st.text_input(label, key=key)

# -------------------------------
# STEP 0: SALARY
# -------------------------------
if st.session_state.step == 0:
    st.subheader("💰 Net Monthly Salary *")

    # Bot asks question (only once)
    if len(st.session_state.messages) == 0:
        add_message("bot", "Please enter your monthly salary.")

    # Timeout messages (converted to chat)
    elapsed = time.time() - st.session_state.start_time

    if elapsed > 15 and st.session_state.warning_level < 1:
        add_message("bot", "We need this information to evaluate your eligibility.")
        st.session_state.warning_level = 1

    elif elapsed > 30 and st.session_state.warning_level < 2:
        add_message("bot", "Without this information, your application cannot be processed.")
        st.session_state.warning_level = 2

    elif elapsed > 45:
        add_message("bot", "We are unable to process your application right now. Thanks for considering ABC Credit.")
        st.stop()

    # User input
    salary = st.text_input("Enter salary", key="salary")

    if st.button("Next", key="next_step0"):
        if salary and salary.isdigit() and int(salary) > 0:
            st.session_state.data["net_salary"] = int(salary)
            next_step()
        else:
            st.error("Salary must be greater than 0")

    # force refresh for timer to work
    time.sleep(1)
    st.rerun()

# -------------------------------
# STEP 1: LOAN AMOUNT
# -------------------------------
elif st.session_state.step == 1:
    #show_back()
    st.subheader("🏦 Loan Amount *")

    # Bot asks question (only once)
    if not any("loan amount" in msg["text"].lower() for msg in st.session_state.messages):
        add_message("bot", "Please enter your loan amount.")

    # Timeout logic (chat style)
    elapsed = time.time() - st.session_state.start_time

    if elapsed > 10 and st.session_state.warning_level < 1:
        add_message("bot", "We need this information to evaluate your eligibility.")
        st.session_state.warning_level = 1

    elif elapsed > 20 and st.session_state.warning_level < 2:
        add_message("bot", "Without this information, your application cannot be processed.")
        st.session_state.warning_level = 2

    elif elapsed > 30:
        add_message("bot", "We are unable to process your application right now. Thanks for considering ABC Credit.")
        st.stop()

    # User input
    loan = st.text_input("Enter loan amount", key="loan")

    # -------------------------------
    # BUTTONS (Back + Next)
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.step > 0:
            if st.button("⬅ Back", key="back_step1"):
                prev_step()

    with col2:
        if st.button("Next", key="next_step1"):
            if loan and loan.isdigit() and int(loan) > 0:

                add_message("user", f"My loan amount is {loan}")
                st.session_state.data["loan_amount"] = int(loan)

                next_step()
            else:
                st.error("Loan amount must be greater than 0")

    # Keep timer running
    time.sleep(1)
    st.rerun()

# -------------------------------
# STEP 2: HOUSING
# -------------------------------
elif st.session_state.step == 2:
    #show_back()
    st.subheader("🏠 Housing Category *")

    # Bot asks question (only once)
    if not any("housing" in msg["text"].lower() for msg in st.session_state.messages):
        add_message("bot", "What is your housing category? (Owned / Rent)")

    # Timeout logic
    elapsed = time.time() - st.session_state.start_time

    if elapsed > 10 and st.session_state.warning_level < 1:
        add_message("bot", "We need this information to evaluate your eligibility.")
        st.session_state.warning_level = 1

    if elapsed > 20 and st.session_state.warning_level < 2:
        add_message("bot", "Without this information, your application cannot be processed.")
        st.session_state.warning_level = 2


    if elapsed > 30 and st.session_state.warning_level < 3:
        add_message("bot", "We are unable to process your application right now. Thanks for considering ABC Credit.")
        st.session_state.warning_level = 3
        st.stop()

    # Input
    housing = st.selectbox("Select housing", ["Owned", "Rent"])

    # -------------------------------
    # BUTTONS (Back + Next)
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.step > 0:
            if st.button("⬅ Back", key="back_step2"):
                prev_step()

    with col2:
        if st.button("Next", key="next_step2"):
            add_message("user", f"My housing category is {housing}")
            st.session_state.data["housing"] = housing
            next_step()

    time.sleep(1)
    st.rerun()


# -------------------------------
# STEP 3: BIRTH DATE
# -------------------------------
elif st.session_state.step == 3:
    #show_back()
    st.subheader("📅 Birth Date *")

    if not any("birth" in msg["text"].lower() for msg in st.session_state.messages):
        add_message("bot", "Please select your birth date.")

    elapsed = time.time() - st.session_state.start_time

    if elapsed > 10 and st.session_state.warning_level < 1:
        add_message("bot", "We need this information to evaluate your eligibility.")
        st.session_state.warning_level = 1

    if elapsed > 20 and st.session_state.warning_level < 2:
        add_message("bot", "Without this information, your application cannot be processed.")
        st.session_state.warning_level = 2


    if elapsed > 30 and st.session_state.warning_level < 3:
        add_message("bot", "We are unable to process your application right now. Thanks for considering ABC Credit.")
        st.session_state.warning_level = 3
        st.stop()

    birth = st.date_input("Select birth date", max_value=date.today())

    # -------------------------------
    # BUTTONS (Back + Next)
    # -------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.step > 0:
            if st.button("⬅ Back", key="back_step3"):
                prev_step()

    with col2:
        if st.button("Next", key="next_step3"):
            if birth:
                add_message("user", f"My birth year is {birth.year}")
                st.session_state.data["birth_year"] = birth.year
                st.session_state.data["age"] = date.today().year - birth.year
                next_step()
            else:
                st.error("Birth date required")

    time.sleep(1)
    st.rerun()

# -------------------------------
# STEP 4: LIABILITIES
# -------------------------------
elif st.session_state.step == 4:
    #show_back()
    st.subheader("📊 Existing Liabilities *")

    if not any("liabilities" in msg["text"].lower() for msg in st.session_state.messages):
        add_message("bot", "Do you have existing liabilities?")

    elapsed = time.time() - st.session_state.start_time

    if elapsed > 10 and st.session_state.warning_level < 1:
        add_message("bot", "We need this information to evaluate your eligibility.")
        st.session_state.warning_level = 1

    if elapsed > 20 and st.session_state.warning_level < 2:
        add_message("bot", "Without this information, your application cannot be processed.")
        st.session_state.warning_level = 2


    if elapsed > 30 and st.session_state.warning_level < 3:
        add_message("bot", "We are unable to process your application right now. Thanks for considering ABC Credit.")
        st.session_state.warning_level = 3
        st.stop()

    choice = st.radio("Do you have liabilities?", ["Yes", "No"], index=None, key="liability_choice")

    liabilities = None
    if choice == "Yes":
        liabilities = st.text_input("Enter liabilities amount", key="liab_input")

    # -------------------------------
    # BUTTONS (Back + Next)
    # -------------------------------
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.step > 0:
            if st.button("⬅ Back", key="back_step4"):
                prev_step()

    with col2:
        if st.button("Next", key="next_step4"):
            if choice is None:
                st.error("Please select Yes or No")
            
            elif choice == "Yes":
                if liabilities and liabilities.isdigit() and int(liabilities) > 0:
                    add_message("user", f"My liabilities are {liabilities}")
                    st.session_state.data["liabilities"] = int(liabilities)
                    next_step()
                else:
                    st.error("Liabilities must be > 0")
            else:
                add_message("user", "I have no liabilities")
                st.session_state.data["liabilities"] = 0
                next_step()

    time.sleep(1)
    st.rerun()

# -------------------------------
# STEP 5: EDUCATION
# -------------------------------
elif st.session_state.step == 5:
    #show_back()
    st.subheader("🎓 Education Level")

    if not any("education" in msg["text"].lower() for msg in st.session_state.messages):
        add_message("bot", "What is your education level?")

    education_map = {
        "0 - No Formal Education": 0,
        "1 - Primary Schooling": 1,
        "2 - Secondary Schooling": 2,
        "3 - Higher Secondary": 3,
        "4 - Graduate": 4,
        "5 - Post Graduate / Professional Degree": 5,
        "Prefer not to say": -1
    }

    edu = st.selectbox("Select education", list(education_map.keys()))

    if st.button("Submit"):
        add_message("user", f"My education level is {edu}")

        st.session_state.data["education"] = education_map[edu]
        next_step()

# -------------------------------
# FINAL STEP
# -------------------------------
elif st.session_state.step == 6:
    st.subheader("🔍 Processing Application...")

    payload = st.session_state.data

    st.write("### 📦 Data sent to model/API")
    st.json(payload)

    # -------------------------------
    # SPINNER + PREDICTION CALL
    # -------------------------------
    with st.spinner("Analyzing your financial profile..."):
        result = get_prediction(payload)

    # -------------------------------
    # LOGGING (UI-level)
    # -------------------------------
    import json
    from datetime import datetime

    log_entry = {
        "timestamp": str(datetime.now()),
        "input": payload,
        "output": result
    }

    try:
        with open("loan_logs.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        st.warning("Logging failed")

    # -------------------------------
    # RESULT DISPLAY
    # -------------------------------
    if result["decision"] == "Approved":
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Declined")

    # -------------------------------
    # RESET FLOW
    # -------------------------------
    if st.button("Start New Application", key="restart"):

        # Reset all session state cleanly
        st.session_state.clear()

        st.rerun()