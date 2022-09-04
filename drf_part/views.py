from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from drf_part.models import Part
from drf_part.serializers import PartSerializer
from rest_framework import status


@csrf_exempt
def part_rest_list(request):
    if request.method == "GET":
        data = request.GET
        part_id = data.get("id", None)
        if part_id is None:
            parts = Part.objects.all()
            serializer = PartSerializer(parts, many=True)
            return send_response(
                True,
                "The parts was listed correctly.",
                serializer.data,
                status.HTTP_200_OK,
            )
        else:
            part = Part.objects.get(id=part_id)
            if not part:
                return send_response(
                    False,
                    "Part with id does not exists.",
                    {},
                    status.HTTP_400_BAD_REQUEST,
                )
            serializer = PartSerializer(part)
            return send_response(
                True,
                "The part was obtained correctly.",
                serializer.data,
                status.HTTP_200_OK,
            )
    elif request.method == "POST":
        if len(request.body) > 0:
            data = JSONParser().parse(request)
            serializer = PartSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return send_response(
                    True,
                    "The part was created correctly.",
                    serializer.data,
                    status.HTTP_201_CREATED,
                )
            return send_response(False, serializer.errors, {}, 500)
        else:
            return send_response(
                False,
                "The body of request is empty.",
                {},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    elif request.method == "PUT":
        if len(request.body) > 0:
            data = JSONParser().parse(request)
            part_id = data.get("id", None)
            if part_id is not None:
                part = Part.objects.get(id=part_id)
                if not part:
                    return send_response(
                        False,
                        "Part with id does not exists.",
                        {},
                        status.HTTP_400_BAD_REQUEST,
                    )
                serializer = PartSerializer(part, data=data, partial=True)
                if serializer.is_valid():
                    obj = serializer.save()
                    if obj.id is not None:
                        return send_response(
                            True,
                            "The part was updated correctly.",
                            serializer.data,
                            status.HTTP_200_OK,
                        )
                return send_response(
                    False, serializer.errors, {}, status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            else:
                return send_response(
                    False,
                    "Part ID not provided.",
                    {},
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return send_response(
                False,
                "The body of request is empty.",
                {},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    elif request.method == "DELETE":
        if len(request.body) > 0:
            data = JSONParser().parse(request)
            part_id = data.get("id", None)
            if part_id is not None:
                part = Part.objects.get(id=part_id)
                if not part:
                    return send_response(
                        False,
                        "Part with id does not exists.",
                        {},
                        status.HTTP_400_BAD_REQUEST,
                    )
                part.delete()
                return send_response(
                    True, "The part was deleted correctly.", {}, status.HTTP_200_OK
                )
            else:
                return send_response(
                    False,
                    "Part ID not provided.",
                    {},
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return send_response(
                False,
                "The body of request is empty.",
                {},
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def send_response(status_process: bool, message: str, data: dict, status_code: int):
    response = {
        "status": status_process,
        "message": message,
        "data": data,
    }

    return JsonResponse(response, status=status_code)
