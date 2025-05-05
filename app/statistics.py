import math
from collections import defaultdict
from typing import List, Dict, Optional

from .models import LogEntry, RequestStats


class RequestStatsCalculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.entries: List[LogEntry] = []
        self.response_times: List[float] = []
        self.method_counts: Dict[str, int] = defaultdict(int)
        self.status_counts: Dict[int, int] = defaultdict(int)
        self.url_counts: Dict[str, int] = defaultdict(int)

    def add_entry(self, entry: LogEntry):
        self.entries.append(entry)
        self.response_times.append(entry.request_time)
        self.method_counts[entry.method] += 1
        self.status_counts[entry.status] += 1
        self.url_counts[entry.path] += 1

    def get_stats(self) -> RequestStats:
        if not self.entries:
            return RequestStats(
                total_requests=0,
                average_response_time=0,
                median_response_time=0,
                percentiles={},
                methods={},
                status_codes={},
                top_urls=[]
            )

        sorted_times = sorted(self.response_times)
        total = len(sorted_times)
        avg_time = sum(sorted_times) / total

        # Calculate median
        mid = total // 2
        if total % 2 == 0:
            median_time = (sorted_times[mid - 1] + sorted_times[mid]) / 2
        else:
            median_time = sorted_times[mid]

        # Calculate percentiles
        percentiles = {
            '90': self._calculate_percentile(sorted_times, 90),
            '95': self._calculate_percentile(sorted_times, 95),
            '99': self._calculate_percentile(sorted_times, 99)
        }

        # Get top 5 URLs
        top_urls = sorted(
            self.url_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return RequestStats(
            total_requests=total,
            average_response_time=round(avg_time, 3),
            median_response_time=round(median_time, 3),
            percentiles={k: round(v, 3) for k, v in percentiles.items()},
            methods=dict(self.method_counts),
            status_codes=dict(self.status_counts),
            top_urls=top_urls
        )

    def _calculate_percentile(self, data: List[float], percentile: float) -> float:
        if not data:
            return 0.0

        k = (len(data) - 1) * (percentile / 100)
        f = math.floor(k)
        c = math.ceil(k)

        if f == c:
            return data[int(k)]

        d0 = data[int(f)] * (c - k)
        d1 = data[int(c)] * (k - f)
        return d0 + d1