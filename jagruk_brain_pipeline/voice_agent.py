import asyncio
import io
import os
import re
from dotenv import load_dotenv
import edge_tts
from openai import OpenAI
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

# Path resolution for .env
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

def _detect_indic_voice(text: str) -> str:
    if re.search(r"[\u0980-\u09FF]", text):  # Bengali
        return "bn-IN-TanishaaNeural"
    elif re.search(r"[\u0900-\u097F]", text):  # Devanagari (Hindi/Marathi)
        return "hi-IN-SwaraNeural"
    elif re.search(r"[\u0A00-\u0A7F]", text):  # Gurmukhi (Punjabi)
        return "pa-IN-OjasNeural"
    elif re.search(r"[\u0B80-\u0BFF]", text):  # Tamil
        return "ta-IN-PallaviNeural"
    elif re.search(r"[\u0C00-\u0C7F]", text):  # Telugu
        return "te-IN-ShrutiNeural"
    elif re.search(r"[\u0A80-\u0AFF]", text):  # Gujarati
        return "gu-IN-DhwaniNeural"
    elif re.search(r"[\u0D00-\u0D7F]", text):  # Malayalam
        return "ml-IN-SobhanaNeural"
    elif re.search(r"[\u0C80-\u0CFF]", text):  # Kannada
        return "kn-IN-SapnaNeural"
    elif re.search(r"[\u0600-\u06FF]", text):  # Urdu
        return "ur-IN-GulNeural"
    return "en-IN-NeerjaNeural"

class PatchedTTSResponse:
    def __init__(self, content_bytes: bytes):
        self.content = content_bytes
        
    def read(self) -> bytes:
        return self.content

def patch_client_tts(client_instance):
    def patched_create(*args, **kwargs):
        text = kwargs.get("input", "") or (args[2] if len(args) > 2 else "")
        clean_text = re.sub(r"[*#_`>-]", "", str(text)).strip()
        clean_text = clean_text.replace("।", ".")
        
        if not clean_text:
            clean_text = "Yes"
            
        voice = _detect_indic_voice(clean_text)

        async def _generate_audio():
            communicate = edge_tts.Communicate(clean_text, voice)
            buffer = bytearray()
            async for chunk in communicate.stream():
                if chunk.get("type") == "audio":
                    buffer.extend(chunk["data"])
            return bytes(buffer)

        try:
            audio_bytes = asyncio.run(_generate_audio())
            if not audio_bytes:
                raise ValueError("Empty audio received")
        except Exception:
            communicate = edge_tts.Communicate(clean_text, "en-IN-NeerjaNeural")
            async def _fallback():
                buf = bytearray()
                async for c in communicate.stream():
                    if c.get("type") == "audio":
                        buf.extend(c["data"])
                return bytes(buf)
            audio_bytes = asyncio.run(_fallback())

        return PatchedTTSResponse(audio_bytes)

    client_instance.audio.speech.create = patched_create

patch_client_tts(client)

def listen_and_transcribe() -> str:
    """Listens to the microphone and returns the transcribed text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2

        print("Listening (Speak now)...")
        audio = r.listen(source)

        print("Processing audio (STT)...")
        try:
            stt = r.recognize_google(audio)
            print("You said:", stt)
            return stt
        except Exception as e:
            print("Could not understand audio:", e)
            return ""

def speak_response(text: str):
    """Takes text and converts it to speech output."""
    print("Synthesizing voice response...")
    
    # We rely on the patched client to intercept this and route it to edge_tts
    tts_response = client.audio.speech.create(
        model="canopylabs/orpheus-v1-english",
        voice="troy",
        input=text,
        response_format="wav",
    )

    audio_data = tts_response.read()
    audio_buffer = io.BytesIO(audio_data)
    
    # soundfile converts the bytes so sounddevice can play them
    data, samplerate = sf.read(audio_buffer)

    sd.play(data, samplerate)
    sd.wait()
    
    
 