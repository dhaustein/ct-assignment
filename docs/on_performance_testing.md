# Performance Testing Considerations

Drawing from k6's capabilities and general API performance testing best practices,
the following key metrics are recommended for monitoring the Unix timestamp converter API.

## Key Performance Metrics

### Latency and Throughput

- **Response Time Percentiles**: Track the 50th, 95th, and 99th percentiles to
understand the user experience under different loads.
- **Time to First Byte (TTFB)**: Measures server responsiveness and processing time.
- **Connection Time**: Indicates network latency between the client and server.
- **Requests Per Second (RPS)**: Measures the overall API capacity and throughput.
- **Data Transfer Rates**: Monitors network bandwidth utilization.

### Error Rate

- **Success Rate**: The percentage of successful requests (e.g., HTTP 2xx).
- **HTTP Error Rates**: The percentage of client-side (4xx) and server-side (5xx) errors.
- **Check Failure Rate**: The rate of failures in business logic validation within tests.

## Production Monitoring

### Resource Utilization

- **Memory Usage**: Server memory consumption under load.
- **CPU Utilization**: Processing overhead on the server.
- **Database Connections**: The number of active connections if using persistent storage.
- **Cache Performance**: Hit/miss ratios for the `cached` parameter (if functional).

Alerts should be configured to trigger when these metrics exceed predefined
thresholds to ensure proactive issue resolution.
