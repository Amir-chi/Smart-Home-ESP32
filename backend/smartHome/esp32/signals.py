from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver

logger = logging.getLogger(__name__)

from .models import Esp32Picture
from .utils import send_image_to_group


@receiver(post_save, sender=Esp32Picture)
def photo_saved_handler(sender, instance, created, **kwargs):
    if created:
        if cache.get("is_bot_online"):
            
            try:    

                send_image_to_group('bot_group', instance.image)
                    
            except Esp32Picture.DoesNotExist:
                logger.warning("No image found for capture command")
                
                
                

LED_NAMES = ["led0", "led1", "led2", "led3"]

@receiver(post_migrate)
def initialize_led_status(sender, **kwargs):
    if sender.name == "esp32":  
        from .models import LedStatus
        for led_name in LED_NAMES:
            _, created = LedStatus.objects.get_or_create(
                led_name=led_name,
                defaults={"led_status": "off"}
            )
            if created:
                logger.info(f"LED {led_name} initialized.")
