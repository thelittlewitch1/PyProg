# Высказать интуитивные гипотезы на основе названий колонок
# Провести разведочный анализ датасета: построить графики распределений и отношений переменных, точечные графики,
# посчитать попарные коэффициенты корреляции, тепловая карта корреляций
# Выявить признаки, которые наилучшим образом коррелируют
# Построить для них предсказательные модели (на прошлом этапе) Выявить признаки, которые наилучшим образом коррелируют
# Построить для них предсказательные модели
# Оценить качество предсказания

import pandas
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score


def distribution(data, name):
    print(name + ':\n', data.value_counts())
    sns.distplot(data)
    plt.title("distplot of " + name + " (%d samples)" % len(data))
    plt.savefig("plots/sber/displot_of_" + name + ".png")
    plt.clf()


def correlation(data, cols, name):
    sns.pairplot(data[cols]).fig.suptitle("Pairplot (%d samples)" % len(data), y=(1 - 0.005))
    plt.savefig("plots/sber/pair_" + name + ".png")
    plt.clf()

    cm = np.corrcoef(data[cols].dropna().to_numpy().T)
    plt.figure()
    sns.heatmap(cm,
                cmap='RdYlBu_r', cbar=True, annot=True,
                square=True, fmt='0.2f', annot_kws={'size': 8},
                yticklabels=cols, xticklabels=cols)
    plt.title("Heatmap (%d samples)" % len(data))

    plt.savefig("plots/sber/heat_map_" + name + ".png")
    plt.clf()


def part1(data):
    # распределение значений
    distribution(data.price_doc, "price")
    distribution(data.full_sq, "full square")
    distribution(data.life_sq, "life square")
    distribution(data.floor, "floor")
    distribution(data.state, "state")

    # Попарные отношения и тепловая карта корреляций
    correlation(data, ['life_sq', 'full_sq', 'num_room', 'kitch_sq'], "sqare")
    correlation(data, ['price_doc', 'full_sq', 'kitch_sq', 'state', 'num_room', 'floor', 'max_floor'], "price1")
    correlation(data, ['price_doc', 'school_km', 'preschool_km', 'trc_count_500', 'build_year'], "price2")


def predict(X, y, name):
    # Предсказательная модель
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    slr = LinearRegression()
    slr.fit(X_train, y_train)
    y_train_pred = slr.predict(X_train)
    y_test_pred = slr.predict(X_test)

    print('\n prediction of' + name + '\n')
    print(u'slant: ' + str(slr.coef_[0]))
    print(u'intersection: ' + str(slr.intercept_))
    # Точечный график + регрессия
    plt.scatter(X, y, c='blue', marker='o', s=100)
    plt.plot(X, slr.predict(X), color='red')
    plt.xlabel(u'features')
    plt.ylabel(u"Target variable")
    plt.savefig("plots/sber/predict_"+name+".png")
    plt.clf()
    print('MSE train: ' + str(mean_squared_error(y_train, y_train_pred)))
    print('MSE test: ' + str(mean_squared_error(y_test, y_test_pred)))
    print('R^2 train: ' + str(r2_score(y_train, y_train_pred)))
    print('R^2 test: ' + str(r2_score(y_test, y_test_pred)))


if __name__ == '__main__':
    data = pandas.read_csv('Sber/train.csv', index_col='id')[
        ['timestamp', 'full_sq', 'life_sq', 'floor', 'max_floor', 'build_year', 'num_room',
         'kitch_sq', 'state', 'product_type', 'price_doc', 'school_km', 'preschool_km', 'trc_count_500']
    ].dropna()
    data = data[data.state != 33.0]
    print(data.columns.values.tolist())
    data = data[data.product_type == 'Investment'][
        ['timestamp', 'full_sq', 'life_sq', 'floor', 'max_floor', 'build_year', 'num_room',
         'kitch_sq', 'state', 'price_doc', 'school_km', 'preschool_km', 'trc_count_500']
    ]
    # Моё предположение:
    # 1. полная площадь, жилая площадь и количество комнат взаимосвязаны.
    # 2. цена связана с пощадью, площадью кухни, состоянием квартиры, этажом, этажностью дома
    # расстоянием до школы, дет.сада, торгового центра, годом постройки.
    part1(data)
    predict(data[['full_sq']].values, data[['price_doc']].values, "square-prise")
    predict(data[['num_room']].values, data[['full_sq']].values, "rooms-square")