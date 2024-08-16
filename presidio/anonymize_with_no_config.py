from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NerModelConfiguration
from presidio_anonymizer import AnonymizerEngine
import json
import sys



# Here we define a transformers based NLP engine, 
# but you can use this cell to customize your Presidio Analyzer instance

# Define which model to use
model_config = [{"lang_code": "en", "model_name": "en_core_web_md"
}]


model_to_presidio_entity_mapping = dict(
    CARDINAL="ID",
    DATE="DATE_TIME",
    EVENT="LOCATION",
    FAC="ID",
    GPE="LOCATION",
    LANGUAGE="LOCATION",
    LAW="LOCATION",
    LOC="LOCATION",
    MONEY="MONEY",
    NORP="NRP",
    ORDINAL="ID",
    ORG="ORGANIZATION",
    PERCENT="ID",
    PERSON="PERSON",
    PRODUCT="ORGANIZATION",
    QUANTITY="ID",
    TIME="DATE_TIME",
    WORK_OF_ART="ORGANIZATION",
    US_DRIVER_LICENSE="US_DRIVER_LICENSE",
    IN_PAN="IN_PAN"
)

ner_model_configuration = NerModelConfiguration(labels_to_ignore = {"US_DRIVER_LICENSE","ORGANIZATION"})#, 
                                                #model_to_presidio_entity_mapping=model_to_presidio_entity_mapping)

nlp_engine = SpacyNlpEngine(models=model_config,
                                   ner_model_configuration=ner_model_configuration)

# Set up the engine, loads the NLP module (spaCy model by default) 
# and other PII recognizers
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
print(analyzer.nlp_engine.ner_model_configuration.labels_to_ignore)
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
    #    continue"""
