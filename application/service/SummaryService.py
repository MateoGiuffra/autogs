from application.persistence.SummaryDAO import SummaryDAO
import logging

class SummaryService:
    
    def __init__(self):
        self.dao = SummaryDAO()

    def get_summarys_answer(self, date_setter, month_and_year):
        try:
            summary = self.find_or_create(month_and_year)
            summary.get_total_number(date_setter)
            self.update_summary(summary)
            return summary.answer_of_current_total() 
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise

    def dif_summaries(self, date_setter, month_and_year):
        try:
            summary = self.find_or_create(month_and_year)
            field = date_setter.get_field() # obtengo el field que tengo que buscar, depende de que date setter me pasen. 
            last_month = self.get(field, month_and_year) # obtengo el contenido
            if last_month > 0 and  (not date_setter.is_necesary_calculate()): # si ya se calculo, que no lo haga de vuelta. Solo que haga la cuenta. 
                return summary.calculate_dif(last_month, summary.get_total())    
            #caso contrario, tiene que calcularlo
            last_month = summary.get_total_number(date_setter)
            self.update_summary(summary)
            print(f"Aca esta el total del mes anterior: {last_month}. El tipo es {type(last_month)}")
            return summary.calculate_dif(last_month, summary.get_total())
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise
    
    #get total info
    def get_info(self, month_and_year):
        info = self.dao.get_info(month_and_year)
        return info.get_json()


    #cruds
    def find_or_create(self, month_and_year):
        return self.dao.find_or_create(month_and_year)

    def update(self, field, value):
        month_and_year = self.summary.get_month_and_year()
        self.dao.update(month_and_year, field, value)

    def update_summary(self, summary):
        self.dao.update_summary(summary) 
    
    def get(self, field, month_and_year):
        return self.dao.get(month_and_year, field)
