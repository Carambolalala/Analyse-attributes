import extract
extract.reset()
allCommands = """set predictScore <value>
set predictMAE <value>
find
draw
reset
Алгоритм действия:
1. Установить значения ожидаемых результатов по score и MAE (predictScore, predictMAE)
Дефолтные значения: predictScore = 0.8
                    predictMAE = 0.3
2. Будет выведено количество результатов, подходящее под заданные ожидания (отдельно для
score и mae)
3. Найти результаты, которые будут удовлетворять одновременно для predictScore и predictMAE (find)
4. Будет выведено количество найденных результатов
5. Вывести графики для анализа параметров (draw)
6. На любом из этапов, в случае, если собираетесь менять значение predictScore и predictMAE,
нужно произвести RESET данных (reset)"""
print('List of commands:\n' + allCommands)
while True:
    command = input('>>').split()
    if command[0] == 'exit':
        break
    elif command[0] == 'set':
        if command[1] == 'predictScore':
            extract.setPredictScore(float(command[2]))
        elif command[1] == 'predictMAE':
            extract.setPredictMAE(float(command[2]))
        else:
            print('ERROR: ONLY SET FOR predictScore, predictMAE')
    elif command[0] == 'find':
        extract.findResults()
    elif command[0] == 'draw':
        extract.draw()
    elif command[0] == 'reset':
        extract.reset()
    else:
        print('COMMAND NOT FOUND')