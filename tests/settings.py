DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "healthdatamodel",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECRET_KEY = "test-secret-key-not-for-production"
