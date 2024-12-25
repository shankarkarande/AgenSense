import streamlit as st
import requests
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Constants for API keys and Agent ID
API_KEY = "sk_a795c6415910cba245152e48594dbbe4c7628a0142abaa66"
AGENT_ID = "fhrEpLIzbqKrKQLZIXL1"

client = ElevenLabs(api_key=API_KEY)

# Global variable for the conversation
conversation = None

def start_conversation():
    global conversation
    conversation = Conversation(
        client,
        AGENT_ID,
        requires_auth=bool(API_KEY),
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=lambda response: st.write(f"**Agent:** {response}"),
        callback_agent_response_correction=lambda original, corrected: st.write(f"**Agent:** {original} -> {corrected}"),
        callback_user_transcript=lambda transcript: st.write(f"**User:** {transcript}"),
    )
    conversation.start_session()

# Function to fetch all conversations
def get_conversations():
    url = "https://api.elevenlabs.io/v1/convai/conversations"
    querystring = {"agent_id": AGENT_ID}
    headers = {"xi-api-key": API_KEY}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict) and "conversations" in data:
            conversation_ids = [conversation["conversation_id"] for conversation in data["conversations"]]
            return conversation_ids
        else:
            return []
    else:
        return []

# Function to fetch and return conversation audio file
def get_audio(conversation_id):
    url = f"https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/audio"
    headers = {"xi-api-key": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        audio_data = response.content
        audio_file_path = f"{conversation_id}_audio.mp3"
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(audio_data)
        return audio_file_path
    else:
        return None

# Function to delete a conversation
def delete_conversation(conversation_id):
    url = f"https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}"
    headers = {"xi-api-key": API_KEY}

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return "Conversation deleted successfully."
    else:
        return "Failed to delete the conversation."
    
def get_messages(conversation_id):
    url = f"https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}"
    headers = {"xi-api-key": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "transcript" in data:
            return [message["message"] for message in data["transcript"]]
        else:
            return ["No messages found in this conversation."]
    else:
        return ["Failed to fetch messages."]

# Streamlit UI
def main():
    st.set_page_config(page_title="Agensense - Your Comsense AI Agent", page_icon="🤖", layout="centered")
    st.markdown("""
        <div style="text-align: center;">
            <span style="font-size: 5em;">🤖</span>
            <br><br>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <h1 style="text-align: center; font-size: 3em;">🌟 Welcome to Agensense 🌟</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <p style="text-align: center; font-size: 1.2em;">
        Agensense is here to help you explore Comsense Technologies with ease and efficiency.
        </p>
    """, unsafe_allow_html=True)

    # Dropdown for selecting services
    services = [
        "Select a service", 
        "Start the Agensense", 
        "Get Conversations History", 
        "Get Conversation Audio", 
        "Delete Conversation", 
        "Twillo Configuration", 
        "Send Email", 
        "Schedule Meeting", 
        "Translation"
    ]
    selected_service = st.selectbox("Choose a Service:", services)

    if selected_service == "Start the Agensense":
        st.button("Start Agensense", on_click=start_conversation)
        start_conversation()
        st.write("**Agent has been started**")

    elif selected_service == "Get Conversations History":
        # Fetch conversations only when the service is selected
        conversation_ids = get_conversations()

        if conversation_ids:
            selected_conversation_id = st.selectbox("Select a Conversation ID:", conversation_ids)

            if selected_conversation_id:
                # Display messages immediately after selecting a conversation_id
                messages = get_messages(selected_conversation_id)
                st.markdown(f"### Messages for Conversation ID: {selected_conversation_id}")
                for message in messages:
                    st.write(f"- {message}")
        else:
            st.write("No conversations found!")

    elif selected_service == "Get Conversation Audio":
        conversation_ids = get_conversations()

        if conversation_ids:
            selected_conversation_id = st.selectbox("Select a Conversation ID for Audio:", conversation_ids)

            if selected_conversation_id:
                audio_file_path = get_audio(selected_conversation_id)

                if audio_file_path:
                    st.audio(audio_file_path, format="audio/mp3")
                else:
                    st.error("Failed to retrieve audio. Please try again.")
        else:
            st.write("No conversations found!")

    elif selected_service == "Delete Conversation":
        conversation_ids = get_conversations()

        if conversation_ids:
            selected_conversation_id = st.selectbox("Select a Conversation ID to Delete:", conversation_ids)

            if st.button("Delete Conversation"):
                if selected_conversation_id:
                    result = delete_conversation(selected_conversation_id)
                    st.success(result)
                else:
                    st.error("No Conversation ID selected.")
        else:
            st.write("No conversations found!")

    elif selected_service == "Twillo Configuration":
        st.write("Coming Soon...")

    elif selected_service == "Send Email":
        st.write("Coming Soon...")

    elif selected_service == "Schedule Meeting":
        st.write("Coming Soon...")

    elif selected_service == "Translation":
        st.write("Coming Soon...")

if __name__ == "__main__":
    main()
