"""
Module metadat.py
"""


class Metadata:
    """

    Description
    -----------

    The metadata herein will be recorded in a YAML file.
    """

    def __init__(self):
        pass

    @staticmethod
    def registry() -> dict:
        """

        :return:
            The fields of the registry metadata; vis-à-vis project.
        """

        return {'sequence_id': 'The identification code of the sequence the telemetric device records.',
                'unit_of_measure': 'The unit of measure of the recordings',
                'station_id': 'The identification code of the station that hosts the telemetric device.',
                'pollutant_id': 'The identification code of the pollutant the telemetric device measures.'}

    @staticmethod
    def stations() -> dict:
        """

        :return:
            The fields of the stations metadata; vis-à-vis project.
        """

        return {'station_id': 'The identification code of the telemetric device station.',
                'station_label': 'Address, etc., details of the station.',
                'longitude': 'The x geographic coordinate.',
                'latitude': 'The y geographic coordinate.'}

    @staticmethod
    def substances() -> dict:
        """

        :return:
            The fields of the substances metadata; vis-à-vis project.
        """

        return {
            'pollutant_id': 'The identification code of a pollutant.',
            'uri': 'The European Environment Information and Observation Network (EIONET) page of a pollutant',
            'substance': 'The name, and more, of the pollutant.',
            'notation': 'The chemical formula of the pollutant.',
            'status': 'Denotes whether a substance is still a valid pollutant.',
            'accepted_date': 'Probably the date the substance was accepted as a pollutant.',
            'recommended_unit_of_measure': 'The recommended unit of measure'
        }

    @staticmethod
    def reference() -> dict:
        """

        :return:
            Case registry, stations, and substances.
        """

        return {'sequence_id': 'The identification code of the sequence the telemetric device records.',
                'unit_of_measure': 'The unit of measure of the recordings',
                'pollutant_id': 'The identification code of the pollutant the telemetric device measures.',
                'substance': 'The name, and more, of the pollutant.',
                'notation': 'The chemical formula of the pollutant.',
                'station_id': 'The identification code of the station that hosts the telemetric device.',
                'station_label': 'Address, etc., details of the station.',
                'longitude': 'The x geographic coordinate.',
                'latitude': 'The y geographic coordinate.'}
