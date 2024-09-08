import streamlit as st
import whisper
import tempfile
import os

st.title("Speech to Text Transcription App")

# Upload audio file with Streamlit
audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "mp4", "m4a"])

# Language selection dropdown
language_options = [
    "English", "Spanish", "French", "German", "Chinese", "Hindi", "Japanese",
    "Russian", "Korean", "Portuguese", "Arabic", "Bengali"
]
language_code = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de", "Chinese": "zh",
    "Hindi": "hi", "Japanese": "ja", "Russian": "ru", "Korean": "ko",
    "Portuguese": "pt", "Arabic": "ar", "Bengali": "bn"
}
selected_language = st.sidebar.selectbox("Choose the transcription language", language_options)

model = whisper.load_model("small")
st.text("Model Loaded Successfully")

if st.sidebar.button("Transcribe Audio"):
    if audio_file is not None:
        st.sidebar.success("Transcribing Audio")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(audio_file.read())
            temp_file_path = temp_file.name
        
        # Transcribe the temporary file in the selected language
        transcription = model.transcribe(temp_file_path, language=language_code[selected_language])
        
        # Clean up the temporary file
        os.remove(temp_file_path)
        
        st.sidebar.success("Transcription Complete")
        st.markdown(transcription["text"])
        
        # Allow download of the transcript as a text file
        st.sidebar.header("Download Transcript")
        st.download_button(
            label="Download Transcript",
            data=transcription["text"],
            file_name="transcript.txt",
            mime="text/plain"
        )
    else:
        st.sidebar.error("Please upload a file")

# Play original audio file
if audio_file is not None:
    st.sidebar.header("Play Original Audio File")
    st.sidebar.audio(audio_file)
