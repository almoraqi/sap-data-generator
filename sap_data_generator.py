import random
import sqlite3
from datetime import datetime, timedelta, date
from faker import Faker
import uuid
import json

# Initialize Faker with multiple locales for global organization
fake = Faker(['en_US', 'de_DE', 'fr_FR', 'es_ES', 'it_IT', 'pt_BR', 'zh_CN', 'ja_JP'])

# Configuration
NUM_TRANSACTIONS = 5000
START_DATE = date(2023, 1, 1)    # Early start for complete business cycles
END_DATE = date(2025, 3, 31)     # Extended end to allow realistic payment cycles
ANALYSIS_FOCUS_YEAR = 2024       # Primary analysis year for PowerBI

# Master data configurations
CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'BRL', 'CAD', 'AUD', 'CHF', 'SEK']
REGIONS = {
    'NA': ['US', 'CA', 'MX'],
    'EU': ['DE', 'FR', 'GB', 'IT', 'ES', 'NL', 'SE'],
    'APAC': ['JP', 'CN', 'AU', 'SG', 'IN'],
    'LATAM': ['BR', 'AR', 'CL', 'CO'],
    'MEA': ['AE', 'SA', 'ZA']
}

# Realistic payment terms (extended for enterprise scenarios)
PAYMENT_TERMS = ['Z001', 'Z002', 'Z010', 'Z014', 'Z030', 'Z045', 'Z060', 'Z090', 'Z120']
PAYMENT_TERMS_DAYS = {
    'Z001': 0,    # Immediate
    'Z002': 7,    # 1 week
    'Z010': 10,   # 10 days
    'Z014': 14,   # 2 weeks
    'Z030': 30,   # Net 30
    'Z045': 45,   # Net 45
    'Z060': 60,   # Net 60
    'Z090': 90,   # Net 90
    'Z120': 120   # Net 120 (enterprise/government)
}

# Cost Centers by region
COST_CENTERS = {
    'NA': ['1000', '1010', '1020', '1030', '1040'],
    'EU': ['2000', '2010', '2020', '2030', '2040'],
    'APAC': ['3000', '3010', '3020', '3030', '3040'],
    'LATAM': ['4000', '4010', '4020', '4030', '4040'],
    'MEA': ['5000', '5010', '5020', '5030', '5040']
}

COMPANY_CODES = {
    'NA': ['1000', '1100'],
    'EU': ['2000', '2100', '2200'],
    'APAC': ['3000', '3100'],
    'LATAM': ['4000'],
    'MEA': ['5000']
}

def safe_date_convert(date_obj):
    """Convert date/datetime objects to date consistently"""
    if isinstance(date_obj, datetime):
        return date_obj.date()
    elif isinstance(date_obj, date):
        return date_obj
    else:
        return date_obj

