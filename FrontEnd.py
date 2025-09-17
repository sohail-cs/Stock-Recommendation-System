import streamlit as st
import requests


#Title
st.title('Stock Recommendation System')

st.write('''
     Welcome to Stock Recommendation System! 
     where you will be asked a few questions, and a list of stocks based on your answers will be recommended.
     Please find the questions below:'''
)


#Get User's preferences
user_answers = {
    "user_exp": st.radio("What is your experience?", ("Beginner","Intermediate", "Advanced")),
    "user_cost": st.text_input("How Much are you planning to invest?"),
    "user_plan": st.radio("What is your Investment Plan?", ("Long Term", "Short Term")),
    "user_sector": st.radio("What is Sector do you want to invest in?", ("Technology", "Financial Services", "Healthcare", "Consumer Defensive", "Consumer Cyclical", "Energy")),
}

#Check if button is pressed
if st.button("Submit"):
    #Check if user filled all the required fields
    if len(user_answers["user_cost"]) == 0 or not user_answers["user_cost"].isdigit():
        st.write("Please fill all the required fields")
    else:
        #Server's url
        url = 'http://127.0.0.1:8000'

        try:
            #Send post request to server with user data as JSON object
            response = requests.post(url,json=user_answers)
            #If response is accepted by server
            if response.status_code == 200:
                #Display success message along with recommended stock data
                st.write("Connection Established")
                st.write("User Data:{0}".format(user_answers))
                st.write("RESPONSE FROM SERVER")
                st.write(response.json())

            #If response is error
            else:
            #Display error
             st.error(f"Error: {response.status_code}")
             st.write(response.text)
        except Exception as e:
            st.error("Failed to connect to the backend.")
            st.write(f"Error details: {e}")
