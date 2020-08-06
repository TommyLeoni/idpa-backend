import os

import spacy
from spacy_sentiws import spaCySentiWS


def analyze_german(text):
    nlp = spacy.load('de_core_news_sm')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    doc = nlp(text)

    sentences = []
    for sent in doc.sents:
        sentences.append(sent)

    local_path = os.path.abspath(os.path.dirname(__file__))
    sentiws = spaCySentiWS(sentiws_path=os.path.join(local_path, '../../data/sentiws'))
    nlp.add_pipe(sentiws)

    results = []

    for sentence in sentences:
        doc = nlp(sentence.text)
        results.append({'text': sentence.text})
        filtered_doc = []

        for word in doc:
            if not word.is_stop:
                filtered_doc.append(word)

        for token in filtered_doc:
            if token._.sentiws:
                if token._.sentiws < -0.3:
                    results[-1] = {
                        "text": sentence.text,
                        "danger": [token.text],
                        "danger_value": token._.sentiws,
                        "danger_obj": token.pos_
                    }

    return results
