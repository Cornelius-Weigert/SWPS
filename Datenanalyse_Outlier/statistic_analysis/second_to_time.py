import pandas as pd
import math

def second_to_time(seconds: float) -> str:
    if seconds is None or (isinstance(seconds, float)and math.isnan(seconds)):
        return "-"
    else:
        seconds = int(abs(seconds))
        seconds = int(abs(seconds))

        years, seconds = divmod(seconds, 365 * 24 * 3600)
        months, seconds = divmod(seconds, 30 * 24 * 3600)
        days, seconds = divmod(seconds, 24 * 3600)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        time= []
        if years: time.append(f"{years}Jahr ")
        if months: time.append(f"{months}Monate ")
        if days: time.append(f"{days}Tag ")
        if hours: time.append(f"{hours}Std. ")
        if minutes: time.append(f"{minutes}Min. ")
        if seconds or not time: time.append(f"{seconds}Sek. ")

        return "".join(time)

   