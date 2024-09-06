"""
Module vectors.py
"""
import functools
import operator

import dask
import pandas as pd

import src.elements.sequence as sq


class Vectors:
    """
    Class Vectors

    Notes
    -----
    For parallel execution purposes, this class creates a vector of collections
    whereby each collection denotes the data retrieval parameters of a device, i.e.,
    pollutant, for a particular day.

    """

    def __init__(self, reference: pd.DataFrame, datestr_: list[str]):
        """

        :param reference: A data frame wherein each instance is a set of metadata, or retrieval parameters,
                          for a pollutant telemetry device.
        :param datestr_: The dates.
        """

        self.__reference = reference
        self.__datestr_ = datestr_

    @dask.delayed
    def __append_datestr(self, datestr: str) -> pd.DataFrame:
        """

        :param datestr:
        :return:
        """

        frame = self.__reference.copy()
        frame.loc[:, 'datestr'] = datestr

        return frame

    @dask.delayed
    def __structure(self, blob: pd.DataFrame) -> list[sq.Sequence]:
        """

        :param blob:
        :return:
        """

        structures: list[dict] = blob.copy().to_dict(orient='records')

        return [sq.Sequence(**structure) for structure in structures]

    def exc(self) -> list[sq.Sequence]:
        """
        For parallel execution purposes, this class creates a vector of collections
        whereby each collection denotes the data retrieval parameters of a
        device, i.e., pollutant, for a particular day. For example, for 3 devices and 60 days
        of data, the vector will have 180, i.e., 3 × 60, collections.

        :return:
            
        """

        # Compute
        computation = []
        for datestr in self.__datestr_:
            blob = self.__append_datestr(datestr=datestr)
            computation.append(self.__structure(blob=blob))
        builds = dask.compute(computation, scheduler='threads')[0]

        # Reduce the list of lists to a list
        reduced = functools.reduce(operator.iconcat, builds, [])

        return reduced
