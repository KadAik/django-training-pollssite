import os
import configurations

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polls.settings')
os.environ.setdefault('DJANGO_Configuration', 'Dev')

configurations.setup()