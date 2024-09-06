"""
Module dates.py
"""
import logging

import pandas as pd

import config


class Dates:
    """
    Class Dates

    This class calculates the list of dates for which data is required.
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

        # logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self) -> list[str]:
        """

        :return:
            A series of dates wherein each date is the date of the first day of a month.
        """

        #  The dates
        values = pd.date_range(start=self.__configurations.starting, end=self.__configurations.ending, freq='MS').to_list()
        datestr_ = [str(value.date()) for value in values]
        self.__logger.info('Dates\n%s', datestr_)

        return datestr_
