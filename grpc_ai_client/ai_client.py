import grpc
from . import food_classification_pb2
from . import food_classification_pb2_grpc
from django.conf import settings

HOST = 'localhost'
PORT = '50051'

class GrpcClient:
    @staticmethod
    def check_gpu_request(host, port):
        with grpc.insecure_channel(f'{host}:{port}') as channel:
            stub = food_classification_pb2_grpc.FoodAiStub(channel)
            response = stub.CheckGpuStatus(food_classification_pb2.Empty())
        
        return response.status

    @staticmethod
    def inference_request(host, port, id, image_bytes):
        with grpc.insecure_channel(f'{host}:{port}') as channel:
            stub = food_classification_pb2_grpc.FoodAiStub(channel)
            response = stub.PredictFoodImage(food_classification_pb2.FoodImage(id=id, image=image_bytes))

        return {'food_type': response.food_type, 'probability': response.probability}
