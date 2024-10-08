"""Injection context implementation."""

import copy
from collections import namedtuple
from typing import Mapping, Optional, Type

from .base import BaseInjector, InjectionError
from .injector import Injector, InjectType
from .settings import Settings

Scope = namedtuple("Scope", "name injector")


class InjectionContextError(InjectionError):
    """Base class for issues in the injection context."""


class InjectionContext(BaseInjector):
    """Manager for configuration settings and class providers."""

    ROOT_SCOPE = "application"

    def __init__(
        self,
        *,
        settings: Optional[Mapping[str, object]] = None,
        enforce_typing: bool = True,
    ):
        """Initialize a `ServiceConfig`."""
        self._injector = Injector(settings, enforce_typing=enforce_typing)
        self._scope_name = InjectionContext.ROOT_SCOPE

    @property
    def injector(self) -> Injector:
        """Accessor for scope-specific injector."""
        return self._injector

    @injector.setter
    def injector(self, injector: Injector):
        """Setter for scope-specific injector."""
        self._injector = injector

    @property
    def settings(self) -> Settings:
        """Accessor for scope-specific settings."""
        return self.injector.settings

    @settings.setter
    def settings(self, settings: Settings):
        """Setter for scope-specific settings."""
        self.injector.settings = settings

    def update_settings(self, settings: Mapping[str, object]):
        """Update the scope with additional settings."""
        if settings:
            self.injector.settings.update(settings)

    def start_scope(
        self, settings: Optional[Mapping[str, object]] = None
    ) -> "InjectionContext":
        """Begin a new named scope.

        Args:
            scope_name: The unique name for the scope being entered
            settings: An optional mapping of additional settings to apply

        Returns:
            A new injection context representing the scope

        """
        result = self.copy()
        if settings:
            result.update_settings(settings)
        return result

    def inject(
        self,
        base_cls: Type[InjectType],
        settings: Optional[Mapping[str, object]] = None,
    ) -> InjectType:
        """Get the provided instance of a given class identifier.

        Args:
            base_cls (Type[InjectType]): The base class to retrieve an instance of.
            settings (Optional[Mapping[str, object]]): An optional mapping providing
                configuration to the provider.

        Returns:
            InjectType: An instance of the base class, or None.

        """
        return self.injector.inject(base_cls, settings)

    def inject_or(
        self,
        base_cls: Type[InjectType],
        settings: Optional[Mapping[str, object]] = None,
        default: Optional[InjectType] = None,
    ) -> Optional[InjectType]:
        """Get the provided instance of a given class identifier or default if not found.

        Args:
            base_cls: The base class to retrieve an instance of
            settings: An optional dict providing configuration to the provider
            default: default return value if no instance is found

        Returns:
            An instance of the base class, or None

        """
        return self.injector.inject_or(base_cls, settings, default)

    def copy(self) -> "InjectionContext":
        """Produce a copy of the injector instance."""
        result = copy.copy(self)
        result._injector = self.injector.copy()
        return result
