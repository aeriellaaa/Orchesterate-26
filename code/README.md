# Insurance Claim Evidence Review System

## Overview

This project automates insurance claim review using claim descriptions, uploaded images, and user history.

The system:

1. Extracts claimed objects and damage from customer conversations.
2. Analyzes submitted images using a multimodal AI model.
3. Compares visual evidence against customer claims.
4. Incorporates user history as risk context.
5. Produces structured claim decisions.

## Pipeline

Claim Text
→ Claim Extraction
→ Image Analysis
→ Evidence Review
→ Risk Assessment
→ Structured Output Generation

## Technologies

- Python
- Pandas
- Pillow (PIL)
- Google Gemini API

## Output Fields

- evidence_standard_met
- evidence_standard_met_reason
- risk_flags
- issue_type
- object_part
- claim_status
- claim_status_justification
- supporting_image_ids
- valid_image
- severity

## Setup

1. Install dependencies

```bash
pip install pandas pillow python-dotenv google-genai
```

2. Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

3. Run the pipeline

```bash
python generate_output.py
```

## Notes

- Images are treated as the primary source of truth.
- User history is used only for risk assessment.
- Retry and resume logic are implemented for API failures and quota limits.