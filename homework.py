from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return ('Тип тренировки: {}; '
                'Длительность: {:.3f} ч.; '
                'Дистанция: {:.3f} км; '
                'Ср. скорость: {:.3f} км/ч; '
                'Потрачено ккал: {:.3f}.'
                .format(self.training_type,
                        self.duration,
                        self.distance,
                        self.speed,
                        self.calories))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах)."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Возвращает значение средней скорости движения."""
        distance: float = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Возвращает количество килокалорий."""
        raise NotImplementedError('Метод не определен.')

    def show_training_info(self) -> InfoMessage:
        """Возвращает сообщение о результатах тренировки."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MULTIPLIER: int = 18
    CALORIES_SHIFT: int = 20
    TIME: int = 60

    def get_spent_calories(self) -> float:
        """"Возвращает количества потраченных калорий во время бега."""
        average_speed: float = self.get_mean_speed()
        calories: float = ((self.CALORIES_MULTIPLIER
                           * average_speed
                           - self.CALORIES_SHIFT)
                           * self.weight
                           / self.M_IN_KM * (self.duration
                           * self.TIME))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT: float = 0.035
    CALORIES_WEIGHT_MULT: float = 0.029
    TIME: int = 60
    POW: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """"Возвращает количества потраченных калорий."""
        avr_speed: float = self.get_mean_speed()
        calories: float = ((self.CALORIES_WEIGHT * self.weight
                           + (avr_speed ** self.POW // self.height)
                           * self.CALORIES_WEIGHT_MULT * self.weight)
                           * self.duration * self.TIME)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE: float = 1.1
    MULTIPL_TWO: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах)."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Возвращает значение средней скорости."""
        len_count: float = self.length_pool * self.count_pool
        div_pool_km: float = len_count / self.M_IN_KM
        avr_speed_swim: float = div_pool_km / self.duration
        return avr_speed_swim

    def get_spent_calories(self) -> float:
        """"Возвращает количества потраченных калорий во время плавания."""
        avr_speed_man: float = self.get_mean_speed()
        calories: float = ((avr_speed_man + self.COEFF_CALORIE)
                           * self.MULTIPL_TWO * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    information: dict = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}
    if workout_type not in information:
        raise ValueError('Некорректное название тренировки.')
    return information[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    message: InfoMessage = training.show_training_info()
    return print(message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
