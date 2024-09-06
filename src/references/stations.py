"""Module stations.py"""

import pandas as pd

import src.functions.objects
import src.references.metadata


class Stations:
    """
    Class Stations
    Reads-in the Scottish Air Quality Agency's inventory of telemetric devices.
    """

    def __init__(self):
        """
        :var:
          self.__url: The stations url (uniform resource locator)
          self.__rename: The original field names of the data, and their corresponding new names.
        """

        # Variables
        self.__url = 'https://www.scottishairquality.scot/sos-scotland/api/v1/stations'
        self.__rename = dict(zip(['properties.id', 'properties.label'], ['station_id', 'station_label']))

        # Metadata instance
        self.__metadata = src.references.metadata.Metadata().stations()

    @staticmethod
    def __structure(blob: dict) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        try:
            normalised = pd.json_normalize(data=blob, max_level=2)
        except ImportError as err:
            raise err from err

        coordinates = pd.DataFrame(data=normalised['geometry.coordinates'].to_list(),
                                   columns=['longitude', 'latitude', 'height'])
        data = normalised.copy().drop(columns='geometry.coordinates').join(coordinates, how='left')
        data.drop(columns=['type', 'geometry.type', 'height'], inplace=True)

        return data

    @staticmethod
    def __coordinates(blob: pd.DataFrame) -> pd.DataFrame:
        """
        Exclude records that do not have both coordinate values.

        :param blob:
        :return:
        """

        conditionals = blob['longitude'].isna() | blob['latitude'].isna()
        excerpt: pd.DataFrame = blob.copy().loc[~conditionals, :]

        return excerpt

    @staticmethod
    def __deduplicate(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        frame = blob.copy()['station_id'].value_counts().to_frame()
        frame.reset_index(drop=False, inplace=True)
        core: pd.DataFrame = frame.loc[frame['count'] == 1, :]
        data = core[['station_id']].merge(blob.copy(), how='left', on='station_id')
        data.drop_duplicates(inplace=True)

        return data

    def exc(self) -> pd.DataFrame:
        """

        :return
          data: A descriptive inventory of substances/pollutants.
        """

        # Reading-in the JSON data of telemetric device stations
        objects = src.functions.objects.Objects()
        dictionary: dict = objects.api(url=self.__url)

        # Hence, structuring, and renaming the fields in line with field naming conventions and ontology standards.
        data: pd.DataFrame = self.__structure(blob=dictionary)
        data.rename(columns=self.__rename, inplace=True)
        data: pd.DataFrame = self.__coordinates(blob=data)
        data: pd.DataFrame = self.__deduplicate(blob=data)

        return data[list(self.__metadata.keys())]
