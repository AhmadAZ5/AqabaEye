import os


class Settings:
    def __init__(self) -> None:
        self.env = os.getenv("ENV", "development")
        self.contact_email = os.getenv("CONTACT_EMAIL", "Eyeofaqaba@gmail.com")
        self.site_name_ar = "عين العقبة"
        self.site_name_en = "Eye of Aqaba"

        # published-to-web CSV urls for each tab of the content spreadsheet, one
        # per tab, all optional, if any of these are blank sheets.py just falls
        # back to the committed snapshot.json for that tab and the site still works
        self.sheet_csv_waterparks = os.getenv("SHEET_CSV_WATERPARKS", "")
        self.sheet_csv_attractions = os.getenv("SHEET_CSV_ATTRACTIONS", "")
        self.sheet_csv_posts = os.getenv("SHEET_CSV_POSTS", "")
        self.sheet_csv_faq = os.getenv("SHEET_CSV_FAQ", "")
        self.sheet_csv_settings = os.getenv("SHEET_CSV_SETTINGS", "")


settings = Settings()
