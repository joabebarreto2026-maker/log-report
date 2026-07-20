import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected_stats():
    """Independently derive the expected counts straight from access.log."""
    total = 0
    ips = set()
    paths = Counter()
    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        match = re.search(r'"[A-Z]+ (\S+)', line)
        if match:
            paths[match.group(1)] += 1
    top_path = paths.most_common(1)[0][0]
    return total, len(ips), top_path


def test_report_exists_and_valid_json():
    """Success criterion 1: /app/report.json exists and contains a single valid JSON object."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    data = json.loads(REPORT_PATH.read_text())
    assert isinstance(data, dict), "report.json must contain a single JSON object"


def test_report_has_exact_keys():
    """Success criterion 2: the object has exactly total_requests, unique_ips, top_path."""
    data = json.loads(REPORT_PATH.read_text())
    assert set(data.keys()) == {"total_requests", "unique_ips", "top_path"}


def test_total_requests_correct():
    """Success criterion 3: total_requests equals the number of non-empty log lines."""
    expected_total, _, _ = _expected_stats()
    data = json.loads(REPORT_PATH.read_text())
    assert data["total_requests"] == expected_total


def test_unique_ips_correct():
    """Success criterion 4: unique_ips equals the number of distinct client IPs."""
    _, expected_unique_ips, _ = _expected_stats()
    data = json.loads(REPORT_PATH.read_text())
    assert data["unique_ips"] == expected_unique_ips


def test_top_path_correct():
    """Success criterion 5: top_path equals the single most frequently requested path."""
    _, _, expected_top_path = _expected_stats()
    data = json.loads(REPORT_PATH.read_text())
    assert data["top_path"] == expected_top_path
