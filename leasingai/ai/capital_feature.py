def capitalization(features,sentence):
    count = 0
    for i in range(len(sentence)):
        count += int(sentence[i].isupper())
    features['Capitalization'] = int(count > 3)

