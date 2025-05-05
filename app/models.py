python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List, Tuple


@dataclass
class LogEntry:
    remote_addr: str
    remote_user: Optional[str]
    time_local: datetime
    request: str
    status: int
    body_bytes_sent: int
    http_referer: Optional[str]
    http_user_agent: Optional[str]
    http_x_forwarded_for: Optional[str]
    request_time: float
    upstream_response_time: Optional[float]
    method: str
    path: str


@dataclass
class RequestStats:
    total_requests: int
    average_response_time: float
    median_response_time: float
    percentiles: Dict[str, float]
    methods: Dict[str, int]
    status_codes: Dict[int, int]
    top_urls: List[Tuple[str, int]]