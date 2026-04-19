from rest_framework.permissions import BasePermission


# --- IsLibrarian Custom Permission ---
class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "LIBRARIAN"

    # --- IsOwnerOrReadOnly Custom Permission ---
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.method in [
            "GET",
            "HEAD",
            "OPTIONS",
        ]
