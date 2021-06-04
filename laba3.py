# Придумать, как их вытянуть все в строку
# Например, при помощи сводной таблицы pivot_table
# Можно сделать аналог дамми-кодирования и мешка слов
# Для каждой страны-происхождения по одной колонке
# И в этой колонке флаг: 1 — иммигранты есть в выбранной строке в выбранный год, 0 — иммигрантов нет
import pandas

if __name__ == '__main__':
    data = pandas.read_csv('ILO/MFL_FPOP_SEX_CBR_NB_A.csv')
    data = data[
        (data.classif1 != 'CBR_BRT_TOTAL') &
        (data.classif1 != 'CBR_BRT_X')
        ]
    data = data[data.sex == 'SEX_T']
    data = data[
        ['ref_area', 'time', 'classif1', 'obs_value']
    ]
    data = data.pivot_table(values='obs_value', index=['ref_area', 'time'], columns='classif1',
                            aggfunc='count', fill_value=0)
    print('List of columns values:\n', data.columns.values.tolist())
    print('\nImmigrants to Russia by years:\n', data.loc['RUS'])
    print('\nImmigrants to Russia at 2011:\n', data.loc[('RUS',2011),:])
    print('\nAll table:\n', data)