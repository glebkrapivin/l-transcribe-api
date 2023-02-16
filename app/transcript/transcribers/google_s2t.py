# Import the Speech-to-Text client library
from google.cloud import speech

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
gcs_uri = "gs://leela_bucket/transcripts/3_min_rec.mp3"

def transcribe_speech():
  audio = speech.RecognitionAudio(uri=gcs_uri)

  config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=44100,
    language_code="es-ES",
    model="phone_call",
    audio_channel_count=2,
    enable_word_confidence=True,
    use_enhanced=True,
    enable_word_time_offsets=True,
    max_alternatives=4,
    diarization_config=speech.SpeakerDiarizationConfig(
      enable_speaker_diarization=True,
      min_speaker_count=2,
      max_speaker_count=2,
    ),
  )

  # Detects speech in the audio file
  operation = client.long_running_recognize(config=config, audio=audio)

  print("Waiting for operation to complete...")
  response = operation.result(timeout=90)

  for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))

transcribe_speech()