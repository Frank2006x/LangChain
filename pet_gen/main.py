import langchain_helper as lch
import streamlit as st


st.set_page_config(
    page_title="Pet Name Generator",
    page_icon="🐾",
    layout="centered"
)


st.title("🐾 Pet Name Generator")
st.markdown("Generate creative and cool names for your pets using AI!")


col1, col2 = st.columns(2)

with col1:
    
    animal_type = st.selectbox(
        "🐱 What type of pet do you have?",
        ["Dog", "Cat", "Bird", "Fish", "Rabbit", "Hamster", "Guinea Pig", "Turtle", "Mouse", "Snake", "Other"],
        index=0
    )

with col2:
   
    pet_color = st.selectbox(
        "🎨 What color is your pet?",
        ["Black", "White", "Brown", "Gray", "Golden", "Orange", "Blue", "Green", "Red", "Yellow", "Mixed", "Other"],
        index=0
    )


if animal_type == "Other":
    animal_type = st.text_input("Please specify your pet type:", placeholder="e.g., Lizard, Parrot, etc.")

if pet_color == "Other":
    pet_color = st.text_input("Please specify your pet's color:", placeholder="e.g., Silver, Spotted, etc.")


if st.button("🎯 Generate Pet Names", type="primary"):
    if animal_type and pet_color:
        with st.spinner("Generating awesome names for your pet..."):
            try:
                
                result = lch.pet_name(animal_type.lower(), pet_color.lower())
                
                if result:
                    st.success("Here are some cool names for your pet!")
                    
                   
                    st.markdown("### 🌟 Generated Names:")
                    
                   
                    names = result.strip().split('\n')
                    
                    
                    for i, name in enumerate(names, 1):
                        if name.strip():
                           
                            clean_name = name.strip().lstrip('1234567890.- ')
                            if clean_name:
                                st.markdown(f"**{i}.** {clean_name}")
                    
                   
                    st.balloons()
                    st.markdown("---")
                    st.markdown("💡 **Tip:** Try different colors or animal types for more name ideas!")
                    
                else:
                    st.error("Sorry, I couldn't generate names right now. Please try again!")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key and internet connection.")
    else:
        st.warning("Please select both animal type and color!")


with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This pet name generator uses **Google's Gemini AI** to create unique and creative names for your pets based on their type and color.
    
    **Features:**
    - 🤖 AI-powered name generation
    - 🎨 Color-based suggestions
    - 🐾 Multiple pet types supported
    - ⚡ Fast and easy to use
    """)
    
    st.header("🚀 How to use")
    st.markdown("""
    1. Select your pet type
    2. Choose your pet's color
    3. Click "Generate Pet Names"
    4. Enjoy your new pet names!
    """)
    
    st.header("💡 Examples")
    st.markdown("""
    - **Black Cat** → Shadow, Midnight, Onyx
    - **Golden Dog** → Sunny, Honey, Amber
    - **Blue Bird** → Sky, Azure, Neptune
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Made with ❤️ using Streamlit and LangChain | "
    "Powered by Google Gemini AI"
    "</div>", 
    unsafe_allow_html=True
)