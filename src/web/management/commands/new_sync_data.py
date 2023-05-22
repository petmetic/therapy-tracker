import datetime

from src.web.models import Service

sync_time = datetime.now()
self.stdout.write(str(Service.objects.all().count()))

old_service_num = Service.objects.all().count()
services_import(data_entities)
new_service_num = Service.objects.all().count()

service_diff = new_service_num - old_service_num

self.stdout.write(self.style.SUCCESS("Successfully synced services"))
logger.info(
    f"Successfully synced services {new_service_num - old_service_num} at {sync_time}"
)
