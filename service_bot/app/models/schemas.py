from pydantic import BaseModel

class AppointmentForm(BaseModel):
    name: str
    phone: str
    car_model: str
    problem: str
    appointment_time: str

    def format_for_channel(self) -> str:
        return (f"📝 Новая заявка\n"
                f"👤 Имя: {self.name}\n"
                f"📞 Телефон: {self.phone}\n"
                f"🚗 Машина: {self.car_model}\n"
                f"❗ Проблема: {self.problem}\n"
                f"🕒 Время: {self.appointment_time}\n")