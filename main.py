import os
import pdfplumber
import re
import pandas as pd

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_work_details(text):
    # Multiple patterns for dates and work hours to match various formats
    date_patterns = [
        r'Pay Period\s*[:\-]?\s*(\d{1,2} \w+ \d{4}) - (\d{1,2} \w+ \d{4})',  # Pattern for "23 September - 06 October 2024"
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # Pattern for "21/10/2024 - 03/11/2024"
    ]
    
    hours_patterns = [
        r'Ordinary Hours\s+(\d+\.\d{4})',  # Pattern for "Ordinary Hours 48.0000"
        r'Quantity\s+(\d+\.\d{2})',        # Pattern for "Quantity 76.00"
    ]

    # Try matching each date pattern
    pay_period_start, pay_period_end = None, None
    for pattern in date_patterns:
        dates = re.findall(pattern, text)
        if dates:
            # Check if dates is a tuple from the first pattern, else single date list
            if isinstance(dates[0], tuple):
                pay_period_start, pay_period_end = dates[0]
            else:
                pay_period_start = dates[0] if dates else None
                pay_period_end = dates[1] if len(dates) > 1 else None
            break  # Stop once a match is found
    
    # Try matching each hours pattern
    total_hours_worked = None
    for pattern in hours_patterns:
        hours_match = re.search(pattern, text)
        if hours_match:
            total_hours_worked = hours_match.group(1)
            break  # Stop once a match is found

    return {
        "Pay Period Start": pay_period_start,
        "Pay Period End": pay_period_end,
        "Total Hours Worked": total_hours_worked
    }

def process_payslips(payslip_folder):
    data = []
    
    # Iterate over all PDF files in the Payslips folder
    for filename in os.listdir(payslip_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(payslip_folder, filename)
            print(f"Processing file: {filename}")  # Debug: Verify file processing
            text = extract_text_from_pdf(pdf_path)
            details = extract_work_details(text)
            details["Filename"] = filename  # Add filename for reference
            data.append(details)
    
    # Check if data was collected
    if not data:
        print("No payslip data was extracted.")
        return
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv("output.csv", index=False)
    print("Data saved to output.csv")

# Define the Payslips folder path
payslip_folder = os.path.join(os.path.dirname(__file__), 'Payslips')

# Run the payslip processing
process_payslips(payslip_folder)
