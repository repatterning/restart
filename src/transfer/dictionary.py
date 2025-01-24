"""Module dictionary.py"""
import logging
import glob
import os

import numpy as np
import pandas as pd


class Dictionary:
    """
    Class Dictionary
    """

    def __init__(self):
        """
        Constructor
        """

        # Metadata
        self.__metadata = {
            'timestamp': 'Milliseconds since 1 January 1970',
            'value': 'The water level above a fixed measuring point, i.e., above the station Gauge Datum, in metres.',
            'quality_code': 'The quality code, rating, of the measure.',
            'station_id': 'The measuring station identification code.',
            'catchment_id': 'The identification code of the catchment wherein the measuring station resides.',
            'catchment_size': 'In square kilometres.',
            'gauge_datum': 'The reference point of a gauge site, in metres.',
            'on_river': 'If the measuring station is on a river 1, otherwise 0.'}

    @staticmethod
    def __local(path: str, extension: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :return:
        """

        # Within a remote container this will be /app/
        splitter = os.path.basename(path) + os.path.sep
        logging.info(splitter)

        # The list of files within the path directory, including its child directories.
        files: list[str] = glob.glob(pathname=os.path.join(path, '**', f'*.{extension}'),
                                     recursive=True)

        if len(files) == 0:
            return pd.DataFrame()

        details: list[dict] = [
            {'file': file,
             'vertex': file.rsplit(splitter, maxsplit=1)[1]}
            for file in files]

        return pd.DataFrame.from_records(details)

    def exc(self, path: str, extension: str, prefix: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :param prefix: The Amazon S3 (Simple Storage Service) where the files of path are heading
        :return:
        """

        local: pd.DataFrame = self.__local(path=path, extension=extension)
        logging.info(local)

        local['section'] = local['vertex'].apply(lambda x: str(x).split(sep='/', maxsplit=2)[0])
        logging.info(local)

        if local.empty:
            return pd.DataFrame()

        # Building the Amazon S3 strings
        frame = local.assign(key=prefix + local["vertex"])

        # The metadata dict strings
        frame['metadata'] = np.array(self.__metadata).repeat(frame.shape[0])

        return frame[['file', 'key', 'metadata']]
