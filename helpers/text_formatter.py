from datetime import datetime


class TextFormatter:

    @staticmethod
    def format_rate_adj_date(rate_adj_date):
        date_object = datetime.strptime(rate_adj_date, "%b %d, %Y")
        formatted_date = date_object.strftime("%m-%d-%Y")
        return formatted_date

    @staticmethod
    def format_rate(rate):
        formatted_value = float(rate.replace('$', '').replace(',', '').strip())
        return formatted_value

        