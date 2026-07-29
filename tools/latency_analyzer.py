#!/usr/bin/env python3
"""
Latency Analyzer for Moonlight-Switch (LookADev Optimized Edition)
Sprint 7: Empirical Telemetry & Latency Validation Tool

Reads CSV latency logs generated at /switch/moonlight/logs/ or custom paths,
computes comprehensive summary statistics (Mean, Variance, StdDev, 1% Low, p50, p90, p95, p99),
and supports side-by-side comparative analysis across multiple log runs.
"""

import sys
import os
import csv
import math
import argparse
from typing import List, Dict, Any

def calculate_percentile(data: List[float], percentile: float) -> float:
    if not data:
        return 0.0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[int(f)] * (c - k)
    d1 = sorted_data[int(c)] * (k - f)
    return d0 + d1

def analyze_csv_log(filepath: str) -> Dict[str, Any]:
    if not os.path.exists(filepath):
        print(f"[Error] Log file not found: {filepath}", file=sys.stderr)
        return {}

    timestamps = []
    host_fps = []
    net_fps = []
    dec_fps = []
    render_fps = []
    dec_time = []
    receive_time = []
    render_time = []
    e2e_latency = []
    total_drops = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamps.append(float(row.get('timestamp_ms', 0)))
                host_fps.append(float(row.get('host_fps', 0)))
                net_fps.append(float(row.get('net_fps', 0)))
                dec_fps.append(float(row.get('dec_fps', 0)))
                render_fps.append(float(row.get('render_fps', 0)))
                dec_time.append(float(row.get('dec_time_ms', 0)))
                receive_time.append(float(row.get('receive_time_ms', 0)))
                render_time.append(float(row.get('render_time_ms', 0)))
                e2e_latency.append(float(row.get('estimated_e2e_latency_ms', 0)))
                total_drops.append(float(row.get('total_drops', 0)))
            except (ValueError, KeyError):
                continue

    if not e2e_latency:
        print(f"[Warning] No valid telemetry records found in {filepath}")
        return {}

    n = len(e2e_latency)
    mean_lat = sum(e2e_latency) / n
    variance_lat = sum((x - mean_lat) ** 2 for x in e2e_latency) / n if n > 1 else 0.0
    stddev_lat = math.sqrt(variance_lat)

    # 1% Low FPS (derived from render_fps)
    render_fps_sorted = sorted(render_fps)
    one_percent_low_fps = render_fps_sorted[max(0, int(n * 0.01))] if render_fps_sorted else 0.0

    stats = {
        'filename': os.path.basename(filepath),
        'filepath': filepath,
        'sample_count': n,
        'duration_s': (timestamps[-1] - timestamps[0]) / 1000.0 if len(timestamps) > 1 else 0.0,
        'avg_host_fps': sum(host_fps) / n,
        'avg_net_fps': sum(net_fps) / n,
        'avg_dec_fps': sum(dec_fps) / n,
        'avg_render_fps': sum(render_fps) / n,
        'one_percent_low_fps': one_percent_low_fps,
        'avg_e2e_latency': mean_lat,
        'min_e2e_latency': min(e2e_latency),
        'max_e2e_latency': max(e2e_latency),
        'variance_e2e': variance_lat,
        'stddev_e2e': stddev_lat,
        'p50_e2e': calculate_percentile(e2e_latency, 50),
        'p90_e2e': calculate_percentile(e2e_latency, 90),
        'p95_e2e': calculate_percentile(e2e_latency, 95),
        'p99_e2e': calculate_percentile(e2e_latency, 99),
        'avg_dec_time': sum(dec_time) / n,
        'avg_receive_time': sum(receive_time) / n,
        'avg_render_time': sum(render_time) / n,
        'total_frame_drops': total_drops[-1] - total_drops[0] if total_drops else 0.0
    }
    return stats

