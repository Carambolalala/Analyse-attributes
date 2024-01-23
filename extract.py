import csv
import matplotlib.pyplot as plt

class fullInfo:
    top = 10
    predictMAE = 0.3
    predictScore = 0.8
    comfortTable = []
    sorted_SCORE_comfortTable = []
    sorted_MAE_comfortTable = []
    attributesFileName = 'era5.csv'
    testResultsFileName = 'random_forest_regressor_test_features_weights.csv'
    attributes = []
    countAttributes = {}
    topTable = []
oneInInfo = fullInfo()

def reset():
    oneInInfo.comfortTable = []
    oneInInfo.topTable = []

    attributesFile = open(oneInInfo.attributesFileName)
    oneInInfo.attributes = attributesFile.readline().split(',')
    del oneInInfo.attributes[-1]
    del oneInInfo.attributes[0]
    oneInInfo.attributes.sort()
    attributesFile.close()
    for atr in oneInInfo.attributes:
        oneInInfo.countAttributes[atr] = {'score': 0, 'mae': 0}

    testResultsFile = open(oneInInfo.testResultsFileName, 'r')
    testResultsReader = csv.reader(testResultsFile)
    
    i = 0
    for row in testResultsReader:
        if i >= 1:
            mae = float(row[0])
            score = float(row[1])
            testingAttributes = row[2][1:-1].replace("'", "").split(', ')
            testingAttributes.sort()
            count = int(row[3])
            oneInInfo.comfortTable.append({'row': i, 'mae': mae, 'score': score, 'attributes': testingAttributes, 'count': count})
        i += 1
    testResultsFile.close()

    oneInInfo.sorted_MAE_comfortTable = sorted(oneInInfo.comfortTable, key=lambda x: x['mae'])
    oneInInfo.sorted_SCORE_comfortTable = sorted(oneInInfo.comfortTable, key=lambda x: x['score'], reverse=True)

def setPredictScore(score):
    oneInInfo.predictScore = score
    countScore = 0
    for row in oneInInfo.sorted_SCORE_comfortTable:
        if row['score'] >= oneInInfo.predictScore:
            countScore += 1
        else:
            break
    print('Кол-во результатов, удовлетворяющих predict score: ', countScore)

def setPredictMAE(mae):
    oneInInfo.predictMAE = mae
    countMAE = 0
    for row in oneInInfo.sorted_MAE_comfortTable:
        if row['mae'] <= oneInInfo.predictMAE:
            countMAE += 1
        else:
            break
    print('Кол-во результатов, удовлетворяющих predict MAE: ', countMAE)

def findResults():
    count = 0
    for row in oneInInfo.sorted_SCORE_comfortTable:
        if row['score'] >= oneInInfo.predictScore:
            if row['mae'] <= oneInInfo.predictMAE:
                count += 1
                for atr in row['attributes']:
                    oneInInfo.countAttributes[atr]['score'] += 1
                    oneInInfo.countAttributes[atr]['mae'] += 1
                if count < oneInInfo.top:
                    oneInInfo.topTable.append(row['count'])
        else:
            break
    print('Кол-во результатов, подходящих для predictScore и predictMAE: ', count)
    print('В топ 10 результатов входят такое количество параметров: ', str(oneInInfo.topTable)[1:-1])
def draw():
    bar_width = 0.35
    values = {}
    for key in oneInInfo.countAttributes:
        values[key] = oneInInfo.countAttributes[key]['score']
    sorted_values = sorted(values.items(), key=lambda item: item[1], reverse=True)
    x = []
    y = []
    for item in sorted_values:
        x.append(item[0])
        y.append(item[1])
    scoreBar = plt.bar(x, y, width=bar_width, label='Кол-во раз при лучших Score')
    y = []
    for item in sorted_values:
        y.append(oneInInfo.countAttributes[item[0]]['mae'])
    MAEBar = plt.bar([i + bar_width for i in range(len(x))], y, width=bar_width, label='Кол-во раз при лучших MAE')

    plt.xticks(rotation=85)
    plt.legend()
    plt.show()
