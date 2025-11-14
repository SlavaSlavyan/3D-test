class Vehicle:
    """Базовый класс для всех транспортных средств"""
    
    def __init__(
        self, 
        brand, 
        model, 
        year
    ):
        
        self.brand = brand
        self.model = model
        self.year = year
        self.engine_started = False
    
    def start_engine(self):
        """Запуск двигателя"""
        
        if not self.engine_started:
            self.engine_started = True
            print("Двигатель запущен")
            
        else:
            print("Двигатель уже запущен")
    
    def stop_engine(self):
        """Остановка двигателя"""
        
        if self.engine_started:
            self.engine_started = False
            print("Двигатель остановлен")
            
        else:
            print("Двигатель уже остановлен")
    
    def display_info(self):
        """Отображение информации о транспортном средстве"""
        
        return f"Марка: {self.brand}, Модель: {self.model}, Год: {self.year}"

class Car(Vehicle):
    
    """Класс автомобиля, наследуется от Vehicle"""
    
    def __init__(
        self, 
        brand, 
        model, 
        year, 
        doors, 
        fuel_type):
        
        super().__init__(brand, model, year)
        
        self.doors = doors
        self.fuel_type = fuel_type
    
    def display_info(self):
        
        """Переопределение метода для отображения информации об автомобиле"""
        
        base_info = super().display_info()
        
        return f"{base_info}\nКоличество дверей: {self.doors}, Тип топлива: {self.fuel_type}"


class Motorcycle(Vehicle):
    
    """Класс мотоцикла, наследуется от Vehicle"""
    
    def __init__(
        self, 
        brand, 
        model, 
        year, 
        engine_volume, 
        bike_type):
        
        super().__init__(brand, model, year)
        
        self.engine_volume = engine_volume
        self.bike_type = bike_type
    
    def display_info(self):
        """Переопределение метода для отображения информации о мотоцикле"""
        
        base_info = super().display_info()
        return f"{base_info}\nОбъем двигателя: {self.engine_volume}, Тип: {self.bike_type}"

if __name__ == "__main__":
    
    car = Car("Toyota", "Camry", 2022, 4, "бензин")
    car.start_engine()
    
    print(car.display_info())
    
    car.stop_engine()
    
    motorcycle = Motorcycle("Harley-Davidson", "Sportster", 2020, 1200, "круизер")
    motorcycle.start_engine()
    
    print(motorcycle.display_info())
    
    motorcycle.stop_engine()