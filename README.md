# SAP Dummy Data Generator

Python script that generates realistic SAP transaction data for data analysis. This tool creates authentic business scenarios across Procure-to-Pay (P2P) and Order-to-Cash (O2C) workflows with enterprise-grade complexity.

## Overview

This generator produces **15,000+ records** across **10 authentic SAP tables** with realistic business logic, multi-regional operations, and sophisticated payment behaviours. Perfect for:

- **Power BI Dashboard Development** - Test with realistic data volumes and patterns
- **Analytics Training** - Practise with authentic SAP data structures  
- **Process Analysis** - Understand P2P and O2C workflows
- **Performance Testing** - Validate reports with enterprise-scale datasets

## Key Features

- **Multi-Regional Operations** - 5 regions (NA, EU, APAC, LATAM, MEA) with 10 currencies
- **Extended Business Cycles** - 27-month data range supporting cross-year payment scenarios
- **Realistic Payment Behaviour** - On-time vs. late payments with authentic patterns
- **Complete Workflows** - Full P2P and O2C processes with approval stages
- **Enterprise Payment Terms** - 0-120 day terms including government contracts
- **Authentic NULL Values** - Realistic unpaid/overdue scenarios for ageing analysis
- **Global Company Structure** - Multi-company codes with regional cost centres

## Quick Start

