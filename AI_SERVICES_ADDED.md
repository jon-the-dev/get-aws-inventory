# AI/ML Services Added to AWS Inventory Scanner

## Summary

Added **12 AWS AI/ML services** to the inventory scanner with comprehensive test coverage.

## Services Added

### Paginated Services (7)
1. **Rekognition** - Image and video analysis
   - `list_collections` → CollectionIds
   - `list_stream_processors` → StreamProcessors

2. **Comprehend** - Natural language processing
   - `list_document_classifiers` → DocumentClassifierPropertiesList
   - `list_entities_detection_jobs` → EntitiesDetectionJobPropertiesList

3. **Polly** - Text to speech
   - `list_lexicons` → Lexicons

4. **Textract** - Document text extraction
   - `list_adapters` → Adapters

5. **Forecast** - Time-series forecasting
   - `list_datasets` → Datasets
   - `list_predictors` → Predictors

6. **Personalize** - ML recommendations
   - `list_datasets` → datasets
   - `list_solutions` → solutions

### Non-Paginated Services (6)
7. **Bedrock** - Generative AI foundation models
   - `list_foundation_models` → modelSummaries

8. **Bedrock Agent** - AI agents
   - `list_agents` → agentSummaries

9. **Translate** - Language translation
   - `list_terminologies` → TerminologyPropertiesList

10. **Transcribe** - Speech to text
    - `list_transcription_jobs` → TranscriptionJobSummaries

11. **Lex V2** - Conversational AI
    - `list_bots` → botSummaries

12. **Kendra** - Intelligent search
    - `list_indices` → IndexConfigurationSummaryItems

## Test Suite

Created comprehensive test suite in `tests/test_boto3_validation.py`:

### Test Coverage
- ✅ All boto3 service clients exist
- ✅ All methods exist on their respective clients
- ✅ Pagination support validated for paginated services
- ✅ All 12 AI/ML services properly configured
- ✅ No duplicate services across categories
- ✅ Response keys are valid
- ✅ Service coverage metrics

### Test Results
```
19 tests passed in 0.78s
```

## Usage

The scanner will now automatically inventory these AI/ML services:

```bash
# Scan all regions including AI/ML services
aws-inventory-scanner

# Scan specific regions
aws-inventory-scanner --region us-east-1 --region us-west-2
```

## Output Files

New inventory files will be created for each AI/ML service:

```
./inventory/
├── 123456789012-bedrock-us-east-1-list_foundation_models-modelSummaries.json
├── 123456789012-rekognition-us-east-1-list_collections-CollectionIds.json
├── 123456789012-comprehend-us-east-1-list_document_classifiers-DocumentClassifierPropertiesList.json
├── 123456789012-kendra-us-east-1-list_indices-IndexConfigurationSummaryItems.json
└── ...
```

## Testing

Run the test suite:

```bash
# Using pipenv
pipenv run pytest tests/test_boto3_validation.py -v

# Or install and run
pipenv install --dev
pipenv run pytest -v
```

## Next Steps

Consider adding additional AWS services from `new_services_analysis.md`:
- Networking services (ELBv2, VPC endpoints, Transit Gateway)
- Security services (Security Hub, IAM Access Analyzer)
- Database services (DocumentDB, Neptune, Timestream)
- Analytics services (EMR, Kinesis, MSK, Glue)
- 40+ more services documented

## Notes

- Some AI/ML services may require specific IAM permissions
- Services are scanned across all enabled regions
- Empty results are normal if services aren't in use
- Bedrock may not be available in all regions
