from django.conf import settings


def app_metadata(request):
    # return the value you want as a dictionary. you may add multiple values in there.
    return dict(
        VERSION=settings.VERSION,
        AUTHOR=settings.AUTHOR,
        AUTHOR_URL=settings.AUTHOR_URL,
        APP_GITHUB_URL=settings.APP_GITHUB_URL,
        APP_NAME=settings.APP_NAME,
        APP_DESC=settings.APP_DESC,
        BADGE=settings.BADGE,
        # template hack! override a template tag in the app context
        title=settings.JAZZMIN_SETTINGS["site_title"],
    )
