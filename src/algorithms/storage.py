"""
Module storage.py
"""
import os
import config

import src.elements.s3_parameters as s3p


class Storage:
    """

    Notes
    -----

    Creates a storage area that mirrors the Amazon S3 storage area:
        * Amazon S3: The path is a combination of the bucket & prefix settings.
        * Local Warehouse: The path is a combination of the bucket & prefix parts.
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

    def exc(self) -> str:
        """

        :return:
        """

        # The prefix parts.
        parts: list[str] = self.__s3_parameters.path_internal_points.split(sep='/')
        parts: list[str] = [part for part in parts if part]

        # Prepending the bucket name.
        parts: list[str] = [self.__s3_parameters.internal] + parts

        # Hence, the storage path.
        path: str = os.path.join(self.__configurations.warehouse, *parts)

        return path
