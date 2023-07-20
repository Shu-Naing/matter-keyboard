from rest_framework import serializers
from key.models import Device,QA,CheckDevice,RequestResponse

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('device_id',)

class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = ('question', 'answer')


class CheckDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckDevice
        fields = ('question', 'answer')

class RequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestResponse
        fields = ('request_text', 'response_text')