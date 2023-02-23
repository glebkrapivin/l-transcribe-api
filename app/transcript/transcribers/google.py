import logging
from typing import Union

from google.api_core import operation
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
from google.longrunning import operations_pb2

from app.transcript.transcribers.base import BaseTranscriber, TranscriptDto, WordDto


# API and auth not straighforward
# GOOGLE_APPLICATION_CREDENTIALS needs to be exported with key to the service account


class GoogleTranscriber(BaseTranscriber):
    def __init__(self, **kwargs):
        self.client = speech.SpeechClient(**kwargs)
        self.storage_client = storage.Client(**kwargs)

    def create(self, config: str, audio_location: str) -> str:
        request_config: speech.RecognitionConfig = speech.RecognitionConfig.from_json(config)  # type: ignore
        # TODO: bucket name to env variables
        s3_audio_location = self._upload_audio(audio_location, "leela_bucket")
        audio = speech.RecognitionAudio(uri=s3_audio_location)
        ops = self.client.long_running_recognize(audio=audio, config=request_config)
        name = ops._operation.name
        logging.info('Submited task to google s2t with name %s', name)
        return name

    def _get_lightweight_operation(self, name: str) -> operations_pb2.Operation:
        # seems like a lazy init
        _ = self.client.transport.operations_client
        logging.info('%s', type(name))
        lightweight_operation: operations_pb2.Operation = self.client.transport._operations_client.get_operation(name)
        return lightweight_operation

    def get(self, ext_transcript_id: Union[str, int]) -> TranscriptDto:
        # TODO: there is NO decent exception handling
        lightweight_operation = self._get_lightweight_operation(ext_transcript_id)
        response: operation.Operation = operation.from_gapic(
            lightweight_operation,
            self.client.transport._operations_client,
            speech.types.LongRunningRecognizeResponse,
            metadata_type=speech.types.LongRunningRecognizeMetadata,
        )
        result: speech.types.LongRunningRecognizeResponse = response.result()
        tdto = TranscriptDto(external_id=ext_transcript_id, metadata=response.metadata.__dict__,
                             is_ready=response.done())
        if not response.done():
            return tdto
        words_raw = result.results[-1].alternatives[0].words
        words = []
        for word in words_raw:
            start_at = word.start_time.total_seconds() * 1000
            stop_at = word.end_time.total_seconds() * 1000
            text = word.word
            speaker_tag = word.speaker_tag
            words.append(WordDto(speaker_tag=speaker_tag,
                                 start_at=start_at, end_at=stop_at, word=text))
        tdto.words = words

        try:
            uri = response.metadata.uri
            self._delete_audio(uri, "leela_bucket")
        except:
            uri = "null"
            logging.exception('Failed to delete audio from s3 bucket %s', uri)
        return tdto

    def is_ready(self, ext_transcript_id: Union[str, int]) -> bool:
        return self._get_lightweight_operation(ext_transcript_id).done

    def _upload_audio(self, audio_location, bucket_name) -> str:
        bucket = self.storage_client.bucket(bucket_name)
        dest_name = audio_location.split('/')[-1]
        blob = bucket.blob(dest_name + '.mp3')
        logging.info('Uploading file from %s', audio_location)
        blob.upload_from_filename(audio_location)
        s3_audio_location = "gs://leela_bucket/" + dest_name + '.mp3'
        logging.info('Finished file upload to %s', s3_audio_location)
        return s3_audio_location

    def _delete_audio(self, s3_audio_location: str, bucket_name: str):
        bucket = self.storage_client.bucket(bucket_name=bucket_name)
        filename = s3_audio_location.split('/')[-1]
        blob = bucket.blob(filename)
        blob.delete()
        logging.info('Deleted file from bucket=%s and name=%s', bucket_name, filename)

    def delete(self, ext_transcript_id: Union[str, int]):
        # TODO:
        #   - try to delete audio from S3 bucket as well
        try:
            lightweight_operation = self._get_lightweight_operation(ext_transcript_id)
            response: operation.Operation = operation.from_gapic(
                lightweight_operation,
                self.client.transport._operations_client,
                speech.types.LongRunningRecognizeResponse,
                metadata_type=speech.types.LongRunningRecognizeMetadata,
            )
            response.cancel()
            logging.info('Deleted transcript request with name %s', ext_transcript_id)
        except Exception as e:
            logging.exception(str(e))
