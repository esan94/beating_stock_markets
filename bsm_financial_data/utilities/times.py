import time


def set_time_sleep(is_premium):

    if is_premium:
        time.sleep(1)
    else:
        time.sleep(13)


def show_time(t_init, t_end, t_msg):
    """
    This function shows the time execution for a processing.

    :param float t_init: Initial time for a process.
    :param float t_end: End time for a process.
    :param str t_msg: Message for the process.
    """

    hours, rem = divmod(t_end-t_init, 3600)
    minutes, seconds = divmod(rem, 60)
    print('##### %s - %02d:%02d:%05.2f #####' % (t_msg, int(hours), int(minutes), seconds))


