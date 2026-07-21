from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
from reloop_email.core.result import ReloopApiError, ReloopResult
T=TypeVar("T")
@dataclass(frozen=True)
class ChannelResult(Generic[T]): channel: Optional[T]; channel_error: Optional[ReloopApiError]
@dataclass(frozen=True)
class ChannelListResult: channels: Optional[dict]; channel_error: Optional[ReloopApiError]
def to_channel_result(r:ReloopResult[T])->ChannelResult[T]: return ChannelResult(None,r.error) if r.error else ChannelResult(r.response,None)
def to_channel_list_result(r:ReloopResult[dict])->ChannelListResult: return ChannelListResult(None,r.error) if r.error else ChannelListResult(r.response,None)
