# django-healthdatamodel

A reusable Django app for storing health data in a schema inspired by [Apple HealthKit](https://developer.apple.com/documentation/healthkit).

## Models

### Record

Stores individual health measurements. Mirrors HealthKit's sample model: each record has a `type` (e.g. `ActiveCalories`, `SleepDeep`, `StepCount`), a `value`, a `unit`, and a `startDate`/`endDate` range. Records are associated with a user via `settings.AUTH_USER_MODEL`.

### Workout

Stores workout sessions. Mirrors HealthKit's `HKWorkout`: each entry has a `workoutActivityType`, a duration with unit, a time range, and source metadata (device, app, version).

### WorkoutMetadataEntry

Key/value metadata attached to a `Workout`. Maps to HealthKit's workout metadata dictionary.

### WearableConnection

Tracks a user's connected wearable devices. A user can have multiple simultaneous connections (e.g. Apple Watch for activity, a separate device for sleep). Each connection has a `data_source` (the data pipeline: `apple_health`, `fitbit`, `health_connect`), a `device_brand`, a lifecycle `status` (`active` / `disconnected`), and a `preferred_for_sleep` flag.

### DataSourceRanking

When a user has more than one active data source within the same time window, `DataSourceRanking` determines which source takes precedence. Ranks are resolved at ingestion time.

## Installation

```
pip install django-healthdatamodel
```

Add to `INSTALLED_APPS` and run migrations:

```python
INSTALLED_APPS = [
    ...
    "healthdatamodel",
]
```

```
python manage.py migrate
```

The models use `settings.AUTH_USER_MODEL` for the user FK, so they work with any custom user model.

## Admin

Admin classes (`WorkoutAdmin`, `RecordAdmin`, `WearableConnectionAdmin`, etc.) are defined in `healthdatamodel.admin` but **not registered** — registration is left to the host project. This lets you subclass and extend without the unregister/re-register pattern:

```python
from django.contrib import admin
from healthdatamodel.admin import WearableConnectionAdmin as Base
from healthdatamodel.models import WearableConnection

@admin.register(WearableConnection)
class WearableConnectionAdmin(Base):
    search_fields = list(Base.search_fields) + ["customer__your_custom_field"]
```

See `demo/admin.py` for a plain registration example.

## Test utilities

`healthdatamodel.testing` provides `set_customer_device()`, which creates or updates a `WearableConnection` for a customer and deactivates any conflicting connections:

```python
from healthdatamodel.testing import set_customer_device

set_customer_device(customer, data_source="apple_health", device_brand="apple")
```

## Demo project

A minimal Django project is included under `demo/` to show the models and admin working end-to-end against Django's built-in `auth.User`:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit `/admin/`.
