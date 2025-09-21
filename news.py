import streamlit as st

# State variable to manage expander visibility
if 'show_options' not in st.session_state:
    st.session_state.show_options = False

# State variable to manage chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AI Fact-Checker title at the very top ---
st.markdown("<h1 style='text-align: center;'>📰Live News Fact Checker</h1>", unsafe_allow_html=True)
st.divider()

# --- Welcome Section at the top, just below the title ---
if not st.session_state.messages:
    st.subheader("Welcome to Pathway Live News Fact Checker")
    st.markdown("""
    This application is designed to provide real-time fact-checking summaries for news topics and URLs. Built on the powerful **Pathway** framework, this AI is continuously updated and provides insights based on the latest knowledge.
    """)
    st.divider()

# --- Chat messages will appear in the middle ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- The expander with input tabs at the bottom, above the chat input ---
if st.session_state.show_options:
    with st.expander("Choose Input Type", expanded=True):
        tab1, tab2 = st.tabs(["Image", "Audio/Video"])
        with tab1:
            st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])

        with tab2:
            st.file_uploader("Choose a media file", type=["mp3", "mp4", "wav"])

# --- The unified input area (with + and text input) at the very bottom ---
col1, col2 = st.columns([0.1, 0.9])
with col1:
    if st.button("➕"):
        st.session_state.show_options = not st.session_state.show_options

with col2:
    prompt = st.chat_input("Enter News Topic or URL...")

# --- Chat Logic ---
if prompt:
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display a temporary assistant response with status
    with st.chat_message("assistant"):
        with st.status("Analyzing news...", expanded=True) as status:
            st.write("Fetching latest information...")
            st.write("Analyzing content and sources...")
            st.write("Generating summary...")
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        response = f"Analysis for '{prompt}' is complete. Back-end result will be shown here."
        st.markdown(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})