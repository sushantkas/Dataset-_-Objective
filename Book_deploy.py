import pandas as pd
import streamlit as st
import numpy as np
import sklearn as sk
import pickle


with open('cosine_similarity.pkl', 'rb') as file:
    similarity_scores = pickle.load(file)

pt=pd.read_csv('pt.csv',index_col='title')
    # You can add various elements like text, data, charts, and widgets here.
    # Load cosine similarity and data back from the pickle file

books=pd.read_csv("New_book.csv")

# Define the main page content
def main():
    st.title("Book Recommendation")
    
    st.write("Welcome to my Streamlit web app.")
    # Load cosine similarity and data back from the pickle file
    suggestions=pt.index
    selected_book = st.sidebar.selectbox("Select a Book:", suggestions, help="Start typing to get suggestions.")
    if selected_book:
        st.write("You selected:", selected_book)

    # Load cosine similarity and data back from the pickle file
    return selected_book

# Run the main function to start the Streamlit app
if __name__ == "__main__":
    selected_book=main()




def recommend(book_name):
    # fetch index
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key = lambda x:x[1] , reverse = True)[1:6]
    
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
    
    list_book(recommend(selected_book))
else:
    st.sidebar.write("Click on Recommend book to get the best book for yourself.")