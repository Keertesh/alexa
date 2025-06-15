# Tax Filing Data Schema (Initial Design)

This document defines the initial proposed schema for tax filing data. This schema will evolve as the system's requirements become more refined. We will initially consider a flat structure, potentially in CSV or JSON format for ingestion.

## Core Data Fields:

| Field Name          | Data Type     | Description                                                                 | Example                               | Required | Notes                                              |
|---------------------|---------------|-----------------------------------------------------------------------------|---------------------------------------|----------|----------------------------------------------------|
| `filing_id`         | String        | Unique identifier for the tax filing event.                                 | "TXN-2023-000001"                     | Yes      | Can be system-generated or from source.            |
| `timestamp`         | ISO 8601 Date | Date and time of the filing or data record.                                 | "2023-04-15T10:30:00Z"                | Yes      | Crucial for time-series analysis.                  |
| `user_id`           | String        | Anonymized or pseudonymized identifier for the filer.                       | "USER-XYZ123"                         | Yes      | Ensure privacy compliance.                         |
| `region_code`       | String        | Code representing the geographical region of the filer (e.g., state, county). | "CA-SF"                               | Yes      | For regional trend analysis.                       |
| `income_bracket`    | String        | Pre-defined income bracket of the filer.                                    | "50k-100k"                            | Yes      | Define brackets clearly.                           |
| `filing_type`       | String        | Type of tax filing (e.g., individual, joint, corporate).                    | "individual"                          | Yes      | Based on defined categories.                       |
| `tax_year`          | Integer       | The year for which the taxes are being filed.                               | 2022                                  | Yes      |                                                    |
| `total_income`      | Float         | Total declared income by the filer.                                         | 75000.50                              | No       | May not always be available initially.             |
| `total_deductions`  | Float         | Total deductions claimed.                                                   | 12000.00                              | No       |                                                    |
| `tax_owed`          | Float         | Calculated tax amount owed.                                                 | 8500.75                               | No       |                                                    |
| `refund_amount`     | Float         | Calculated refund amount.                                                   | 1200.25                               | No       | One of tax_owed or refund_amount should exist.     |
| `filing_method`     | String        | Method of filing (e.g., online, paper, tax_professional).                   | "online"                              | No       |                                                    |
| `language_preference`| String        | Filer's preferred language for communication (ISO 639-1 code).              | "en"                                  | No       | For multilingual support.                          |

## Considerations:

*   **Data Source:** The actual fields available will depend on the source of the tax filing data. This schema is a target/ideal state for initial analysis.
*   **Anonymization/Pseudonymization:** Fields like `user_id` must be handled with strict privacy considerations.
*   **Extensibility:** The schema should be designed to allow for additional fields as more complex analyses are introduced (e.g., specific deduction types, demographic information).
*   **Data Validation:** Clear validation rules will be needed for each field (e.g., format, range, allowed values).
*   **Normalization:** For a more relational structure, some fields (like `region_code`, `income_bracket`, `filing_type`) could be broken out into separate lookup tables with foreign keys in the main data table. However, for initial ingestion and analysis by some agents, a denormalized structure might be simpler.

This initial schema will be used to guide the development of the `DataIngestionAgent`.
