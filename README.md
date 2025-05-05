# Nginx Statistics Service

[![CI](https://github.com/yourusername/nginx-stat-service/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/nginx-stat-service/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A real-time log analysis service that provides statistical insights about Nginx web server traffic.

## Features

- Real-time and historical log analysis
- Comprehensive request statistics:
  - Average and median response times
  - 90th, 95th, and 99th percentiles
  - Request method distribution (GET, POST, etc.)
  - HTTP status code distribution
  - Most frequently accessed URLs
- Multiple output formats (JSON, plain text)
- Configurable analysis intervals
- Docker support for easy deployment

## Prerequisites

- Python 3.8+
- Nginx with configured access logs (see [Log Format](#log-format))
- Docker (optional)

## Installation

### Using pip

```bash
pip install git+https://github.com/yourusername/nginx-stat-service.git
