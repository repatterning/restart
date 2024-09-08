"""Module interface.py"""
import logging

import src.data.depositories
import src.data.metadata
import src.data.points
import src.elements.s3_parameters as s3p
import src.elements.sequence as sq
import src.elements.service as sr
import src.s3.ingress


class Interface:
    """
    Class Interface
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, sequences: list[sq.Sequence]):
        """

        :param service:
        :param s3_parameters: The S3 parameters settings for this project
        :param sequences: Each list item is the detail of a sequence, in collection form.
        """

        self.__service = service
        self.__s3_parameters = s3_parameters
        self.__sequences = sequences

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __transfer(self, storage: str) -> list[str]:
        """
        Transfers data to Amazon S3 (Simple Storage Service)

        :param storage: The temporary local storage area of the retrieved data
        :return:
        """

        # Metadata
        metadata = src.data.metadata.Metadata().points()

        # Transfer
        messages: list[str] = src.s3.ingress.Ingress(service=self.__service, bucket_name=self.__s3_parameters.internal,
                                                     metadata=metadata).exc(path=storage)

        return messages

    def exc(self, storage: str):
        """

        :param storage: The temporary local storage area for the retrieved data
        :return:
        """

        # Prepare storage area
        src.data.depositories.Depositories(
            sequences=self.__sequences, storage=storage).exc()

        # Retrieve data per date, but for several stations & pollutants in parallel
        points = src.data.points.Points(sequences=self.__sequences, storage=storage)
        messages = points.exc()
        self.__logger.info(msg=messages)

        # Transfer
        messages = self.__transfer(storage=storage)
        self.__logger.info(messages)
