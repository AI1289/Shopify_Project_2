# Shopify GUI Project – Developer Onboarding Summary

This document serves as a comprehensive and self-contained overview of the Shopify GUI Importer & Manager.  
It is intended for new contributors or developers to quickly understand the architecture, current status, and ongoing development priorities.

---

## Overview

The Shopify GUI Importer is a Streamlit-based application that converts raw supplier spreadsheets (CSV/XLSX) into fully Shopify-compliant import files.

It features:
- Editable product tables
- Formula-based price and weight adjustments
- Validation logic
- Template save/load capabilities
- Export functionality

---

## Current Repository

- **GitHub:** [Shopify_Project_2 – new-project branch](https://github.com/AI1289/Shopify_Project_2/tree/new-project)
- **Branch:** `new-project`

---

## File Structure

```
shopify_gui/
├── app.py                       # Streamlit app entry point
├── src/
│   ├── formula_engine.py        # Safe AST-based formula evaluator
│   ├── header_mapper.py         # Fuzzy mapping logic (needs alias support)
│   ├── validation_rules.py      # Validation for required Shopify fields
│   ├── shopify_csv_handler.py   # CSV export logic for Shopify compliance
│   └── template_manager.py      # Save/load template JSON
├── templates/                   # Folder to store template JSON files
├── formulas.json                # Sample formula configuration
└── requirements.txt             # Dependencies (streamlit, pandas, openpyxl)
```

---

## Modules and Responsibilities

- **formula_engine.py**: Evaluates formulas using secure AST parsing
- **header_mapper.py**: Maps columns to Shopify headers (needs alias dictionary)
- **validation_rules.py**: Validates required fields (e.g., Title, Handle)
- **template_manager.py**: Loads/saves reusable templates
- **shopify_csv_handler.py**: Generates Shopify-compliant export files

---

## Known Limitations

- ❌ Header mapping fails for common fields like `ID`, `Name` (fuzzy match only)
- ❌ Formula engine doesn’t visibly apply changes; needs debug visibility
- ❌ Templates only save filenames, not mappings or formulas
- ❌ No Shopify API sync (currently local CSV export only)

---

## Suggested Improvements (Next Sprints)

- Add alias dictionary to improve header mapping
- Fix formula engine to apply + preview changes with debug
- Enhance template save logic to include current mapping + formulas
- Add Shopify API integration (Phase 3)

---

## Getting Started

```bash
git clone https://github.com/AI1289/Shopify_Project_2
cd Shopify_Project_2
git checkout new-project
pip install -r requirements.txt
python -m streamlit run app.py
```

- Upload a test file like `test_input.xlsx`
- Apply formulas and mappings
- Validate and export final CSV

---

This file is recommended to be included in the project root or linked from the main README.
