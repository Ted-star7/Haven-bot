import os
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import GoogleAPICallError

# Load environment variables
load_dotenv()

class DialogflowManager:
    def __init__(self):
        # Get project ID with fallback
        self.project_id = os.getenv("DIALOGFLOW_PROJECT_ID", "mindhaven-schoolproject")
        location = 'global'  # Using 'global' location for Dialogflow agents
        self.parent = f"projects/{self.project_id}/locations/{location}/agent"
        
        print(f"\n🔍 Working with Project: {self.project_id}")
        print(f"🔧 Parent path: {self.parent}")
        
        # Verify service account access
        try:
            self.agents_client = dialogflow.AgentsClient()
            agent = self.agents_client.get_agent(request={"parent": self.parent})
            print(f"✅ Agent verified: {agent.display_name}")
        except Exception as e:
            print(f"❌ Agent verification failed. Please check:")
            print(f"1. Project ID is correct (currently: {self.project_id})")
            print(f"2. Agent exists in Dialogflow Console")
            print(f"3. Service account has 'Dialogflow API Admin' role")
            print(f"Full error: {str(e)}")
            raise

    def create_intent(self, display_name, training_phrases, message_text):
        try:
            # Format training phrases
            training_phrases_obj = [
                {"parts": [{"text": phrase}]} for phrase in training_phrases
            ]
            
            # Create intent
            intent = {
                "display_name": display_name,
                "training_phrases": training_phrases_obj,
                "messages": [{"text": {"text": [message_text]}}]
            }
            
            # Connect to API
            client = dialogflow.IntentsClient()
            response = client.create_intent(
                request={"parent": self.parent, "intent": intent}
            )
            print(f"\n🎉 Success! Created intent: {display_name}")
            print(f"🔗 View in Console: https://console.cloud.google.com/dialogflow/es/project/{self.project_id}/agent/intents")
            return response
        except GoogleAPICallError as e:
            print(f"\n❌ Failed to create intent: {e.message}")
            print("Possible solutions:")
            print("1. Wait 5 minutes after enabling API")
            print("2. Check credentials in Google Cloud IAM")
            print("3. Verify Dialogflow API is enabled")
            return None

if __name__ == "__main__":
    try:
        print("🚀 Starting Dialogflow Intent Creator...")
        manager = DialogflowManager()
        
        # Example intent
        manager.create_intent(
            display_name="StressHelp",
            training_phrases=[
                "I'm feeling stressed",
                "How to reduce anxiety?",
                "Stress management techniques"
            ],
            message_text="Try the 4-7-8 breathing method: Inhale 4 seconds, Hold 7 seconds, Exhale 8 seconds."
        )
        
    except Exception as e:
        print(f"\n💥 Critical Error: {str(e)}")
        print("Immediate actions:")
        print("1. Check .env file exists in your project folder")
        print("2. Verify service account JSON file path")
        print("3. Confirm project ID in Dialogflow Console")
