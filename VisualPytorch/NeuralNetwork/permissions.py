from NeuralNetwork.models import Network

class ChangeModel(object):

    def has_permission(self, request,view):
        aquire_object = Network.objects.get(pk=view.kwargs['pk'])
        if request.method == 'GET' or request.user.id == aquire_object.creator_id:
            return True
        else:
            return False
