# Evaluation Report

## Dataset

Development was performed using `dataset/sample_claims.csv`.

## Strategy 1

* Extract claim details from the conversation transcript.
* Analyze uploaded images using Gemini Vision.
* Compare visual evidence against claimed damage.
* Generate structured outputs.

### Observations

* Good object recognition.
* Sometimes conservative when evidence was partially visible.

## Strategy 2

* Added explicit evidence-review instructions.
* Treated images as the primary source of truth.
* Incorporated user history only as risk context.

### Observations

* More consistent claim decisions.
* Better handling of multi-image claims.
* Reduced contradictions caused by claim text alone.

## Final Strategy

The final system:

1. Extracts claim information from conversation text.
2. Reviews one or more submitted images using Gemini.
3. Checks evidence sufficiency.
4. Assesses risk using user history.
5. Produces structured outputs:

   * evidence_standard_met
   * risk_flags
   * issue_type
   * object_part
   * claim_status
   * severity

## Operational Analysis

### Model

* Gemini 2.5 Flash / Flash Lite

### Runtime Characteristics

* One multimodal request per claim.
* Retry handling for transient failures.
* Resume processing for quota interruptions.

### Cost Considerations

* Image analysis dominates cost.
* Multi-image claims require additional context tokens.
* Resume pipeline prevents reprocessing completed rows.

## Final Result

Generated predictions for all rows in `dataset/claims.csv` and exported them to `output.csv`.
