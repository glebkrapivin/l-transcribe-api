from google.api_core import operation, exceptions
from google.cloud import speech_v1p1beta1 as speech
from google.longrunning import operations_pb2
import logging


# API and auth not straighforward
# GOOGLE_APPLICATION_CREDENTIALS needs to be exported with key to the service account
client = speech.SpeechClient()

def _get_lightweight_operation(name: str) -> operations_pb2.Operation:
    # seems like a lazy init
    _ = client.transport.operations_client
    logging.info('%s', type(name))
    lightweight_operation: operations_pb2.Operation = client.transport._operations_client.get_operation(name)
    return lightweight_operation


def get_transcript_result(name: str) -> speech.LongRunningRecognizeResponse:
    # TODO: there is NO decent exception handling
    lightweight_operation = _get_lightweight_operation(name)
    response: operation.Operation = operation.from_gapic(
        lightweight_operation,
        client.transport._operations_client,
        speech.types.LongRunningRecognizeResponse,
        metadata_type=speech.types.LongRunningRecognizeMetadata,
    )
    return response.result()

def get_transcript_status(name: str) -> bool:

    lightweight_operation = _get_lightweight_operation(name)
    return lightweight_operation.done
