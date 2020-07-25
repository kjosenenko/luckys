# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from noflys.managers import NoFlyManager

@api_view(['GET', 'POST'])
def noflys(request):
    """
    Either returns a list of nofly or creates new nofly for a specified Project.

    """
    if request.method == 'GET':
        return Response(NoFlyManager.ReturnNoFlys(), status=status.HTTP_200_OK)

    elif request.method == 'POST':
        success, result = NoFlyManager.Create(request.data)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def nofly(request, id):
    """
    Performs operations on a single nofly including viewing,
    editing and deleting.

    """
    if request.method == 'GET':
        found, result = NoFlyManager.Find(id, serialize=True)
        if found:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        success, result = NoFlyManager.Update(id, request.data)
        if result is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if NoFlyManager.Delete(id):
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def noflyByLocation(request, location_id):
    """
    Either returns a list of nofly or creates new nofly for a specified Project.

    """
    if request.method == 'GET':
        return Response(NoFlyManager.ReturnNoFlysByLocation(location_id, True), status=status.HTTP_200_OK)

