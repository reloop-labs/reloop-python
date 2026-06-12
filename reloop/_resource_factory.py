from __future__ import annotations

from typing import Any, Callable, Optional, TypeVar

from ._parameters import for_response
from ._resource import (
    ApiKey,
    ApiKeyList,
    ChannelList,
    Contact,
    ContactChannel,
    ContactGroup,
    ContactList,
    ContactProperty,
    GroupList,
    PropertyList,
    Resource,
)

T = TypeVar("T", bound=Resource)


def _build(resource_cls: type[T], data: dict[str, Any]) -> T:
    return resource_cls.from_dict(for_response(data))


def api_key(data: dict[str, Any]) -> ApiKey:
    return _build(ApiKey, data)


def api_key_list(data: dict[str, Any]) -> ApiKeyList:
    normalized = for_response(data)
    if isinstance(normalized.get("api_keys"), list):
        normalized["api_keys"] = [api_key(item) for item in normalized["api_keys"]]
    return ApiKeyList.from_dict(normalized)


def contact(data: dict[str, Any]) -> Contact:
    return _build(Contact, data)


def contact_list(data: dict[str, Any]) -> ContactList:
    normalized = for_response(data)
    if isinstance(normalized.get("contacts"), list):
        normalized["contacts"] = [contact(item) for item in normalized["contacts"]]
    return ContactList.from_dict(normalized)


def contact_property(data: dict[str, Any]) -> ContactProperty:
    return _build(ContactProperty, data)


def property_list(data: dict[str, Any]) -> PropertyList:
    normalized = for_response(data)
    if isinstance(normalized.get("properties"), list):
        normalized["properties"] = [
            contact_property(item) for item in normalized["properties"]
        ]
    return PropertyList.from_dict(normalized)


def contact_group(data: dict[str, Any]) -> ContactGroup:
    normalized = for_response(data)
    if isinstance(normalized.get("contacts"), list):
        normalized["contacts"] = [contact(item) for item in normalized["contacts"]]
    return ContactGroup.from_dict(normalized)


def group_list(data: dict[str, Any]) -> GroupList:
    normalized = for_response(data)
    if isinstance(normalized.get("groups"), list):
        normalized["groups"] = [contact_group(item) for item in normalized["groups"]]
    return GroupList.from_dict(normalized)


def contact_channel(data: dict[str, Any]) -> ContactChannel:
    normalized = for_response(data)
    if isinstance(normalized.get("contact"), dict):
        normalized["contact"] = contact(normalized["contact"])
    return ContactChannel.from_dict(normalized)


def channel_list(data: dict[str, Any]) -> ChannelList:
    normalized = for_response(data)
    if isinstance(normalized.get("channels"), list):
        normalized["channels"] = [
            contact_channel(item) for item in normalized["channels"]
        ]
    return ChannelList.from_dict(normalized)
