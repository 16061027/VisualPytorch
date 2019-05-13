class ChangeModel(object):

    def has_permission(self, request,view):
        if request.method == 'GET' or request.user.id == view.kwargs['pk']:
            return True
        else:
            return False
