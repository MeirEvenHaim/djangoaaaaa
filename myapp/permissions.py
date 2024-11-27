from rest_framework.permissions import BasePermission
class IsAdminOrSelf(BasePermission):
    """
    Custom permission to allow only admin to perform any action
    and regular users to retrieve or update their own profile.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can perform any action
        if request.user.role == 'admin':
            return True
        # Regular users can only view/update their own profile
        return obj == request.user
    
class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        # Allow cart creation (POST) for all authenticated users
        if request.method == 'POST':
            return request.user.is_authenticated
        
        # Admins can access anything
        if request.user.is_staff:
            return True
        
        # For other methods (e.g., GET), allow authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins can access anything
        if request.user.is_staff:
            return True

        # Regular users can only access their own carts
        return obj.user == request.user.client_profile