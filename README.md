# System Monitor Pro

An enhanced version of Task Manager for system monitoring using Python and PyQt5.

## Features

- Real-time CPU, RAM, and Disk usage monitoring
- Network activity monitoring (bytes sent/received per second)
- Process activity display (top 20 processes by CPU usage)
- High usage alerts (CPU > 80%, RAM > 80%, Disk > 90%)
- Alerts logged to system_monitor.log
- Graphical interface with automatic updates every 2 seconds

## Requirements

- Python 3.x
- psutil
- PyQt5

## Installation

1. Install dependencies: `pip install -r requirements.txt`

## Usage

Run the application: `python system_monitor_pro.py`

The graphical interface will display system metrics and update automatically.

## Notes

- Network speeds are calculated in seconds.

- Processes are sorted by CPU usage in descending order.

- Alerts appear as pop-up windows and are logged.
