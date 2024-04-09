import streamlit as st
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

# Load JSON data from train.json
with open('train.json', 'r') as json_file:
    investment_data = json.load(json_file)

# Extract plans and target audience, handling missing 'plan' key
plans = [plan.get('plan', '').lower() for plan in investment_data['schemes']]
target_audience_list = [plan.get('target_audience', '').lower() for plan in investment_data['schemes']]

# Combine plan names and target audience for similarity analysis
combined_text = [f"{plan} {audience}" for plan, audience in zip(plans, target_audience_list)]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(combined_text)

def get_most_similar_plan(user_input):
    # Process user input
    user_input = user_input.lower()

    # Transform user input using the same vectorizer
    user_tfidf = vectorizer.transform([user_input])

    # Calculate cosine similarity
    similarities = cosine_similarity(user_tfidf, tfidf_matrix)[0]

    # Get the indices of the most similar plans
    most_similar_indices = [i for i, sim in sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)]

    # Select a random index from the top 3 most similar plans
    random_index = random.choice(most_similar_indices[:3])

    # Get the recommended plan and target audience
    recommended_plan = plans[random_index]
    target_audience = target_audience_list[random_index]

    # Reframe the sentence by capitalizing the first letter of each word
    reframed_response = recommended_plan.title()

    return f"{reframed_response} - {target_audience}"

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

if __name__ == '__main__':
    main()
