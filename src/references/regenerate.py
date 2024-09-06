"""
Module regenerate.py
"""

import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.references.metadata
import src.references.registry
import src.references.stations
import src.references.substances
import src.s3.upload


class Regenerate:
    """
    Notes upcoming.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Metadata
        self.__metadata = src.references.metadata.Metadata()

        # S3 Upload Instance
        self.__upload = src.s3.upload.Upload(service=self.__service, s3_parameters=self.__s3_parameters)

    def __registry(self) -> pd.DataFrame:
        """

        :return:
        """

        key_name: str = f'{self.__s3_parameters.path_internal_references}registry.csv'
        data: pd.DataFrame = src.references.registry.Registry().exc()
        self.__upload.bytes(data=data, metadata=self.__metadata.registry(), key_name=key_name)

        return data

    def __stations(self) -> pd.DataFrame:
        """

        :return:
        """

        key_name: str = f'{self.__s3_parameters.path_internal_references}stations.csv'
        data: pd.DataFrame = src.references.stations.Stations().exc()
        self.__upload.bytes(data=data, metadata=self.__metadata.stations(), key_name=key_name)

        return data

    def __substances(self) -> pd.DataFrame:
        """

        :return:
        """

        key_name: str = f'{self.__s3_parameters.path_internal_references}substances.csv'
        data: pd.DataFrame = src.references.substances.Substances().exc()
        self.__upload.bytes(data=data, metadata=self.__metadata.substances(), key_name=key_name)

        return data

    def __reference(self, registry: pd.DataFrame, stations: pd.DataFrame, substances: pd.DataFrame) -> pd.DataFrame:
        """
        Integrates the frames such that each record has the details of each distinct
        sequence identification code.

        :param registry: An inventory of sequence identification codes; a code is associated with a distinct device &
                         pollutant combination.
        :param stations: An inventory telemetry devices stations.
        :param substances: An inventory of pollutants.
        :return:
        """

        frame = registry.merge(stations, how='left', on='station_id')
        frame = frame.copy().merge(
            substances.copy()[['pollutant_id', 'substance', 'notation']], how='left', on='pollutant_id')
        frame = frame.copy()[list(self.__metadata.reference().keys())]

        key_name: str = f'{self.__s3_parameters.path_internal_references}reference.csv'
        self.__upload.bytes(data=frame, metadata=self.__metadata.reference(), key_name=key_name)

        return frame

    def exc(self) -> pd.DataFrame:
        """

        :return:
          The integration of registry, stations, substances
        """

        registry: pd.DataFrame = self.__registry()
        stations: pd.DataFrame = self.__stations()
        substances: pd.DataFrame = self.__substances()

        return self.__reference(
            registry=registry, stations=stations, substances=substances)
