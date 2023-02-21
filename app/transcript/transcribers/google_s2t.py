import logging

from google.api_core import operation
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
from google.longrunning import operations_pb2

# API and auth not straighforward
# GOOGLE_APPLICATION_CREDENTIALS needs to be exported with key to the service account
client = speech.SpeechClient()
storage_client = storage.Client()


def _get_lightweight_operation(name: str) -> operation.Operation:
    # seems like a lazy init
    _ = client.transport.operations_client
    logging.info('%s', type(name))
    lightweight_operation: operations_pb2.Operation = client.transport._operations_client.get_operation(name)
    return lightweight_operation


def get_transcript_result(name: str) -> (speech.LongRunningRecognizeResponse, str):
    # TODO: there is NO decent exception handling
    lightweight_operation = _get_lightweight_operation(name)
    response: operation.Operation = operation.from_gapic(
        lightweight_operation,
        client.transport._operations_client,
        speech.types.LongRunningRecognizeResponse,
        metadata_type=speech.types.LongRunningRecognizeMetadata,
    )
    uri = None
    if response.metadata:
        uri = response.metadata.uri
    return response.result(), uri


def get_transcript_status(name: str) -> bool:
    lightweight_operation = _get_lightweight_operation(name)
    return lightweight_operation.done


def upload_audio(audio_location, bucket_name) -> str:
    bucket = storage_client.bucket(bucket_name)
    dest_name = audio_location.split('/')[-1]
    blob = bucket.blob(dest_name + '.mp3')
    logging.info('Uploading file from %s', audio_location)
    blob.upload_from_filename(audio_location)
    s3_audio_location = "gs://leela_bucket/" + dest_name + '.mp3'
    logging.info('Finished file upload to %s', s3_audio_location)
    return s3_audio_location


def delete_audio(s3_audio_location: str, bucket_name: str):
    bucket = storage_client.bucket(bucket_name=bucket_name)
    filename = s3_audio_location.split('/')[-1]
    blob = bucket.blob(filename)
    blob.delete()
    logging.info('Deleted file from bucket=%s and name=%s', bucket_name, filename)


def create_transcript_request(config: str, audio_location: str) -> str:
    request_config: speech.RecognitionConfig = speech.RecognitionConfig.from_json(config)  # type: ignore
    # TODO: bucket name to env variables
    s3_audio_location = upload_audio(audio_location, "leela_bucket")
    audio = speech.RecognitionAudio(uri=s3_audio_location)
    ops = client.long_running_recognize(audio=audio, config=request_config)
    name = ops._operation.name
    logging.info('Submited task to google s2t with name %s', name)
    return name


def try_delete_transcript_request(name: str):
    try:
        lightweight_operation = _get_lightweight_operation(name)
        response: operation.Operation = operation.from_gapic(
        lightweight_operation,
        client.transport._operations_client,
        speech.types.LongRunningRecognizeResponse,
        metadata_type=speech.types.LongRunningRecognizeMetadata,
        )
        response.cancel()
        logging.info('Deleted transcript request with name %s', name)
    except Exception as e:
        logging.exception(str(e))