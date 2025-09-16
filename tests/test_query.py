import types

import pytest

from ics_cal.query import fetch_events_by_keyword


class DummyResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP {self.status_code}")


HTML_FIXTURE = """
<div class="YunTech_calendar">
  <div class="YunTech_calendar_date">06/20</div>
  <div class="YunTech_calendar_events">暑假開始</div>
  <div class="YunTech_calendar_more"></div>
</div>
<div class="YunTech_calendar_holiday">
  <div class="YunTech_calendar_date">09/09</div>
  <div class="YunTech_calendar_events">暑假結束</div>
  <div class="YunTech_calendar_more"></div>
</div>
"""


def test_fetch_events_by_keyword_matches(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        return DummyResponse(HTML_FIXTURE)

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    results = fetch_events_by_keyword(2025, "暑假")
    assert ("2025/06/20", "暑假開始") in results
    assert ("2025/09/09", "暑假結束") in results


def test_fetch_events_by_keyword_no_match(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        return DummyResponse(HTML_FIXTURE)

    import requests
    monkeypatch.setattr(requests, "get", fake_get)

    results = fetch_events_by_keyword(2025, "期末考")
    assert results == []


def test_fetch_events_by_keyword_network_error(monkeypatch):
    import requests

    def fake_get(url, headers=None, timeout=None):
        raise requests.RequestException("network")

    monkeypatch.setattr(requests, "get", fake_get)

    results = fetch_events_by_keyword(2025, "暑假")
    assert results == []


