"""
Module config
"""
import os
import datetime
import time


class Config:
    """
    Class Config

    For project settings
    """

    def __init__(self):
        """
        Constructor
        """

        self.warehouse: str = os.path.join(os.getcwd(), 'warehouse')
        self.series_ = os.path.join(self.warehouse, 'data', 'series')
        self.references_ = os.path.join(self.warehouse, 'references')

        # Template
        self.s3_parameters_key = 's3_parameters.yaml'

        '''
        For configurations repository
        '''

        # Seed
        self.seed = 5

        # Span
        self.starting = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
        self.at_least = datetime.datetime.strptime('2025-01-05', '%Y-%m-%d')

        # Limits per access
        self.n_stations = 9

        # Period: P1D, P1M, P1Y, etc.
        self.period = 'P1Y'

        # The training/testing cut-off point
        datestr = datetime.datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.cutoff = 1000 * time.mktime(datestr.timetuple())
