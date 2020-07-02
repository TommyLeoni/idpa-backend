import spacy
from model.response import Response
from spacy_sentiws import spaCySentiWS


def analyze_text(text):
    nlp = spacy.load('de_core_news_sm')
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    doc = nlp(text)

    sentences = []
    for sent in doc.sents:
        sentences.append(sent)

    sentiws = spaCySentiWS(sentiws_path='data/sentiws/')
    nlp.add_pipe(sentiws)

    results = []

    for sentence in sentences:
        doc = nlp(sentence.text)
        filtered_doc = []

        for word in doc:
            if not word.is_stop:
                filtered_doc.append(word)

        for token in filtered_doc:
            if token._.sentiws:
                if token._.sentiws < -0.3:
                    results.append({
                        "text": sentence.text,
                        "danger": [token.text],
                        "danger_value": token._.sentiws,
                        "danger_obj": token.pos_
                    })

    return results