class SAPDataGenerator:
    def __init__(self):
        self.vendors = []
        self.customers = []
        self.purchase_orders = []
        self.sales_orders = []
        self.invoices = []
        self.payments = []
        self.chart_of_accounts = []
        self.cost_centers_data = []
        
    def generate_vendors(self, count=200):
        """Generate LFA1 (Vendor Master), LFB1 (Vendor Company Data), LFM1 (Vendor Purchasing Data)"""
        vendors = []
        vendor_company_data = []
        vendor_purchasing_data = []
        
        for i in range(count):
            vendor_id = f"V{10000 + i:06d}"
            region = random.choice(list(REGIONS.keys()))
            country = random.choice(REGIONS[region])
            currency = random.choice(CURRENCIES)
            
            # LFA1 - Vendor Master
            vendor = {
                'LIFNR': vendor_id,
                'NAME1': fake.company()[:35],
                'SORTL': fake.lexify('????').upper(),
                'STRAS': fake.street_address()[:35],
                'ORT01': fake.city()[:35],
                'PSTLZ': fake.postcode()[:10],
                'LAND1': country,
                'SPRAS': 'EN',
                'TELF1': fake.phone_number()[:16],
                'TELFX': fake.phone_number()[:16],
                'SMTP_ADDR': fake.company_email()[:50],
                'KTOKK': 'Z001',
                'ERDAT': fake.date_between(start_date=START_DATE, end_date=END_DATE),
                'ERNAM': fake.user_name()[:12],
                'SPERR': '' if random.random() > 0.05 else 'X',
                'LOEVM': '' if random.random() > 0.02 else 'X'
            }
            vendors.append(vendor)
            
            # LFB1 - Vendor Company Code Data
            for company_code in COMPANY_CODES[region]:
                vendor_company = {
                    'LIFNR': vendor_id,
                    'BUKRS': company_code,
                    'AKONT': random.choice(['2100000', '2110000', '2120000']),
                    'ZTERM': random.choice(PAYMENT_TERMS),
                    'REPRF': '' if random.random() > 0.1 else 'X',
                    'ZWELS': random.choice(['C', 'T', 'U']),
                    'ZAHLS': '' if random.random() > 0.05 else 'B',
                    'FDGRV': '',
                    'SPERR': '' if random.random() > 0.03 else 'X'
                }
                vendor_company_data.append(vendor_company)
            
            # LFM1 - Vendor Purchasing Data
            vendor_purchasing = {
                'LIFNR': vendor_id,
                'EKORG': f"{region}00",
                'SPERM': '' if random.random() > 0.05 else 'X',
                'LIFER': fake.lexify('???????????'),
                'LIBES': '' if random.random() > 0.1 else 'X',
                'LIPRE': '' if random.random() > 0.15 else 'X',
                'LISER': '' if random.random() > 0.2 else 'X',
                'ZTERM': random.choice(PAYMENT_TERMS),
                'INCO1': random.choice(['EXW', 'FCA', 'CPT', 'CIP', 'DAP', 'DDP']),
                'INCO2': fake.city()[:28],
                'WAERS': currency
            }
            vendor_purchasing_data.append(vendor_purchasing)
        
        return vendors, vendor_company_data, vendor_purchasing_data
    
    def generate_customers(self, count=150):
        """Generate KNA1 (Customer Master)"""
        customers = []
        
        for i in range(count):
            customer_id = f"C{20000 + i:06d}"
            region = random.choice(list(REGIONS.keys()))
            country = random.choice(REGIONS[region])
            
            customer = {
                'KUNNR': customer_id,
                'NAME1': fake.company()[:35],
                'SORTL': fake.lexify('????').upper(),
                'STRAS': fake.street_address()[:35],
                'ORT01': fake.city()[:35],
                'PSTLZ': fake.postcode()[:10],
                'LAND1': country,
                'SPRAS': 'EN',
                'TELF1': fake.phone_number()[:16],
                'TELFX': fake.phone_number()[:16],
                'SMTP_ADDR': fake.company_email()[:50],
                'KTOKD': 'Z001',
                'ERDAT': fake.date_between(start_date=START_DATE, end_date=END_DATE),
                'ERNAM': fake.user_name()[:12],
                'SPERR': '' if random.random() > 0.03 else 'X',
                'LOEVM': '' if random.random() > 0.01 else 'X'
            }
            customers.append(customer)
        
        return customers
    
    def generate_payment_terms(self):
        """Generate T052 (Payment Terms)"""
        payment_terms = []
        
        for term_code, days in PAYMENT_TERMS_DAYS.items():
            term = {
                'ZTERM': term_code,
                'SPRAS': 'EN',
                'TEXT1': f"Net {days} days" if days > 0 else "Immediate payment",
                'ZTAG1': days,
                'ZPRZ1': 0,
                'ZMTAG': 0,
                'ZTAG2': 0,
                'ZPRZ2': 0,
                'ZTAG3': 0,
                'ZPRZ3': 0
            }
            
            # Add realistic early payment discounts for longer terms
            if days >= 30:
                term['ZTAG1'] = 10 if days <= 60 else 14
                term['ZPRZ1'] = 2.0 if days <= 60 else 2.5
                term['ZMTAG'] = 0
                term['ZTAG2'] = days
            elif days >= 14:
                term['ZTAG1'] = 7
                term['ZPRZ1'] = 1.0
                term['ZTAG2'] = days
            
            payment_terms.append(term)
        
        return payment_terms
    
    def generate_purchase_orders(self, vendors, count=1500):
        """Generate EKKO (Purchase Order Header) and EKPO (Purchase Order Items)"""
        po_headers = []
        po_items = []
        
        for i in range(count):
            po_number = f"P{40000000 + i:010d}"
            vendor = random.choice(vendors)
            region = [k for k, v in REGIONS.items() if vendor['LAND1'] in v][0]
            company_code = random.choice(COMPANY_CODES[region])
            
            # Weight PO dates toward analysis focus year (2024) but allow full range
            if random.random() < 0.7:
                focus_start = date(ANALYSIS_FOCUS_YEAR, 1, 1)
                focus_end = date(ANALYSIS_FOCUS_YEAR, 12, 31)
                order_date = fake.date_between(start_date=focus_start, end_date=focus_end)
            else:
                order_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
            
            # Determine approval status and workflow
            approval_status = random.choices(
                ['approved', 'pending', 'rejected'],
                weights=[85, 10, 5]
            )[0]
            
            po_header = {
                'EBELN': po_number,
                'BUKRS': company_code,
                'BSTYP': 'F',
                'BSART': random.choice(['NB', 'UB', 'FO']),
                'LIFNR': vendor['LIFNR'],
                'EKORG': f"{region[:2]}00",
                'EKGRP': f"{region[:2]}01",
                'WAERS': random.choice(CURRENCIES),
                'BEDAT': order_date,
                'KDATB': order_date + timedelta(days=random.randint(1, 30)),
                'KDATE': order_date + timedelta(days=random.randint(60, 365)),
                'ZTERM': random.choice(PAYMENT_TERMS),
                'INCO1': random.choice(['EXW', 'FCA', 'CPT', 'CIP', 'DAP', 'DDP']),
                'INCO2': fake.city()[:28],
                'ERNAM': fake.user_name()[:12],
                'AEDAT': order_date,
                'FRGKE': 'X' if approval_status == 'approved' else '',
                'FRGZU': approval_status.upper(),
                'PROCSTAT': '05' if approval_status == 'approved' else ('03' if approval_status == 'pending' else '01'),
                'MEMORY': '' if random.random() > 0.1 else 'X'
            }
            po_headers.append(po_header)
            
            # Generate 1-5 line items per PO
            num_items = random.randint(1, 5)
            for item_num in range(1, num_items + 1):
                po_item = {
                    'EBELN': po_number,
                    'EBELP': f"{item_num:05d}",
                    'MATNR': f"M{random.randint(100000, 999999):06d}",
                    'TXZ01': fake.catch_phrase()[:40],
                    'MENGE': round(random.uniform(1, 1000), 2),
                    'MEINS': random.choice(['EA', 'KG', 'M', 'L', 'PC']),
                    'NETPR': round(random.uniform(10, 5000), 2),
                    'PEINH': 1,
                    'NETWR': 0,
                    'WERKS': f"{company_code[:2]}01",
                    'LGORT': '0001',
                    'MATKL': f"0{random.randint(1000, 9999)}",
                    'KOSTL': random.choice(COST_CENTERS[region]),
                    'EINDT': order_date + timedelta(days=random.randint(7, 60)),
                    'UEBTK': '' if random.random() > 0.1 else 'X',
                    'UNTTO': round(random.uniform(0, 10), 1),
                    'UEBTO': round(random.uniform(0, 10), 1),
                    'EREKZ': '' if random.random() > 0.05 else 'X',
                    'REPOS': '' if random.random() > 0.03 else 'X'
                }
                po_item['NETWR'] = round(po_item['MENGE'] * po_item['NETPR'], 2)
                po_items.append(po_item)
        
        return po_headers, po_items
    
    def generate_vendor_invoices(self, po_headers, po_items, count=2000):
        """Generate RBKP (Vendor Invoice Header) and related documents"""
        invoices = []
        accounting_docs = []
        
        # Filter approved POs
        approved_pos = [po for po in po_headers if po['FRGKE'] == 'X']
        
        for i in range(count):
            po = random.choice(approved_pos)
            po_items_for_po = [item for item in po_items if item['EBELN'] == po['EBELN']]
            
            # Convert PO date to date object
            po_date = safe_date_convert(po['BEDAT'])
            
            # Generate invoice 1-45 days after PO (realistic processing time)
            invoice_date = fake.date_between(
                start_date=po_date + timedelta(days=1),
                end_date=min(po_date + timedelta(days=45), END_DATE)
            )
            
            # Simulate approval workflow
            approval_status = random.choices(
                ['approved', 'pending', 'rejected', 'parked'],
                weights=[70, 15, 5, 10]
            )[0]
            
            invoice_number = f"INV{50000000 + i:010d}"
            vendor_invoice_ref = fake.lexify('???-#######')
            
            total_amount = sum([item['NETWR'] for item in po_items_for_po])
            tax_amount = round(total_amount * random.uniform(0.05, 0.25), 2)
            
            invoice = {
                'BELNR': invoice_number,
                'BUKRS': po['BUKRS'],
                'GJAHR': invoice_date.year,
                'BLART': 'RE',
                'BLDAT': invoice_date,
                'BUDAT': invoice_date,
                'XBLNR': vendor_invoice_ref,
                'LIFNR': po['LIFNR'],
                'WAERS': po['WAERS'],
                'RMWWR': total_amount,
                'WMWST1': tax_amount,
                'EBELN': po['EBELN'],
                'USNAM': fake.user_name()[:12],
                'CPUDT': invoice_date,
                'CPUTM': fake.time(),
                'TCODE': 'MIRO',
                'STBLG': '' if approval_status != 'rejected' else invoice_number,
                'STJAH': '' if approval_status != 'rejected' else str(invoice_date.year)
            }
            invoices.append(invoice)
            
            # Generate BSEG entries for the invoice
            line_item_counter = 1
            
            # Vendor line (credit)
            vendor_line = {
                'BUKRS': po['BUKRS'],
                'BELNR': invoice_number,
                'GJAHR': invoice_date.year,
                'BUZEI': f"{line_item_counter:03d}",
                'KOART': 'K',
                'KONTO': po['LIFNR'],
                'DMBTR': -(total_amount + tax_amount),
                'WRBTR': -(total_amount + tax_amount),
                'SHKZG': 'H',
                'WAERS': po['WAERS'],
                'ZTERM': po['ZTERM'],
                'ZBD1T': PAYMENT_TERMS_DAYS[po['ZTERM']],
                'BLDAT': invoice_date,
                'BUDAT': invoice_date,
                'KOSTL': '',
                'AUGDT': None,
                'AUGBL': ''
            }
            
            # Calculate payment due date
            payment_due = invoice_date + timedelta(days=PAYMENT_TERMS_DAYS[po['ZTERM']])
            
            # Realistic payment simulation
            if approval_status == 'approved' and random.random() < 0.8:
                payment_behavior = random.choices(
                    ['early_on_time', 'late'],
                    weights=[75, 25]
                )[0]
                
                if payment_behavior == 'early_on_time':
                    payment_start = invoice_date + timedelta(days=max(1, PAYMENT_TERMS_DAYS[po['ZTERM']] - 5))
                    payment_end = payment_due + timedelta(days=10)
                else:
                    payment_start = payment_due + timedelta(days=11)
                    payment_end = payment_due + timedelta(days=60)
                
                # Generate payment if date falls within our data range
                if payment_start <= END_DATE:
                    actual_payment_end = min(payment_end, END_DATE)
                    if payment_start <= actual_payment_end:
                        payment_date = fake.date_between(
                            start_date=payment_start,
                            end_date=actual_payment_end
                        )
                        vendor_line['AUGDT'] = payment_date
                        vendor_line['AUGBL'] = f"PAY{random.randint(10000000, 99999999):08d}"
            
            accounting_docs.append(vendor_line)
            line_item_counter += 1
            
            # Expense lines (debit)
            for po_item in po_items_for_po:
                expense_line = {
                    'BUKRS': po['BUKRS'],
                    'BELNR': invoice_number,
                    'GJAHR': invoice_date.year,
                    'BUZEI': f"{line_item_counter:03d}",
                    'KOART': 'S',
                    'KONTO': random.choice(['6000000', '6100000', '6200000']),
                    'DMBTR': po_item['NETWR'],
                    'WRBTR': po_item['NETWR'],
                    'SHKZG': 'S',
                    'WAERS': po['WAERS'],
                    'ZTERM': '',
                    'ZBD1T': 0,
                    'BLDAT': invoice_date,
                    'BUDAT': invoice_date,
                    'KOSTL': po_item['KOSTL'],
                    'AUGDT': None,
                    'AUGBL': ''
                }
                accounting_docs.append(expense_line)
                line_item_counter += 1
            
            # Tax line (debit)
            if tax_amount > 0:
                tax_line = {
                    'BUKRS': po['BUKRS'],
                    'BELNR': invoice_number,
                    'GJAHR': invoice_date.year,
                    'BUZEI': f"{line_item_counter:03d}",
                    'KOART': 'S',
                    'KONTO': '1500000',
                    'DMBTR': tax_amount,
                    'WRBTR': tax_amount,
                    'SHKZG': 'S',
                    'WAERS': po['WAERS'],
                    'ZTERM': '',
                    'ZBD1T': 0,
                    'BLDAT': invoice_date,
                    'BUDAT': invoice_date,
                    'KOSTL': '',
                    'AUGDT': None,
                    'AUGBL': ''
                }
                accounting_docs.append(tax_line)
        
        return invoices, accounting_docs
    
    def generate_sales_invoices(self, customers, count=1800):
        """Generate VBRK (Billing Document Header) and related accounting entries"""
        sales_invoices = []
        sales_accounting = []
        
        for i in range(count):
            customer = random.choice(customers)
            region = [k for k, v in REGIONS.items() if customer['LAND1'] in v][0]
            company_code = random.choice(COMPANY_CODES[region])
            
            # Weight invoice dates toward analysis focus year (2024) but allow full range
            if random.random() < 0.7:
                focus_start = date(ANALYSIS_FOCUS_YEAR, 1, 1)
                focus_end = date(ANALYSIS_FOCUS_YEAR, 12, 31)
                invoice_date = fake.date_between(start_date=focus_start, end_date=focus_end)
            else:
                invoice_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
            
            invoice_number = f"90{random.randint(10000000, 99999999):08d}"
            
            net_amount = round(random.uniform(1000, 50000), 2)
            tax_rate = random.uniform(0.05, 0.25)
            tax_amount = round(net_amount * tax_rate, 2)
            gross_amount = net_amount + tax_amount
            
            # Sales invoice header
            sales_invoice = {
                'VBELN': invoice_number,
                'FKART': 'F2',
                'FKDAT': invoice_date,
                'BUKRS': company_code,
                'KUNRG': customer['KUNNR'],
                'KUNAG': customer['KUNNR'],
                'WAERK': random.choice(CURRENCIES),
                'NETWR': net_amount,
                'MWSBP': tax_amount,
                'RFBSK': 'C' if random.random() < 0.95 else 'A',
                'ERDAT': invoice_date,
                'ERNAM': fake.user_name()[:12],
                'FKSTO': '' if random.random() > 0.02 else 'X',
                'VBTYP': 'M',
                'SFAKN': '',
                'KNUMV': f"{random.randint(1000000000, 9999999999):010d}"
            }
            sales_invoices.append(sales_invoice)
            
            # Generate accounting entries if released
            if sales_invoice['RFBSK'] == 'C':
                accounting_doc_number = f"AC{random.randint(10000000, 99999999):08d}"
                selected_payment_terms = random.choice(PAYMENT_TERMS)
                
                # Customer receivable (debit)
                customer_line = {
                    'BUKRS': company_code,
                    'BELNR': accounting_doc_number,
                    'GJAHR': invoice_date.year,
                    'BUZEI': '001',
                    'KOART': 'D',
                    'KONTO': customer['KUNNR'],
                    'DMBTR': gross_amount,
                    'WRBTR': gross_amount,
                    'SHKZG': 'S',
                    'WAERS': sales_invoice['WAERK'],
                    'ZTERM': selected_payment_terms,
                    'ZBD1T': PAYMENT_TERMS_DAYS[selected_payment_terms],
                    'BLDAT': invoice_date,
                    'BUDAT': invoice_date,
                    'KOSTL': '',
                    'AUGDT': None,
                    'AUGBL': ''
                }
                
                # Calculate payment due date
                payment_due = invoice_date + timedelta(days=PAYMENT_TERMS_DAYS[selected_payment_terms])
                
                # Realistic customer payment simulation
                if random.random() < 0.75:
                    payment_behavior = random.choices(
                        ['early_on_time', 'late'],
                        weights=[67, 33]
                    )[0]
                    
                    if payment_behavior == 'early_on_time':
                        payment_start = invoice_date + timedelta(days=max(1, PAYMENT_TERMS_DAYS[selected_payment_terms] - 3))
                        payment_end = payment_due + timedelta(days=15)
                    else:
                        payment_start = payment_due + timedelta(days=16)
                        payment_end = payment_due + timedelta(days=90)
                    
                    # Generate payment if date falls within our data range
                    if payment_start <= END_DATE:
                        actual_payment_end = min(payment_end, END_DATE)
                        if payment_start <= actual_payment_end:
                            payment_date = fake.date_between(
                                start_date=payment_start,
                                end_date=actual_payment_end
                            )
                            customer_line['AUGDT'] = payment_date
                            customer_line['AUGBL'] = f"REC{random.randint(10000000, 99999999):08d}"
                
                sales_accounting.append(customer_line)
                
                # Revenue (credit)
                revenue_line = {
                    'BUKRS': company_code,
                    'BELNR': accounting_doc_number,
                    'GJAHR': invoice_date.year,
                    'BUZEI': '002',
                    'KOART': 'S',
                    'KONTO': random.choice(['4000000', '4100000', '4200000']),
                    'DMBTR': -net_amount,
                    'WRBTR': -net_amount,
                    'SHKZG': 'H',
                    'WAERS': sales_invoice['WAERK'],
                    'ZTERM': '',
                    'ZBD1T': 0,
                    'BLDAT': invoice_date,
                    'BUDAT': invoice_date,
                    'KOSTL': random.choice(COST_CENTERS[region]),
                    'AUGDT': None,
                    'AUGBL': ''
                }
                sales_accounting.append(revenue_line)
                
                # Output tax (credit)
                if tax_amount > 0:
                    tax_line = {
                        'BUKRS': company_code,
                        'BELNR': accounting_doc_number,
                        'GJAHR': invoice_date.year,
                        'BUZEI': '003',
                        'KOART': 'S',
                        'KONTO': '2300000',
                        'DMBTR': -tax_amount,
                        'WRBTR': -tax_amount,
                        'SHKZG': 'H',
                        'WAERS': sales_invoice['WAERK'],
                        'ZTERM': '',
                        'ZBD1T': 0,
                        'BLDAT': invoice_date,
                        'BUDAT': invoice_date,
                        'KOSTL': '',
                        'AUGDT': None,
                        'AUGBL': ''
                    }
                    sales_accounting.append(tax_line)
        
        return sales_invoices, sales_accounting
    
    def generate_all_data(self):
        """Generate all SAP data and return as dictionaries"""
        print("Generating vendors...")
        vendors, vendor_company_data, vendor_purchasing_data = self.generate_vendors()
        
        print("Generating customers...")
        customers = self.generate_customers()
        
        print("Generating payment terms...")
        payment_terms = self.generate_payment_terms()
        
        print("Generating purchase orders...")
        po_headers, po_items = self.generate_purchase_orders(vendors)
        
        print("Generating vendor invoices...")
        vendor_invoices, vendor_accounting = self.generate_vendor_invoices(po_headers, po_items)
        
        print("Generating sales invoices...")
        sales_invoices, sales_accounting = self.generate_sales_invoices(customers)
        
        # Combine all accounting entries
        all_accounting = vendor_accounting + sales_accounting
        
        return {
            'LFA1': vendors,
            'LFB1': vendor_company_data,
            'LFM1': vendor_purchasing_data,
            'KNA1': customers,
            'T052': payment_terms,
            'EKKO': po_headers,
            'EKPO': po_items,
            'RBKP': vendor_invoices,
            'VBRK': sales_invoices,
            'BSEG': all_accounting
        }
    
    def create_sql_script(self, data):
        """Generate SQL script to create tables and insert data"""
        sql_script = """
-- SAP Dummy Data SQL Script
-- Generated for PowerBI Dashboard Demo

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

"""
        
        # Table creation statements
        table_definitions = {
            'LFA1': """
CREATE TABLE LFA1 (
    LIFNR VARCHAR(10) PRIMARY KEY,    -- Vendor account number
    NAME1 VARCHAR(35),                -- Name 1
    SORTL VARCHAR(10),                -- Sort field
    STRAS VARCHAR(35),                -- Street address
    ORT01 VARCHAR(35),                -- City
    PSTLZ VARCHAR(10),                -- Postal code
    LAND1 VARCHAR(3),                 -- Country key
    SPRAS VARCHAR(1),                 -- Language key
    TELF1 VARCHAR(16),                -- Telephone 1
    TELFX VARCHAR(31),                -- Fax number
    SMTP_ADDR VARCHAR(241),           -- Email address
    KTOKK VARCHAR(4),                 -- Vendor account group
    ERDAT DATE,                       -- Created on
    ERNAM VARCHAR(12),                -- Created by
    SPERR VARCHAR(1),                 -- Central posting block
    LOEVM VARCHAR(1)                  -- Central deletion flag
);
""",
            'LFB1': """
CREATE TABLE LFB1 (
    LIFNR VARCHAR(10),                -- Vendor account number
    BUKRS VARCHAR(4),                 -- Company code
    AKONT VARCHAR(10),                -- Reconciliation account
    ZTERM VARCHAR(4),                 -- Payment terms
    REPRF VARCHAR(1),                 -- Double invoice check
    ZWELS VARCHAR(10),                -- Payment methods
    ZAHLS VARCHAR(1),                 -- Payment block
    FDGRV VARCHAR(10),                -- Planning group
    SPERR VARCHAR(1),                 -- Posting block
    PRIMARY KEY (LIFNR, BUKRS),
    FOREIGN KEY (LIFNR) REFERENCES LFA1(LIFNR)
);
""",
            'LFM1': """
CREATE TABLE LFM1 (
    LIFNR VARCHAR(10),                -- Vendor account number
    EKORG VARCHAR(4),                 -- Purchasing organization
    SPERM VARCHAR(1),                 -- Purchasing block
    LIFER VARCHAR(35),                -- Vendor sub-range
    LIBES VARCHAR(1),                 -- Order confirmation required
    LIPRE VARCHAR(1),                 -- Price comparison
    LISER VARCHAR(1),                 -- Service-based invoice verification
    ZTERM VARCHAR(4),                 -- Payment terms
    INCO1 VARCHAR(3),                 -- Incoterms part 1
    INCO2 VARCHAR(28),                -- Incoterms part 2
    WAERS VARCHAR(5),                 -- Currency
    PRIMARY KEY (LIFNR, EKORG),
    FOREIGN KEY (LIFNR) REFERENCES LFA1(LIFNR)
);
""",
            'KNA1': """
CREATE TABLE KNA1 (
    KUNNR VARCHAR(10) PRIMARY KEY,    -- Customer number
    NAME1 VARCHAR(35),                -- Name 1
    SORTL VARCHAR(10),                -- Sort field
    STRAS VARCHAR(35),                -- Street address
    ORT01 VARCHAR(35),                -- City
    PSTLZ VARCHAR(10),                -- Postal code
    LAND1 VARCHAR(3),                 -- Country key
    SPRAS VARCHAR(1),                 -- Language key
    TELF1 VARCHAR(16),                -- Telephone 1
    TELFX VARCHAR(31),                -- Fax number
    SMTP_ADDR VARCHAR(241),           -- Email address
    KTOKD VARCHAR(4),                 -- Customer account group
    ERDAT DATE,                       -- Created on
    ERNAM VARCHAR(12),                -- Created by
    SPERR VARCHAR(1),                 -- Central posting block
    LOEVM VARCHAR(1)                  -- Central deletion flag
);
""",
            'T052': """
CREATE TABLE T052 (
    ZTERM VARCHAR(4) PRIMARY KEY,     -- Payment terms key
    SPRAS VARCHAR(1),                 -- Language
    TEXT1 VARCHAR(50),                -- Description
    ZTAG1 INTEGER,                    -- Days 1
    ZPRZ1 DECIMAL(5,3),              -- Percentage 1
    ZMTAG INTEGER,                    -- Additional months
    ZTAG2 INTEGER,                    -- Days 2
    ZPRZ2 DECIMAL(5,3),              -- Percentage 2
    ZTAG3 INTEGER,                    -- Days 3
    ZPRZ3 DECIMAL(5,3)               -- Percentage 3
);
""",
            'EKKO': """
CREATE TABLE EKKO (
    EBELN VARCHAR(10) PRIMARY KEY,    -- Purchase document number
    BUKRS VARCHAR(4),                 -- Company code
    BSTYP VARCHAR(1),                 -- Purchasing document category
    BSART VARCHAR(4),                 -- Purchasing document type
    LIFNR VARCHAR(10),                -- Vendor account number
    EKORG VARCHAR(4),                 -- Purchasing organization
    EKGRP VARCHAR(3),                 -- Purchasing group
    WAERS VARCHAR(5),                 -- Currency
    BEDAT DATE,                       -- Purchase document date
    KDATB DATE,                       -- Validity start date
    KDATE DATE,                       -- Validity end date
    ZTERM VARCHAR(4),                 -- Payment terms
    INCO1 VARCHAR(3),                 -- Incoterms part 1
    INCO2 VARCHAR(28),                -- Incoterms part 2
    ERNAM VARCHAR(12),                -- Created by
    AEDAT DATE,                       -- Changed on
    FRGKE VARCHAR(1),                 -- Release indicator
    FRGZU VARCHAR(2),                 -- Release state
    PROCSTAT VARCHAR(2),              -- Procurement process status
    MEMORY VARCHAR(1),                -- Incomplete indicator
    FOREIGN KEY (LIFNR) REFERENCES LFA1(LIFNR),
    FOREIGN KEY (ZTERM) REFERENCES T052(ZTERM)
);
""",
            'EKPO': """
CREATE TABLE EKPO (
    EBELN VARCHAR(10),                -- Purchase document number
    EBELP VARCHAR(5),                 -- Purchase document item number
    MATNR VARCHAR(18),                -- Material number
    TXZ01 VARCHAR(40),                -- Short text
    MENGE DECIMAL(13,3),              -- Purchase order quantity
    MEINS VARCHAR(3),                 -- Order unit
    NETPR DECIMAL(11,2),              -- Net price
    PEINH DECIMAL(5,0),               -- Price unit
    NETWR DECIMAL(13,2),              -- Net order value
    WERKS VARCHAR(4),                 -- Plant
    LGORT VARCHAR(4),                 -- Storage location
    MATKL VARCHAR(9),                 -- Material group
    KOSTL VARCHAR(10),                -- Cost center
    EINDT DATE,                       -- Delivery date
    UEBTK VARCHAR(1),                 -- Unlimited overdelivery allowed
    UNTTO DECIMAL(3,1),               -- Underdelivery tolerance
    UEBTO DECIMAL(3,1),               -- Overdelivery tolerance
    EREKZ VARCHAR(1),                 -- Final invoice indicator
    REPOS VARCHAR(1),                 -- Invoice receipt indicator
    PRIMARY KEY (EBELN, EBELP),
    FOREIGN KEY (EBELN) REFERENCES EKKO(EBELN)
);
""",
            'RBKP': """
CREATE TABLE RBKP (
    BELNR VARCHAR(10),                -- Document number
    BUKRS VARCHAR(4),                 -- Company code
    GJAHR INTEGER,                    -- Fiscal year
    BLART VARCHAR(2),                 -- Document type
    BLDAT DATE,                       -- Document date
    BUDAT DATE,                       -- Posting date
    XBLNR VARCHAR(16),                -- Reference document number
    LIFNR VARCHAR(10),                -- Vendor account number
    WAERS VARCHAR(5),                 -- Currency
    RMWWR DECIMAL(13,2),              -- Gross invoice amount
    WMWST1 DECIMAL(13,2),             -- Tax amount
    EBELN VARCHAR(10),                -- Purchase order number
    USNAM VARCHAR(12),                -- User name
    CPUDT DATE,                       -- Entry date
    CPUTM TIME,                       -- Entry time
    TCODE VARCHAR(20),                -- Transaction code
    STBLG VARCHAR(10),                -- Reversal document number
    STJAH INTEGER,                    -- Reversal fiscal year
    PRIMARY KEY (BELNR, BUKRS, GJAHR),
    FOREIGN KEY (LIFNR) REFERENCES LFA1(LIFNR),
    FOREIGN KEY (EBELN) REFERENCES EKKO(EBELN)
);
""",
            'VBRK': """
CREATE TABLE VBRK (
    VBELN VARCHAR(10) PRIMARY KEY,    -- Billing document
    FKART VARCHAR(4),                 -- Billing type
    FKDAT DATE,                       -- Billing date
    BUKRS VARCHAR(4),                 -- Company code
    KUNRG VARCHAR(10),                -- Payer
    KUNAG VARCHAR(10),                -- Sold-to party
    WAERK VARCHAR(5),                 -- Currency
    NETWR DECIMAL(15,2),              -- Net value
    MWSBP DECIMAL(13,2),              -- Tax amount
    RFBSK VARCHAR(1),                 -- Status for transfer to accounting
    ERDAT DATE,                       -- Created on
    ERNAM VARCHAR(12),                -- Created by
    FKSTO VARCHAR(1),                 -- Billing document is cancelled
    VBTYP VARCHAR(1),                 -- Document category
    SFAKN VARCHAR(10),                -- Cancellation document
    KNUMV VARCHAR(10),                -- Document condition
    FOREIGN KEY (KUNRG) REFERENCES KNA1(KUNNR),
    FOREIGN KEY (KUNAG) REFERENCES KNA1(KUNNR)
);
""",
            'BSEG': """
CREATE TABLE BSEG (
    BUKRS VARCHAR(4),                 -- Company code
    BELNR VARCHAR(10),                -- Document number
    GJAHR INTEGER,                    -- Fiscal year
    BUZEI VARCHAR(3),                 -- Line item number
    KOART VARCHAR(1),                 -- Account type
    KONTO VARCHAR(10),                -- Account number
    DMBTR DECIMAL(13,2),              -- Amount in local currency
    WRBTR DECIMAL(13,2),              -- Amount in document currency
    SHKZG VARCHAR(1),                 -- Debit/Credit indicator
    WAERS VARCHAR(5),                 -- Currency
    ZTERM VARCHAR(4),                 -- Payment terms
    ZBD1T INTEGER,                    -- Cash discount days 1
    BLDAT DATE,                       -- Document date
    BUDAT DATE,                       -- Posting date
    KOSTL VARCHAR(10),                -- Cost center
    AUGDT DATE,                       -- Clearing date
    AUGBL VARCHAR(10),                -- Clearing document
    PRIMARY KEY (BUKRS, BELNR, GJAHR, BUZEI),
    FOREIGN KEY (ZTERM) REFERENCES T052(ZTERM)
);
"""
        }
        
        # Add table creation statements
        for table_name, create_stmt in table_definitions.items():
            sql_script += create_stmt + "\n"
        
        # Define standard field structure for each table
        standard_fields = {
            'LFA1': ['LIFNR', 'NAME1', 'SORTL', 'STRAS', 'ORT01', 'PSTLZ', 'LAND1', 'SPRAS', 'TELF1', 'TELFX', 'SMTP_ADDR', 'KTOKK', 'ERDAT', 'ERNAM', 'SPERR', 'LOEVM'],
            'LFB1': ['LIFNR', 'BUKRS', 'AKONT', 'ZTERM', 'REPRF', 'ZWELS', 'ZAHLS', 'FDGRV', 'SPERR'],
            'LFM1': ['LIFNR', 'EKORG', 'SPERM', 'LIFER', 'LIBES', 'LIPRE', 'LISER', 'ZTERM', 'INCO1', 'INCO2', 'WAERS'],
            'KNA1': ['KUNNR', 'NAME1', 'SORTL', 'STRAS', 'ORT01', 'PSTLZ', 'LAND1', 'SPRAS', 'TELF1', 'TELFX', 'SMTP_ADDR', 'KTOKD', 'ERDAT', 'ERNAM', 'SPERR', 'LOEVM'],
            'T052': ['ZTERM', 'SPRAS', 'TEXT1', 'ZTAG1', 'ZPRZ1', 'ZMTAG', 'ZTAG2', 'ZPRZ2', 'ZTAG3', 'ZPRZ3'],
            'EKKO': ['EBELN', 'BUKRS', 'BSTYP', 'BSART', 'LIFNR', 'EKORG', 'EKGRP', 'WAERS', 'BEDAT', 'KDATB', 'KDATE', 'ZTERM', 'INCO1', 'INCO2', 'ERNAM', 'AEDAT', 'FRGKE', 'FRGZU', 'PROCSTAT', 'MEMORY'],
            'EKPO': ['EBELN', 'EBELP', 'MATNR', 'TXZ01', 'MENGE', 'MEINS', 'NETPR', 'PEINH', 'NETWR', 'WERKS', 'LGORT', 'MATKL', 'KOSTL', 'EINDT', 'UEBTK', 'UNTTO', 'UEBTO', 'EREKZ', 'REPOS'],
            'RBKP': ['BELNR', 'BUKRS', 'GJAHR', 'BLART', 'BLDAT', 'BUDAT', 'XBLNR', 'LIFNR', 'WAERS', 'RMWWR', 'WMWST1', 'EBELN', 'USNAM', 'CPUDT', 'CPUTM', 'TCODE', 'STBLG', 'STJAH'],
            'VBRK': ['VBELN', 'FKART', 'FKDAT', 'BUKRS', 'KUNRG', 'KUNAG', 'WAERK', 'NETWR', 'MWSBP', 'RFBSK', 'ERDAT', 'ERNAM', 'FKSTO', 'VBTYP', 'SFAKN', 'KNUMV'],
            'BSEG': ['BUKRS', 'BELNR', 'GJAHR', 'BUZEI', 'KOART', 'KONTO', 'DMBTR', 'WRBTR', 'SHKZG', 'WAERS', 'ZTERM', 'ZBD1T', 'BLDAT', 'BUDAT', 'KOSTL', 'AUGDT', 'AUGBL']
        }
        
        # Add data insertion statements
        for table_name, records in data.items():
            if records:
                sql_script += f"\n-- Insert data into {table_name}\n"
                
                # Use standard field structure
                columns = standard_fields.get(table_name, list(records[0].keys()))
                columns_str = ', '.join(columns)
                
                sql_script += f"INSERT INTO {table_name} ({columns_str}) VALUES\n"
                
                value_statements = []
                for record in records:
                    values = []
                    for col in columns:
                        # Handle missing keys gracefully
                        value = record.get(col, None)
                        if value is None or value == '':
                            values.append('NULL')
                        elif isinstance(value, str):
                            # Escape single quotes and limit length
                            escaped_value = str(value).replace("'", "''")
                            values.append(f"'{escaped_value}'")
                        elif isinstance(value, (int, float)):
                            values.append(str(value))
                        elif isinstance(value, (datetime, date)):
                            if hasattr(value, 'strftime'):
                                values.append(f"'{value.strftime('%Y-%m-%d')}'")
                            else:
                                values.append(f"'{str(value)}'")
                        else:
                            values.append(f"'{str(value)}'")
                    
                    value_statements.append(f"({', '.join(values)})")
                
                # Split into chunks to avoid SQL statement size limits
                chunk_size = 100
                for i in range(0, len(value_statements), chunk_size):
                    chunk = value_statements[i:i + chunk_size]
                    if i == 0:
                        sql_script += ',\n'.join(chunk)
                    else:
                        sql_script += f";\n\nINSERT INTO {table_name} ({columns_str}) VALUES\n"
                        sql_script += ',\n'.join(chunk)
                
                sql_script += ";\n\n"
        
        return sql_script

