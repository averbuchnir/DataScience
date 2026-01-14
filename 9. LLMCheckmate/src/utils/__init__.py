from datetime import datetime


def get_current_time_display():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]
