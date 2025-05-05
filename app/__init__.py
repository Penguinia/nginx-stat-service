#!/usr/bin/env python3
import argparse
import time
from typing import Optional

from .parser import LogParser
from .statistics import RequestStatsCalculator
from .utils import output_stats


def main():
    parser = argparse.ArgumentParser(description='Nginx log statistics service')
    parser.add_argument('--log-file', required=True, help='Path to nginx log file')
    parser.add_argument('--follow', action='store_true', help='Follow log file changes')
    parser.add_argument('--interval', type=int, default=60,
                       help='Statistics output interval in seconds')
    parser.add_argument('--output', choices=['json', 'text'], default='json',
                       help='Output format: json, text')

    args = parser.parse_args()

    stats_calculator = RequestStatsCalculator()
    log_parser = LogParser(stats_calculator)

    try:
        if args.follow:
            print(f"Monitoring {args.log_file} for new entries...", flush=True)
            while True:
                log_parser.parse_file(args.log_file)
                output_stats(stats_calculator.get_stats(), args.output)
                time.sleep(args.interval)
                stats_calculator.reset()  # Reset for next interval
        else:
            log_parser.parse_file(args.log_file)
            output_stats(stats_calculator.get_stats(), args.output)
    except KeyboardInterrupt:
        print("\nExiting...")
    except FileNotFoundError:
        print(f"Error: File {args.log_file} not found")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()