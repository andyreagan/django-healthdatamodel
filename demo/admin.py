from django.contrib import admin

from healthdatamodel.admin import (
    DataSourceRankingAdmin,
    RecordAdmin,
    WearableConnectionAdmin,
    WorkoutAdmin,
    WorkoutMetadataEntryAdmin,
)
from healthdatamodel.models import (
    DataSourceRanking,
    Record,
    WearableConnection,
    Workout,
    WorkoutMetadataEntry,
)

admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(DataSourceRanking, DataSourceRankingAdmin)
admin.site.register(WorkoutMetadataEntry, WorkoutMetadataEntryAdmin)
admin.site.register(WearableConnection, WearableConnectionAdmin)
