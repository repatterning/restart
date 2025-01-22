"""Module stations.py"""
import pandas as pd

import src.elements.text_attributes as txa
import src.functions.objects
import src.functions.streams


class Stations:
    """
    <b>Notes</b><br>
    ------<br>

    The stations.<br>
    """

    def __init__(self):
        """
        Constructor
        """

        self.__streams = src.functions.streams.Streams()

        # The uniform resource locator for the stations vis-à-vis <Level>
        self.__uri = (
            'https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0'
            '&request=getstationlist&stationparameter_name=Level&returnfields=station_id,station_no,station_name,'
            'stationparameter_no,'
            'stationparameter_name,catchment_id,catchment_no,catchment_name,station_latitude,station_longitude,'
            'station_carteasting,station_cartnorthing,river_id,river_name,ca_sta&'
            'ca_sta_returnfields=CATCHMENT_SIZE,GAUGE_DATUM,GROUND_DATUM,GWREF_DATUM&object_type=General&format=csv')

    def exc(self) -> pd.DataFrame:
        """
        logging.info(data[['catchment_id', 'catchment_no', 'catchment_name']].drop_duplicates())

        :return:
        """

        text = txa.TextAttributes(uri=self.__uri, header=0, sep=';')
        data = self.__streams.api(text=text)
        data.info()

        return data
