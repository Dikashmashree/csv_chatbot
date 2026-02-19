import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Book Chatbot",
    page_icon="",
    layout="centered"
)

st.title("Book Chatbot")
st.caption("Ask me anything about books — authors, ratings, genres, and more.")


def render_response(data: dict):
    response_text = data.get("response") or ""
    metadata = data.get("metadata") or []

    # to handle completely empty respons
    if not response_text and not metadata:
        st.warning("No results found for your query. Try rephrasing.")
        return

    # PRIMARY: Structured json
    st.markdown("**Structured Output**")
    st.json({
        "response": response_text,
        "metadata": metadata
    })

    # SECONDARY: human language answer (only if non-empty)
    if response_text.strip():
        with st.expander("View natural language response"):
            st.markdown(response_text)

    # TERTIARY:Book cards(only if results exist)
    if metadata:
        with st.expander(f"View {len(metadata)} book card(s)"):
            for i, book in enumerate(metadata, 1):
                st.markdown(f"**{i}. {book.get('title', 'Unknown Title')}**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"- **Author:** {book.get('authors', 'N/A')}")
                    st.markdown(f"- **Rating:** {book.get('average_rating', 'N/A')}")
                    st.markdown(f"- **Pages:** {book.get('num_pages', 'N/A')}")
                with col2:
                    st.markdown(f"- **Year:** {book.get('published_year', 'N/A')}")
                    st.markdown(f"- **Categories:** {book.get('categories', 'N/A')}")
                    st.markdown(f"- **Ratings Count:** {book.get('ratings_count', 'N/A')}")
                st.divider()

# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_response(msg["data"])
        else:
            st.markdown(msg["content"])

# CHAT I/p
if prompt := st.chat_input("Ask about a book or author..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching books..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    render_response(data)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "data": data
                    })

                else:
                    try:
                        err = response.json()
                    except Exception:
                        err = {"error": response.text}
                    st.error(f"API Error {response.status_code}")
                    st.json(err)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API. Make sure FastAPI is running:\n\n`uvicorn api.main:app --reload`")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The model may be slow — try again.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")