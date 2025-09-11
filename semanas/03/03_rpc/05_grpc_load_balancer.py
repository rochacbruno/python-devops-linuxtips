import grpc
import random
import metrics_pb2_grpc

class LoadBalancedChannel:
    def __init__(self, addresses):
        self.channels = [
            grpc.insecure_channel(addr) 
            for addr in addresses
        ]
    
    def get_stub(self):
        # Round-robin ou random
        channel = random.choice(self.channels)
        return metrics_pb2_grpc.MonitoringServiceStub(channel)

# Usar com múltiplos servidores
lb = LoadBalancedChannel([
    'server1:50051',
    'server2:50051',
    'server3:50051'
])

stub = lb.get_stub()
# response = stub.GetMetric(request)