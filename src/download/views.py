"""
Download views.

This file contains a viewset for the BaseRequests.
Due to the polymorphic nature of the BaseRequests and
use of the polymorphic serializers all registered handler Requests
are automatically handled by this viewset.
"""
from django.db.models import QuerySet
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import BaseRequest
from .serializers import PolymorphicRequestSerializer, LogSerializer
from .tasks import handle_request
from .utils import list_files


class RequestViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    A Polymorphic view set for creating, viewing and retrying Request instances and associated logs.
    """
    queryset = BaseRequest.objects.all()
    serializer_class = PolymorphicRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self) -> QuerySet:
        """
        Filter the queryset based on the user, so that it can only view it's own requests.

        :return: a QuerySet containing BaseRequests created by the user.
        """
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a Request and add the user from the request to the payload to prevent overwriting the user.

        :param request: *
        :param args: *
        :param kwargs: *
        :return: *
        """
        request.data['user'] = self.request.user.id
        return super().create(request, *args, **kwargs)

    @action(detail=True)
    def logs(self, request, pk=None) -> Response:
        """
        Get request logs for a given BaseRequest.

        :param request: Request
        :param pk: str
        :return: Response
        """
        request_object = self.get_object()
        return Response(LogSerializer(request_object.log_set, many=True).data)

    @action(detail=True)
    def files(self, request, pk=None) -> Response:
        """
        Get request files for a given BaseRequest.

        :param request: Request
        :param pk: str
        :return: Response
        """
        request_object = self.get_object()
        return Response(list_files(request_object))

    @action(detail=True, methods=['PUT'])
    def retry(self, request, pk=None) -> Response:
        """
        Retry a failed request by resetting the status and planning the asynchronous handle request task (again).

        :param request: *
        :param pk: str
        :return: Response
        """
        request_object = self.get_object()
        serializer = self.get_serializer(request_object)
        if request_object.status != BaseRequest.STATUS_FAILED:
            return Response(status=400)
        else:
            request_object.set_status(BaseRequest.STATUS_PENDING)
            handle_request.delay(request_object.id)
            return Response(serializer.data)
