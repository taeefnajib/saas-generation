import pandas as pd

country_codes = {
    "United States": {
        "alpha_2_code": "US",
        "alpha_3_code": "USA",
        "continent": "North America",
        "telephone_code": "+1",
        "currency": {
            1: {"currency_code": "USD", "conversion_rate": 1.0, "currency_symbol": "$"}
        },
        "language": {1: {"language_name": "English", "locale": "en-US"}},
    },
    "Japan": {
        "alpha_2_code": "JP",
        "alpha_3_code": "JPN",
        "continent": "Asia",
        "telephone_code": "+81",
        "currency": {
            1: {
                "currency_code": "JPY",
                "conversion_rate": 0.0073,
                "currency_symbol": "¥",
            }
        },
        "language": {1: {"language_name": "Japanese", "locale": "ja-JP"}},
    },
    "India": {
        "alpha_2_code": "IN",
        "alpha_3_code": "IND",
        "continent": "Asia",
        "telephone_code": "+91",
        "currency": {
            1: {
                "currency_code": "INR",
                "conversion_rate": 0.012,
                "currency_symbol": "₹",
            }
        },
        "language": {
            1: {"language_name": "Hindi", "locale": "hi-IN"},
            2: {"language_name": "English", "locale": "en-IN"},
        },
    },
    "China": {
        "alpha_2_code": "CN",
        "alpha_3_code": "CHN",
        "continent": "Asia",
        "telephone_code": "+86",
        "currency": {
            1: {"currency_code": "CNY", "conversion_rate": 0.14, "currency_symbol": "¥"}
        },
        "language": {1: {"language_name": "Mandarin", "locale": "zh-CN"}},
    },
    "Brazil": {
        "alpha_2_code": "BR",
        "alpha_3_code": "BRA",
        "continent": "South America",
        "telephone_code": "+55",
        "currency": {
            1: {
                "currency_code": "BRL",
                "conversion_rate": 0.20,
                "currency_symbol": "R$",
            }
        },
        "language": {1: {"language_name": "Portuguese", "locale": "pt-BR"}},
    },
    "Mexico": {
        "alpha_2_code": "MX",
        "alpha_3_code": "MEX",
        "continent": "North America",
        "telephone_code": "+52",
        "currency": {
            1: {
                "currency_code": "MXN",
                "conversion_rate": 0.057,
                "currency_symbol": "$",
            }
        },
        "language": {1: {"language_name": "Spanish", "locale": "es-MX"}},
    },
    "Egypt": {
        "alpha_2_code": "EG",
        "alpha_3_code": "EGY",
        "continent": "Africa",
        "telephone_code": "+20",
        "currency": {
            1: {
                "currency_code": "EGP",
                "conversion_rate": 0.032,
                "currency_symbol": "E£",
            }
        },
        "language": {1: {"language_name": "Arabic", "locale": "ar-EG"}},
    },
    "Bangladesh": {
        "alpha_2_code": "BD",
        "alpha_3_code": "BGD",
        "continent": "Asia",
        "telephone_code": "+880",
        "currency": {
            1: {
                "currency_code": "BDT",
                "conversion_rate": 0.0093,
                "currency_symbol": "৳",
            }
        },
        "language": {1: {"language_name": "Bengali", "locale": "bn-BD"}},
    },
    "Iran": {
        "alpha_2_code": "IR",
        "alpha_3_code": "IRN",
        "continent": "Asia",
        "telephone_code": "+98",
        "currency": {
            1: {
                "currency_code": "IRR",
                "conversion_rate": 0.000024,
                "currency_symbol": "﷼",
            }
        },
        "language": {1: {"language_name": "Persian", "locale": "fa-IR"}},
    },
    "Pakistan": {
        "alpha_2_code": "PK",
        "alpha_3_code": "PAK",
        "continent": "Asia",
        "telephone_code": "+92",
        "currency": {
            1: {
                "currency_code": "PKR",
                "conversion_rate": 0.0034,
                "currency_symbol": "₨",
            }
        },
        "language": {
            1: {"language_name": "Urdu", "locale": "ur-PK"},
            2: {"language_name": "English", "locale": "en-PK"},
        },
    },
    "Argentina": {
        "alpha_2_code": "AR",
        "alpha_3_code": "ARG",
        "continent": "South America",
        "telephone_code": "+54",
        "currency": {
            1: {
                "currency_code": "ARS",
                "conversion_rate": 0.0029,
                "currency_symbol": "$",
            }
        },
        "language": {1: {"language_name": "Spanish", "locale": "es-AR"}},
    },
    "Turkey": {
        "alpha_2_code": "TR",
        "alpha_3_code": "TUR",
        "continent": "Europe",
        "telephone_code": "+90",
        "currency": {
            1: {
                "currency_code": "TRY",
                "conversion_rate": 0.036,
                "currency_symbol": "₺",
            }
        },
        "language": {1: {"language_name": "Turkish", "locale": "tr-TR"}},
    },
    "Philippines": {
        "alpha_2_code": "PH",
        "alpha_3_code": "PHL",
        "continent": "Asia",
        "telephone_code": "+63",
        "currency": {
            1: {
                "currency_code": "PHP",
                "conversion_rate": 0.018,
                "currency_symbol": "₱",
            }
        },
        "language": {
            1: {"language_name": "Filipino", "locale": "fil-PH"},
            2: {"language_name": "English", "locale": "en-PH"},
        },
    },
    "Nigeria": {
        "alpha_2_code": "NG",
        "alpha_3_code": "NGA",
        "continent": "Africa",
        "telephone_code": "+234",
        "currency": {
            1: {
                "currency_code": "NGN",
                "conversion_rate": 0.0013,
                "currency_symbol": "₦",
            }
        },
        "language": {1: {"language_name": "English", "locale": "en-NG"}},
    },
    "DR Congo": {
        "alpha_2_code": "CD",
        "alpha_3_code": "COD",
        "continent": "Africa",
        "telephone_code": "+243",
        "currency": {
            1: {
                "currency_code": "CDF",
                "conversion_rate": 0.00039,
                "currency_symbol": "FC",
            }
        },
        "language": {1: {"language_name": "French", "locale": "fr-CD"}},
    },
    "Russia": {
        "alpha_2_code": "RU",
        "alpha_3_code": "RUS",
        "continent": "Europe",
        "telephone_code": "+7",
        "currency": {
            1: {
                "currency_code": "RUB",
                "conversion_rate": 0.011,
                "currency_symbol": "₽",
            }
        },
        "language": {1: {"language_name": "Russian", "locale": "ru-RU"}},
    },
    "France": {
        "alpha_2_code": "FR",
        "alpha_3_code": "FRA",
        "continent": "Europe",
        "telephone_code": "+33",
        "currency": {
            1: {"currency_code": "EUR", "conversion_rate": 1.07, "currency_symbol": "€"}
        },
        "language": {1: {"language_name": "French", "locale": "fr-FR"}},
    },
    "Colombia": {
        "alpha_2_code": "CO",
        "alpha_3_code": "COL",
        "continent": "South America",
        "telephone_code": "+57",
        "currency": {
            1: {
                "currency_code": "COP",
                "conversion_rate": 0.00026,
                "currency_symbol": "$",
            }
        },
        "language": {1: {"language_name": "Spanish", "locale": "es-CO"}},
    },
    "Indonesia": {
        "alpha_2_code": "ID",
        "alpha_3_code": "IDN",
        "continent": "Asia",
        "telephone_code": "+62",
        "currency": {
            1: {
                "currency_code": "IDR",
                "conversion_rate": 0.000064,
                "currency_symbol": "Rp",
            }
        },
        "language": {1: {"language_name": "Indonesian", "locale": "id-ID"}},
    },
    "Peru": {
        "alpha_2_code": "PE",
        "alpha_3_code": "PER",
        "continent": "South America",
        "telephone_code": "+51",
        "currency": {
            1: {
                "currency_code": "PEN",
                "conversion_rate": 0.27,
                "currency_symbol": "S/",
            }
        },
        "language": {1: {"language_name": "Spanish", "locale": "es-PE"}},
    },
    "Thailand": {
        "alpha_2_code": "TH",
        "alpha_3_code": "THA",
        "continent": "Asia",
        "telephone_code": "+66",
        "currency": {
            1: {
                "currency_code": "THB",
                "conversion_rate": 0.029,
                "currency_symbol": "฿",
            }
        },
        "language": {1: {"language_name": "Thai", "locale": "th-TH"}},
    },
    "South Korea": {
        "alpha_2_code": "KR",
        "alpha_3_code": "KOR",
        "continent": "Asia",
        "telephone_code": "+82",
        "currency": {
            1: {
                "currency_code": "KRW",
                "conversion_rate": 0.00075,
                "currency_symbol": "₩",
            }
        },
        "language": {1: {"language_name": "Korean", "locale": "ko-KR"}},
    },
    "United Kingdom": {
        "alpha_2_code": "GB",
        "alpha_3_code": "GBR",
        "continent": "Europe",
        "telephone_code": "+44",
        "currency": {
            1: {"currency_code": "GBP", "conversion_rate": 1.27, "currency_symbol": "£"}
        },
        "language": {1: {"language_name": "English", "locale": "en-GB"}},
    },
    "Vietnam": {
        "alpha_2_code": "VN",
        "alpha_3_code": "VNM",
        "continent": "Asia",
        "telephone_code": "+84",
        "currency": {
            1: {
                "currency_code": "VND",
                "conversion_rate": 0.000041,
                "currency_symbol": "₫",
            }
        },
        "language": {1: {"language_name": "Vietnamese", "locale": "vi-VN"}},
    },
    "Angola": {
        "alpha_2_code": "AO",
        "alpha_3_code": "AGO",
        "continent": "Africa",
        "telephone_code": "+244",
        "currency": {
            1: {
                "currency_code": "AOA",
                "conversion_rate": 0.0012,
                "currency_symbol": "Kz",
            }
        },
        "language": {1: {"language_name": "Portuguese", "locale": "pt-AO"}},
    },
    "Malaysia": {
        "alpha_2_code": "MY",
        "alpha_3_code": "MYS",
        "continent": "Asia",
        "telephone_code": "+60",
        "currency": {
            1: {
                "currency_code": "MYR",
                "conversion_rate": 0.22,
                "currency_symbol": "RM",
            }
        },
        "language": {1: {"language_name": "Malay", "locale": "ms-MY"}},
    },
    "Hong Kong": {
        "alpha_2_code": "HK",
        "alpha_3_code": "HKG",
        "continent": "Asia",
        "telephone_code": "+852",
        "currency": {
            1: {
                "currency_code": "HKD",
                "conversion_rate": 0.13,
                "currency_symbol": "HK$",
            }
        },
        "language": {
            1: {"language_name": "Chinese", "locale": "zh-HK"},
            2: {"language_name": "English", "locale": "en-HK"},
        },
    },
    "Saudi Arabia": {
        "alpha_2_code": "SA",
        "alpha_3_code": "SAU",
        "continent": "Asia",
        "telephone_code": "+966",
        "currency": {
            1: {"currency_code": "SAR", "conversion_rate": 0.27, "currency_symbol": "﷼"}
        },
        "language": {1: {"language_name": "Arabic", "locale": "ar-SA"}},
    },
    "Iraq": {
        "alpha_2_code": "IQ",
        "alpha_3_code": "IRQ",
        "continent": "Asia",
        "telephone_code": "+964",
        "currency": {
            1: {
                "currency_code": "IQD",
                "conversion_rate": 0.00077,
                "currency_symbol": "د.ع",
            }
        },
        "language": {1: {"language_name": "Arabic", "locale": "ar-IQ"}},
    },
    "Chile": {
        "alpha_2_code": "CL",
        "alpha_3_code": "CHL",
        "continent": "South America",
        "telephone_code": "+56",
        "currency": {
            1: {
                "currency_code": "CLP",
                "conversion_rate": 0.0013,
                "currency_symbol": "$",
            }
        },
        "language": {1: {"language_name": "Spanish", "locale": "es-CL"}},
    },
    "Spain": {
        "alpha_2_code": "ES",
        "alpha_3_code": "ESP",
        "continent": "Europe",
        "telephone_code": "+34",
        "currency": {
            1: {"currency_code": "EUR", "conversion_rate": 1.07, "currency_symbol": "€"}
        },
        "language": {1: {"language_name": "Spanish", "locale": "es-ES"}},
    },
    "Canada": {
        "alpha_2_code": "CA",
        "alpha_3_code": "CAN",
        "continent": "North America",
        "telephone_code": "+1",
        "currency": {
            1: {"currency_code": "CAD", "conversion_rate": 0.74, "currency_symbol": "$"}
        },
        "language": {
            1: {"language_name": "English", "locale": "en-CA"},
            2: {"language_name": "French", "locale": "fr-CA"},
        },
    },
    "Tanzania": {
        "alpha_2_code": "TZ",
        "alpha_3_code": "TZA",
        "continent": "Africa",
        "telephone_code": "+255",
        "currency": {
            1: {
                "currency_code": "TZS",
                "conversion_rate": 0.00040,
                "currency_symbol": "Sh",
            }
        },
        "language": {
            1: {"language_name": "Swahili", "locale": "sw-TZ"},
            2: {"language_name": "English", "locale": "en-TZ"},
        },
    },
    "Singapore": {
        "alpha_2_code": "SG",
        "alpha_3_code": "SGP",
        "continent": "Asia",
        "telephone_code": "+65",
        "currency": {
            1: {
                "currency_code": "SGD",
                "conversion_rate": 0.73,
                "currency_symbol": "S$",
            }
        },
        "language": {1: {"language_name": "English", "locale": "en-SG"}},
    },
    "Sudan": {
        "alpha_2_code": "SD",
        "alpha_3_code": "SDN",
        "continent": "Africa",
        "telephone_code": "+249",
        "currency": {
            1: {
                "currency_code": "SDG",
                "conversion_rate": 0.0018,
                "currency_symbol": "£",
            }
        },
        "language": {1: {"language_name": "Arabic", "locale": "ar-SD"}},
    },
    "South Africa": {
        "alpha_2_code": "ZA",
        "alpha_3_code": "ZAF",
        "continent": "Africa",
        "telephone_code": "+27",
        "currency": {
            1: {
                "currency_code": "ZAR",
                "conversion_rate": 0.052,
                "currency_symbol": "R",
            }
        },
        "language": {1: {"language_name": "English", "locale": "en-ZA"}},
    },
    "Myanmar": {
        "alpha_2_code": "MM",
        "alpha_3_code": "MMR",
        "continent": "Asia",
        "telephone_code": "+95",
        "currency": {
            1: {
                "currency_code": "MMK",
                "conversion_rate": 0.00048,
                "currency_symbol": "K",
            }
        },
        "language": {1: {"language_name": "Burmese", "locale": "my-MM"}},
    },
}

