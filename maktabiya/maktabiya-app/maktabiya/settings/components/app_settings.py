from maktabiya.settings import env

################
# APP SETTINGS #
################
AUTHOR = "Moin Uddin"
APP_NAME = "Maktabiya"
APP_DESC = """Maktabiya ("مكتبية") derives from the word Maktab ("مكتب"), which means "desk" or "workspace" in Arabic. The suffix -iya ("-ية") is added to create an adjectival form.
Maktabiya can be translated into English as MyDesk."""
VERSION = env("APP_VERSION", default="Production")
AUTHOR_URL = "https://github.com/Aladdin-97"
APP_GITHUB_URL = "https://github.com/Aladdin-97/pycon-de-2026"
BADGE = f"{VERSION} Release".upper()
MYBOOK_URL = f'http://{env("APP_DOMAIN", default="localhost:8000")}/{env("MYBOOK_URL", default="my-bookings")}'


##################
# ADMIN SETTINGS #
##################

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Maktabiya | MyDesk",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Maktabiya | MyDesk",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Maktabiya-Admin",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Maktabiya Admin Site!",
    # Copyright on the footer
    "copyright": f"{AUTHOR}",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "app_core/img/logo.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "app_core/img/logo.png",
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-rounded",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "app_core/img/logo.png",
    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": [
        "user.User",
        "booking.Booking",
        "app_core.Office",
        "app_core.Room",
    ],
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": "avatar",
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "app_core/css/custom.css",
    "custom_js": "app_core/js/custom.js",
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": False,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # Side menu Custom links to append to app groups, keyed on app name
    "custom_links": {
        "app_core": [
            {
                "name": "Maktabiya App",
                "url": "/",
                "icon": "fas fa-calendar-check",
                "new_window": True,
            },
        ]
    },
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app_core.Office": "fas fa-building",
        "app_core.Desk": "fas fa-desktop",
        "app_core.Room": "fas fa-laptop-house",
        "app_core.Setting": "fas fa-sliders-h",
        "booking.Booking": "fas fa-calendar-alt",
        "django_q.Failure": "fas fa-exclamation-triangle",
        "django_q.Success": "fas fa-tasks",
        "django_q.OrmQ": "fas fa-th-list",
        "django_q.Schedule": "fas fa-calendar-day",
        "email_templates.EmailTemplate": "fas fa-mail-bulk",
        "user.Manager": "fas fa-user-tie",
        "user.User": "fas fa-user-ninja",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-calendar-check ",
    "default_icon_children": "fas fa-circle",
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "app_core",
        "app_core.Office",
        "app_core.Room",
        "app_core.Desk",
        "app_core.Setting",
        # "auth",
        "booking",
        "django_q",
        "django_q.Schedule",
        "django_q.OrmQ",
        "django_q.Success",
        "django_q.Failure",
        "email_templates",
        "user",
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-light",
    "accent": "accent-orange",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-orange",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "pulse",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
    "actions_sticky_top": False,
}
