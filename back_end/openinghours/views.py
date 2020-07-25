# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from openinghours.managers import OpeningHourManager

@api_view(['GET', 'POST'])
def openingHours(request):
    """
    Either returns a list of openingHour or creates new openingHour for a specified Project.

    """
    if request.method == 'GET':
        return Response(OpeningHourManager.ReturnOpeningHours(), status=status.HTTP_200_OK)

    elif request.method == 'POST':
        success, result = OpeningHourManager.Create(request.data)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def openingHour(request, id):
    """
    Performs operations on a single openingHour including viewing,
    editing and deleting.

    """
    if request.method == 'GET':
        found, result = OpeningHourManager.Find(id, serialize=True)
        if found:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        success, result = OpeningHourManager.Update(id, request.data)
        if result is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if OpeningHourManager.Delete(id):
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)