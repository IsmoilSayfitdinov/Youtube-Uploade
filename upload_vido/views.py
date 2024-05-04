from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoSerializer
from .youtube_uploader import upload_to_youtube  # Tashqi YouTube yuklash funksiyasi

class VideoUploadAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            video_id = upload_to_youtube(video)  # YouTube'ga yuklash
            return Response({'video_id': video_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
