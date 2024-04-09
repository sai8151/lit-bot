import streamlit as st
import json

# Load JSON data from train.json
with open('train.json', 'r') as json_file:
    investment_data = json.load(json_file)

# Extract plans and target audience, handling missing 'plan' key
plans = [plan.get('plan', '').lower() for plan in investment_data['schemes']]
target_audience_list = [plan.get('target_audience', '').lower() for plan in investment_data['schemes']]

# Streamlit app
def main():
    st.title("Investment Bot")

    user_message = st.text_input("Enter your message:")
    
    if st.button("Submit"):
        if user_message:
            response = get_most_similar_plan(user_message)
            st.write(f"Bot Response: {response}")
        else:
            st.write("Error: No message provided.")

def get_most_similar_plan(user_input):
    user_input = user_input.lower()

    # Find the most similar plan based on keyword matching
    max_similarity = -1
    most_similar_plan = ""
    target_audience = ""
    for plan, audience in zip(plans, target_audience_list):
        similarity = sum(word in user_input for word in plan.split())
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_plan = plan
            target_audience = audience

    return f"{most_similar_plan.title()} - {target_audience}"

if __name__ == '__main__':
    main()
