# Check
import pandas as pd 
import numpy as np
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Caching data loading functions to optimize performance
@st.cache_data
def load_cleaned_data(file_path):
    return pd.read_csv(file_path)

@st.cache_data
def load_encoded_data(file_path):
    return joblib.load(file_path, mmap_mode='r')

# Caching K-Means clustering to avoid recomputation
@st.cache_data
def kmeans_clustering(encoded_data, n_clusters=5):
    # Select only numeric columns for clustering
    numeric_data = encoded_data.select_dtypes(include=[np.number])

    # Scale the data before clustering
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_data)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    encoded_data['Cluster'] = kmeans.fit_predict(scaled_data)

    return encoded_data, kmeans

# Caching merge function to avoid recomputing merge each time
@st.cache_data
def merge_data(cleaned_data, encoded_data_with_clusters):
    return pd.merge(cleaned_data, encoded_data_with_clusters[['Cluster', 'name']], on='name', how='left')

# Load cleaned data and encoded data
cleaned_data = load_cleaned_data(r'D:\APS\cleaned_data.csv')
encoded_data = load_encoded_data(r'D:\APS\encoded_data.joblib')

# Perform K-Means clustering
encoded_data_with_clusters, kmeans_model = kmeans_clustering(encoded_data, n_clusters=5)

# Merge cleaned data with encoded data (clusters)
merged_data = merge_data(cleaned_data, encoded_data_with_clusters)

# Streamlit App
st.title("Swiggy Restaurant Recommendations")

# Page Selection
page = st.sidebar.radio("Select a page", ("Top 5 Recommendations", "User Input Filters"))

# Page 1: Top 5 Recommendations Based on City
if page == "Top 5 Recommendations":
    st.subheader("Top 5 Recommended Restaurants by City")

    # Dropdown to select a city
    selected_city = st.selectbox("Choose a City", merged_data['city'].unique())

    # Filter by selected city and sort by rating and rating_count
    top_5_city = (
        merged_data[merged_data['city'] == selected_city]
        .sort_values(by=['rating', 'rating_count'], ascending=[False, False])
        .head(5)
    )

    # Show top 5 recommendations
    st.write(top_5_city[['name', 'city', 'cuisine', 'rating', 'cost']])

    # Toggle to select pie chart type
    pie_option = st.radio("Show pie chart for:", ("Cuisine", "Cluster"))

    st.subheader(f"{pie_option} Distribution in Top 5")

    if pie_option == "Cuisine":
        pie_data = top_5_city['cuisine'].value_counts()
    else:
        pie_data = top_5_city['Cluster'].value_counts()

    # Plot pie chart
    st.pyplot(
        pie_data.plot.pie(
            autopct='%1.1f%%',
            figsize=(5, 5),
            title=f"Top 5 {pie_option} Breakdown"
        ).figure
    )

    # Scatter plot for clusters
    st.subheader("Cluster Distribution")

    # Scatter plot of the first two principal components or features
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=encoded_data_with_clusters, x='feature1', y='feature2', hue='Cluster', palette='Set1', s=100)
    plt.title('Clusters of Restaurants')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    st.pyplot()

    if st.checkbox('Show full data'):
        st.write(merged_data)


# Page 2: User Input Filters
elif page == "User Input Filters":
    st.subheader("Filter Restaurants Based on Your Preferences")

    # City Filter
    city = st.selectbox('Select City', merged_data['city'].unique())

    # Cuisine Filter
    cuisine = st.selectbox('Select Cuisine', merged_data['cuisine'].unique())

    # Rating Filter
    rating = st.slider('Select Rating Range', 1.0, 5.0, (1.0, 5.0), step=0.5)

    # Cost Filter (step by 200, max 300350)
    cost = st.slider('Select Cost Range', 0, 300350, (0, 300350), step=200)

    # Rating Count Filter (step by 500, max 10000)
    rating_count = st.slider('Select Rating Count Range', 0, 10000, (0, 10000), step=500)

    # Apply filters
    filtered_data = merged_data[ 
        (merged_data['city'] == city) & 
        (merged_data['cuisine'].str.contains(cuisine, case=False)) & 
        (merged_data['rating'] >= rating[0]) & (merged_data['rating'] <= rating[1]) & 
        (merged_data['cost'] >= cost[0]) & (merged_data['cost'] <= cost[1]) & 
        (merged_data['rating_count'] >= rating_count[0]) & (merged_data['rating_count'] <= rating_count[1]) 
    ]

    st.write(filtered_data)
