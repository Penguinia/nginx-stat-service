import pytest
from datetime import datetime, timezone

from app.models import LogEntry
from app.statistics import RequestStatsCalculator


@pytest.fixture
def stats_calculator():
    return RequestStatsCalculator()


def test_empty_stats(stats_calculator: RequestStatsCalculator):
    stats = stats_calculator.get_stats()
    assert stats.total_requests == 0
    assert stats.average_response_time == 0
    assert stats.median_response_time == 0
    assert not stats.percentiles
    assert not stats.methods
    assert not stats.status_codes
    assert not stats.top_urls


def test_add_entry(stats_calculator: RequestStatsCalculator):
    entry = LogEntry(
        remote_addr='127.0.0.1',
        remote_user=None,
        time_local=datetime.now(timezone.utc),
        request='GET / HTTP/1.1',
        status=200,
        body_bytes_sent=1234,
        http_referer=None,
        http_user_agent='Mozilla/5.0',
        http_x_forwarded_for=None,
        request_time=0.1,
        upstream_response_time=0.1,
        method='GET',
        path='/'
    )

    stats_calculator.add_entry(entry)
    stats = stats_calculator.get_stats()

    assert stats.total_requests == 1
    assert stats.average_response_time == 0.1
    assert stats.median_response_time == 0.1
    assert stats.methods['GET'] == 1
    assert stats.status_codes[200] == 1
    assert ('/', 1) in stats.top_urls


def test_percentiles(stats_calculator: RequestStatsCalculator):
    times = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for i, t in enumerate(times):
        entry = LogEntry(
            remote_addr=f'127.0.0.{i}',
            remote_user=None,
            time_local=datetime.now(timezone.utc),
            request=f'GET /{i} HTTP/1.1',
            status=200,
            body_bytes_sent=1234,
            http_referer=None,
            http_user_agent='Mozilla/5.0',
            http_x_forwarded_for=None,
            request_time=t,
            upstream_response_time=t,
            method='GET',
            path=f'/{i}'
        )
        stats_calculator.add_entry(entry)

    stats = stats_calculator.get_stats()

    assert stats.percentiles['90'] == pytest.approx(0.91)
    assert stats.percentiles['95'] == pytest.approx(0.955)
    assert stats.percentiles['99'] == pytest.approx(0.991)