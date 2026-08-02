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

        # Apps Script web app url that appends a row to the "clicks" tab, optional,
        # click tracking just quietly does nothing if this is blank
        self.clicks_webhook_url = os.getenv("CLICKS_WEBHOOK_URL", "")

        # SMTP creds for the contact form, blank user/password means the form
        # can't send and api_contact reports that instead of pretending it worked
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")


settings = Settings()
