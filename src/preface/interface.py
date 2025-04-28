"""Module interface.py"""
import typing

import boto3

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        pass

    @staticmethod
    def __get_attributes(connector: boto3.session.Session) -> dict:
        """

        :return:
        """

        key_name = 'data/restart/attributes.json'

        return src.s3.configurations.Configurations(connector=connector).objects(key_name=key_name)

    def exc(self) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()
        attributes: dict = self.__get_attributes(connector=connector)

        src.preface.setup.Setup(
            service=service, s3_parameters=s3_parameters).exc(reacquire=attributes['reacquire'])

        return connector, s3_parameters, service, attributes
