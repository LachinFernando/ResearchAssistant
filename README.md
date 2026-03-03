# ResearchAssistant
This is the main repo for teacher assistant chatbot


## How to run the app (Local)
1. Clone the repo
2. Install the requirements
3. Create *.streamlit/secrets.toml* file and add the following
    [llm]
    OPENAI_API_KEY = "your_openai_api_key"
    
    [admin]
    PASSWORD = "your_password"

4. Run the app
    streamlit run LogIn.py

## How to run the app (Online)
1. Create a repo and push the code to GitHub 
2. Create a Streamlit account
3. Create a Streamlit app
4. Deploy the app to Streamlit
5. Go to Manage App > Secrets
    then add the following
        [llm]
        OPENAI_API_KEY = "your_openai_api_key"
        
        [admin]
        PASSWORD = "your_password"
6. Then run the app

