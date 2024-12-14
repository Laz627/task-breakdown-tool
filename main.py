import streamlit as st
import openai

# App title
st.title("Task Breakdown Assistant")
st.markdown("Enter a task, its description, and effort level, and let GPT-4 break it down for you.")

# User input for OpenAI API key
st.sidebar.title("API Key Setup")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if api_key:
    openai.api_key = api_key

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
        total_time_estimate = st.number_input(
            "Total Time Estimate (in hours)", min_value=0.0, step=0.5, help="Enter your estimated total time for the task."
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
                f"Complexity Level: {complexity_level}\n"
                f"Total Time Estimate: {total_time_estimate} hours\n\n"
                "Please break down this task into clear, actionable steps, distributing the total time estimate across the steps. Indicate the time/effort needed for each step."
                " If the breakdown seems unrealistic based on the input time estimate, provide a warning and suggest adjustments."
            )

            try:
                # Call OpenAI's API
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",  # Replace with your preferred model
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that breaks down tasks."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
                )

                # Extract and display the output
                task_breakdown = response["choices"][0]["message"]["content"].strip()
                if "warning" in task_breakdown.lower():
                    st.warning("The provided time estimate may be underestimated. Consider revising it based on the suggested steps.")
                
                st.subheader("Task Breakdown")
                st.markdown(task_breakdown)

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.sidebar.warning("Please enter your OpenAI API Key to use the application.")

# Add a footer with usage instructions
st.markdown("---")
st.markdown(
    "### How to Use:\n"
    "1. Enter your OpenAI API Key in the sidebar.\n"
    "2. Enter the task details.\n"
    "3. Choose the estimated effort level and complexity.\n"
    "4. Enter your total time estimate for the task.\n"
    "5. Click 'Generate Task Breakdown' to get actionable steps.\n"
    "6. If the estimate seems off, you'll receive a warning with suggestions."
)
