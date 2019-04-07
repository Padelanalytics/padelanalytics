from django.conf import settings


def google(request):
    return {'PADEL_GOOGLE_TRACK_ID': settings.PADEL_GOOGLE_TRACK_ID}