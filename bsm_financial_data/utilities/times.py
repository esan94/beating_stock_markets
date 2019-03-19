"""

#######################################################
## Author: Esteban M. Sánchez García                 ##
## E-mail: emsg94@gmail.com                          ##
##                                                   ##
## Project for master in data science from KSCHOOL   ##
##   Title: Beating Stock Markets                    ##
#######################################################

This script manages times about the process.

"""
import time


def set_time_sleep(is_premium):
    """
    This function is to stop the process for a while.

    :param bool is_premium: Boolean wich decide if the key to choose is
    for free account or for premium account.
    """

    if is_premium:
        time.sleep(1.2)
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
