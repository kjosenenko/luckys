# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from locations.managers import LocationManager

@api_view(['GET', 'POST'])
def locations(request):
    """
    Either returns a list of location or creates new location for a specified Project.

    """
    if request.method == 'GET':
        return Response(LocationManager.ReturnLocations(), status=status.HTTP_200_OK)
    elif request.method == 'POST':
        success, result = LocationManager.Create(request.data)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def location(request, id):
    """
    Performs operations on a single location including viewing,
    editing and deleting.

    """
    if request.method == 'GET':
        found, result = LocationManager.Find(id, serialize=True)
        if found:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        success, result = LocationManager.Update(id, request.data)
        if result is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if LocationManager.Delete(id):
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)