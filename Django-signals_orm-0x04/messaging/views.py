from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()


@csrf_exempt
def delete_user(request, user_id):
    """
    Deletes a user account.
    """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    user.delete()

    return JsonResponse(
        {"message": "User and all related data deleted successfully"}
    )


@csrf_exempt
def list_users(request):
    """
    Lists all users.
    """
    users = User.objects.all().values(
        "user_id", "username",
        "email", "first_name",
        "last_name"
    )
    return JsonResponse({"users": list(users)}, status=200)
