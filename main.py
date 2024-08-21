import streamlit  as st   # Streamlit
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI # OpenAI

# Create a prompt template
template = """
For the following text, extract the following \
information:

sentiment: Is the customer happy with the product? 
Answer Positive if yes, Negative if \
not, Neutral if either of them, or Unknown if unknown.

delivery_days: How many days did it take \
for the product to arrive? If this \
information is not found, output No information about this.

price_perception: How does it feel the customer about the price? 
Answer Expensive if the customer feels the product is expensive, 
Cheap if the customer feels the product is cheap,
not, Neutral if either of them, or Unknown if unknown.

Format the output as bullet-points text with the \
following keys:
- Sentiment
- How long took it to deliver?
- How was the price perceived?

Input example:
This dress is pretty amazing. It arrived in two days, just in time for my wife's anniversary present. It is cheaper than the other dresses out there, but I think it is worth it for the extra features.

Output example:
- Sentiment: Positive
- How long took it to deliver? 2 days
- How was the price perceived? Cheap

text: {review}
"""

prompt = PromptTemplate(
    input_variable=["review"],
    template=template,
)

## LLM Model
def load_LLM(openai_api_key):
    openai = OpenAI(openai_api_key=openai_api_key, temperature=0)
    return openai

## page title and header
st.set_page_config(
    page_title="Extract Key Information from Product Reviews",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="expanded",
)
st.header("Extract Key Information from Product Reviews")

# intro
col1, col2 =st.columns(2)
with col1:
    st.markdown("Extract Key Information from Product Reviews")
    st.markdown(
    """
    - Sentiment
    - How long took it to deliver?
    - How was its price perceived?
    """
    )
with col2:
    st.write("Contact with [Toraaglobal](https://toraaglobal.com) to build your AI solution")


st.sidebar.text("Enter your OpenAI API Key")
openai_api_key = st.sidebar.text_input("API Key", type="password", placeholder="Enter your OpenAI API Key", key="api_key")

## input
def get_review():
    review = st.text_area("Enter your review here", height=200,label_visibility="collapsed", key="review", placeholder="Enter your review here")
    return review

review_input = get_review()

## output
st.markdown("### Key Data Extracted:- ")

if st.button("Extract Key Information"):
    if review_input:
        if not openai_api_key:
            st.warning("Please enter your OpenAI API Key \
                       Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)",
                       icon="warning")
            st.stop()
        llm = load_LLM(openai_api_key=openai_api_key)

        prompt_with_review = prompt.format(review=review_input)

        key_data_extraction = llm(prompt_with_review)
        st.write(key_data_extraction)
