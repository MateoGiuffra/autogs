class Info():
    def __init__(self):
        self.last_month = 0
        self.last_month_today = 0

    def set_last_month(self, num):
        self.last_month = num

    def set_last_month_today(self, num):
        self.last_month_today = num

    def get_json(self):
        return { "message_lmt": f"El mes pasado en total se recaudaron {self.last_month} " , 
                 "message_lmtt": f"Este mismo dia pero del mes pasado se llego a: {self.last_month_today}"
            }