from io import BytesIO

import pandas as pd
from matplotlib import pyplot as plt

obj = {
    0: 'вебинарам',
    1: 'программам',
    2: 'преподавателям'
}


def get_all_plots(data):
    df = pd.DataFrame(data, columns=['timestamp', 'question_1', 'question_2', 'question_3', 'question_4', 'question_5',
                                     'is_relevant', 'object', 'is_positive'])
    df["is_positive"] = df["is_positive"].astype(int)
    df["is_relevant"] = df["is_relevant"].astype(int)
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')
    res = (get_all_pn_plot(df), get_all_pn_plot(df, True),
           get_specifically_pn_plot(df, 0), get_specifically_pn_plot(df, 0, True),
           get_specifically_pn_plot(df, 1), get_specifically_pn_plot(df, 1, True),
           get_specifically_pn_plot(df, 2), get_specifically_pn_plot(df, 2, True)
           )
    try:
        res = res.__add__((get_all_obj_all_rew_plot(df, 0), get_all_obj_all_rew_plot(df, 0, True),
                           get_all_obj_all_rew_plot(df, 1), get_all_obj_all_rew_plot(df, 1, True),
                           get_all_obj_all_rew_plot(df, 2), get_all_obj_all_rew_plot(df, 2, True)))
    except:
        return res
    return res


def get_all_pn_plot(df, in_percent: bool = False):
    time_intervals = list(df['timestamp'].unique())
    if in_percent:
        positive_percentages = [
            (sum(df[df['timestamp'] == i]['is_positive']) / len(df[df['timestamp'] == i]['is_positive'])) * 100
            for i in time_intervals]
        negative_percentages = [
            (df[df['timestamp'] == i]['is_positive'].eq(0).sum() / len(df[df['timestamp'] == i]['is_positive'])) * 100
            for i in time_intervals]
    else:
        positive_percentages = [sum(df[df['timestamp'] == i]['is_positive']) for i in time_intervals]
        negative_percentages = [df[df['timestamp'] == i]['is_positive'].eq(0).sum() for i in time_intervals]

    plt.figure(figsize=(20, 12))
    plt.bar(time_intervals, positive_percentages, color='lightblue', label='Положительные')
    plt.bar(time_intervals, negative_percentages, color='salmon', bottom=positive_percentages, label='Отрицательные')

    plt.xlabel('Время')
    plt.ylabel(f'{"Процент" if in_percent else "Количество"} отзывов')
    plt.title(
        f'{"Процент" if in_percent else "Количество"} положительных и отрицательных отзывов по времени всех отзывов')
    plt.legend()

    plt.xticks(rotation=45)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def get_specifically_pn_plot(df, specifically_object: int, in_percent: bool = False):
    time_intervals = list(df['timestamp'].unique())

    positive_percentages = []
    negative_percentages = []

    if in_percent:
        for interval in time_intervals:
            feedbacks_in_interval = df[(df['timestamp'] == interval) & (df['object'] == specifically_object)]
            if not feedbacks_in_interval.empty:
                positive_feedbacks = feedbacks_in_interval['is_positive'].sum()
                total_feedbacks = len(feedbacks_in_interval)
                positive_percent = (positive_feedbacks / total_feedbacks) * 100
                negative_percent = ((total_feedbacks - positive_feedbacks) / total_feedbacks) * 100
                positive_percentages.append(positive_percent)
                negative_percentages.append(negative_percent)
            else:
                positive_percentages.append(0)
                negative_percentages.append(0)
    else:
        for interval in time_intervals:
            feedbacks_in_interval = df[(df['timestamp'] == interval) & (df['object'] == specifically_object)]
            if not feedbacks_in_interval.empty:
                positive_feedbacks = feedbacks_in_interval['is_positive'].sum()
                total_feedbacks = len(feedbacks_in_interval)
                negative_feedbacks = total_feedbacks - positive_feedbacks
                positive_percentages.append(positive_feedbacks)
                negative_percentages.append(negative_feedbacks)
            else:
                positive_percentages.append(0)
                negative_percentages.append(0)

    plt.figure(figsize=(20, 12))
    plt.bar(time_intervals, positive_percentages, color='lightblue', label='Положительные')
    plt.bar(time_intervals, negative_percentages, color='salmon', bottom=positive_percentages, label='Отрицательные')

    # Настраиваем график
    plt.xlabel('Время')
    plt.ylabel(f'{"Процент" if in_percent else "Количество"} отзывов')
    plt.title(
        f'{"Процент" if in_percent else "Количество"} положительных и отрицательных отзывов за {obj[specifically_object]} по времени')
    plt.xticks(rotation=45)
    plt.legend()

    # Отображаем график
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def get_all_obj_all_rew_plot(df, rew_type: int, in_percent: bool = False):
    """
    :param rew_type: 0 - негативные, 1 - положительные, 2 - все
    :param in_percent: вернуть график отношения в процентах или нет
    :return: график отношений
    """
    plt.figure(figsize=(20, 12))

    dff = df
    if rew_type == 0:
        dff = df[df['is_positive'] == 0]
    elif rew_type == 1:
        dff = df[df['is_positive'] == 1]

    reviews_counts = dff.groupby(['timestamp', 'object']).size().unstack(fill_value=0)
    total_reviews = reviews_counts.sum(axis=1)
    reviews_percentages = reviews_counts.div(total_reviews, axis=0) * 100

    if in_percent:
        plt.bar(range(len(reviews_percentages.index)), reviews_percentages[0], color='#172d5c', label='Вебинары')
        plt.bar(range(len(reviews_percentages.index)), reviews_percentages[1], bottom=reviews_percentages[0],
                color='#c33d72', label='Материал')
        plt.bar(range(len(reviews_percentages.index)), reviews_percentages[2],
                bottom=reviews_percentages[0] + reviews_percentages[1], color='#ffa600', label='Преподаватели')

        # Настраиваем метки оси x
        plt.xticks(range(len(reviews_percentages.index)), reviews_percentages.index, rotation=45)
    else:
        plt.bar(range(len(reviews_counts.index)), reviews_counts[0], color='#172d5c', label='Вебинары')
        plt.bar(range(len(reviews_counts.index)), reviews_counts[1], bottom=reviews_counts[0], color='#c33d72',
                label='Материал')
        plt.bar(range(len(reviews_counts.index)), reviews_counts[2], bottom=reviews_counts[0] + reviews_counts[1],
                color='#ffa600', label='Преподаватели')

        # Настраиваем метки оси x
        plt.xticks(range(len(reviews_counts.index)), reviews_counts.index, rotation=45)

    # Настраиваем график
    plt.xlabel('Время')
    plt.ylabel(f'{"Процент" if in_percent else "Количество"} отзывов')
    plt.title('Отношение объектов по всем отзывам от времени')
    plt.legend()

    # Отображаем график
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf
