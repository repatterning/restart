"""Module interface.py"""
import logging
import pandas as pd

import config
import src.data.assets
import src.data.codes
import src.data.partitions
import src.data.points
import src.data.rating
import src.data.stations
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

    @staticmethod
    def __on_river(assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return: Only stations located on a river.
        """

        return assets.loc[assets['on_river'], :]

    def __span(self, assets: pd.DataFrame) -> pd.DataFrame:
        """

        :param assets:
        :return:
        """

        conditionals = (assets['from'] <= self.__configurations.starting) & (assets['to'] >= self.__configurations.at_least)
        assets = assets.loc[conditionals, :]
        assets.info()

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
        assets = self.__span(assets=assets.copy())
        assets = self.__on_river(assets=assets.copy())

        # Rating
        src.data.rating.Rating().exc()

        # Partitions for parallel data retrieval; for parallel computing.
        partitions = src.data.partitions.Partitions(data=assets).exc()
        logging.info(partitions)

        # Retrieving time series points
        src.data.points.Points().exc(partitions=partitions)
