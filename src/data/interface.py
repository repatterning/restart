"""Module interface.py"""
import logging
import os.path

import pandas as pd

import config
import src.data.assets
import src.data.codes
import src.data.partitions
import src.data.points
import src.data.rating
import src.data.stations
import src.functions.directories
import src.functions.streams


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # An instance for reading & writing CSV (comma separated values) data files.
        self.__streams = src.functions.streams.Streams()

        # the references directory
        directories = src.functions.directories.Directories()
        directories.create(path=self.__configurations.references_)

    def __persist(self, blob: pd.DataFrame, name: str) -> None:
        """

        :param blob:
        :param name:
        :return:
        """

        message = self.__streams.write(blob=blob, path=os.path.join(self.__configurations.references_, f'{name}.csv'))
        logging.info(message)

    def __span(self, assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return:
        """

        conditionals = (assets['from'] <= self.__configurations.starting) & (assets['to'] >= self.__configurations.at_least)
        assets = assets.loc[conditionals, :]

        return assets

    def __specific(self, assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return:
        """

        assets = assets.loc[assets['ts_id'].isin(self.__configurations.specific), :]

        return assets

    def exc(self):
        """

        :return:
        """

        # Retrieving the codes of <level> sequences.
        codes = src.data.codes.Codes().exc()

        # Stations that record <level> sequences.
        stations = src.data.stations.Stations().exc()

        # Hence, assets; joining codes & stations, subsequently limiting by stations
        # that were recording measures from a starting point of interest.
        assets = src.data.assets.Assets(codes=codes, stations=stations).exc()
        self.__persist(blob=assets, name='assets')

        # Rating
        rating = src.data.rating.Rating().exc()
        self.__persist(blob=rating, name='rating')

        # Partitions for parallel data retrieval; for parallel computing.
        assets = self.__span(assets=assets.copy())
        assets = self.__specific(assets=assets.copy())
        partitions = src.data.partitions.Partitions(data=assets).exc()
        logging.info(partitions)

        # Retrieving time series points
        src.data.points.Points().exc(partitions=partitions)
