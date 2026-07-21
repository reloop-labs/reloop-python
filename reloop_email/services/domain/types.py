from __future__ import annotations
from typing import List, Literal, Optional, TypedDict
DomainStatus = Literal["pending", "verifying", "active", "suspended", "failed"]
DomainTlsMode = Literal["opportunistic", "enforced"]
class DnsRecord(TypedDict, total=False):
 id: str; recordType: str; recordTypeName: str; domain: str; name: str; value: str; ttl: str; priority: Optional[int]; verificationError: Optional[str]; purpose: str; createdAt: str; status: DomainStatus; updatedAt: str
class Domain(TypedDict, total=False):
 object: str; id: str; domain: str; status: DomainStatus; userVerifiedDomain: bool; systemVerified: bool; customReturnPath: str; trackingSubdomain: str; isClickTrackingEnabled: bool; isOpenTrackingEnabled: bool; tls: DomainTlsMode; isTrackingDomain: bool; isSendingEmailEnabled: bool; isReceivingEmailEnabled: bool; verificationFailedReason: Optional[str]; dnsRecords: List[DnsRecord]; lastVerifiedAt: Optional[str]; createdAt: str; updatedAt: str; event: str
class CreateDomainParams(TypedDict, total=False):
 domain: str; click_tracking: bool; open_tracking: bool; tls: DomainTlsMode; sending_email: bool; receiving_email: bool
class UpdateDomainParams(TypedDict, total=False):
 click_tracking: bool; open_tracking: bool; sending_email: bool; receiving_email: bool; tls: DomainTlsMode
class ListDomainsParams(TypedDict, total=False): page: int; limit: int; q: str; status: DomainStatus
class DomainListResponse(TypedDict, total=False): object: str; domains: List[Domain]; total: int; page: int; limit: int; event: str
class DomainStatusResponse(TypedDict, total=False): id: str; status: DomainStatus; event: str
