from django.db import models


class DataSource(models.TextChoices):
    APPLE_HEALTH = "apple_health", "Apple Health"
    FITBIT = "fitbit", "Fitbit"
    HEALTH_CONNECT = "health_connect", "Health Connect"


class DeviceBrand(models.TextChoices):
    APPLE = "apple", "Apple"
    SAMSUNG = "samsung", "Samsung"
    FITBIT = "fitbit", "Fitbit"
    GARMIN = "garmin", "Garmin"
    OURA = "oura", "Oura"
    WHOOP = "whoop", "WHOOP"
    DATAJET = "datajet", "DataJet"  # this is for testing


class ConnectionStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    DISCONNECTED = "disconnected", "Disconnected"
