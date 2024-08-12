import streamlit as st
import pandas as pd
from datetime import datetime

# Load the CSV file
data = pd.read_csv('trending_news_.csv')

# Convert 'created_at' to datetime format
data['created_at'] = pd.to_datetime(data['created_at'], format='%d-%m-%Y %H:%M')

# Extract all unique categories from the entire dataset
categories = data['category_names'].apply(lambda x: x.split(','))
unique_categories = set([cat.strip() for sublist in categories for cat in sublist])

def show_home_page():
    st.markdown("<h1 style='text-align: center; color: #ff6347;'>WELCOME TO GANIT NEWSPAPER</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Today's Date: {datetime.now().strftime('%B %d, %Y')}</h3>", unsafe_allow_html=True)
    
    # Red strip with app download message
    st.markdown(
        """
        <div style="background-color: #FF6347; color: white; padding: 10px; text-align: center; margin-bottom: 20px;">
            For the best experience, download the app
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Create three columns
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        for i, row in enumerate(data.iloc[:2].itertuples(), start=1):  # First 2 news items
            st.markdown(
                f"""
                <div style="border: 2px solid #0066cc; border-radius: 10px; padding: 10px; margin-bottom: 20px;">
                    <h4>News {i}</h4>
                    <img src="{row.image_url}" style="width: 100%; border-radius: 10px;"/>
                    <p style="font-size: 12px;">{row.content}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

    with col2:
        selected_item = st.selectbox("Choose a category:", sorted(unique_categories))
        if st.button("Submit"):
            st.session_state.selected_item = selected_item
            st.session_state.page = 'next_page'
        
        # Display the 3rd news item in the center column
        if len(data) > 2:
            st.markdown(
                f"""
                <div style="border: 2px solid #009933; border-radius: 10px; padding: 10px; margin-bottom: 20px;">
                    <h4>News 3</h4>
                    <img src="{data.iloc[2].image_url}" style="width: 100%; border-radius: 10px;"/>
                    <p style="font-size: 12px;">{data.iloc[2].content}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

    with col3:
        for i, row in enumerate(data.iloc[3:5].itertuples(), start=4):  # Remaining news items
            st.markdown(
                f"""
                <div style="border: 2px solid #ff6600; border-radius: 10px; padding: 10px; margin-bottom: 20px;">
                    <h4>News {i}</h4>
                    <img src="{row.image_url}" style="width: 100%; border-radius: 10px;"/>
                    <p style="font-size: 12px;">{row.content}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

def show_next_page():
    st.title("Next Page")
    st.write(f"You selected: {st.session_state.selected_item}")

    # Filter the entire data to get all rows that match the selected category
    selected_rows = data[data['category_names'].apply(lambda x: st.session_state.selected_item in [cat.strip() for cat in x.split(',')])]

    # Display each row's content with title, author, date, and a "Read more" link
    for _, row in selected_rows.iterrows():
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <img src="{row['image_url']}" style="width: 100%; border-radius: 10px;"/>
                <h2 style="margin-top: 20px;">{row['title']}</h2>
                <p><strong>Author:</strong> {row['author_name']} | <strong>Date:</strong> {row['created_at'].strftime('%B %d, %Y %H:%M')}</p>
                <p>{row['content']}</p>
                <p><a href="{row['source_url']}" target="_blank" style="color: #0066cc;">Read more</a></p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    if st.button("Back to Home"):
        st.session_state.page = 'home'

# Initialize session state if it does not exist
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Render the appropriate page based on session state
if st.session_state.page == 'home':
    show_home_page()
elif st.session_state.page == 'next_page':
    show_next_page()
