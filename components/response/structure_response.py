import spacy
from nltk import sent_tokenize
from spacy_langdetect import LanguageDetector


def structure_response(results, original_text):
    global nlp
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
    doc = nlp(original_text)

    if doc._.language['language'] == 'de':
        nlp = spacy.load('de_core_news_sm')

    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    doc = nlp(original_text)

    org_text_sentences = []
    for sent in doc.sents:
        org_text_sentences.append(sent)

    results_index = 0
    structured_results = []
    for sentence in org_text_sentences:
        if results_index < len(results) and sentence.text == results[results_index]['text']:
            structured_results.append({'text': sentence.text,
                                       'danger_result': results[results_index]})
        else:
            structured_results.append({'text': sentence.text})

        results_index += 1

    return structured_results
