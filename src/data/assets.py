"""Module assets.py"""
import pandas as pd


class Assets:
    """
    <b>Notes</b><br>
    -----------<br>

    Selects, ascertains, <level> asset instances that (a) have a catchment size value, (b) have a gauge datum value,
    (c) have a measuring station <on_river> identifier, (d) have <from> & <to> date values of type
    datetime (%Y-%m-%d), (e) have longitude & latitude values of type float, (f) have a water level time
    series identification code value, (g) and more.  The <from> & <to> values encode the time span of a series.
    """

    def __init__(self, codes: pd.DataFrame, stations: pd.DataFrame):
        """

        :param codes:
        :param stations:
        """

        self.__codes = codes
        self.__stations = stations

    def __get_instances(self) -> pd.DataFrame:
        """

        :return:
        """

        left = ['station_id', 'catchment_id', 'catchment_name', 'ts_id', 'ts_name', 'from', 'to',
                'stationparameter_no', 'parametertype_id']
        right = ['station_id', 'station_latitude', 'station_longitude', 'river_id',
                 'CATCHMENT_SIZE', 'GAUGE_DATUM']

        data = self.__codes[left].merge(self.__stations[right], on='station_id', how='left')

        return data

    @staticmethod
    def __coordinates(instances: pd.DataFrame) -> pd.DataFrame:
        """

        :param instances:
        :return:
        """

        instances['station_latitude'] = pd.to_numeric(instances['station_latitude'], errors='coerce')
        instances['station_longitude'] = pd.to_numeric(
            instances['station_longitude'].str.replace("'", ""), errors='coerce')

        return instances

    @staticmethod
    def __datum(instances: pd.DataFrame) -> pd.DataFrame:
        """
        instances['GROUND_DATUM'] = pd.to_numeric(instances['GROUND_DATUM'], errors='coerce')

        :param instances:
        :return:
        """

        instances['GAUGE_DATUM'] = pd.to_numeric(instances['GAUGE_DATUM'], errors='coerce')

        return instances

    @staticmethod
    def __time(instances: pd.DataFrame):
        """

        :param instances:
        :return:
        """

        instances['from'] = pd.to_datetime(instances['from'], format='%Y-%m-%d')
        instances['to'] = pd.to_datetime(instances['to'], format='%Y-%m-%d')

        return instances

    @staticmethod
    def __on_river(instances: pd.DataFrame):
        """

        :param instances:
        :return:
        """

        instances['on_river'] = instances['river_id'].notna()

        return instances

    @staticmethod
    def __filter(instances: pd.DataFrame) -> pd.DataFrame:
        """

        :param instances:
        :return:
        """

        conditionals = instances['ts_id'].notna() & instances['GAUGE_DATUM'].notna() & instances['CATCHMENT_SIZE'].notna()

        return instances.loc[conditionals, :]

    # noinspection PyTypeChecker
    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        instances = self.__get_instances()
        instances = self.__coordinates(instances=instances.copy())
        instances = self.__datum(instances=instances.copy())
        instances = self.__time(instances=instances.copy())
        instances = self.__on_river(instances=instances.copy())
        instances = self.__filter(instances=instances.copy())
        instances.rename(str.lower, axis=1, inplace=True)
        instances.info()

        return instances
