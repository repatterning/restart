"""
This is the data type Sequence
"""
import typing


class Sequence(typing.NamedTuple):
    """
    The data type class ⇾ Sequence

    Attributes
    ----------
      sequence_id :
        The identification code of the sequence the telemetric device records.

      unit_of_measure :
        The unit of measure of the recordings.

      station_id :
        The identification code of the station that hosts the telemetric device.

      pollutant_id :
        The identification code of the pollutant the telemetric device measures.

      station_label :
        Address, etc., details of the station.

      longitude :
        The x geographic coordinate.

      latitude :
        The y geographic coordinate.

      substance :
        The name, and more, of the pollutant.

      notation :
        The chemical formula of the pollutant.
    """

    sequence_id: int
    unit_of_measure: str
    station_id: int
    pollutant_id: int
    station_label: str
    longitude: float
    latitude: float
    substance: str
    notation: str
    datestr: str
