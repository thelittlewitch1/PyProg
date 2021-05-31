# Лаба 2.0
# Воспроизвести код лекции
# Построить графики для других стран по коду ref_area
# Построить графики для других наборов продуктов (коды потребительских корзин)

# Лаба 2.1.1
# Если предположить, что цена на ружье с патронами движется соответственно средней инфляции
# Сколько стоит ружье Деда с патронами в рублях с учетом деноминации и инфляции сейчас (в 2020 году)?
# Продав ружье с патронами в 1996-м году за $200, он выиграл или проиграл по сравнению с ситуацией,
# если бы он продал его в 2020 году за рубли? Если выиграл или проиграл, то сколько?

# Лаба 2.1.2
# Что такое один миллион долларов США в США из 1967-го (1969) года в 1997-м году в США?
# Что такое сто миллиардов долларов США в США из 1997-го года в 1967-м (1969) году в США?
# Что такое сто миллиардов долларов США в США из 1997-го года в 2019-м году в США?

# Лаба 2.2
# Взять данные по инфляции в России с сайта Росстата
# Сравнить с данными по инфляции МОТ (ILO)
# Построить графики для России с данными Росстата, сравнить результат
# Фактчек: найти методику Росстата по вычислению коэффициента потребильских цен (уровня инфляции) в период
# деноминации на рубеже 1997-1998 годов
# Найти правила сравнения цен до номинации и после номинации
# Проверить дополнительно: закон о деноминации, август 1997

# Лаба 2.3 — свободная тема
# Построить любые другие графики по рассмотренному датасету
# Взять любой другой датасет, исследовать его

import matplotlib.pyplot as plt
import pandas


def part1(area='RUS', code='COI_COICOP_CP01T12'):
    plt.rc('font', size=7)

    data = pandas.read_csv('ILO/EAR_4MTH_SEX_ECO_CUR_NB_A.csv')
    data = data[(data.ref_area != 'BLR') & (data.ref_area != 'ZWE')]
    data = data[['ref_area', 'sex', 'classif1', 'classif2', 'time', 'obs_value']]
    data = data[(data.classif1 == 'ECO_AGGREGATE_TOTAL') & (data.sex == 'SEX_T')]

    data_cur = data[data.ref_area == area]
    data_cur = data_cur.set_index('time').sort_index()
    ax = data_cur[data_cur.classif2 == 'CUR_TYPE_USD'][['obs_value']] \
        .plot(kind='bar', title='Average monthly wages in ' + area + ' by years')
    ax.legend(['Average monthly wages by year (USD)'])

    pivot = data_cur.pivot_table(values='obs_value', index='time', columns='classif2')
    if area == 'RUS':
        pivot.loc[pivot.index <= 1996, 'CUR_TYPE_LCU'] /= 1000
    pivot.plot(kind='bar', title='Average monthly wages by year', subplots=True)
    name = 'plots/wages_by_years_at_' + area + '_with_' + code + '.png'
    plt.savefig(name)

    # inflation
    data_cpi = pandas.read_csv('ILO/CPI_NCYR_COI_RT_A.csv')
    classiff = pandas.read_csv('ILO/classif1_en.csv')
    typeofclassif = classiff.rename(columns={' classif1.label': 'label'})[classiff.classif1 == code].label.to_string(
        header=False, index=False)[12:]

    data_cpi = data_cpi[data_cpi.classif1 == code][['ref_area', 'time', 'obs_value']]
    data_cpi = data_cpi.rename(columns={'obs_value': 'cpi_change'})
    data_cpi = data_cpi.set_index(['ref_area', 'time'])
    data = data.join(data_cpi, on=['ref_area', 'time'])
    data_cpi['cpi_value'] = data_cpi.cpi_change + 100
    data_cpi['cpi_factor'] = data_cpi.cpi_value / 100

    data_cpi_1993 = data_cpi.loc[data_cpi.index.get_level_values(1) > 1992]
    data_cpi_1993['cpi_factor_1992'] = data_cpi_1993.sort_index().groupby(by=['ref_area'])['cpi_factor'].cumprod()
    data = data.drop(columns=['cpi_change'])
    data = data.join(data_cpi_1993, on=['ref_area', 'time'])
    data['wage_corr_cpi_1992'] = data.obs_value / data.cpi_factor_1992
    data_lcu_1993 = data[
        (data.ref_area == area) &
        (data.classif2 == 'CUR_TYPE_LCU') &
        (data.time >= 1993)
        ]
    if area == 'RUS':
        data_lcu_1993.loc[
            data_lcu_1993.time >= 1997,
            ['obs_value', 'wage_corr_cpi_1992']
        ] *= 1000
    data_lcu_1993.set_index('time').sort_index()[['obs_value', 'wage_corr_cpi_1992']] \
        .plot(title='Nominal wages vs real wages content in the prices of 1992 \nв '
                    + area + '(ILO) для ' + typeofclassif + '.',
              kind='bar', subplots=True)

    name = 'plots/wages_at_1992_vs_other_at_' + area + '_with_' + code + '.png'
    plt.savefig(name)


def part3(area='GBR'):
    data = pandas.read_csv('ILO/EAR_4MTH_SEX_ECO_CUR_NB_A.csv')
    data = data[
        (data.ref_area == area) &
        (data.classif1 == 'ECO_AGGREGATE_TOTAL') &
        (data.classif2 == 'CUR_TYPE_USD') &
        ((data.sex == 'SEX_M') | (data.sex == 'SEX_F'))
        ][['sex', 'time', 'obs_value']]
    pivot = data.pivot_table(index='time', columns='sex', values='obs_value', aggfunc='median')
    pivot.plot(kind='bar', title='Wages for males and females in ' + area + ' by years.')
    name = 'plots/wages_for_mvsf_in_' + area + '.png'
    plt.savefig(name)
    pivot['dif'] = (pivot.SEX_M - pivot.SEX_F)
    pivot[['dif']].plot(kind='bar',
                        title='Difference between male\'s and female\'s wages by years')
    name = 'plots/comparison_of_wages_by_sex_in_' + area + '.png'
    plt.savefig(name)


if __name__ == '__main__':
    part1()
    part1(area='USA')
    part1(area='CHN')
    part1(code='COI_COICOP_CP06')
    part1(area='USA', code='COI_COICOP_CP06')
    part3('EGY')  # EGY, LKA
