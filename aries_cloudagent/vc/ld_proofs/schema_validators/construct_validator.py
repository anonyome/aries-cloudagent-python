"""Vc Schema Validator constructor functions."""


from .edtech_schema_validator import EdJsonVcSchemaValidator
from .schema_validator_base import VcSchemaValidator


def construct_validator(vc_schema:dict) -> VcSchemaValidator:  
    """Instantiates a supported Vc Schema Validator for a given credentialSchema.

    :param vc_schema: dict containing the schema id and type.
    :returns: VcSchemaValidator the appropriate validator for the given schema. 
    """
    schema_type = vc_schema.get('type')
    if schema_type == '1EdTechJsonSchemaValidator2019':
        return EdJsonVcSchemaValidator(vc_schema)
    else:
        return VcSchemaValidator(vc_schema)
    