def print_single_report(stats: Dict[str, Any]):
    if not stats:
        return
    print("=" * 65)
    print(f" MOONLIGHT-SWITCH TELEMETRY REPORT: {stats['filename']}")
    print("=" * 65)
    print(f" Samples Captured  : {stats['sample_count']} ({stats['duration_s']:.1f} s duration)")
    print(f" Render FPS        : {stats['avg_render_fps']:.2f} (1% Low: {stats['one_percent_low_fps']:.2f} FPS)")
    print(f" Network FPS       : {stats['avg_net_fps']:.2f} | Decode FPS: {stats['avg_dec_fps']:.2f}")
    print("-" * 65)
    print(" LATENCY BREAKDOWN (ms)")
    print(f"   Average Receive Time : {stats['avg_receive_time']:.2f} ms")
    print(f"   Average Decode Time  : {stats['avg_dec_time']:.2f} ms")
    print(f"   Average Render Time  : {stats['avg_render_time']:.2f} ms")
    print(f"   End-to-End Mean      : {stats['avg_e2e_latency']:.2f} ms (StdDev: {stats['stddev_e2e']:.2f} ms)")
    print(f"   Min / Max Latency    : {stats['min_e2e_latency']:.2f} ms / {stats['max_e2e_latency']:.2f} ms")
    print("-" * 65)
    print(" LATENCY PERCENTILES (ms)")
    print(f"   p50 (Median)         : {stats['p50_e2e']:.2f} ms")
    print(f"   p90                  : {stats['p90_e2e']:.2f} ms")
    print(f"   p95                  : {stats['p95_e2e']:.2f} ms")
    print(f"   p99                  : {stats['p99_e2e']:.2f} ms")
    print(f" Total Frame Drops      : {int(stats['total_frame_drops'])}")
    print("=" * 65)

def print_comparison_table(all_stats: List[Dict[str, Any]]):
    valid_stats = [s for s in all_stats if s]
    if not valid_stats:
        return
    print("\n" + "=" * 80)
    print(" SIDE-BY-SIDE LATENCY TELEMETRY COMPARISON")
    print("=" * 80)
    header = f"{'Metric':<25}" + "".join(f"{s['filename'][:16]:>18}" for s in valid_stats)
    print(header)
    print("-" * 80)

    metrics = [
        ("Avg Render FPS", lambda s: f"{s['avg_render_fps']:.2f}"),
        ("1% Low FPS", lambda s: f"{s['one_percent_low_fps']:.2f}"),
        ("Avg E2E Latency (ms)", lambda s: f"{s['avg_e2e_latency']:.2f}"),
        ("Min E2E Latency (ms)", lambda s: f"{s['min_e2e_latency']:.2f}"),
        ("p50 Latency (ms)", lambda s: f"{s['p50_e2e']:.2f}"),
        ("p95 Latency (ms)", lambda s: f"{s['p95_e2e']:.2f}"),
        ("p99 Latency (ms)", lambda s: f"{s['p99_e2e']:.2f}"),
        ("StdDev Latency (ms)", lambda s: f"{s['stddev_e2e']:.2f}"),
        ("Avg Receive Time (ms)", lambda s: f"{s['avg_receive_time']:.2f}"),
        ("Avg Decode Time (ms)", lambda s: f"{s['avg_dec_time']:.2f}"),
        ("Avg Render Time (ms)", lambda s: f"{s['avg_render_time']:.2f}"),
        ("Total Frame Drops", lambda s: f"{int(s['total_frame_drops'])}")
    ]

    for label, fn in metrics:
        row = f"{label:<25}" + "".join(f"{fn(s):>18}" for s in valid_stats)
        print(row)
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="Moonlight-Switch Latency Log Analyzer")
    parser.add_argument("logs", nargs="*", help="CSV log file paths to analyze")
    parser.add_argument("--compare", action="store_true", help="Print side-by-side comparative table")
    args = parser.parse_args()

    if not args.logs:
        print("Usage: python3 tools/latency_analyzer.py <log1.csv> [log2.csv ...]")
        sys.exit(1)

    reports = []
    for log_path in args.logs:
        stats = analyze_csv_log(log_path)
        if stats:
            reports.append(stats)
            if not args.compare:
                print_single_report(stats)

    if args.compare or len(reports) > 1:
        print_comparison_table(reports)

if __name__ == "__main__":
    main()
