import pandas as pd
import streamlit as st
import numpy as np
import sklearn as sk
import pickle

# Define custom CSS for the book recommendation page
custom_css = """
<style>
    /* Body styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f0f0;
        margin: 0;
        padding: 0;
    }

    /* Header styling */
    .header {
        background-color: #333;
        color: #fff;
        padding: 20px;
        text-align: center;
    }

    /* Page container */
    .container {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }

    /* Book card styling */
    .book-card {
        border: 1px solid #ddd;
        padding: 10px;
        margin: 10px 0;
        background-color: #fff;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-radius: 4px;
    }

    /* Book image */
    .book-image {
        max-width: 100%;
        height: auto;
    }

    /* Book title */
    .book-title {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }

    /* Book author */
    .book-author {
        font-size: 16px;
        color: #555;
    }

    /* Book description */
    .book-description {
        font-size: 16px;
        margin-top: 10px;
    }

</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Rest of your Streamlit app content goes here


with open('cosine_similarity.pkl', 'rb') as file:
    similarity_scores = pickle.load(file)

pt=pd.read_csv('pt.csv',index_col='title')
    # You can add various elements like text, data, charts, and widgets here.
    # Load cosine similarity and data back from the pickle file

books=pd.read_csv("New_book.csv")

# Define the main page content
def main():
    st.title("Book Recommendation")
    
    st.write("Based on your Favourite book we have recommended you might like.")
    # Load cosine similarity and data back from the pickle file
    suggestions=pt.index
    selected_book = st.sidebar.selectbox("Select a Book:", suggestions, help="Start typing to get suggestions.")
    list_b=[5,10,15,20,30,50,70]
    r_number=st.sidebar.selectbox("Numbers of Recommendations:",list_b , help="Start typing to get suggestions.")
    if selected_book:
        st.write("You selected:", selected_book)

    # Load cosine similarity and data back from the pickle file
    return selected_book, r_number

# Run the main function to start the Streamlit app
if __name__ == "__main__":
    selected_book, r_number=main()




def recommend(book_name,numbers):
    # fetch index
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key = lambda x:x[1] , reverse = True)[1:numbers+1]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['author'].values))
        item.extend(list(temp_df.drop_duplicates('title')['year'].values))
        item.extend(list(temp_df.drop_duplicates('title')['publisher'].values))
        item.extend(list(temp_df.drop_duplicates('title')['img_url_l'].values))
        data.append(item)
    return data
      #  print(pt.index[i[0]])
    
def list_book(book_data):
    for book in book_data:
        title, author, year, publisher, l_url = book

    # Display book title, author, and an image
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(l_url, use_column_width=True)
        with col2:
            st.subheader(title)
            st.write(f"Author: {author}")
            st.write(f'Publisher Name: ',publisher)
            st.write(f'Publisher Year: ',year)

    # Display larger image on click
        if st.button("Show Larger Image", key=title):
            st.image(l_url, use_column_width=True, caption=title)

        st.write("\n---\n")  # Add a horizontal line between books

if st.sidebar.button("Recommend Books"):
    
    list_book(recommend(selected_book,r_number ))
else:
    st.sidebar.write("Click on Recommend book to get the best book for yourself.")