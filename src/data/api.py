"""Module api.py"""
import logging

import pandas as pd


class API:
    """
    Class API
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __pattern(self, sequence_id: int, datestr: str) -> str:
        """

        :param sequence_id: The identification code of an air pollutant sequence
        :param datestr: Date string 'YYYY-mm-dd'.
        :return:
        """

        ending = str(pd.date_range(start=datestr, periods=1, freq='ME').to_list()[0].date())

        string = f"""https://www.scottishairquality.scot/sos-scotland/api/v1/timeseries/{sequence_id}/getData?""" + \
                 f"""expanded=true&phenomenon=1&format=highcharts&timespan={datestr}T00:00:00Z/{ending}T23:59:59Z"""

        self.__logger.info(string)

        return string

    def exc(self, sequence_id: int, datestr: str) -> str:
        """

        :param sequence_id: The identification code of an air pollutant sequence
        :param datestr: Date string 'YYYY-mm-dd'.
        :return:
        """

        return self.__pattern(sequence_id=sequence_id, datestr=datestr)
