from typing import Any, TypedDict


class User_(TypedDict):
    id: int
    user_name: str
    temp_key: Any
    is_connected: bool
    password: str
    connections: int


class Message_(TypedDict):
    time_stemp: Any
    owner_id: int
    sender: str
    message: str


class Client_(TypedDict):
    temp_key: Any
    connection: Any
    address: Any
