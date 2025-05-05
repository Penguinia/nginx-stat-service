import pytest
from datetime import datetime, timedelta, timezone

from app.models import LogEntry
from app.parser import LogParser
from app.statistics import RequestStatsCalculator


@pytest.fixture
def sample_log_line():
    return (
        '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] '
        '"GET /api/v1/users HTTP/1.1" 200 1234 '
        '"https://example.com" "Mozilla/5.0" "-" '
        '0.045 0.045'
    )


@pytest.fixture
def stats_calculator():
    return RequestStatsCalculator()


@pytest.fixture
def parser(stats_calculator):
    return LogParser(stats_calculator)


def test_parse_line(parser: LogParser, sample_log_line: str):
    entry = parser.parse_line(sample_log_line)

    assert entry is not None
    assert entry.remote_addr == '127.0.0.1'
    assert entry.remote_user is None
    assert entry.time_local == datetime(2023, 10, 10, 13, 55, 36, tzinfo=timezone.utc)
    assert entry.request == 'GET /api/v1/users HTTP/1.1'
    assert entry.status == 200
    assert entry.body_bytes_sent == 1234
    assert entry.http_referer == 'https://example.com'
    assert entry.http_user_agent == 'Mozilla/5.0'
    assert entry.http_x_forwarded_for is None
    assert entry.request_time == 0.045
    assert entry.upstream_response_time == 0.045
    assert entry.method == 'GET'
    assert entry.path == '/api/v1/users'


def test_parse_invalid_line(parser: LogParser):
    assert parser.parse_line('invalid log line') is None


def test_parse_file(tmp_path, parser: LogParser, stats_calculator: RequestStatsCalculator):
    log_file = tmp_path / "test.log"
    log_file.write_text(
        '127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /api/v1/users HTTP/1.1" 200 1234 "https://example.com" "Mozilla/5.0" "-" 0.045 0.045\n'
        '192.168.1.1 - user [10/Oct/2023:13:55:37 +0000] "POST /api/v1/login HTTP/1.1" 201 567 "-" "curl/7.68.0" "-" 0.120 0.100\n'
    )

    parser.parse_file(str(log_file))
    stats = stats_calculator.get_stats()

    assert stats.total_requests == 2
    assert stats.methods['GET'] == 1
    assert stats.methods['POST'] == 1
    assert stats.status_codes[200] == 1
    assert stats.status_codes[201] == 1