def main():
    """Main function to generate SAP data and create SQL script"""
    generator = SAPDataGenerator()
    
    print("Starting SAP data generation...")
    data = generator.generate_all_data()
    
    print("Creating SQL script...")
    sql_script = generator.create_sql_script(data)
    
    # Save to file
    with open('sap_dummy_data.sql', 'w', encoding='utf-8') as f:
        f.write(sql_script)
    
    print(f"SQL script generated successfully: sap_dummy_data.sql")
    
    # Print summary statistics
    print("\nData Generation Summary:")
    print("=" * 60)
    for table_name, records in data.items():
        print(f"{table_name}: {len(records):,} records")
    
    print(f"\nTotal records generated: {sum(len(records) for records in data.values()):,}")
    
    # Print data range and analysis recommendations
    print(f"\nData Range: {START_DATE} to {END_DATE}")
    print(f"Primary Analysis Year: {ANALYSIS_FOCUS_YEAR}")
    print("\nRecommended PowerBI Filters:")
    print(f"  - Transaction Analysis: {ANALYSIS_FOCUS_YEAR}-01-01 to {ANALYSIS_FOCUS_YEAR}-12-31")
    print(f"  - Payment Analysis: {ANALYSIS_FOCUS_YEAR}-01-01 to {END_DATE}")
    print(f"  - Outstanding Items: Filter AUGDT IS NULL for unpaid items")
    
    # Print payment terms summary
    print(f"\nPayment Terms Generated:")
    for term, days in PAYMENT_TERMS_DAYS.items():
        print(f"  {term}: {days} days")
    
    print(f"\nRealistic Business Scenarios:")
    print(f"  - Late 2024 transactions may have payments extending into 2025")
    print(f"  - NULL payment dates represent realistic unpaid/overdue items")
    print(f"  - Payment terms up to 120 days simulate enterprise scenarios")
    
    return data, sql_script

if __name__ == "__main__":
    data, sql_script = main()