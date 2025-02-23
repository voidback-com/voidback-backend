from transformers import pipeline




def textSentimentAnalysis(text):
    try:
        model = pipeline("text-classification", "../../models/multilingual-sentiment-analysis", device="cpu")

        data = model(text)

        labels = {
            "LABEL_1": "VERY-NEGATIVE",
            "LABEL_2": "NEGATIVE",
            "LABEL_3": "NEUTRAL",
            "LABEL_4": "POSITIVE",
            "LABEL_5": "VERY-POSITIVE"
        }

        data = data[0]

        data['label'] = labels[data['label']]

        return data

    except KeyboardInterrupt:
        return None


def textToxicity(text):
    try:
        model = pipeline("text-classification", "../../models/distilbert-nsfw-text-classifier", device="cpu")

        data = model(text)

        return data[0]

    except KeyboardInterrupt:
        return




x = textToxicity("Hello")
y = textSentimentAnalysis("Hello WOrld")
print(x, y)
