
# Import necessary libraries
import json
import streamlit as st
import requests
import pandas as pd
import numpy as np


# Define the URL of your Fast API

API_URL = "http://127.0.0.1:8000/predict/csv"


# Create the Streamlit app
def main():
    st.title('Music Genre Classification')
    st.write('Upload a CSV file containing vectorized data to classify its music genre:')

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file...", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file as a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the head of the uploaded data
        st.write('Head of Uploaded Data:')
        st.write(df.head())

        # Button to trigger prediction
        if st.button('Predict'):
            # Add a progress bar
            progress_bar = st.progress(0)

            # Function to make prediction using the API
            def make_prediction(input_data):
                # Send the request with JSON serializable data

                response = requests.request("POST", API_URL,files={"file" : uploaded_file.getvalue()})

                #response = requests.post(API_URL, json={'data': input_data})
                if response.status_code == 200:
                    return response.json()
                else:
                    return None

            # Make prediction using the API
            prediction = make_prediction(uploaded_file)

            # Update progress bar
            progress_bar.progress(100)

            # Create a DataFrame with prediction results
            if prediction:
                # Extract the list of predictions
                predictions_list = prediction['music_labels']

                prediction_df = pd.DataFrame({'prediction': predictions_list}, index=range(1, len(predictions_list) + 1))

                # Add an index to the DataFrame
                prediction_df.index = range(1, len(prediction_df) + 1)

                # Display the prediction results DataFrame
                st.write('Prediction Results:')
                st.table(prediction_df)  # Set the height and width for the prediction results DataFrame

if __name__ == '__main__':
    main()