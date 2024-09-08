"""Module interface.py"""

import pandas as pd

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.references.regenerate


class Interface:
    """
    Class Interface
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A collection of Amazon services
        :param s3_parameters: Amazon S3 parameters
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Sequences in focus
        self.__configurations = config.Config()

    def __excerpt(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        # Extract the records in focus.
        excerpt = blob.copy().loc[blob['sequence_id'].isin(self.__configurations.sequence_id_filter), :]

        return excerpt

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # Retrieve the raw references data from Scottish Air & European Environment Information and
        # Observation Network depositories.
        frame: pd.DataFrame = src.references.regenerate.Regenerate(
            service=self.__service, s3_parameters=self.__s3_parameters).exc()

        # Excerpt
        reference: pd.DataFrame = self.__excerpt(blob=frame)

        return reference
