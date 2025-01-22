"""Module rating.py"""
import logging

import src.functions.objects


class Rating:
    """
    <b>Notes</b><br>
    ------<br>

    The <a href="https://timeseriesdoc.sepa.org.uk/api-documentation/before-you-start/how-data-validity-may-change/">
    quality rating</a> of a measurement.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__url = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices'
                      '&request=getQualityCodes&datasource=0&format=json')

        self.__code = {'50': 'G', '100': 'E', '140': 'PROV', '150': 'S', '200': 'V', '254': 'U'}
        self.__description = {'50': 'Good', '100': 'Estimated', '140': 'Provisional', '150': 'Suspect',
                              '200': 'Unchecked (imported from legacy database)',
                              '254': 'Unchecked'}

    def exc(self):
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        rating = objects.api(url=self.__url)
        logging.info('RATING:\n%s', rating)
