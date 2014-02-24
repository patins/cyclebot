from pytz import timezone
from cyclebot import ScheduledAnnouncement

SCHEDULE_FILE = 'schedule.sqlite'

CYCLES = 6
SCHOOL_TZ = timezone('US/Eastern')

DATE_FORMAT = '%A %m/%d/%y'

ANNOUNCEMENTS = [
    ScheduledAnnouncement(4, 30, 'Today ({date}) is cycle {cycle}', 'Today\'s ({date}) cycle is unavailable due to \'{reason}\''),
    ScheduledAnnouncement(12 + 8, 00, 'Tomorrow ({date}) is cycle {cycle}', 'Tomorrow\'s ({date}) cycle is unavailable due to \'{reason}\'', 1),
]

IGNORED_REASONS = [
    'weekend',
    'vacation',
    'holiday'
]

APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''