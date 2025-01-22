"""Module codes.py"""
import pandas as pd

import src.elements.text_attributes as txa
import src.functions.streams


class Codes:
    """
    <b>Notes</b><br>
    ------<br>

    Extracts time series codes.<br>
    """

    def __init__(self):
        """
        Construction
        """

        self.__streams = src.functions.streams.Streams()

        # # The uniform resource locator for the time series codes list vis-à-vis <Level>
        self.__uri = ('https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0'
                      '&request=getTimeseriesList&catchment_no=*&stationparameter_name=Level&ts_name=15minute'
                      '&returnfields=catchment_id,catchment_no,catchment_name,station_id,station_no,station_name,'
                      'stationparameter_no,stationparameter_name,parametertype_id,parametertype_name,'
                      'ts_name,ts_id,ts_path,coverage'
                      '&dateformat=yyyy-MM-dd&format=csv')

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        text = txa.TextAttributes(uri=self.__uri, header=0, sep=';')
        frame = self.__streams.api(text=text)
        frame.info()

        return frame
