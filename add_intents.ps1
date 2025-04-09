$env:GOOGLE_APPLICATION_CREDENTIALS = "config/mindhaven-service-account.json"

# Create a temporary Python script file
@'
import json
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

def main():
    try:
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file('config/mindhaven-service-account.json')
        client = dialogflow.IntentsClient(credentials=credentials)
        parent = 'projects/mindhaven-schoolproject/locations/global/agent'

        # Load intents
        with open('intents.json', 'r', encoding='utf-8') as f:
            intents = json.load(f)

        # Create each intent
        for intent_data in intents:
            try:
                # Prepare training phrases
                training_phrases = []
                for phrase in intent_data['trainingPhrases']:
                    training_phrases.append({
                        'parts': [{'text': part['text']} for part in phrase['parts']],
                        'type_': dialogflow.Intent.TrainingPhrase.Type.EXAMPLE
                    })
                
                # Create intent object
                intent = {
                    'display_name': intent_data['name'],
                    'training_phrases': training_phrases,
                    'messages': [{
                        'text': {
                            'text': intent_data['messages'][0]['text']['text']
                        }
                    }]
                }
                
                # Set priority if specified
                if 'priority' in intent_data and intent_data['priority'] == 'HIGH':
                    intent['priority'] = 500000  # High priority
                
                # Create the intent
                response = client.create_intent(
                    request={
                        'parent': parent,
                        'intent': intent
                    }
                )
                print('✅ Created intent: ' + response.display_name)
                
            except Exception as e:
                print('❌ Failed to create ' + intent_data["name"] + ': ' + str(e))
                
    except Exception as e:
        print('❌ Script failed: ' + str(e))

if __name__ == '__main__':
    main()
'@ | Out-File -FilePath "temp_script.py" -Encoding utf8

# Execute the Python script
python temp_script.py

# Clean up
Remove-Item temp_script.py -ErrorAction SilentlyContinue