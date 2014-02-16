from datetime import timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, DateTime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from twython import Twython

Base = declarative_base()

class CycleDefinition(Base):
    __tablename__ = 'definitions'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    cycle = Column(Integer)

    def __repr__(self):
        return "<CycleDefinition(date='%s', cycle='%s')>" % (self.date, self.cycle)

class CycleException(Base):
    __tablename__ = 'exceptions'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    reason = Column(String)

    def __repr__(self):
        return "<CycleException(date='%s', reason='%s')>" % (self.date, self.cycle)

class CycleSchedule:
    def __init__(self, session, cycles):
        self.session = session
        self.cycles = cycles
    def get_cycle(self, date):
        exception_reason = self.is_day_exception(date)
        if exception_reason:
            return (-1, exception_reason)
        definition = self.session.query(CycleDefinition).\
                    filter(date > CycleDefinition.date).\
                    order_by(CycleDefinition.date.desc()).first()
        if not definition:
            return (-1, 'cycle data not available for extrapolation')
        current_cycle = definition.cycle - 1
        for i in range((date - definition.date).days + 1):
            if self.is_day_exception(definition.date + timedelta(days=i)):
                continue
            current_cycle += 1
            if current_cycle > self.cycles:
                current_cycle = 1
        return (current_cycle,)
    def is_day_exception(self, date):
        if date.weekday() == 5 or date.weekday() == 6:
            return 'weekend'
        exception = self.session.query(CycleException).\
                    filter(CycleException.date == date).first()
        if exception:
            return exception.reason
        return False

def load_schedule(configuration):
    engine = create_engine('sqlite:///%s' % configuration.SCHEDULE_FILE)
    return CycleSchedule(sessionmaker(bind=engine)(), configuration.CYCLES)

class ScheduledAnnouncement:
    def __init__(self, hours, minutes, message, message_exception, advance=0):
        self.hours = hours
        self.minutes = minutes
        self.message = message
        self.message_exception = message_exception
        self.advance = advance

def tweet(content, configuration):
    twitter = Twython(configuration.APP_KEY,
                      configuration.APP_SECRET,
                      configuration.OAUTH_TOKEN,
                      configuration.OAUTH_TOKEN_SECRET)
    twitter.update_status(status=content)