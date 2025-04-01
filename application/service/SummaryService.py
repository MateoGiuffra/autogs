from application.persistence.SummaryDAO import SummaryDAO
from application.models.Summary import Summary
import logging
from application.persistence.SummaryDAO import SummaryDAO
from application.models.Summary import Summary
import logging
import asyncio

class SummaryService:
    
    def __init__(self):
        self.dao = SummaryDAO()

    # to update the summary according to date 
    def update_by_date_setter(self, month_and_year, date_setter):
        try: 
            summary_json = self.get_json(month_and_year)
            if (not date_setter.is_necessary_again(month_and_year, summary_json, self)):
                return summary_json
            summary = self.find_or_create(month_and_year)
            summary.get_total_number(date_setter)
            self.update_summary(summary)
            return summary.to_summary_dict()
        except AttributeError as ar:
            print(f"Aca esta el attribute error {ar}")
        except Exception as e: 
            message = f"Error al obtener el summary de {date_setter}: {e}"
            logging.error(message)
            raise 
        
    def update_summary(self, summary):
        self.dao.update_summary(summary) 
    
    # get only json summary 
    def get_json(self, month_and_year):
        try:
            return self.dao.get_json(month_and_year)
        except Exception as e:
            print(f"Ocurrio un error: {e}")
            raise 
    
    def find_or_create(self, month_and_year):
        summary = self.dao.find(month_and_year)
        if summary == None: 
            return self.dao.save(Summary(month_and_year))
        return summary

    
    # methods to get or to update specific fields 
    def update_field_of(self, month_and_year, field, value):
        print("entre aca update_field_of") 
        self.dao.update_field_of(month_and_year, field,value)
        
    def get_field_of(self, month_and_year, field):
        return self.dao.get_field_of(month_and_year, field)