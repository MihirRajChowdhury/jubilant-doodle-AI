import streamlit as st
from langchain import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# Prompt template
template = """
    Below is a draft text that may be poorly worded.
    Your goal is to:
    - Properly redact the draft text
    - Convert the draft text to a specified tone
    - Convert the draft text to a specified dialect

    Here are some examples different Tones:
    - Formal: Greetings! OpenAI has announced that Sam Altman is rejoining...
    - Informal: Hey everyone, it's been a wild week...

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment...
    - British: chips, candyfloss, flat...

    Example Sentences from each dialect:
    - American: Greetings! OpenAI has announced that Sam Altman is rejoining...
    - British: On Wednesday, OpenAI, the esteemed artificial intelligence start-up...

    Please start the redaction with a warm introduction. Add the introduction if you need to.
    
    Below is the draft text, tone, and dialect:
    DRAFT: {draft}
    TONE: {tone}
    DIALECT: {dialect}

    YOUR {dialect} RESPONSE:
"""


prompt = PromptTemplate(
    input_variables = ["tone","draft","dialect"],
    template = template
)

def load_LLM(google_api_key):
    import os
    # google_api_key = os.environ["GOOGLE_API_KEY"]
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, google_api_key=google_api_key)
    return llm


st.set_page_config(page_title="Re-write your text")
st.header("Welcome, What do you want me to rewrite?")

col1,col2=st.columns(2)

with col1:
    st.markdown("Re-write your text in different styles.")
with col2:
    st.write("Contact with [Mihir Raj Chowdhury](Mihirrajchowdhury.netlify.app) to build your AI Projects")

st.markdown("## Enter Your Gemini API Key")
def get_google_api_key():
    input_text = st.text_input(
        label="Gemini API Key", 
        placeholder="Ex: AIzaSyD4-abc123...", 
        key="google_api_key_input", 
        type="password"
    )
    return input_text

google_api_key = get_google_api_key()

st.markdown("## Enter the text you want to re-write")
def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox('Which tone would you like your redaction to have?', ('Formal', 'Informal', 'Geeky','Bold'))
with col2:
    option_dialect = st.selectbox('Which English Dialect would you like?', ('American', 'British', 'Indian'))

st.markdown("### Your Re-written text:")


if draft_input:
    if not google_api_key:
        st.warning('Please insert Gemini API Key. Instructions [here](https://makersuite.google.com/app/apikey)', icon="⚠️")
        st.stop()

    llm = load_LLM(google_api_key=google_api_key)
    
    prompt_with_draft = prompt.format(
        tone=option_tone, 
        dialect=option_dialect, 
        draft=draft_input
    )

    improved_redaction = llm.invoke(prompt_with_draft)

    st.write(improved_redaction)
