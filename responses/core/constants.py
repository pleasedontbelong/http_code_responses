from pytz import common_timezones

from model_utils import Choices


TIMEZONES = Choices(*zip(common_timezones, common_timezones))
