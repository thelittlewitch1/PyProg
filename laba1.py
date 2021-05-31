import pandas

def laba0(data):
    (row_count, col_count) = data.shape
    print("row count = " + str(row_count) + ", column count = " + str(col_count))
    print("Values of columns:\n", data.columns.values.tolist())
    print("Counts of values in \'ref_area\':\n", data.ref_area.value_counts())
    print("Data in USA:\n", data[data.ref_area == 'USA'])
    print("Data in Russia:\n", data[data.ref_area == 'RUS'])
    print("Counts of values in \'time\' for Russia:\n", data[data.ref_area == 'RUS'].time.value_counts().sort_index())
    print("Counts of values in Russia at 2005:\n", data[(data.ref_area == 'RUS') & (data.time == 2005)])
    print("Counts of values in Russia for total economic activities, at 2013-2015:\n", data[
              (data.ref_area == 'RUS') &
              (data.classif1 == 'ECO_AGGREGATE_TOTAL') &
              ((data.time >= 2013) & (data.time <= 2015))
              ])
    data_rus = data[
        (data.ref_area == 'RUS') &
        (data.classif1 == 'ECO_AGGREGATE_TOTAL') &
        ((data.time >= 2013) & (data.time <= 2015))
        ]
    bool_filter = (data_rus.time == 2014)
    print("boolean filter:\n", bool_filter)
    print("type of boolean filter:\n", type(bool_filter))
    print("data after using boolean filter on it:\n", data_rus[bool_filter])

    print("Counts of values in \'ref_area\':\n", data.ref_area.value_counts())

    print("INFO for across all industries, for all sexes, in USD.")
    data_TTU = data[
        (data.classif1 == 'ECO_AGGREGATE_TOTAL') &
        (data.sex == 'SEX_T') &
        (data.classif2 == 'CUR_TYPE_USD') &
        (data.ref_area != 'BLR') & (data.ref_area != 'ZWE')
        ]
    print("min: " + str(data_TTU.obs_value.min()))
    print("max: " + str(data_TTU.obs_value.max()))
    print("mean: " + str(data_TTU.obs_value.mean()))
    print("median: " + str(data_TTU.obs_value.median()))

    data_TTU = data_TTU[['ref_area', 'ref_area_label', 'sex', 'classif1', 'classif2', 'time', 'obs_value']]

    print("Top-20 countries by highest wages:")
    print(data_TTU.sort_values(by='obs_value', ascending=False)[:20])
    print("\nTop-20 countries by lowest wages:")
    print(data_TTU.sort_values(by='obs_value', ascending=True)[:20])
    print("Top-20 countries by highest wages at 2019:")
    print(data_TTU[data_TTU.time == 2019].sort_values(by='obs_value', ascending=False)[:20])
    print("Top-20 countries by lowest wages at 2019:")
    print(data_TTU[data_TTU.time == 2019].sort_values(by='obs_value', ascending=True)[:20])
    print("Top-20 countries by highest wages at 1989:")
    print(data_TTU[data_TTU.time == 1989].sort_values(by='obs_value', ascending=False)[:20])
    print("Top-20 countries by lowest wages at 1989:")
    print(data_TTU[data_TTU.time == 1989].sort_values(by='obs_value', ascending=True)[:20])


def laba1sex(data):
    country = 'EGY'
    print("\n\nINFO across all industries, in USD, in " + country + ", comparison by sex.")
    data_TMU = data[
        (data.classif1 == 'ECO_AGGREGATE_TOTAL') &
        (data.sex == 'SEX_M') &
        (data.classif2 == 'CUR_TYPE_USD') &
        (data.ref_area == country)
        ]
    data_TMU = data_TMU[['time', 'obs_value']]
    print("Males:\n", data_TMU.sort_values(by='time', ascending=True))
    data_TFU = data[
        (data.classif1 == 'ECO_AGGREGATE_TOTAL') &
        (data.sex == 'SEX_F') &
        (data.classif2 == 'CUR_TYPE_USD') &
        (data.ref_area == country)
        ]
    data_TFU = data_TFU[['time', 'obs_value']]
    print("Females:\n", data_TFU.sort_values(by='time', ascending=True))
    INFO = pandas.DataFrame(
        {
            'Male': [data_TMU.obs_value.min(), data_TMU.obs_value.max(), data_TMU.obs_value.mean(),
                     data_TMU.obs_value.median()],
            'Female': [data_TFU.obs_value.min(), data_TFU.obs_value.max(), data_TFU.obs_value.mean(),
                       data_TFU.obs_value.median()]
        }, index=['min', 'max', 'mean', 'median']
    )
    print(INFO)


