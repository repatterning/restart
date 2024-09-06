"""
Module config
"""
import os
import datetime


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

        # A S3 parameters template
        self.s3_parameters_template = 'https://raw.githubusercontent.com/enqueter/.github/master/profile/s3_parameters.yaml'

        # After the development phase the start date will be a few years earlier.
        self.starting = datetime.datetime.strptime('2011-01-01', '%Y-%m-%d')
        self.ending = datetime.datetime.today() - datetime.timedelta(days=3)

        # Devices in focus, via their sequence identifiers
        # pollutant: Nitrogen Dioxide
        # area: Edinburgh
        # sequence (station): 155 (901), 531 (1014), 177 (460), 150 (791), 165(327), 142 (196)
        self.sequence_id_filter = [155, 531, 177, 150, 165, 142]