# Load CSV files
us_cities_df = pd.read_csv("saas/us_cities_population.csv")
global_cities_df = pd.read_csv("saas/global_cities_population.csv")

logins = {}

new_accounts = {}

social_shares = {}

add_to_carts = {}

orders = {}

pageviews = {}

visits = {}

device_types = ["Desktop", "Mobile"]

# visitor information
tech_specs = {
    "Desktop": {
        "OS": ["Windows", "Mac OS", "Linux"],
        "Screen Size": [
            '13.3"',
            '13.6"',
            '15.4"',
            '15.6"',
            '16.2"',
            '17.3"',
            '18.5"',
            '19.5"',
            '21.45"',
            '21.5"',
            '22.0"',
            '22.9"',
            '23.0"',
            '24.0"',
            '27.0"',
            '31.5"',
        ],
    },
    "Mobile": {
        "OS": ["Android", "iOS"],
        "Screen Size": ['4.0"', '4.7"', '5.0"', '5.5"', '6.1"', '6.5"', '6.7"', '7.0"'],
    },
}

# Define possible social share platforms
social_share_platforms = [
    "Facebook",
    "Twitter",
    "LinkedIn",
    "Reddit",
    "Instagram",
    "Whatsapp",
    "Messenger",
    "Telegram",
    "Tiktok",
    "Pinterest",
    "Discord",
    "Snapchat",
]

# Product colors
product_colors = [
    "Red",
    "Blue",
    "Green",
    "Yellow",
    "Purple",
    "Orange",
    "Black",
    "White",
]
# Product sizes
product_sizes = ["Extra Large", "Large", "Medium", "Small", "Extra Small"]
# Product categories
product_categories = ["Tee", "Jacket", "Hoodie", "Pants", "Shorts"]
# Product brands
product_brands = ["Nike", "Adidas", "Puma", "Under Armour"]

# Define possible signup methods
signup_methods = ["Google", "Facebook", "Email"]


updates = {
    "no_of_add_to_carts": 0,
    "qty_added_to_carts": 0,
    "no_of_orders": 0,
    "qty_ordered": 0,
}
