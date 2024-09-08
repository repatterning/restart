"""
Module metadata.py
"""


class Metadata:
    """
    Metadata Class
    """

    def __init__(self):
        pass

    @staticmethod
    def points() -> dict:
        """

        :return:
        """

        return {'epoch_ms': 'The milliseconds unix epoch time  when the measure was recorded',
                'measure': 'The unit of measure of the pollutant under measure',
                'timestamp': 'The timestamp of the measure',
                'date': 'The date the measure was recorded',
                'sequence_id': 'The identification code of the sequence this record is part of.'}
