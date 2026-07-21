from __future__ import annotations
from typing import Any, Dict, List, Optional, TypedDict, Union
from typing_extensions import NotRequired
class Webhook(TypedDict): id:str; name:str; url:str; secret:str; status:str; customHeaders:Optional[Dict[str,str]]; rateLimitEnabled:bool; maxRequestsPerMinute:int; maxRetries:int; retryBackoffMultiplier:float; filteringOptions:Optional[Dict[str,Any]]; lastTriggeredAt:Optional[str]; successCount:int; failureCount:int; consecutiveFailures:int; events:List[str]; createdAt:str; updatedAt:str
class CreateWebhookParams(TypedDict): description:str; url:str; events:List[str]
class UpdateWebhookParams(TypedDict): description:NotRequired[str]; name:NotRequired[str]; url:NotRequired[str]; secret:NotRequired[str]; status:NotRequired[str]; customHeaders:NotRequired[Dict[str,str]]; rateLimitEnabled:NotRequired[bool]; maxRequestsPerMinute:NotRequired[float]; maxRetries:NotRequired[float]; retryBackoffMultiplier:NotRequired[float]; filteringOptions:NotRequired[Dict[str,Any]]
class ListWebhooksParams(TypedDict): page:NotRequired[int]; limit:NotRequired[int]; status:NotRequired[str]; organizationId:NotRequired[str]; userId:NotRequired[str]
class VerifyWebhookParams(TypedDict): payload:Union[str,bytes]; headers:Dict[str,Optional[str]]; secret:str; tolerance:NotRequired[int]
class WebhookEvent(TypedDict): id:str; event:str; payload:Dict[str,Any]; timestamp:float
class WebhookSignatureVerificationError(Exception): pass
