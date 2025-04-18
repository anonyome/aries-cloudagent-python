"""A message decorator for services.

A service decorator adds routing information to a message so agent can respond without
needing to perform a handshake.
"""

from typing import List, Optional

from marshmallow import EXCLUDE, fields

from ..models.base import BaseModel, BaseModelSchema
from ..valid import (
    RAW_ED25519_2018_PUBLIC_KEY_EXAMPLE,
    RAW_ED25519_2018_PUBLIC_KEY_VALIDATE,
)


class ServiceDecorator(BaseModel):
    """Class representing service decorator."""

    class Meta:
        """ServiceDecorator metadata."""

        schema_class = "ServiceDecoratorSchema"

    def __init__(
        self,
        *,
        endpoint: str,
        recipient_keys: List[str],
        routing_keys: Optional[List[str]] = None,
    ):
        """Initialize a ServiceDecorator instance.

        Args:
            endpoint: Endpoint which this agent can be reached at
            recipient_keys: List of recipient keys
            routing_keys: List of routing keys

        """
        super().__init__()
        self._endpoint = endpoint
        self._recipient_keys = recipient_keys
        self._routing_keys = routing_keys

    @property
    def endpoint(self):
        """Accessor for service endpoint.

        Returns:
            This service's `serviceEndpoint`

        """
        return self._endpoint

    @property
    def recipient_keys(self):
        """Accessor for recipient keys.

        Returns:
            This service's `recipientKeys`

        """
        return self._recipient_keys

    @property
    def routing_keys(self):
        """Accessor for routing keys.

        Returns:
            This service's `routingKeys`

        """
        return self._routing_keys


class ServiceDecoratorSchema(BaseModelSchema):
    """Thread decorator schema used in serialization/deserialization."""

    class Meta:
        """ServiceDecoratorSchema metadata."""

        model_class = ServiceDecorator
        unknown = EXCLUDE

    recipient_keys = fields.List(
        fields.Str(
            validate=RAW_ED25519_2018_PUBLIC_KEY_VALIDATE,
            metadata={
                "description": "Recipient public key",
                "example": RAW_ED25519_2018_PUBLIC_KEY_EXAMPLE,
            },
        ),
        data_key="recipientKeys",
        required=True,
        metadata={"description": "List of recipient keys"},
    )
    endpoint = fields.Str(
        data_key="serviceEndpoint",
        required=True,
        metadata={
            "description": "Service endpoint at which to reach this agent",
            "example": "http://192.168.56.101:8020",
        },
    )
    routing_keys = fields.List(
        fields.Str(
            validate=RAW_ED25519_2018_PUBLIC_KEY_VALIDATE,
            metadata={
                "description": "Routing key",
                "example": RAW_ED25519_2018_PUBLIC_KEY_EXAMPLE,
            },
        ),
        data_key="routingKeys",
        required=False,
        metadata={"description": "List of routing keys"},
    )
