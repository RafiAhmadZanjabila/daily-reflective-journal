from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.models import Emotion
from .serializers import EmotionSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def emotion_list(request):
    energy_type = request.GET.get('type')
    if energy_type:
        emotions = Emotion.objects.filter(type=energy_type)
    else:
        emotions = Emotion.objects.all()
    
    serializer = EmotionSerializer(emotions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
