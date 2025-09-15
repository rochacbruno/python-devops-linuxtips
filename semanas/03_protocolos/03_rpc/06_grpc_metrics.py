# Prometheus metrics
from prometheus_client import Counter, Histogram

grpc_requests = Counter('grpc_requests_total', 'Total gRPC requests')
grpc_duration = Histogram('grpc_request_duration_seconds', 'gRPC request duration')