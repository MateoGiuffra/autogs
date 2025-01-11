from application.persistence.SummaryDAO import SummaryDAO
import logging
from application.automation.Summary import Summary
from application.automation.date_setter.DateSetterCurrentMonth import DateSetterCurrentMonth
from application.automation.date_setter.DateSetterLastMonth import DateSetterLastMonth 
from application.automation.date_setter.DateSetterLastMonthToday import DateSetterLastMonthToday  

class SummaryService:
    
    def __init__(self):
        self.dao = SummaryDAO()

    def get_summarys_answer(self, date_setter, month_and_year):
        try:
            s = Summary(None)
            print(f"aca esta el last report date: {s.get_last_report_date()}")
            summary = self.find_or_create(month_and_year)
            summary.get_total_number(date_setter)
            summary.get_total_number(date_setter)
            self.update_summary(summary)
            return summary.answer_of_current_total() 
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise
    
    #actualizar el summary segun la fecha requerida
    def update_by_date_setter(self, month_and_year, date_setter):
        summary = self.find_or_create(month_and_year)
        summary.get_total_number(date_setter)
        return self.dao.update_summary(summary)

    def dif_summaries(self, date_setter, month_and_year):
        try:
            summary = self.find_or_create(month_and_year)
            field = date_setter.get_field() # obtengo el field que tengo que buscar, depende de que date setter me pasen. 
            last_month = self.get(field, month_and_year) # obtengo el contenido
            if last_month > 0 and  (not date_setter.is_necesary_calculate()): # si ya se calculo, que no lo haga de vuelta. Solo que haga la cuenta. 
                return summary.calculate_dif(last_month, summary.get_total(),date_setter)    
            #caso contrario, tiene que calcularlo
            last_month = summary.get_total_number(date_setter)
            self.update_summary(summary)
            print(f"Aca esta el total del mes anterior: {last_month}. El tipo es {type(last_month)}")
            return summary.calculate_dif(last_month, summary.get_total(), date_setter)
        except Exception as e:
            logging.error(f"Error al obtener el resumen: {e}")
            raise
    
    # obtener del DAO SOLO el JSON de un Summary 
    def get_json(self, month_and_year):
        return self.dao.get_json(month_and_year)
    
    #get total info
    def get_info(self, month_and_year):
        summary_saved = self.dao.find_or_create(month_and_year)
        return summary_saved.get_info()

    #cruds
    def find_or_create(self, month_and_year):
        return self.dao.find_or_create(month_and_year)
    

    def update_summary(self, summary):
        self.dao.update_summary(summary) 
    
    def get(self, field, month_and_year):
        return self.dao.get(month_and_year, field)

    # actualiza un campo especifico con el valor dado
    # def update(self, field, value):
    #     month_and_year = self.summary.get_month_and_year()
    #     self.dao.update(month_and_year, field, value)
