from datetime import datetime

class Formatter():
    def make_readable(self, key: str) -> str:
        """
        Make a property on a dataclass human readable and neatly formatted.

        Args:
            key: str a single property to format.
        """
        return ' '.join(map(str.capitalize, key.split('_')))
    
    def day_suffix(self, day: int):
        #Matches the number of the day of a month with the correct suffix.
        return ("th" if 4 <= day <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th"))

    def format_date(self, date: datetime):
        return date.strftime(f"%H:%M %p %d{self.day_suffix(date.day)} %B %y")
    
    def format_object(self, obj) -> str:
        formatted_entries = []
        for (key, value) in vars(obj).items():
            if isinstance(value, datetime):
                formatted_value = self.format_date(value)
            else:
                formatted_value = str(value)
            formatted_entries.append(f"{self.make_readable(key)}: {formatted_value}  ")
        formatted_entries.append(" ")
        return formatted_entries