import streamlit as st
import openai

# Use correct key structure: adjust based on your secrets.toml
openai.api_key = st.secrets["openai_key"]  # Or st.secrets["openai"]["api_key"] if nested

# Define neutral product features, benefits, pain points, and desires
product_features_list = ["Voice control", "Touch screen interface", "Smart inventory management", "Recipe suggestions"]
product_benefits_list = ["Convenience", "Reduced food waste", "Personalized cooking assistance", "Energy efficiency", "Longer food freshness"]
target_audience_list = ["Busy families", "Health-conscious individuals", "Tech enthusiasts", "Cooking aficionados", "Home chefs"]
pain_points_list = ["Limited kitchen space", "Difficulty meal planning", "Time constraints", "Food spoilage concerns"]
desires_list = ["Simplified cooking", "Healthier eating", "Optimized organization", "Culinary inspiration"]
channels = ["Instagram", "Facebook", "Twitter", "Email"]
tones = ["Casual", "Informative", "Enthusiastic", "Humorous", "Inspirational"]

# Function to generate marketing copy
def generate_copy(product_name, features, benefits, audience, pains, wants, channel, tone):
    # Ensure all are strings
    audience_str = audience if isinstance(audience, str) else ", ".join(audience)
    features_str = ", ".join(features) if features else "N/A"
    benefits_str = ", ".join(benefits) if benefits else "N/A"
    pains_str = ", ".join(pains) if pains else "N/A"
    wants_str = ", ".join(wants) if wants else "N/A"

    prompt = f"""
You're a marketing copywriter. Write a {channel} post caption and image description to promote the {product_name}, a new smart refrigerator.

**Target audience:** {audience_str}

**Highlight:**
* Key features: {features_str}
* Benefits: {benefits_str}
* Address these pain points: {pains_str}
* Appeal to these desires: {wants_str}

**Tone:** {tone}

**Image description:** A photo of the {product_name} in a modern kitchen setting, with the door open to showcase the organized interior and a user interacting with it.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a marketing copywriter."},
            {"role": "user", "content": prompt}
        ]
    )
    
    copy = response['choices'][0]['message']['content']

    # Defensive split: fallback if \n\n not present
    parts = copy.strip().split("\n\n", 1)
    caption = parts[0].strip()
    image_description = parts[1].strip() if len(parts) > 1 else "(No image description generated.)"
    
    return caption, image_description

# Streamlit UI
st.title("Smart Fridge Pro Marketing Copy Generator")

product_name = st.text_input("Product Name:", value="Smart Fridge Pro")
selected_features = st.multiselect("Product Features:", product_features_list, default=product_features_list[:2])
selected_benefits = st.multiselect("Product Benefits:", product_benefits_list, default=product_benefits_list[:2])
selected_audience = st.selectbox("Target Audience:", target_audience_list)
selected_pain_points = st.multiselect("Pain Points:", pain_points_list, default=pain_points_list[:2])
selected_desires = st.multiselect("Desires:", desires_list, default=desires_list[:2])
selected_channel = st.selectbox("Channel:", channels)
selected_tone = st.selectbox("Tone:", tones)

if st.button("Generate Marketing Copy"):
    try:
        caption, image_description = generate_copy(
            product_name,
            selected_features,
            selected_benefits,
            selected_audience,
            selected_pain_points,
            selected_desires,
            selected_channel,
            selected_tone
        )
        st.subheader("Caption:")
        st.write(caption)
        st.subheader("Image Description:")
        st.write(image_description)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
