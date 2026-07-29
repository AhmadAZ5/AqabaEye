"""
Placeholder content shaped exactly like the Google Sheets schema in PRD FR-2.
Phase 2 swaps this module for a live sheet fetch without touching templates.
"""

WATERPARKS = [
    {
        "slug": "saraya-aqaba-waterpark",
        "name_ar": "سرايا العقبة ووتر بارك",
        "name_en": "Saraya Aqaba Waterpark",
        "summary_ar": "منتزه مائي عائلي على شاطئ سرايا العقبة بألعاب مائية لكل الأعمار.",
        "summary_en": "A family waterpark on the Saraya Aqaba shoreline with rides for every age.",
        "description_ar": "نص وصفي مؤقت لمنتزه سرايا العقبة المائي. سيُستبدل بمحتوى فعلي من العميل في مرحلة لاحقة.",
        "description_en": "Placeholder description for Saraya Aqaba Waterpark. Real copy, photography and pricing arrive from the client in a later phase.",
        "price_adult": 25,
        "price_child": 15,
        "currency": "JOD",
        "hours": "10:00 - 18:00",
        "lat": 29.5123,
        "lng": 34.9938,
        "partner_url": "https://example.com/PLACEHOLDER-saraya-waterpark",
        "image_urls": [],
        "is_featured": True,
        "is_published": True,
        "last_verified": "2026-07-01",
    },
    {
        "slug": "sindbad-group-jordan",
        "name_ar": "مجموعة سندباد الأردن",
        "name_en": "Sindbad Group Jordan",
        "summary_ar": "أنشطة بحرية ومائية متنوعة على ساحل العقبة.",
        "summary_en": "A range of marine and water activities on the Aqaba coastline.",
        "description_ar": "نص وصفي مؤقت لمجموعة سندباد الأردن. سيُستبدل بمحتوى فعلي من العميل في مرحلة لاحقة.",
        "description_en": "Placeholder description for Sindbad Group Jordan. Real copy, photography and pricing arrive from the client in a later phase.",
        "price_adult": 20,
        "price_child": 12,
        "currency": "JOD",
        "hours": "09:00 - 17:00",
        "lat": 29.5177,
        "lng": 34.9857,
        "partner_url": "https://example.com/PLACEHOLDER-sindbad-group",
        "image_urls": [],
        "is_featured": True,
        "is_published": True,
        "last_verified": "2026-07-01",
    },
    {
        "slug": "saraya-aqaba-beach-club",
        "name_ar": "نادي سرايا العقبة الشاطئي",
        "name_en": "Saraya Aqaba Beach Club",
        "summary_ar": "نادي شاطئي هادئ مع إطلالة على البحر الأحمر.",
        "summary_en": "A relaxed beach club with Red Sea views.",
        "description_ar": "نص وصفي مؤقت لنادي سرايا العقبة الشاطئي. سيُستبدل بمحتوى فعلي من العميل في مرحلة لاحقة.",
        "description_en": "Placeholder description for Saraya Aqaba Beach Club. Real copy, photography and pricing arrive from the client in a later phase.",
        "price_adult": 15,
        "price_child": 8,
        "currency": "JOD",
        "hours": "08:00 - 19:00",
        "lat": 29.5108,
        "lng": 34.9951,
        "partner_url": "https://example.com/PLACEHOLDER-saraya-beach-club",
        "image_urls": [],
        "is_featured": False,
        "is_published": True,
        "last_verified": "2026-06-15",
    },
]

POSTS = [
    {
        "slug": "best-time-to-visit-aqaba",
        "title_ar": "أفضل وقت لزيارة العقبة",
        "title_en": "The Best Time to Visit Aqaba",
        "body_ar": "محتوى مدونة مؤقت. سيُستبدل بمقال فعلي عن أفضل الأوقات لزيارة العقبة.",
        "body_en": "Placeholder blog content. Will be replaced with a real article about the best seasons to visit Aqaba.",
        "cover_image": "",
        "published_at": "2026-06-01",
        "is_published": True,
    },
    {
        "slug": "diving-in-the-red-sea",
        "title_ar": "الغوص في البحر الأحمر",
        "title_en": "Diving in the Red Sea",
        "body_ar": "محتوى مدونة مؤقت عن مواقع الغوص في العقبة.",
        "body_en": "Placeholder blog content about dive sites near Aqaba.",
        "cover_image": "",
        "published_at": "2026-06-10",
        "is_published": True,
    },
    {
        "slug": "a-weekend-itinerary",
        "title_ar": "برنامج نهاية أسبوع في العقبة",
        "title_en": "A Weekend Itinerary in Aqaba",
        "body_ar": "محتوى مدونة مؤقت لبرنامج مقترح لنهاية أسبوع.",
        "body_en": "Placeholder blog content suggesting a two-day weekend itinerary.",
        "cover_image": "",
        "published_at": "2026-06-20",
        "is_published": True,
    },
]

FAQ = [
    {
        "question_ar": "هل يمكنني الحجز والدفع من خلال هذا الموقع؟",
        "question_en": "Can I book and pay through this site?",
        "answer_ar": "لا، هذا الموقع يعرض الأسعار وأوقات الزيارة ثم يوجهك إلى موقع الجهة المشغلة لإتمام الحجز.",
        "answer_en": "No — this site shows prices and hours, then sends you to the operator's own site to book and pay.",
        "sort_order": 1,
    },
    {
        "question_ar": "هل الأسعار المعروضة محدثة دائمًا؟",
        "question_en": "Are the listed prices always current?",
        "answer_ar": "نعرض تاريخ آخر تحقق من كل سعر. ننصح بالتأكد من السعر النهائي مع الجهة المشغلة.",
        "answer_en": "Each price shows a last-verified date. Please confirm the final price with the operator directly.",
        "sort_order": 2,
    },
]

SETTINGS = {
    "phone": "+962 000 000 000",
    "email": "Eyeofaqaba@gmail.com",
    "address_ar": "العقبة، الأردن",
    "address_en": "Aqaba, Jordan",
}
