import logging
from application.configuration.firebase_config import db
from application.automation.Summary import Summary

class SummaryDAO:

    def __init__(self):
        self.initialize_logging()
        self.db = db

    def initialize_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='webdriver_errors.log',
            filemode='a'
        )
    def find_or_create(self, month_and_year):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            summary_recuperado = Summary(month_and_year)
            summary_recuperado.set_total(float(data.get("total", 0)))  
            summary_recuperado.set_last_total(float(data.get("last_total", 0)))  
            summary_recuperado.set_last_months_total(float(data.get("last_months_total", 0)))  
            summary_recuperado.set_last_months_total_today(float(data.get("last_months_total_today", 0)))  
            return summary_recuperado
        else:
            summary_creado = Summary(month_and_year)
            return self.save(summary_creado)

    def update_summary(self, summary):
        try:
            doc_ref = self.db.collection("summary").document(f"{summary.get_month_and_year()}")
            doc_ref.update({
                "total": summary.get_total(),
                "last_total": summary.get_last_total(),
                "last_months_total": summary.get_last_months_total(),
                "last_months_total_today": summary.get_last_months_total_today()
            })
        except Exception as e:
            print(f"Error al actualizar el documento: {e}")

    def update(self, month_and_year, field, value):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc_ref.update({field: value})

    def save(self, summary):
        doc_ref = self.db.collection("summary").document(f"{summary.get_month_and_year()}")
        new_summary = {
            "total": summary.get_total(),  
            "last_total": summary.get_last_total(),  
            "last_months_total": summary.get_last_months_total(),  
            "last_months_total_today": summary.get_last_months_total_today()  
        }
        doc_ref.set(new_summary)
        return summary

    
    def get(self, month_and_year, field):
        doc_ref = self.db.collection("summary").document(f"{month_and_year}")
        doc = doc_ref.get()    
        if doc.exists:
            data = doc.to_dict()
            return data.get(field, f"No existe el campo: {field}")
        return None 
    
# def main():
#     dao = SummaryDAO()
#     # dao.create_new_summary(12)
#     # dao.update(12,"total",1100000)
#     # total = dao.get(12,"total")
#     # noexiste = dao.get(12,"totala")
#     # tiene0 = dao.get(12,"last_total")
#     # print(total)
#     # print(noexiste)
#     # print(tiene0)
#     dao.find_or_create("12-2024")

# main()     


   