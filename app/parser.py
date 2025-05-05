python
import re
from datetime import datetime
from typing import Optional

from .models import LogEntry
from .statistics import RequestStatsCalculator


class LogParser:
    LOG_FORMAT = (
        r'(?P<remote_addr>\S+) - (?P<remote_user>\S+) \[(?P<time_local>[^\]]+)\] '
        r'"(?P<request>[^"]*)" (?P<status>\d+) (?P<body_bytes_sent>\d+) '
        r'"(?P<http_referer>[^"]*)" "(?P<http_user_agent>[^"]*)" '
        r'"(?P<http_x_forwarded_for>[^"]*)" (?P<request_time>\S+) '
        r'(?P<upstream_response_time>\S+)'
    )

    def __init__(self, stats_calculator: RequestStatsCalculator):
        self.pattern = re.compile(self.LOG_FORMAT)
        self.stats_calculator = stats_calculator

    def parse_file(self, file_path: str):
        with open(file_path, 'r') as f:
            for line in f:
                self.parse_line(line.strip())

    def parse_line(self, line: str):
        match = self.pattern.match(line)
        if not match:
            return None

        data = match.groupdict()

        # Parse request into method and path
        request_parts = data['request'].split()
        method = request_parts[0] if len(request_parts) > 0 else 'UNKNOWN'
        path = request_parts[1] if len(request_parts) > 1 else 'UNKNOWN'

        entry = LogEntry(
            remote_addr=data['remote_addr'],
            remote_user=data['remote_user'] if data['remote_user'] != '-' else None,
            time_local=datetime.strptime(data['time_local'], '%d/%b/%Y:%H:%M:%S %z'),
            request=data['request'],
            status=int(data['status']),
            body_bytes_sent=int(data['body_bytes_sent']),
            http_referer=data['http_referer'] if data['http_referer'] != '-' else None,
            http_user_agent=data['http_user_agent'] if data['http_user_agent'] != '-' else None,
            http_x_forwarded_for=(
                data['http_x_forwarded_for']
                if data['http_x_forwarded_for'] != '-' else None
            ),
            request_time=float(data['request_time']),
            upstream_response_time=(
                float(data['upstream_response_time'])
                if data['upstream_response_time'] != '-' else None
            ),
            method=method,
            path=path
        )

        self.stats_calculator.add_entry(entry)
        return entry