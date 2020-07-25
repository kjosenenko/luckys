# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from slots.managers import SlotManager

@api_view(['GET', 'POST'])
def slots(request):
    """
    Either returns a list of slot or creates new slot for a specified Project.

    """
    if request.method == 'GET':
        return Response(SlotManager.ReturnSlots(), status=status.HTTP_200_OK)

    elif request.method == 'POST':
        success, result = SlotManager.Create(request.data)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def slot(request, id):
    """
    Performs operations on a single slot including viewing,
    editing and deleting.

    """
    if request.method == 'GET':
        found, result = SlotManager.Find(id, serialize=True)
        if found:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        success, result = SlotManager.Update(id, request.data)
        if result is None:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if SlotManager.Delete(id):
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def slotByLocation(request, location_id):
    """
    Either returns a list of slot or creates new slot for a specified Project.

    """
    if request.method == 'GET':
        return Response(SlotManager.ReturnSlotsByLocation(location_id, True), status=status.HTTP_200_OK)

@api_view(['GET'])
def slotsOpen(request):
    if request.method == 'GET':
        return Response(SlotManager.ReturnSlotsOpen(True), status=status.HTTP_200_OK)