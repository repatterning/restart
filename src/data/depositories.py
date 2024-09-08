"""
Module depositories.py
"""
import os

import dask
import numpy as np

import src.elements.sequence as sq
import src.functions.directories


class Depositories:
    """
    Class Depositories
    """

    def __init__(self, sequences: list[sq.Sequence], storage: str):
        """

        :param sequences:
        :param storage:
        """

        self.__sequences = sequences
        self.__storage = storage

        # Instances
        self.__directories = src.functions.directories.Directories()

    @dask.delayed
    def __local(self, matrix: np.ndarray) -> bool:
        """

        :param matrix: [pollutant_id, station_id]
        :return:
        """

        return self.__directories.create(
            path=os.path.join(self.__storage, f'pollutant_{matrix[0]}', f'station_{matrix[1]}'))

    def exc(self) -> list[str]:
        """

        :return:
        """

        # Determining the set of unique pollutant code & station code combinations.
        matrices = np.array([[sequence.pollutant_id, sequence.station_id] for sequence in self.__sequences])
        matrices = np.unique(matrices, axis=0)

        # Hence, create the storage zones
        computation = []
        for matrix in matrices:
            message = self.__local(matrix=matrix)
            computation.append(message)
        messages = dask.compute(computation, scheduler='threads')[0]

        return messages
