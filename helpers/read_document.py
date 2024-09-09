from pprint import pprint
from helpers.utilities import extract_infortmation, process_excel, convert_values
from openpyxl import load_workbook
import pandas as pd
import re
import os
import glob


class SdHandler:

    @staticmethod
    def extract_sdm_information(account_name: str):
        account_folder = r'C:\Users\Usuario\Documents\invoicing-automation\DocumentsGeneratedIA\*.xlsx'
        archivo_excel = glob.glob(account_folder)
        account = archivo_excel[0]

        # archivo_excel = account
        df = pd.read_excel(account)
        archivo_txt = 'z.txt'
        df.to_csv(archivo_txt, sep='\t', index=False)

        with open('z.txt', 'r', encoding='utf-8') as archivo:
            content = archivo.read()
            archivo.close()

        company_name = re.findall(r'Company:\s*(.*)', content)[0].strip()
        cleaned_company_name = re.split(r'\t', company_name)[0]

        wb = load_workbook(account)
        sheet = wb['Sheet1']

        results = process_excel(sheet)

        valid_results = {x: 'workplace' if y == '' else y for x, y in results[2].items()}

        df = pd.DataFrame(results[0], columns=results[1])

        employees = extract_infortmation(df, 'IA', cleaned_company_name, account, valid_results['rate'],
                                         valid_results['equipment'], valid_results['active_date'],
                                         valid_results['rate_adjustment'], valid_results['credit_days'],
                                         account.split('\\')[1], valid_results['set_up_fee'], valid_results['bonus'],
                                         valid_results['ot_hours'], valid_results['ot_amount'],
                                         valid_results['assigned_date'])

        for item in employees:
            for key in item:
                convert_values(item[key])
        os.remove(account)
        return employees

    @staticmethod
    def get_total_employees(sd_employees: list):
        return str(len(sd_employees))

    @staticmethod
    def get_employees_by_status(employee_list):
        results = {}

        for employee in employee_list:
            details = list(employee.values())[0]
            status = details['status']

            if status not in results:
                results[status] = 1
            else:
                results[status] += 1

        return results

    @staticmethod
    def get_all_employee_ids(employee_list):
        ids = []
        for employee in employee_list:
            for key, value in employee.items():
                ids.append(value['id'])
        return ids

    @staticmethod
    def get_employee_data_by_id(employee_list, employee_id):
        for employee in employee_list:
            for key, value in employee.items():
                if value['id'] == employee_id:
                    return value
        return None
