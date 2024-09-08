"""Module points.py"""
import os

import dask
import pandas as pd

import src.data.api
import src.elements.sequence as sq
import src.functions.objects
import src.functions.streams


class Points:
    """
    Class Points

    Retrieves telemetric device data points by date, structures the data sets, and saves them.
    """

    def __init__(self, sequences: list[sq.Sequence], storage: str):
        """

        :param sequences:
        :param storage:
        """

        self.__sequences = sequences
        self.__storage = storage

        self.__api = src.data.api.API()
        self.__objects = src.functions.objects.Objects()
        self.__streams = src.functions.streams.Streams()

    @dask.delayed
    def __url(self, sequence_id: int, datestr: str) -> str:
        """
        Builds a Scottish Air Quality API (Application Programming Interface) URL (Uniform Resource Locator) for a
        data period covering a single calendar month.

        :param sequence_id:
        :param datestr:
        :return:
        """

        return self.__api.exc(sequence_id=sequence_id, datestr=datestr)

    @dask.delayed
    def __reading(self, url: str) -> dict:
        """

        :param url:
        :return:
        """

        content: dict = self.__objects.api(url=url)
        dictionary = content[0]['data']

        return dictionary

    @dask.delayed
    def __building(self, dictionary: dict, sequence_id: int) -> pd.DataFrame:
        """

        :param dictionary:
        :param sequence_id:
        :return:
        """

        if not bool(dictionary):
            data = pd.DataFrame()
        else:
            data = pd.DataFrame(data=dictionary, columns=['epoch_ms', 'measure'])
            data.dropna(axis=0, inplace=True)
            data.loc[:, 'timestamp'] = pd.to_datetime(data.loc[:, 'epoch_ms'].array, unit='ms', origin='unix')
            data.loc[:, 'date'] = data.loc[:, 'timestamp'].dt.date.array
            data.loc[:, 'sequence_id'] = sequence_id
            data = data.copy().loc[data['measure'] >= 0, :]

        return data

    @dask.delayed
    def __depositing(self, blob: pd.DataFrame, datestr: str, sequence: sq.Sequence) -> str:
        """

        :param blob:
        :param datestr:
        :param sequence:
        :return:
        """

        if blob.empty:
            return f'{sequence.sequence_id} -> empty'

        basename = os.path.join(self.__storage, f'pollutant_{sequence.pollutant_id}', f'station_{sequence.station_id}')
        return self.__streams.write(blob=blob, path=os.path.join(basename, f'{datestr}.csv'))

    def exc(self):
        """

        :return:
        """

        computations = []
        for sequence in self.__sequences:
            url = self.__url(sequence_id=sequence.sequence_id, datestr=sequence.datestr)
            dictionary = self.__reading(url=url)
            data = self.__building(dictionary=dictionary, sequence_id=sequence.sequence_id)
            message = self.__depositing(blob=data, datestr=sequence.datestr, sequence=sequence)
            computations.append(message)
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
