import grpc
from concurrent import futures
import time
import random

# Import dos arquivos gerados
import metrics_pb2
import metrics_pb2_grpc

class MonitoringService(metrics_pb2_grpc.MonitoringServiceServicer):
    
    def GetMetric(self, request, context):
        """Retorna uma métrica"""
        value = random.uniform(0, 100)
        
        return metrics_pb2.MetricResponse(
            hostname=request.hostname,
            metric_type=request.metric_type,
            value=value,
            timestamp=int(time.time()),
            unit="percent" if request.metric_type == "cpu" else "GB"
        )
    
    def StreamMetrics(self, request, context):
        """Stream de métricas"""
        for i in range(10):
            yield self.GetMetric(request, context)
            time.sleep(1)
    
    def CheckHealth(self, request, context):
        """Health check"""
        return metrics_pb2.HealthResponse(
            healthy=True,
            message=f"Service {request.service} is running"
        )