"""Module rating.py"""
import logging

import src.functions.objects


class Rating:
    """
    <b>Notes</b><br>
    ------<br>

    The types of quality ratings of a measurement.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__url = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices'
                      '&request=getQualityCodes&datasource=0&format=json')

    def exc(self):
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        rating = objects.api(url=self.__url)
        logging.info('RATING:\n%s', rating)