def laba1ea(data):
    print("\n\nINFO in USD, in all countries, for total by sex, for art, entertainment, recreational activity.")
    data_ATU = data[
        (data.sex == 'SEX_T') &
        (data.classif2 == 'CUR_TYPE_USD') &
        (data.classif1 == 'ECO_ISIC4_R')
        ]
    data_ATU = data_ATU[['ref_area', 'ref_area_label', 'time', 'obs_value']]
    print(data_ATU)

    print("min: " + str(data_ATU.obs_value.min()))
    print("max: " + str(data_ATU.obs_value.max()))
    print("mean: " + str(data_ATU.obs_value.mean()))
    print("median: " + str(data_ATU.obs_value.median()))

    print("Top-20 countries by highest wages:")
    print(data_ATU.sort_values(by='obs_value', ascending=False)[:20])
    print("\nTop-20 countries by lowest wages:")
    print(data_ATU.sort_values(by='obs_value', ascending=True)[:20])


def laba2():
    data = pandas.read_csv('ILO/EMP_2EMP_AGE_STE_NB_A.csv')
    # ref_area,indicator,source,classif1,classif2,time,obs_value,obs_status
    data = data[['ref_area', 'classif1', 'classif2', 'time', 'obs_value']]
    data_ref_area = pandas.read_csv('ILO/ref_area_en.csv', index_col='ref_area')
    data_ref_area = data_ref_area.rename(columns={' ref_area.label': 'ref_area_label'})
    data_ref_area = data_ref_area[['ref_area_label']]
    data = data.join(data_ref_area, on=['ref_area'])
    data = data[['ref_area', 'ref_area_label', 'classif1', 'classif2', 'time', 'obs_value']]

    for i in range(1, 91):
        if i < 10:
            buf = 'X0' + str(i)
        else:
            buf = 'X' + str(i)
        data = data[data.ref_area != buf]

    # classif1 - ages, classif2 - Status in employment
    print("Employment in thousands for across age 15-24, for all statuses, in 2019.")
    data_AA2019 = data[
        (data.classif1 == 'AGE_YTHADULT_Y15-24') &
        (data.time == 2019) &
        (data.classif2 == 'STE_AGGREGATE_TOTAL')
        ]
    print(data_AA2019)
    print("\nmin: " + str(data_AA2019.obs_value.min()))
    print(data_AA2019[data_AA2019.obs_value == data_AA2019.obs_value.min()][
              ['ref_area', 'ref_area_label', 'time', 'obs_value']])
    print("\nmax: " + str(data_AA2019.obs_value.max()))
    print(data_AA2019[data_AA2019.obs_value == data_AA2019.obs_value.max()][
              ['ref_area', 'ref_area_label', 'time', 'obs_value']])
    print("\nmean: " + str(data_AA2019.obs_value.mean()))
    print("\nmedian: " + str(data_AA2019.obs_value.median()))

    print("Top-20 countries by highest number of thousands of employed:")
    print(data_AA2019.sort_values(by='obs_value', ascending=False)[:20][
              ['ref_area', 'ref_area_label', 'classif2', 'time', 'obs_value']])
    print("\nTop-20 countries by lowest number of thousands of employed:")
    print(data_AA2019.sort_values(by='obs_value', ascending=True)[:20][
              ['ref_area', 'ref_area_label', 'classif2', 'time', 'obs_value']])


if __name__ == '__main__':
    data = pandas.read_csv('ILO/EAR_4MTH_SEX_ECO_CUR_NB_A.csv')
    data = data[['ref_area', 'sex', 'classif1', 'classif2', 'time', 'obs_value']]

    data_ref_area = pandas.read_csv('ILO/ref_area_en.csv', index_col='ref_area')
    data_ref_area = data_ref_area.rename(columns={' ref_area.label': 'ref_area_label'})
    data_ref_area = data_ref_area[['ref_area_label']]
    data = data.join(data_ref_area, on=['ref_area'])
    data = data[['ref_area', 'ref_area_label', 'sex', 'classif1', 'classif2', 'time', 'obs_value']]
    # classif1 - разделение по отрослям. "...Aggregate..." - суммарный.
    # classif2 - валюта. USD, LCU, PPP.
    laba0(data)
    laba1sex(data)
    laba1ea(data)
    laba2()
