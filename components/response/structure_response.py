from nltk import sent_tokenize


def structure_response(results, original_text):
    org_text_sentences = sent_tokenize(original_text)

    results_index = 0
    structured_results = []
    for sentence in org_text_sentences:
        if results_index < len(results) and sentence == results[results_index]['text']:
            print(sentence)
            structured_results.append({'text': sentence,
                                       'danger_result': results[results_index]})
        else:
            structured_results.append({'text': sentence})

        results_index += 1

    return structured_results
