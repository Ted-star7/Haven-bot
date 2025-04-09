import os
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# Set credentials
credentials = service_account.Credentials.from_service_account_file(
    "config/mindhaven-service-account.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Correct Parent Path
parent = "projects/mindhaven-schoolproject/locations/global/agent"

client = dialogflow.AgentsClient(credentials=credentials)

try:
    agent = client.get_agent(request={"parent": parent})
    print(f"✅ Agent Found: {agent.display_name}")
    
    intents_client = dialogflow.IntentsClient(credentials=credentials)
    
    intent = dialogflow.Intent(
        display_name="StressHelp",
        training_phrases=[
            dialogflow.Intent.TrainingPhrase(
                parts=[dialogflow.Intent.TrainingPhrase.Part(text="I'm feeling stressed")]
            )
        ],
        messages=[dialogflow.Intent.Message(text=dialogflow.Intent.Message.Text(text=["Try relaxing with deep breathing"]))]
    )
    
    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    print(f"🎉 Created Intent: {response.display_name}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
