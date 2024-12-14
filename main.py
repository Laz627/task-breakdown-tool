import streamlit as st
import openai

# Set up OpenAI API key (ensure your key is securely stored and not hard-coded in production)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App title
st.title("Task Breakdown Assistant")
st.markdown("Enter a task, its description, and effort level, and let GPT-4 break it down for you.")

# User inputs
with st.form("task_form"):
    task_name = st.text_input("Task Name", placeholder="E.g., Clean the house")
    task_description = st.text_area("Brief Description", placeholder="Describe the task in detail.")
    effort_level = st.selectbox(
        "Estimated Effort Level",
        ["Low", "Medium", "High"],
        help="Select how much effort the task will likely require."
    )
    complexity_level = st.slider(
        "Complexity / Steps to Break Down Task Into",
        min_value=1,
        max_value=10,
        value=3,
        help="Choose how many steps the task should be broken into."
    )
    submitted = st.form_submit_button("Generate Task Breakdown")

# Generate output when form is submitted
if submitted:
    if not task_name or not task_description:
        st.error("Please fill out all fields.")
    else:
        # Generate prompt for GPT-4
        prompt = (
            f"Task Name: {task_name}\n"
            f"Description: {task_description}\n"
            f"Effort Level: {effort_level}\n"
            f"Complexity Level: {complexity_level}\n\n"
            "Please break down this task into clear, actionable steps, indicating the time/effort needed for each step. Provide time estimates for completing each step as well."
        )

        try:
            # Call OpenAI's API
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Replace with your preferred model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that breaks down tasks."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )

            # Extract and display the output
            task_breakdown = response["choices"][0]["message"]["content"].strip()
            st.subheader("Task Breakdown")
            st.markdown(task_breakdown)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Add a footer with usage instructions
st.markdown("---")
st.markdown(
    "### How to Use:\n"
    "1. Enter the task details.\n"
    "2. Choose the estimated effort level and complexity.\n"
    "3. Click 'Generate Task Breakdown' to get actionable steps."
)
