import streamlit as st
import google.generativeai as genai

# Configure API Key securely from Streamlit secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize the model (recommended latest flash version)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to run the Streamlit app
def main():
    st.title("🧠 AI Code Reviewer")
    st.write("Submit your code for review and get bug reports & fixes!")

    # User Input
    code_input = st.text_area("Paste your code here:", height=200)
    language = st.selectbox("Select Programming Language:", [
        "Python", "JavaScript", "Java", "C++", "C#", "Go", "Ruby", "Swift", "Kotlin", "PHP", "Rust", "Other"
    ])

    if st.button("Review Code"):
        if code_input.strip():
            with st.spinner("Reviewing your code... ⏳"):
                user_prompt = (
                    f"""
                    You are a professional software code reviewer.
                    - Analyze the following {language} code for **errors, inefficiencies, and improvements**.
                    - Provide a **bug report** with explanations.
                    - Give a **fully corrected version** of the code.
                    - Format the output using bullet points for readability.
                    - Ensure the fixed code is presented inside a Markdown block with a copy button.

                    Here is the user's code:
                    ```{language.lower()}
                    {code_input}
                    ```

                    Return the response strictly in this format:
                    ## Bug Report
                    - **Issue:** [Brief description of the issue]
                    - **Description:** [Detailed explanation of the problem]
                    - **Severity:** [Low / Medium / High]
                    - **Explanation:** [Why this issue occurs and its impact]
                    - **Steps to Reproduce:**
                      1. [Step 1]
                      2. [Step 2]
                    - **Expected Result:** [What should happen]
                    - **Actual Result:** [What actually happens]

                    ## Fixed Code
                    Below is the corrected version of the code. You can copy it directly:
                    ```{language.lower()}
                    [Fixed code here]
                    ```
                    """
                )

                # Send prompt to Gemini (fixed to use list input for generate_content)
                try:
                    response = model.generate_content([user_prompt])
                    st.subheader("🔍 AI Code Review Report")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"🚨 Error generating review: {e}")

        else:
            st.warning("⚠️ Please enter code before submitting.")

if __name__ == "__main__":
    main()
