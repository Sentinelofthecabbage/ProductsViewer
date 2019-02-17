class MainTableInteractor:
    def __init__(self):
        pass

    def get_data(self, row_filter, column_filter):
        data = [
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Сулейманов"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Наиль", "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин",
             "Андрей",
             "Федоров", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Макс", "Озирный", "Виталий", "Перятин", "Андрей", "Федоров",
             "Наиль",
             "Сулейманов", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров", "Наиль", "Ласт"],
            ["Виталий", "Перятин", "Андрей", "Федоров", "Наиль", "Сулейманов",
             "Макс",
             "Озирный", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Андрей", "Федоров", "Наиль", "Сулейманов", "Макс", "Озирный",
             "Виталий",
             "Перятин", "Макс", "Озирный", "Виталий", "Перятин", "Андрей",
             "Федоров",
             "Наиль", "Ласт"],
            ["Ласт", "Ласт", "Ласт", "Ласт", "Ласт", "Ласт",
             "Ласт",
             "Ласт", "Ласт", "Ласт", "Ласт", "Ласт", "Ласт",
             "Ласт",
             "Ласт", "Ласт"]
        ]
        return data
