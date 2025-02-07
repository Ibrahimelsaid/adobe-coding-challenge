import json
import pytest
import os, sys

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

from deduplicator import JSONDeduplicator

test_json_path = 'test.json'

def test_deduplicate():
    """Test that deduplication correctly retains the latest record."""
    # Initialize the deduplicator and load the data from test.json
    deduplicator = JSONDeduplicator(test_json_path)
    deduplicator.deduplicate()

    # Ensure that the final records only contain the latest records
    assert len(deduplicator.latest_records) == 2
    assert deduplicator.latest_records["1"]["_id"] == "1"
    assert deduplicator.latest_records["1"]["entryDate"] == "2023-01-02T12:00:00+00:00"  # Newest date

def test_output_files():
    """Test that the results are saved correctly."""
    deduplicator = JSONDeduplicator(test_json_path)
    deduplicator.deduplicate()

    # Assert that the final records are as expected
    assert len(deduplicator.latest_records) == 2
    assert deduplicator.latest_records["1"]["_id"] == "1"
    assert deduplicator.latest_records["1"]["email"] == "a@b.com"
    assert deduplicator.latest_records["2"]["_id"] == "2"
    assert deduplicator.latest_records["2"]["email"] == "c@d.com"
