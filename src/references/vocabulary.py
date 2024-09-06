"""Module vocabulary.py"""
import logging

import pandas as pd

import src.functions.streams
import src.elements.text_attributes as txa


class Vocabulary:
    """
    Class Vocabulary
    Reads-in the air quality pollutants dictionary
    """

    def __init__(self):
        """
        Constructor
        """

        # The url (uniform resource locator) of the air-quality-pollutants dictionary.
        self.__uri: str = 'https://dd.eionet.europa.eu/vocabulary/aq/pollutant/csv'

        # Its date fields
        self.__date_format = {'AcceptedDate': '%Y-%m-%d'}

        # The data source field names <labels>, and their corresponding new names <names>; the new names are
        # in line with field-naming standards & defined ontology.
        labels = ['URI', 'Label', 'Notation', 'Status', 'AcceptedDate', 'recommendedUnit']
        names = ['uri', 'substance', 'notation', 'status', 'accepted_date', 'recommended_unit']
        self.__dtype = dict(zip(labels, [str] * len(labels)))
        self.__rename = dict(zip(labels, names))

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def __feature_engineering(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        data = blob.copy()

        # Deriving the <pollutant_id>
        identifiers = data.copy().loc[:, 'uri'].str.rsplit(pat='/', n=1, expand=True)
        data.loc[:, 'pollutant_id'] = identifiers.loc[:, 1].astype(dtype=int).array

        # Extracting the <recommended_unit_of_measure>.
        units = data.copy().loc[:, 'recommended_unit'].str.rsplit(pat='/', n=1, expand=True)
        data.loc[:, 'recommended_unit_of_measure'] = units.loc[:, 1].array
        data.drop(columns='recommended_unit', inplace=True)

        return data

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # Reads-in the details of each substance
        streams = src.functions.streams.Streams()
        text = txa.TextAttributes(uri=self.__uri, header=0, usecols=list(self.__dtype.keys()),
                                  dtype=self.__dtype, date_format=self.__date_format)
        data: pd.DataFrame = streams.api(text=text)

        # Hence, (a) renaming the fields in line with field naming conventions and ontology standards, and (b)
        # adding & dropping features.
        data = data.copy().rename(columns=self.__rename)
        data = self.__feature_engineering(blob=data)

        return data
