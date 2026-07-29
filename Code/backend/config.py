import os


class Settings:
    def __init__(self) -> None:
        self.env = os.getenv("ENV", "development")
        self.contact_email = os.getenv("CONTACT_EMAIL", "Eyeofaqaba@gmail.com")
        self.site_name_ar = "عين العقبة"
        self.site_name_en = "Eye of Aqaba"


settings = Settings()
