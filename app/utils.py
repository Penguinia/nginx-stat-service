import json
from typing import Any

from .models import RequestStats


def output_stats(stats: RequestStats, format: str = 'json'):
    if format == 'json':
        print(json.dumps(stats.__dict__, indent=2))
    else:
        print("\n=== Request Statistics ===")
        print(f"Total requests: {stats.total_requests}")
        print(f"Average response time: {stats.average_response_time:.3f}s")
        print(f"Median response time: {stats.median_response_time:.3f}s")

        print("\nPercentiles:")
        for p, val in stats.percentiles.items():
            print(f"  {p}%: {val:.3f}s")

        print("\nMethods:")
        for method, count in stats.methods.items():
            print(f"  {method}: {count}")

        print("\nStatus codes:")
        for status, count in stats.status_codes.items():
            print(f"  {status}: {count}")

        print("\nTop URLs:")
        for url, count in stats.top_urls:
            print(f"  {url}: {count}")