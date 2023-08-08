import sys
from _collections_abc import Sequence as seq


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

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM = 1000
    HOURS_IN_MINUTES = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self,) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        duration_in_minutes = self.duration * self.HOURS_IN_MINUTES
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                     + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                    / self.M_IN_KM * duration_in_minutes)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_COEFF = 0.035
    HEIGHT_COEFF = 0.029
    KILOM_PER_HOUR_IN_METR_PER_SEC = 0.278
    METR_IN_SANTIMETR = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_in_minutes = self.duration * self.HOURS_IN_MINUTES
        speed_in_minute = (self.get_mean_speed()
                           * self.KILOM_PER_HOUR_IN_METR_PER_SEC)
        height_in_metr = self.height / self.METR_IN_SANTIMETR
        calories = ((self.WEIGHT_COEFF * self.weight
                     + (speed_in_minute**2 / height_in_metr)
                     * self.HEIGHT_COEFF * self.weight) * duration_in_minutes)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    SPEED_COEFF = 1.1
    SUM_SPEED_COEFF = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        callories = ((speed + self.SPEED_COEFF) * self.SUM_SPEED_COEFF
                     * self.weight * self.duration)
        return callories

    def get_distance(self) -> float:
        return super().get_distance()


def read_package(workout_type: str, data: seq[list[int]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_type_dict: dict[str, Training] = ({'SWM': Swimming,
                                             'RUN': Running,
                                             'WLK': SportsWalking})
    try:
        used_train = train_type_dict[workout_type](*data)
        return used_train
    except KeyError:
        print('Передан неизвестный workout_type')
        sys.exit()


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('QWE', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
