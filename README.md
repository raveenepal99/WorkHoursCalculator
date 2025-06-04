# WorkHours Calculator

This project extracts pay period dates and total hours worked from PDF payslips.
It can run from the command line or with a simple graphical interface.

## Requirements
- Python 3.8+
- `pdfplumber`
- `pandas`

## Command Line Usage
Place your PDF files inside a folder named `Payslips` in the same directory
as `main.py` and run:

```bash
python main.py
```

The script will generate `output.csv` with the extracted information.

## Graphical Interface
Launch the GUI with:

```bash
python gui.py
```

Select your payslip folder and click **Process Payslips**. The results will be
saved to `output.csv` inside the chosen folder.
