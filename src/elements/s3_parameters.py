"""
This is data type S3Parameters
"""
import typing


class S3Parameters(typing.NamedTuple):
    """
    The data type class ⇾ S3Parameters

    Attributes
    ----------
    region_name : str
      The Amazon Web Services region code.

    region_name_identifier : str
      The identification code for extracting the <region_name> value

    location_constraint : str
      The region code of the region that the data is limited to.

    access_control_list : str
      Access control list selection.

    project_identifier : str
      The project's identifier within the cloud platform.

    internal : str
      The Amazon S3 (Simple Storage Service) bucket that hosts this project's data.

    path_internal_points : str
      The bucket path of the telemetric data.

    path_internal_references : str
      The bucket path of the telemetric data references.

    external: str
      The name of the bucket that the project's calculations will be delivered to.

    path_external_quantiles: str
      A path
    """

    region_name: str
    region_name_identifier: str
    location_constraint: str
    access_control_list: str
    project_identifier: str
    internal: str
    path_internal_points: str
    path_internal_references: str
    external: str
    path_external_quantiles: str
