from collections import Counter

def calculate_emotion_stats(predictions):
    if not predictions:
        return None, {}
    total = len(predictions)
    counts = Counter(predictions)
    percentages = {
        emotion: round((count / total) * 100,2)
        for emotion, count in counts.items()
    }
    main_emotion = counts.most_common(1)[0][0]
    return main_emotion, percentages