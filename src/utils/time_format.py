# funtion to convert seconds to a readable format
def convert_seconds(seconds):
    """
    Convert seconds to a more readable format: days, hours, minutes, seconds.
    
    :param seconds: Time duration in seconds.
    :return: A string representing the time in days, hours, minutes, and seconds.
    """

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_str = ''

    if days > 0:
        time_str += f"{days} Dia{'s' if days > 1 else ''}, "
    if hours > 0 or days > 0:
        time_str += f"{hours} hora{'s' if hours > 1 else ''}, "
    if minutes > 0 or hours > 0 or days > 0:
        time_str += f"{minutes} minuto{'s' if minutes > 1 else ''}, "
    
    time_str += f"{seconds} segundo{'s' if seconds > 1 else ''}"

    return time_str

