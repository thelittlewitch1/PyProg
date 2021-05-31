import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Самостоятельная работа:
# Николас Кейдж vs бассейны
# Найти исходные данные (источники)
# Проверить вычисления, приведенные на графике (фактчек)
# Убедиться, что источники содержат актуализированные данные за период времени после 2009 года
# Вычислить корреляцию для новых данных (2009-2019)
# Построить новый график и вычислить корреляцию для всего периода (1999 — 2019)
# еще: www.tylervigen.com/spurious-correlations
def cage_vs_pool():
    death = pandas.read_csv('mycsv/pool_death_by_years.csv', index_col='Year')
    cage = pandas.read_csv('mycsv/Cage.csv', index_col='Year')
    #cage['roles_val'] = cage.Films + cage.Multfilms
    data = pandas.concat([cage['Films'], death['death']], axis=1)
    data = data.dropna()
    data.plot(title='Is number of people, who drowned in swimming pool, \ncorrelates with number of film, Nicolas Cage appeared in?', grid=True)
    plt.show()


# Самостоятельна работа: ILO
# Взять 3 любые таблицы МОТ (ILO)
# Свести данные в общую таблицу
# Провести разведочный анализ:
# - Распределение значений
# - Попарные отношения
# - Тепловая карта корреляций
def ILO():
    sns.set(style='whitegrid', font_scale=1.6)

    wages = pandas.read_csv('ILO/EAR_4MTH_SEX_ECO_CUR_NB_A.csv')
    wages = wages[(wages.classif1 == 'ECO_AGGREGATE_TOTAL') &(wages.sex == 'SEX_T')]
    wages = wages.pivot_table(values='obs_value', index=['ref_area', 'time'], columns='classif2')
    wages = wages.rename(columns={
        'CUR_TYPE_USD': 'val_wage_usd',
        'CUR_TYPE_PPP': 'val_wage_ppp',
        'CUR_TYPE_LCU': 'val_wage_lcu'
    })
    wages['val_wage_lcu_prev'] = wages.sort_index(ascending=True).groupby(by=['ref_area'])['val_wage_lcu'].shift()
    wages['val_wage_change_lcu'] = wages['val_wage_lcu']/wages['val_wage_lcu_prev'] * 100 - 100

    inflat = pandas.read_csv('ILO/CPI_NCYR_COI_RT_A.csv')
    inflat = inflat[inflat.classif1 == 'COI_COICOP_CP01T12'][['ref_area', 'time', 'obs_value']]
    inflat = inflat.rename(columns={'obs_value': 'val_cpi_change'})
    inflat = inflat.set_index(['ref_area', 'time'])

    employ = pandas.read_csv('ILO/EMP_2EMP_AGE_STE_NB_A.csv')
    employ = employ.pivot_table(values='obs_value', index=['ref_area', 'time'], columns='classif2', aggfunc=np.sum)
    employ = employ.rename(columns={
        'STE_ICSE93_3' : 'Own-account_workers',
        'STE_ICSE93_1' : 'Employees',
        'STE_ICSE93_5' : 'Contributing_family_workers',
        'STE_ICSE93_TOTAL' : 'Total',
        'STE_ICSE93_2' : 'Employers',
        'STE_AGGREGATE_EES' : 'Employees_Agg',
        'STE_AGGREGATE_TOTAL' : 'Total_Agg',
        'STE_AGGREGATE_SLF' : 'Self-employed_Agg'
    })[['Own-account_workers', 'Employees', 'Contributing_family_workers', 'Employers']]

    data = wages.join([inflat, employ])
    #data = data.dropna()
    print(data, '\n', data.columns.values.tolist())

    # sns.pairplot(data[[
    #     'val_wage_lcu', 'val_wage_ppp', 'val_wage_usd',
    #     'val_wage_lcu_prev', 'val_wage_change_lcu', 'val_cpi_change',
    #     'Own-account_workers', 'Employees', 'Contributing_family_workers', 'Employers'
    # ]]).fig.suptitle("ILO pairplot (%d samples)" % len(data), y=(1 - 0.005))
    data = data[['val_wage_lcu', 'val_wage_change_lcu', 'Own-account_workers']].dropna()
    sns.pairplot(data).fig.suptitle("ILO pairplot (%d samples)" % len(data), y=(1 - 0.005))

    plt.show()

if __name__ == '__main__':
    cage_vs_pool()
    # ILO()