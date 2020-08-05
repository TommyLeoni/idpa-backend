from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.corpus import stopwords, sentiwordnet as swn
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

results = []


# Function to analyze text using nltk (English)
def analyze_english(text):

    # Split into sentences
    for sentence in sent_tokenize(text):

        # Split into words
        tokenized = word_tokenize(sentence)

        # Filter out stop words, lemmatize and to lowercase (for consistency)
        filtered_tokens = []
        for token in tokenized:
            if token not in stop_words:
                filtered_tokens.append(lemmatizer.lemmatize(token).lower())

        # Filter out non-alphabetic characters & get part of speech (pos) tag
        cleaned_tokens = [token for token in filtered_tokens if token.isalpha()]
        tagged_tokens = pos_tag(cleaned_tokens)

        # Get sentimental value based on pos
        for tagged_token in tagged_tokens:
            if tagged_token[1] == 'NN':
                synset_results = list(swn.senti_synsets(tagged_token[0], 'n'))

                # Collect average negative score for every result
                if not synset_results == []:
                    neg_score = 0
                    for synset in synset_results:
                        neg_score += synset.neg_score()

                    # Return in form of same json object as used by german_analyzation.py if negative enough
                    if neg_score / len(synset_results) > 0.05:
                        results.append({
                            "text": sentence,
                            "danger": tagged_token[0],
                            "danger_value": neg_score / len(synset_results),
                            "danger_obj": tagged_token[1]
                        })

    return results
