from rest_framework.decorators import api_view
from rest_framework.response import Response
from key.serializers import DeviceSerializer,QASerializer,CheckDeviceSerializer
from key.models import Device,QA,CheckDevice,RequestResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import secrets
import requests
import gpt4all as gp

# @api_view(['POST'])
# def save_info_id(request):
#     serializer = DeviceSerializer(data=request.data)
#     if serializer.is_valid():
#         device = serializer.save()

#         # Generate and save the token
#         token = secrets.token_hex(32)
#         device.token = token

#         # Add timestamp
#         device.timestamp = datetime.now()

#         device.save()

#         response_data = {
#             'status': 201,
#             'message': 'Device ID and token saved successfully.',
#             # 'Device_id': Device.Info_id,
#             'token': token
#         }
#         return Response(response_data, status=201)  
#     return Response(serializer.errors, status=400)


@api_view(['POST'])
def save_info_id(request):
    provided_key = request.data.get('key')

    expected_key = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJmVcouFAfJp5OxW/W5Qsbr+co3pqglnwfi0UrCtyYhGABBjK4X0z7wQt7XqiIkQGEugAcPgKR4HM5OGDAe+VUcCAwEAAQ=='

    if provided_key == expected_key:
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            device = serializer.save()

            token = secrets.token_hex(32)
            device.token = token

            device.timestamp = datetime.now()

            device.save()

            response_data = {
                'status': 201,
                'message': 'Device ID and token saved successfully.',
                'token': token
            }

            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)
    else:
        response_data = {
            'status': 401,
            'message': 'Unauthorized access. Invalid key provided.'
        }
        return Response(response_data, status=401)

# # @api_view(['POST'])
# # def chatbot_api(request):
# #     Info_id = request.data.get('Info_id')
# #     token = request.data.get('token')
# #     question = request.data.get('question')

# #     try:
# #         Info = Info.objects.get(Info_id=Info_id, token=token)
# #     except Info.DoesNotExist:
# #         return Response({'error': 'Invalid Info ID or token'}, status=400)

# #     response = requests.post('https://api.openai.com/v1/chat/completions', json={
# #         'model': 'gpt-3.5-turbo',
# #         'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
# #                      {'role': 'user', 'content': question}]
# #     }, headers={'Authorization': 'Bearer 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'})

# #     answer = response.json()['choices'][0]['message']['content']

# #     QA = Chatgpt(question=question, answer=answer)
# #     Chatgpt.save()

# #     response_data = {
# #         'status': 201,
# #         'question_id': Chatgpt.id,
# #         'question': question,
# #         'answer': answer
# #     }
# #     return Response(response_data, status=201)

@api_view(['POST'])
def chatbot_api(request):
    device_id = request.data.get('device_id')
    token = request.data.get('token')
    question = request.data.get('question')
    print(device_id, token, question)

    try:
        device = Device.objects.get(device_id=device_id, token=token)
    except Device.DoesNotExist:
        return Response({'error': 'Invalid Device ID or token'}, status=400)

    prompt = f"10 lists of recommended and related conversation for '{question}'"
    temperature = 0.9
    max_tokens = 150
    top_p = 1
    frequency_penalty = 0.0
    presence_penalty = 0.6
    stop = ["Human:", "AI:"]

    response = requests.post('https://api.openai.com/v1/chat/completions', json={
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': prompt}]
    }, headers={'Authorization': 'Bearer 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'})

    try:
        # Access the 'choices' key
        answer = response.json()['choices'][0]['message']['content']
    except KeyError:
        return Response({'error': 'Invalid response from the OpenAI API'}, status=500)

    print(answer)

    lines = answer.strip().split("\n")
    formatted_output = {}

    for i, line in enumerate(lines):
        parts = line.split(".")
        if len(parts) >= 2:
            formatted_output[i+1] = parts[1].strip().strip('"\\"')

    timestamp = datetime.now()
    qa = QA(question=question, answer=answer, timestamp=timestamp)
    qa.save()

    response_data = {
        'question_id': qa.id,
        'question': question,
        'alternatives': formatted_output
    }
    return Response(response_data, status=200)



@api_view(['POST'])
def check_device(request):
    device_id = request.data.get('device_id')
    token = request.data.get('token')
    client_data = request.data.get('data') or {}

    try:
        device = Device.objects.get(device_id=device_id, token=token)
    except Device.DoesNotExist:
        response_data = {
            'status': '400 Bad Request',
            'message': 'Device ID and token do not match.'
        }
        return Response(response_data, status=400)

    new_device = CheckDevice(device_id=device_id, token=token, client_data=client_data, timestamp=timezone.now())
    new_device.save()

    response_data = {
        'status': '200 OK',
        'message': 'Device ID and token match.',
        'data': client_data,
        'timestamp': timezone.now()
    }
    return Response(response_data, status=200)

@csrf_exempt
@api_view(['POST'])
def api(request):
    data = request.data
    text = data.get("text")
    if text is None:
        return JsonResponse({"error": "No 'text' provided."}, status=400)

    model_path = "/home/mat/Project/Modal/ggml-gpt4all-j-v1.3-groovy.bin"
    model = gp.GPT4All(model_path)

    prompt_mesg1 = "10 list of recommended alternative sentences for"
    prompt_mesg2 = "3 list of recommended alternative sentences for"

    output = model.generate(prompt_mesg1 + "'" + text + "'", max_tokens=300)

    lines = output.strip().split("\n")
    formatted_output = {i: line.split(".")[1].strip() for i, line in enumerate(lines)}
    formatted_output = {int(k): v.strip('"\\"') for k, v in formatted_output.items()}

    request_response = RequestResponse.objects.create(
        request_text=text,
        response_text=json.dumps(formatted_output)
    )
    request_response.save()

    return JsonResponse(formatted_output, status=200)