# Water Consumption and Payment Tracking Dashboard

This Streamlit application provides a user-friendly interface for residents to monitor their water consumption, payment amounts, and outstanding balances. The dashboard connects directly to a Google Drive spreadsheet to display real-time billing information and generates visual representations of payment history throughout the year.

The application simplifies water consumption tracking by allowing users to select their name and billing period from dropdown menus. It then presents their consumption data in cubic meters, current payment amount, and any outstanding balance. The dashboard includes an interactive bar chart that visualizes payment amounts across all months, helping users understand their payment patterns and plan accordingly.

## Repository Structure
```
.
├── main.py              # Main application file containing Streamlit dashboard implementation
└── images/
    └── logo.png        # Application logo image file (referenced in code)
```

## Usage Instructions
### Prerequisites
- Python 3.6 or higher
- pip package manager
- Internet connection for Google Drive access

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install required packages
pip install streamlit pandas gdown matplotlib
```

### Quick Start
1. Start the Streamlit application:
```bash
streamlit run main.py
```

2. Use the dashboard:
   - Select your name from the dropdown menu
   - Choose the desired month and year
   - View your consumption, payment amount, and outstanding balance
   - Examine the payment history chart

### More Detailed Examples
#### Viewing Monthly Consumption
```python
# Select user and month from dropdowns
# Example output:
Consumo: 10.5 m³
Valor a pagar: R$ 150,00
Valor em Atraso: R$ 0,00
```

#### Analyzing Payment History
The bar chart displays payment amounts for all months, allowing you to:
- Track payment trends
- Identify months with higher consumption
- Plan for seasonal variations

### Troubleshooting
#### Common Issues
1. Google Drive Access Error
   - Error message: "Unable to download spreadsheet"
   - Solution: Check your internet connection and verify the Google Drive URL

2. Data Display Issues
   - Error message: "Indisponível" (Unavailable)
   - Solution: Verify that the selected month has data entered in the spreadsheet

#### Debugging
- Check the Streamlit logs in the terminal for error messages
- Verify that the spreadsheet URL is accessible
- Ensure all required packages are installed correctly

## Data Flow
The application retrieves data from a Google Drive spreadsheet and processes it to display user-specific consumption information.

```ascii
[Google Drive] --> [Download Spreadsheet] --> [Load Data] --> [User Selection] --> [Filter Data] --> [Display Results]
                                                                                               └--> [Generate Charts]
```

Key component interactions:
1. Application downloads the Excel spreadsheet from Google Drive
2. Pandas loads the spreadsheet data into a DataFrame
3. User interface collects name and month selections
4. Data filtering extracts relevant consumption and payment information
5. Matplotlib generates payment history visualization
6. Interface displays filtered data and charts to the user
7. Application removes the downloaded spreadsheet after use