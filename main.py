from __future__ import annotations

class Training:
    """Базовый класс."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    def __init__ (self, action:int, duraction:float, weight:float) -> None:
        self.action = action       #количество совершённых действий для метода get_distance()
        self.duraction = duraction #длителльность тренировки для метода get_mean_speed()
        self.weight = weight       #вес спортсмена для рассчета каллориев в наследуюемых классах

    def get_distance(self) -> float:
        """Возвращает дистанцию (в километрах), которую преодолел пользователь за время тренировки."""
        distance:float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Возвращает значение средней скорости движения во время тренировки."""
        avr_speed:float = self.distance/self.duraction
        return avr_speed

    def get_spent_calories(self) -> None:
        """Возвращает количество килокалорий, израсходованных за время тренировки."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращает сообщение о результатах тренировки."""
        #Добавить параметр training_type
        return InfoMessage(self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())

class Running(Training):
    """Класс-наследник. Бег."""
    training_type = 'RUN'
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    def __init__(self, action:int, duraction:float, weight:float) -> None:
        super().__init__(action, duraction, weight)

    def get_spent_calories(self) -> float:
        """"Возвращает количества потраченных калорий во время бега."""
        calories_run: float = ((self.coeff_calorie_1 * self.get_mean_speed - self.coeff_calorie_2)
                           * self.weight/self.M_IN_KM * (self.duraction * 60))
        return calories_run

class SportsWalking(Training):
    """Класс-наследник. Спортивная ходьба."""
    training_type = 'WLK'
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029
    def __init__(self, action: int, duraction:float, weight:float, height:float) -> None:
        super().__init__(action, duraction, weight)
        self.height = height

    def get_spent_calories(self):
        """"Возвращает количества потраченных калорий во время спортивной ходьбы."""
        calories_walk: float = (self.coeff_calorie_3 * self.weight +
                                (self.get_mean_speed**2 // self.height)
                                * self.coeff_calorie_4 * self.weight) * (self.duraction*60)
        return calories_walk

class Swimming(Training):
    """Класс-наследник. Плавание."""
    training_type = 'SWM'
    LEN_SWIM: float = 1.38
    coeff_calorie_5: float = 1.1
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
        distance: float = (self.action * self.LEN_SWIM / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Возвращает значение средней скорости."""
        avr_speed: float = self.length_pool * self.count_pool / self.M_IN_KM / self.duraction
        return avr_speed

    def get_spent_calories(self):
        """"Возвращает количества потраченных калорий во время плавания."""
        calories_swim = (self.avr_speed + self.coeff_calorie_5) * 2 * self.weight
        return calories_swim

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):  # Выводим сообщение о треннировке
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительнось: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потраченно ккал: {self.calories}.')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

def main(Training) -> None:
    message = Training.show_training_info()
    print(message)

def read_package(workout_type, data) -> Training:
    result: dict = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}
    if workout_type == 'RUN':
        return Running.show_training_info()
    elif workout_type == 'WLK':
        return SportsWalking.show_training_info()
    else:
        return Swimming.show_training_info()


#________________________main___________________________
print('Укажите тип тренировки. '
      'бег - Running, '
      'спортивная ходьба - SportsWalking, '
      'плавание - Swimming: ')
training_type = input()

print('Укажите количество действий. ')
number_of_actions = int(input())

print('Укажите длительность тренировки в часах. ')
duration = float(input())

print('Укажите вес спортсмена. ')
man_weight = float(input())