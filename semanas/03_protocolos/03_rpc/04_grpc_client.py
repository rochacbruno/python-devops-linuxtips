import grpc
import metrics_pb2
import metrics_pb2_grpc

def run_client():
    # Conectar ao servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = metrics_pb2_grpc.MonitoringServiceStub(channel)
        
        # 1. Chamada simples
        print("📊 Métrica única:")
        response = stub.GetMetric(
            metrics_pb2.MetricRequest(
                hostname="server01",
                metric_type="cpu"
            )
        )
        print(f"  CPU: {response.value:.1f}%")
        
        # 2. Stream de métricas
        print("\n📈 Stream de métricas:")
        request = metrics_pb2.MetricRequest(
            hostname="server01",
            metric_type="memory"
        )
        
        for metric in stub.StreamMetrics(request):
            print(f"  Memory: {metric.value:.2f} GB")
        
        # 3. Health check
        health = stub.CheckHealth(
            metrics_pb2.HealthRequest(service="api")
        )
        print(f"\n❤️ Health: {health.message}")