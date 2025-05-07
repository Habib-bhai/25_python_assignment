import re
import string
import random
from graph import Graph, Vertex
import streamlit as st
from io import StringIO

def get_words_from_text(text):
    # Process text input
    text = re.sub(r'\[(.+)\]', ' ', text)
    text = ' '.join(text.split())
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    return words

def make_graph(words):
    g = Graph()
    prev_word = None
    for word in words:
        word_vertex = g.get_vertex(word)
        if prev_word:
            prev_word.increment_edge(word_vertex)
        prev_word = word_vertex
    g.generate_probability_mappings()
    return g

def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)
    return composition

def main():
    st.title("🎵 Markov Graph Text Composer")
    st.write("Generate text using a Markov Chain based on your input file or custom text!")

    # File upload section
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    user_text = st.text_area("Or enter your text here:", placeholder="Type or paste your text here...")

    length = st.slider("Generated Text Length", min_value=10, max_value=500, value=100, step=10)

    if st.button("Compose Text"):
        if uploaded_file:
            text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        elif user_text:
            text = user_text
        else:
            st.error("Please provide a text file or enter text in the field.")
            return

        # Process the input text
        words = get_words_from_text(text)

        # Create the Markov graph
        g = make_graph(words)

        # Compose text
        composition = compose(g, words, length)

        # Display output
        st.subheader("Generated Composition")
        st.write(' '.join(composition))

if __name__ == '__main__':
    main()
