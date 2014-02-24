import config, cyclebot
from time import sleep
from datetime import datetime, timedelta
from json import dumps

schedule = cyclebot.load_schedule(config)

def write_out_cycle(cycle, time):
    f = open(config.CYCLE_FILE, 'w')
    cycle_dictionary = {
        'cycle': cycle,
        'date': time.strftime('%m-%d-%Y')
    }
    f.write(dumps(cycle_dictionary))
    f.close()

try:
    while True:
        time = datetime.now(config.SCHOOL_TZ)
        for announcement in config.ANNOUNCEMENTS:
            if time.hour == announcement.hours and time.minute == announcement.minutes:
                cycle_date = time.date() + timedelta(days=announcement.advance)
                formatted_date = cycle_date.strftime(config.DATE_FORMAT)
                cycle = schedule.get_cycle(cycle_date)
                content = None
                if cycle[0] == -1 and cycle[1] != None and cycle[1] not in config.IGNORED_REASONS:
                    content = announcement.message_exception.format(date=formatted_date, reason=cycle[1])
                elif cycle[0] > -1:
                    content = announcement.message.format(date=formatted_date, cycle=cycle[0])
                if content != None:
                    cyclebot.tweet(content, config)
        if config.CYCLE_FILE:
            write_out_cycle(schedule.get_cycle(time.date())[0],  time.date())
        sleep(60)
except (KeyboardInterrupt, SystemExit):
    pass