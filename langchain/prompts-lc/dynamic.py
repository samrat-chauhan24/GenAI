# when a basic template of prompt is defined by developer but the key inputs are given by the user
# then this type of prompts are known as dynamic

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt


load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

# streamlit block
st.header("Research Tool")

paper_input = st.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"])

style_input = st.selectbox("Select Explanation Style", ["Beginner-Friendly", "Technical",
"Code-Oriented", "Mathematical"] )

length_input = st. selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation) "] )

template = load_prompt('template.json')

if st.button("summarize"):
    # initially i was using  invoke 2 time so made a chain and invoked it
    chain = template | model
    result = chain.invoke({
    'paper_input': paper_input,
    'length_input': length_input,
    'style_input': style_input
    })
    st.write(result.content)


 