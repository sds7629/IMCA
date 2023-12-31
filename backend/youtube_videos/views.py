from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response
from .models import Youtube_Video
from .serializers import Youtube_VideoSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from django.db.models import F
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class Youtube_Videos(APIView):
    # authentication_classes = [JWTAuthentication]  # JWT 토큰 인증 사용
    # permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 허용

    @extend_schema(
        tags=["youtube_videos 게시글 API"],
        summary="youtube_videos 게시글 리스트를 가져옴",
        description="youtube_videos 게시판의 모든 게시글을 가져온다.",
        responses={200: Youtube_VideoSerializer(many=True)},
    )
    def get(self, request):
        youtube_videos = Youtube_Video.objects.all()
        serializer = Youtube_VideoSerializer(youtube_videos, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["youtube_videos 게시글 API"],
        summary="youtube_videos 게시글을 만듦",
        description="새로운 youtube_videos 게시글을 만든다.",
        request=Youtube_VideoSerializer,
        responses={201: Youtube_VideoSerializer()},
    )
    def post(self, request):
        try:
            serializer = Youtube_VideoSerializer(data=request.data)
            if serializer.is_valid():
                content = serializer.save()
                return Response(
                    Youtube_VideoSerializer(content).data, status=HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class Youtube_VideoDetail(APIView):
    # authentication_classes = [JWTAuthentication]  # JWT 토큰 인증 사용
    # permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 허용

    @extend_schema(
        tags=["youtube_videos 게시글 API"],
        summary="youtube_videos 상세 게시글을 가져옴.",
        description="youtube_videos 상세 게시글을 가져온다.",
        request=Youtube_VideoSerializer,
        responses={200: Youtube_VideoSerializer()},
    )
    def get(self, request, pk):
        # 쿠키에서 이미 조회한 비디오의 목록을 가져옴
        youtube_video = self.get_object(pk)
        viewed_videos = request.COOKIES.get("viewed_videos", "").split(",")
        if str(pk) not in viewed_videos:
            Youtube_Video.objects.filter(pk=pk).update(views_count=F("views_count") + 1)
            # 데이터베이스에는 +1이 되었지만, serializer.data에는 반영이 안되어 있음
            viewed_videos.append(str(pk))
        # youtube_video.views_count += 1  # Increase the views_count
        # youtube_video.save()  # Save the changes to the database
        # Youtube_Video.objects.filter(pk=pk).update(
        #     views_count=F("views_count") + 1)
        # serializer = Youtube_VideoSerializer(youtube_video)
        serializer = Youtube_VideoSerializer(youtube_video)
        response = Response(serializer.data)

        # # 쿠키 설정
        # expires = datetime.strftime(
        #     datetime.utcnow() + timedelta(days=30), "%a, %d-%b-%Y %H:%M:%S GMT"
        # )
        # response.set_cookie(
        #     "viewed_videos",
        #     ",".join(viewed_videos),
        #     expires=expires,
        #     httponly=True,
        #     secure=True,
        #     samesite="Lax",
        # )

                return response
            else:
                return Response(data)
        except Youtube_Video.DoesNotExist:
            return Response({"error": "Board not found"}, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        tags=["youtube_videos 게시글 API"],
        summary="youtube_videos 상세 게시글을 수정.",
        description="youtube_videos 상세 게시글을 수정한다.",
        request=Youtube_VideoSerializer,
        responses={200: Youtube_VideoSerializer()},
    )
    def put(self, request, pk):
        youtube_video = self.get_object(pk)
        serializer = Youtube_VideoSerializer(youtube_video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @extend_schema(
        tags=["youtube_videos 게시글 API"],
        summary="youtube_videos 상세 게시글을 삭제",
        description="youtube_videos 상세 게시글을 삭제한다",
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        youtube_video = self.get_object(pk)
        youtube_video.delete()
        return Response(status=HTTP_404_NOT_FOUND)

    def get_object(self, pk):
        try:
            return Youtube_Video.objects.get(pk=pk)
        except Youtube_Video.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


# class CountResult(APIView):
#     def get(self, request):
#         results = Youtube_Video.objects.all()
#         count = results.count()
#         return Response(
#             {"count": count},
#         )
