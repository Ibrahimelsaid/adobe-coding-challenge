#!/usr/bin/env python3

import argparse
from deduplicator import JSONDeduplicator

def main():
    parser = argparse.ArgumentParser(description="De-duplicate JSON records based on _id and email.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    args = parser.parse_args()

    deduplicator = JSONDeduplicator(args.input_file)
    deduplicator.deduplicate()
    deduplicator.save_results()
    deduplicator.save_log()

if __name__ == "__main__":
    main()