### Prerequisites
- Python 3.9+
- Conda (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/almoraqi/sap-dummy-data-generator.git
   cd sap-dummy-data-generator
   ```

2. **Create conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate sap-data-generator
   ```

3. **Generate data**
   ```bash
   python sap_data_generator.py
   ```

4. **Output files**
   - `sap_dummy_data.sql` - Complete SQL script with DDL and data
   - Database summary with 15,000+ records across 10 tables

## Generated Tables

| Table | Purpose | Records | Description |
|-------|---------|---------|-------------|
| **LFA1** | Vendor Master | 200 | Global vendor information |
| **LFB1** | Vendor Company Data | 400+ | Company-specific vendor settings |
| **LFM1** | Vendor Purchasing | 200 | Purchasing organisation data |
| **KNA1** | Customer Master | 150 | Global customer information |
| **T052** | Payment Terms | 9 | Realistic payment term configurations |
| **EKKO** | Purchase Orders | 1,500 | PO headers with approval workflows |
| **EKPO** | PO Line Items | 4,500+ | Detailed purchase order items |
| **RBKP** | Vendor Invoices | 2,000 | Invoice headers with processing status |
| **VBRK** | Sales Invoices | 1,800 | Customer billing documents |
| **BSEG** | Accounting Entries | 8,000+ | Complete financial postings |

## Realistic Business Scenarios Implemented

### Enterprise-Grade Realism
Our data generator implements sophisticated business logic to create authentic SAP data that mirrors real-world operations:

#### Extended Business Cycles
- **Data Range**: 2023-01-01 to 2025-03-31 (27 months)
- **Analysis Focus**: 2024 (70% of transactions weighted to this year)
- **Cross-Year Payments**: Late 2024 invoices naturally flow into 2025 payments
- **Seasonal Patterns**: Holiday delays, fiscal year-end processing

#### Realistic Payment Behaviour
- **Vendor Payments**: 75% on-time, 25% late (11-60 days after due)
- **Customer Payments**: 67% on-time, 33% late (16-90 days after due)
- **Payment Terms**: 0-120 days (including enterprise/government contracts)
- **Early Payment Discounts**: 2/10 Net 30, 2.5/14 Net 60, etc.

#### Authentic NULL Values
- **Unpaid Invoices**: Payments beyond END_DATE remain NULL (realistic)
- **Overdue Analysis**: Natural ageing buckets for Power BI dashboards
- **Cash Flow Forecasting**: Outstanding items show realistic collection patterns

#### Global Operations
- **Multi-Regional**: NA, EU, APAC, LATAM, MEA with region-specific patterns
- **Multi-Currency**: 10 currencies with realistic exchange scenarios
- **Regional Cost Centres**: Authentic organisational structures

#### Approval Workflows
- **Purchase Orders**: 85% approved, 10% pending, 5% rejected
- **Invoice Processing**: 70% approved, 15% pending, 5% rejected, 10% parked
- **Processing Delays**: 1-45 days PO to invoice timing

## Master Data Tables

### LFA1 - Vendor Master (General Section)
**Purpose**: Contains general vendor master data that is valid across all company codes.

| Field | Description | Type | Purpose |
|-------|-------------|------|---------|
| LIFNR | Vendor account number | VARCHAR(10) | Primary key, unique vendor identifier |
| NAME1 | Name 1 | VARCHAR(35) | Vendor company name |
| SORTL | Sort field | VARCHAR(10) | Search term for vendor |
| STRAS | Street address | VARCHAR(35) | Vendor street address |
| ORT01 | City | VARCHAR(35) | Vendor city |
| PSTLZ | Postal code | VARCHAR(10) | Vendor postal/ZIP code |
| LAND1 | Country key | VARCHAR(3) | ISO country code |
| SPRAS | Language key | VARCHAR(1) | Communication language |
| TELF1 | Telephone 1 | VARCHAR(16) | Primary phone number |
| TELFX | Fax number | VARCHAR(31) | Fax number |
| SMTP_ADDR | Email address | VARCHAR(241) | Email address |
| KTOKK | Vendor account group | VARCHAR(4) | Controls field status and number ranges |
| ERDAT | Created on | DATE | Record creation date |
| ERNAM | Created by | VARCHAR(12) | User who created the record |
| SPERR | Central posting block | VARCHAR(1) | Blocks all postings to vendor |
| LOEVM | Central deletion flag | VARCHAR(1) | Marks vendor for deletion |

### LFB1 - Vendor Master (Company Code Section)
**Purpose**: Contains vendor data specific to individual company codes, including accounting information.

| Field | Description | Type | Purpose |
|-------|-------------|------|---------|
| LIFNR | Vendor account number | VARCHAR(10) | Foreign key to LFA1 |
| BUKRS | Company code | VARCHAR(4) | Company code identifier |
| AKONT | Reconciliation account | VARCHAR(10) | G/L account for vendor postings |
| ZTERM | Payment terms | VARCHAR(4) | Default payment terms |
| REPRF | Double invoice check | VARCHAR(1) | Enable duplicate invoice checking |
| ZWELS | Payment methods | VARCHAR(10) | Allowed payment methods |
| ZAHLS | Payment block | VARCHAR(1) | Block automatic payments |
| FDGRV | Planning group | VARCHAR(10) | For cash management planning |
| SPERR | Posting block | VARCHAR(1) | Block postings in this company code |

### LFM1 - Vendor Master (Purchasing Section)
**Purpose**: Contains vendor data specific to purchasing organisations.

| Field | Description | Type | Purpose |
|-------|-------------|------|---------|
| LIFNR | Vendor account number | VARCHAR(10) | Foreign key to LFA1 |
| EKORG | Purchasing organisation | VARCHAR(4) | Purchasing organisation identifier |
| SPERM | Purchasing block | VARCHAR(1) | Block purchase orders |
| LIFER | Vendor sub-range | VARCHAR(35) | Sub-range indicator |
| LIBES | Order confirmation required | VARCHAR(1) | Vendor must confirm orders |
| LIPRE | Price comparison | VARCHAR(1) | Include in price comparisons |
| LISER | Service-based invoice verification | VARCHAR(1) | Enable service entry sheets |
| ZTERM | Payment terms | VARCHAR(4) | Default payment terms for POs |
| INCO1 | Incoterms part 1 | VARCHAR(3) | Delivery terms (EXW, FOB, etc.) |
| INCO2 | Incoterms part 2 | VARCHAR(28) | Delivery location |
| WAERS | Currency | VARCHAR(5) | Default currency for POs |

### KNA1 - Customer Master (General Section)
**Purpose**: Contains general customer master data valid across all company codes.

| Field | Description | Type | Purpose |
|-------|-------------|------|---------|
| KUNNR | Customer number | VARCHAR(10) | Primary key, unique customer identifier |
| NAME1 | Name 1 | VARCHAR(35) | Customer company name |
| SORTL | Sort field | VARCHAR(10) | Search term for customer |
| STRAS | Street address | VARCHAR(35) | Customer street address |
| ORT01 | City | VARCHAR(35) | Customer city |
| PSTLZ | Postal code | VARCHAR(10) | Customer postal/ZIP code |
| LAND1 | Country key | VARCHAR(3) | ISO country code |
| SPRAS | Language key | VARCHAR(1) | Communication language |
| TELF1 | Telephone 1 | VARCHAR(16) | Primary phone number |
| TELFX | Fax number | VARCHAR(31) | Fax number |
| SMTP_ADDR | Email address | VARCHAR(241) | Email address |
| KTOKD | Customer account group | VARCHAR(4) | Controls field status and number ranges |
| ERDAT | Created on | DATE | Record creation date |
| ERNAM | Created by | VARCHAR(12) | User who created the record |
| SPERR | Central posting block | VARCHAR(1) | Blocks all postings to customer |
| LOEVM | Central deletion flag | VARCHAR(1) | Marks customer for deletion |

## Configuration

Key parameters can be modified at the top of `sap_data_generator.py`:

```python
# Configuration
NUM_TRANSACTIONS = 5000
START_DATE = date(2023, 1, 1)
END_DATE = date(2025, 3, 31)
ANALYSIS_FOCUS_YEAR = 2024
```

## Troubleshooting

### Common Issues

**Memory Errors**: Reduce `NUM_TRANSACTIONS` if encountering memory issues on smaller systems.

**Date Range Issues**: Ensure `START_DATE` is before `END_DATE` and allows sufficient time for payment cycles.

**Missing Dependencies**: Run `conda env create -f environment.yml` to install all required packages.

## Licence

This project is licensed under the MIT Licence - see the [LICENCE](LICENCE) file for details.