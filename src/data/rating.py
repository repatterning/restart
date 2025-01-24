"""Module rating.py"""

import pandas as pd

import src.functions.directories
import src.functions.objects
import src.functions.streams


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

        # The fields in focus
        self.__fields = ['key', 'code', 'description']

        # The codes & descriptions of a key
        self.__code = {'50': 'G', '100': 'E', '140': 'PROV', '150': 'S', '200': 'V', '254': 'U'}
        self.__description = {'50': 'Good', '100': 'Estimated', '140': 'Provisional', '150': 'Suspect',
                              '200': 'Unchecked (imported from legacy database)',
                              '254': 'Unchecked'}

    def __structure(self, values: list[dict]) -> pd.DataFrame:
        """

        :param values:
        :return:
        """

        data = pd.DataFrame.from_records(data=values)

        return data[self.__fields]

    def __anomalies(self, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        frame = data.copy()
        frame = frame.assign(code=frame['key'].astype(str).map(self.__code))
        frame = frame.assign(description=frame['key'].astype(str).map(self.__description))

        return frame

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        objects = src.functions.objects.Objects()
        values = objects.api(url=self.__url)

        data = self.__structure(values=values)
        data = self.__anomalies(data=data.copy())

        return data
