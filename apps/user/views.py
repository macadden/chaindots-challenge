import logging
from rest_framework import (
    status,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions import IsAuthenticated
from .models import User
from .serializers import (
    FollowUserSerializer,
    UserSerializer,
)
from apps.user import serializers

logger = logging.getLogger(__name__)


class UserList(APIView):


    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            logger.info("obtencion OK de usuarios")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Posteo OK")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Error al devolver la data")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            logger.info("sucess getting user %s", user.id)
            return Response(serializer.data)
        except User.DoesNotExist:
            logger.error("User %s not found", pk)
            return Response({'error': f'User {pk} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            follow_id = request.data.get('follow_id')
            if not follow_id:
                return Response({'error': 'follow_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            to_follow = User.objects.get(pk=follow_id)
            
            if user == to_follow:
                return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.following.filter(pk=to_follow.pk).exists():
                return Response({'status': 'Already following'}, status=status.HTTP_200_OK)
            
            user.following.add(to_follow)
            logger.info(f"user {user.id} followed {to_follow.id}")
            return Response({'status': 'User followed'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"User {pk} or follow_id not found")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FollowUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, follow_id):
        try:
            logger.info(f"Request to follow user: {user_id} following {follow_id}")

            serializer = FollowUserSerializer(data={'user_id': user_id, 'follow_id': follow_id})
            serializer.is_valid(raise_exception=True)
            user_id = serializer.validated_data['user_id']
            follow_id = serializer.validated_data['follow_id']

            user = User.objects.get(id=user_id)
            user_to_follow = User.objects.get(id=follow_id)

            if user_to_follow in user.following.all():
                logger.warning(f"User {user_id} is already following user {follow_id}")
                return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)

            user.following.add(user_to_follow)
            user.save()

            logger.info(f"User {user_id} successfully followed user {follow_id}")
            return Response({'status': f'{user_id} Following user {follow_id}'}, status=status.HTTP_200_OK)
        
        except serializers.ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            logger.error(f"User not found: user_id={user_id} or follow_id={follow_id}")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return Response({'error': 'Internal server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
