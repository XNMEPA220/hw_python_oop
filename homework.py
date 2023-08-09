import sys
from _collections_abc import Sequence as seq
from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    HOURS_IN_MINUTES: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Не определен метод в дочернем классе")

    def show_training_info(self,) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[int] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        duration_in_minutes = self.duration * self.HOURS_IN_MINUTES
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * speed
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * duration_in_minutes)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    WEIGHT_COEFF: ClassVar[float] = 0.035
    HEIGHT_COEFF: ClassVar[float] = 0.029
    KILOM_PER_HOUR_IN_METR_PER_SEC: ClassVar[float] = 0.278
    METR_IN_SANTIMETR: ClassVar[int] = 100

    def get_spent_calories(self) -> float:
        duration_in_minutes = self.duration * self.HOURS_IN_MINUTES
        speed_in_minute = (self.get_mean_speed()
                           * self.KILOM_PER_HOUR_IN_METR_PER_SEC)
        height_in_metr = self.height / self.METR_IN_SANTIMETR
        return ((self.WEIGHT_COEFF * self.weight
                 + (speed_in_minute**2 / height_in_metr)
                 * self.HEIGHT_COEFF * self.weight) * duration_in_minutes)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int

    SPEED_COEFF: ClassVar[float] = 1.1
    SUM_SPEED_COEFF: ClassVar[int] = 2
    LEN_STEP: ClassVar[float] = 1.38

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        return ((speed + self.SPEED_COEFF) * self.SUM_SPEED_COEFF
                * self.weight * self.duration)

    def get_distance(self) -> float:
        return super().get_distance()


def read_package(workout_type: str, data: seq[list[int]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_type_dict: dict[str, Training] = ({'SWM': Swimming,
                                             'RUN': Running,
                                             'WLK': SportsWalking})
    if workout_type in train_type_dict:
        used_train = train_type_dict[workout_type](*data)
        return used_train
    else:
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
