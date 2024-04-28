import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv(
    r"D:\Программирование\Хакатоны\цп\цп 26.04.24-28.04.24\train_dataset_train_Feedback\train_Feedback\train_data.csv")[
     :101]
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')
time_intervals = list(df['timestamp'].unique())
obj = {
    0: 'вебинарам',
    1: 'программам',
    2: 'преподавателям'
}


def get_all_pn_plot(in_percent: bool = False):
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
    plt.show()


def get_specifically_pn_plot(specifically_object: int, in_percent: bool = False):
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
    plt.legend()

    # Отображаем график
    plt.xticks(rotation=45)
    plt.show()


def get_all_obj_all_rew_plot(in_percent: bool = False):
    plt.figure(figsize=(20, 12))

    reviews_counts = df.groupby(['timestamp', 'object']).size().unstack(fill_value=0)
    total_reviews = reviews_counts.sum(axis=1)
    reviews_percentages = reviews_counts.div(total_reviews, axis=0) * 100
    if in_percent:
        plt.bar(reviews_percentages.index, reviews_percentages[0], color='lightblue', label='Вебинары')
        plt.bar(reviews_percentages.index, reviews_percentages[1], bottom=reviews_percentages[0], color='salmon', label='Материал')
        plt.bar(reviews_percentages.index, reviews_percentages[2], bottom=reviews_percentages[0] + reviews_percentages[1], color='green', label='Преподаватели')

    else:
        plt.bar(reviews_counts.index, reviews_counts[0], color='lightblue', label='Вебинары')
        plt.bar(reviews_counts.index, reviews_counts[1], bottom=reviews_counts[0], color='salmon', label='Материал')
        plt.bar(reviews_counts.index, reviews_counts[2], bottom=reviews_counts[0] + reviews_counts[1], color='green',
                label='Преподаватели')

    # Настраиваем график
    plt.xlabel('Время')
    plt.ylabel(f'{"Процент" if in_percent else "Количество"} отзывов')
    plt.title('Отношение объектов по всем отзывам от времени')
    plt.xticks(range(len(time_intervals)), time_intervals, rotation=45)
    plt.legend()

    # Отображаем график
    plt.tight_layout()
    plt.show()


def plot_positive_or_negative_reviews_ratio(in_percent: bool = False):
    plt.figure(figsize=(20, 12))
    reviews_counts = df[df['is_relevant'] == 1].groupby(['timestamp', 'object']).size().unstack(fill_value=0)
    total_reviews = reviews_counts.sum(axis=1)
    reviews_percentages = reviews_counts.div(total_reviews, axis=0) * 100

    if in_percent:
        plt.bar(reviews_percentages.index, reviews_percentages[0], color='lightblue', label='Вебинары')
        plt.bar(reviews_percentages.index, reviews_percentages[1], bottom=reviews_percentages[0], color='salmon', label='Материал')
        plt.bar(reviews_percentages.index, reviews_percentages[2], bottom=reviews_percentages[0] + reviews_percentages[1], color='green', label='Преподаватели')

    else:
        plt.bar(reviews_counts.index, reviews_counts[0], color='lightblue', label='Вебинары')
        plt.bar(reviews_counts.index, reviews_counts[1], bottom=reviews_counts[0], color='salmon', label='Материал')
        plt.bar(reviews_counts.index, reviews_counts[2], bottom=reviews_counts[0] + reviews_counts[1], color='green',
                label='Преподаватели')



plot_positive_or_negative_reviews_ratio()