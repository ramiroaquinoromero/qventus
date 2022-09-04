from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_nltk.models import Part
from drf_nltk.serializers import PartSerializer
import nltk


QUANTITY_COMMON_WORDS = 5


@csrf_exempt
def part_common_word_list(request):
    parts = Part.objects.all()
    serializer = PartSerializer(parts, many=True)
    description = []
    for data in serializer.data:
        description.append(data["description"])
    text_description = " ".join(description)
    common_words = get_common_word(text_description)
    for data in serializer.data:
        data["description"] = data["description"] + ". " + common_words
    return send_response(True, "The part description common words was listed correctly.", serializer.data, 200)


def get_common_word(text: str):
    all_words = nltk.tokenize.word_tokenize(text)
    all_word_dist = nltk.FreqDist(w.lower() for w in all_words)
    most_common = all_word_dist.most_common(QUANTITY_COMMON_WORDS)
    res_common = [x[0] for x in most_common]
    final_common = ", ".join(res_common)
    final_common_text = f"The {QUANTITY_COMMON_WORDS} words most commons are: '{final_common}'."
    return final_common_text


def send_response(status: bool, message: str, data: dict, status_code: int):
    response = {
        "status": status,
        "message": message,
        "data": data,
    }

    return JsonResponse(
        response, status=status_code
    )
