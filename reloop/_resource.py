from __future__ import annotations

from typing import Any, Iterator, Mapping


class Resource(Mapping[str, Any]):
    """StripeObject-style resource with snake_case attribute access."""

    _repr_attr = "id"

    def __init__(self, **attributes: Any) -> None:
        self._values = dict(attributes)
        for key, value in attributes.items():
            object.__setattr__(self, key, value)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Resource:
        return cls(**data)

    def __getitem__(self, key: str) -> Any:
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __repr__(self) -> str:
        ident = getattr(self, self._repr_attr, None)
        class_name = self.__class__.__name__
        if ident is not None:
            return f"<{class_name} {self._repr_attr}={ident!r}>"
        return f"<{class_name}>"


class ApiKey(Resource):
    pass


class ApiKeyList(Resource):
    pass


class Contact(Resource):
    pass


class ContactList(Resource):
    pass


class ContactProperty(Resource):
    pass


class PropertyList(Resource):
    pass


class ContactGroup(Resource):
    pass


class GroupList(Resource):
    pass


class ContactChannel(Resource):
    pass


class ChannelList(Resource):
    pass
