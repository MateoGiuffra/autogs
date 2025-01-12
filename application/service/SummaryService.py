from application.persistence.SummaryDAO import SummaryDAO
from application.models.Summary import Summary
import logging

class SummaryService:
    
    def __init__(self):
        self.dao = SummaryDAO()

    #actualizar el summary segun la fecha requerida
    def update_by_date_setter(self, month_and_year, date_setter):
        try: 
            summary = self.find_or_create(month_and_year)
            summary.get_total_number(date_setter)
            return self.dao.update_summary(summary)
        except Exception as e: 
            message = f"Error al obtener el summary de {date_setter}: {e}"
            print(message)
            logging.error(message)
    
    # obtener del DAO SOLO el JSON de un Summary 
    def get_json(self, month_and_year):
        return self.dao.get_json(month_and_year)
    
    def find_or_create(self, month_and_year):
        summary = self.dao.find(month_and_year)
        if summary == None: 
            return self.dao.save(Summary(month_and_year))
        return summary
    
    def update_summary(self, summary):
        self.dao.update_summary(summary) 
    
