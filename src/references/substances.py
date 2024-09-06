"""Module substances.py"""

import pandas as pd

import src.functions.objects
import src.references.metadata
import src.references.vocabulary


class Substances:
    """

    Notes
    -----

    Reads-in the pollutants' data.
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        # The substances url (uniform resource locator)
        self.__url: str = 'https://www.scottishairquality.scot/sos-scotland/api/v1/phenomena'

        # The data source field names <labels>, their corresponding new names <names>,
        # and their expected data types <casts>.
        labels = ['id', 'label']
        names = ['pollutant_id', 'uri']
        casts = [int, str]
        self.__rename = dict(zip(labels, names))
        self.__dtype = dict(zip(names, casts))

        # Metadata instance
        self.__metadata = src.references.metadata.Metadata().substances()

    @staticmethod
    def __structure(blob: dict) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        try:
            return pd.json_normalize(data=blob, max_level=1)
        except ImportError as err:
            raise err from err

    def __casting(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        return blob.copy().astype(dtype=self.__dtype)

    @staticmethod
    def __extra_fields(blob: pd.DataFrame):
        """

        :param blob:
        :return:
        """

        definitions = src.references.vocabulary.Vocabulary().exc()
        data = blob.copy().drop(columns='uri').merge(definitions, how='left', on='pollutant_id')

        return data

    @staticmethod
    def __deduplicate(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        frame = blob.copy()['pollutant_id'].value_counts().to_frame()
        frame.reset_index(drop=False, inplace=True)
        core: pd.DataFrame = frame.loc[frame['count'] == 1, :]
        data = core[['pollutant_id']].merge(blob.copy(), how='left', on='pollutant_id')
        data.drop_duplicates(inplace=True)

        return data

    def exc(self) -> pd.DataFrame:
        """

        :return
          data: A descriptive inventory of substances/pollutants.
        """

        # Reading-in the JSON data of substances
        objects = src.functions.objects.Objects()
        dictionary: dict = objects.api(url=self.__url)

        # Hence, (a) structuring, (b) renaming fields in line with standards, (c) ensuring
        # the appropriate data type per data field, and (d) adding fields that outline what each
        # <pollutant_id> denotes.
        data = self.__structure(blob=dictionary)
        data.rename(columns=self.__rename, inplace=True)
        data = self.__casting(blob=data)
        data = self.__extra_fields(blob=data)
        data = self.__deduplicate(blob=data)

        return data[list(self.__metadata.keys())]
