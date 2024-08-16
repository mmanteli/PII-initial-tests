from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
import json
import sys


conf_file = "en-spacy-config.yml"
# Create NLP engine based on configuration
provider = NlpEngineProvider(conf_file=conf_file)
nlp_engine = provider.create_engine()

# Pass the created NLP engine and supported_languages to the AnalyzerEngine
analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine, 
    supported_languages=["en"])

anonymizer = AnonymizerEngine()


for line in sys.stdin:
    j = json.loads(line)

    text = j["raw_content"]
    ner_results = analyzer.analyze(text=text, language="en")
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=ner_results)
    print(json.dumps({"redacted":str(anonymized_text.text)}))
    #    j["redacted"] = anonymized_text
    #    print(json.dumps(j))
    #except:
    #    print("error")
    #    continue
