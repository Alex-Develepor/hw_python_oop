class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.workout_type = 'Training'

        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.workout_type, self.duration,
                            self.get_distance(), self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ):
        super().__init__(action, duration, weight)
        self.coeff_calories_1 = 18
        self.coeff_calories_2 = 20
        self.workout_type = 'Running'

    def get_spent_calories(self) -> float:
        minute = self.duration * 60
        spent_calories = ((self.coeff_calories_1 * self.get_mean_speed()
                           - self.coeff_calories_2) * self.weight
                          / self.M_IN_KM * minute)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height
        self.K1 = 0.035
        self.K2 = 0.029
        self.workout_type = 'SportsWalking'

    def get_spent_calories(self) -> float:
        minutes = self.duration * 60
        spent_calories = ((self.K1 * self.weight + (
                self.get_mean_speed() ** 2 // self.height)
                           * self.K2 * self.weight) * minutes)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

        self.workout_type = 'Swimming'

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    Training(data[0], data[1], data[2])
    if workout_type == 'SWM' and len(data) == 5:
        swimming = Swimming(data[0], data[1], data[2], data[3], data[4])
        return swimming
    elif workout_type == 'RUN':
        run = Running(data[0], data[1], data[2])
        return run
    elif workout_type == 'WLK':
        walk = SportsWalking(data[0], data[1], data[2], data[3])
        return walk


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info = info.get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),

    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
