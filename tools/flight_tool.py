import os
import re
import certifi
import airportsdata
import pycountry
import requests
from dotenv import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

# Default origin when user says only destination, e.g. "Bali Trip"
# Change this if your default location is Delhi
DEFAULT_ORIGIN_IATA = os.getenv(
    "DEFAULT_ORIGIN_IATA",
    "Delhi"
    )

BASE_URL = "https://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load('IATA')

COUNTRY_ALIASES = {

    # =========================
    # A
    # =========================

    "afghanistan": "AF",
    "afghan": "AF",

    "albania": "AL",
    "albanian": "AL",

    "algeria": "DZ",
    "algerian": "DZ",

    "andorra": "AD",
    "andorran": "AD",

    "angola": "AO",
    "angolan": "AO",

    "antigua and barbuda": "AG",
    "antigua": "AG",

    "argentina": "AR",
    "argentinian": "AR",
    "argentine": "AR",

    "armenia": "AM",
    "armenian": "AM",

    "australia": "AU",
    "australian": "AU",
    "aussie": "AU",

    "austria": "AT",
    "austrian": "AT",

    "azerbaijan": "AZ",
    "azerbaijani": "AZ",


    # =========================
    # B
    # =========================

    "bahamas": "BS",
    "the bahamas": "BS",
    "bahamian": "BS",

    "bahrain": "BH",
    "bahraini": "BH",

    "bangladesh": "BD",
    "bangladeshi": "BD",

    "barbados": "BB",
    "barbadian": "BB",

    "belarus": "BY",
    "belarusian": "BY",

    "belgium": "BE",
    "belgian": "BE",

    "belize": "BZ",
    "belizean": "BZ",

    "benin": "BJ",
    "beninese": "BJ",

    "bhutan": "BT",
    "bhutanese": "BT",

    "bolivia": "BO",
    "bolivian": "BO",

    "bosnia and herzegovina": "BA",
    "bosnia": "BA",
    "bosnian": "BA",

    "botswana": "BW",
    "botswanan": "BW",

    "brazil": "BR",
    "brasil": "BR",
    "brazilian": "BR",

    "brunei": "BN",
    "bruneian": "BN",

    "bulgaria": "BG",
    "bulgarian": "BG",

    "burkina faso": "BF",
    "burkinabe": "BF",

    "burundi": "BI",
    "burundian": "BI",


    # =========================
    # C
    # =========================

    "cabo verde": "CV",
    "cape verde": "CV",
    "cape verdean": "CV",

    "cambodia": "KH",
    "cambodian": "KH",

    "cameroon": "CM",
    "cameroonian": "CM",

    "canada": "CA",
    "canadian": "CA",

    "central african republic": "CF",
    "car": "CF",

    "chad": "TD",
    "chadian": "TD",

    "chile": "CL",
    "chilean": "CL",

    "china": "CN",
    "chinese": "CN",
    "prc": "CN",
    "peoples republic of china": "CN",

    "colombia": "CO",
    "colombian": "CO",

    "comoros": "KM",
    "comorian": "KM",

    "congo": "CG",
    "republic of congo": "CG",
    "congo brazzaville": "CG",

    "democratic republic of the congo": "CD",
    "drc": "CD",
    "dr congo": "CD",
    "congo kinshasa": "CD",

    "costa rica": "CR",
    "costa rican": "CR",

    "croatia": "HR",
    "croatian": "HR",

    "cuba": "CU",
    "cuban": "CU",

    "cyprus": "CY",
    "cypriot": "CY",

    "czechia": "CZ",
    "czech republic": "CZ",
    "czech": "CZ",


    # =========================
    # D
    # =========================

    "denmark": "DK",
    "danish": "DK",

    "djibouti": "DJ",
    "djiboutian": "DJ",

    "dominica": "DM",
    "dominican": "DM",

    "dominican republic": "DO",


    # =========================
    # E
    # =========================

    "ecuador": "EC",
    "ecuadorian": "EC",

    "egypt": "EG",
    "egyptian": "EG",

    "el salvador": "SV",
    "salvadoran": "SV",

    "equatorial guinea": "GQ",

    "eritrea": "ER",
    "eritrean": "ER",

    "estonia": "EE",
    "estonian": "EE",

    "eswatini": "SZ",
    "swaziland": "SZ",
    "swazi": "SZ",

    "ethiopia": "ET",
    "ethiopian": "ET",


    # =========================
    # F
    # =========================

    "fiji": "FJ",
    "fijian": "FJ",

    "finland": "FI",
    "finnish": "FI",

    "france": "FR",
    "french": "FR",


    # =========================
    # G
    # =========================

    "gabon": "GA",
    "gabonese": "GA",

    "gambia": "GM",
    "the gambia": "GM",

    "georgia": "GE",
    "georgian": "GE",

    "germany": "DE",
    "german": "DE",
    "deutschland": "DE",

    "ghana": "GH",
    "ghanaian": "GH",

    "greece": "GR",
    "greek": "GR",

    "grenada": "GD",

    "guatemala": "GT",
    "guatemalan": "GT",

    "guinea": "GN",
    "guinean": "GN",

    "guinea bissau": "GW",

    "guyana": "GY",
    "guyanese": "GY",


    # =========================
    # H
    # =========================

    "haiti": "HT",
    "haitian": "HT",

    "honduras": "HN",
    "honduran": "HN",

    "hungary": "HU",
    "hungarian": "HU",


    # =========================
    # I
    # =========================

    "iceland": "IS",
    "icelandic": "IS",

    "india": "IN",
    "indian": "IN",
    "bharat": "IN",
    "hindustan": "IN",

    "indonesia": "ID",
    "indonesian": "ID",

    "iran": "IR",
    "iranian": "IR",
    "persia": "IR",

    "iraq": "IQ",
    "iraqi": "IQ",

    "ireland": "IE",
    "irish": "IE",

    "israel": "IL",
    "israeli": "IL",

    "italy": "IT",
    "italian": "IT",
    "italia": "IT",


    # =========================
    # J
    # =========================

    "jamaica": "JM",
    "jamaican": "JM",

    "japan": "JP",
    "japanese": "JP",
    "nippon": "JP",

    "jordan": "JO",
    "jordanian": "JO",


    # =========================
    # K
    # =========================

    "kazakhstan": "KZ",
    "kazakh": "KZ",

    "kenya": "KE",
    "kenyan": "KE",

    "kiribati": "KI",

    "north korea": "KP",
    "north korean": "KP",
    "dprk": "KP",

    "south korea": "KR",
    "south korean": "KR",
    "korea": "KR",
    "republic of korea": "KR",
    "rok": "KR",

    "kuwait": "KW",
    "kuwaiti": "KW",

    "kyrgyzstan": "KG",
    "kyrgyz": "KG",


    # =========================
    # L
    # =========================

    "laos": "LA",
    "lao": "LA",
    "lao people's democratic republic": "LA",

    "latvia": "LV",
    "latvian": "LV",

    "lebanon": "LB",
    "lebanese": "LB",

    "lesotho": "LS",
    "lesothan": "LS",

    "liberia": "LR",
    "liberian": "LR",

    "libya": "LY",
    "libyan": "LY",

    "liechtenstein": "LI",

    "lithuania": "LT",
    "lithuanian": "LT",

    "luxembourg": "LU",
    "luxembourgish": "LU",


    # =========================
    # M
    # =========================

    "madagascar": "MG",
    "malagasy": "MG",

    "malawi": "MW",
    "malawian": "MW",

    "malaysia": "MY",
    "malaysian": "MY",

    "maldives": "MV",
    "maldivian": "MV",

    "mali": "ML",
    "malian": "ML",

    "malta": "MT",
    "maltese": "MT",

    "marshall islands": "MH",

    "mauritania": "MR",
    "mauritanian": "MR",

    "mauritius": "MU",
    "mauritian": "MU",

    "mexico": "MX",
    "mexican": "MX",
    "méxico": "MX",

    "micronesia": "FM",
    "federated states of micronesia": "FM",

    "moldova": "MD",
    "moldovan": "MD",

    "monaco": "MC",
    "monégasque": "MC",

    "mongolia": "MN",
    "mongolian": "MN",

    "montenegro": "ME",
    "montenegrin": "ME",

    "morocco": "MA",
    "moroccan": "MA",

    "mozambique": "MZ",
    "mozambican": "MZ",

    "myanmar": "MM",
    "burma": "MM",
    "burmese": "MM",


    # =========================
    # N
    # =========================

    "namibia": "NA",
    "namibian": "NA",

    "nauru": "NR",

    "nepal": "NP",
    "nepalese": "NP",

    "netherlands": "NL",
    "dutch": "NL",
    "holland": "NL",

    "new zealand": "NZ",
    "new zealander": "NZ",
    "nz": "NZ",

    "nicaragua": "NI",
    "nicaraguan": "NI",

    "niger": "NE",
    "nigerien": "NE",

    "nigeria": "NG",
    "nigerian": "NG",

    "north macedonia": "MK",
    "macedonia": "MK",
    "macedonian": "MK",

    "norway": "NO",
    "norwegian": "NO",


    # =========================
    # O
    # =========================

    "oman": "OM",
    "omani": "OM",


    # =========================
    # P
    # =========================

    "pakistan": "PK",
    "pakistani": "PK",

    "palau": "PW",

    "panama": "PA",
    "panamanian": "PA",

    "papua new guinea": "PG",

    "paraguay": "PY",
    "paraguayan": "PY",

    "peru": "PE",
    "peruvian": "PE",

    "philippines": "PH",
    "philippine": "PH",

    "poland": "PL",
    "polish": "PL",

    "portugal": "PT",
    "portuguese": "PT",


    # =========================
    # Q
    # =========================

    "qatar": "QA",
    "qatari": "QA",


    # =========================
    # R
    # =========================

    "romania": "RO",
    "romanian": "RO",

    "russia": "RU",
    "russian": "RU",
    "russian federation": "RU",

    "rwanda": "RW",
    "rwandan": "RW",


    # =========================
    # S
    # =========================

    "saint kitts and nevis": "KN",

    "saint lucia": "LC",

    "saint vincent and the grenadines": "VC",

    "samoa": "WS",
    "samoan": "WS",

    "san marino": "SM",

    "sao tome and principe": "ST",

    "saudi arabia": "SA",
    "saudi": "SA",
    "ksa": "SA",

    "senegal": "SN",
    "senegalese": "SN",

    "serbia": "RS",
    "serbian": "RS",

    "seychelles": "SC",

    "sierra leone": "SL",

    "singapore": "SG",
    "singaporean": "SG",
    "sg": "SG",

    "slovakia": "SK",
    "slovak": "SK",

    "slovenia": "SI",
    "slovenian": "SI",

    "solomon islands": "SB",

    "somalia": "SO",
    "somali": "SO",

    "south africa": "ZA",
    "south african": "ZA",
    "rsa": "ZA",

    "south sudan": "SS",

    "spain": "ES",
    "spanish": "ES",
    "espana": "ES",
    "españa": "ES",

    "sri lanka": "LK",
    "srilanka": "LK",
    "sri lankan": "LK",

    "sudan": "SD",
    "sudanese": "SD",

    "suriname": "SR",
    "surinamese": "SR",

    "sweden": "SE",
    "swedish": "SE",

    "switzerland": "CH",
    "swiss": "CH",

    "syria": "SY",
    "syrian": "SY",

    "tajikistan": "TJ",
    "tajik": "TJ",

    "tanzania": "TZ",
    "tanzanian": "TZ",

    "thailand": "TH",
    "thai": "TH",

    "timor leste": "TL",
    "east timor": "TL",

    "togo": "TG",
    "togolese": "TG",

    "tonga": "TO",
    "tongan": "TO",

    "trinidad and tobago": "TT",
    "trinidad": "TT",

    "tunisia": "TN",
    "tunisian": "TN",

    "turkey": "TR",
    "turkiye": "TR",
    "türkiye": "TR",
    "turkish": "TR",

    "turkmenistan": "TM",
    "turkmen": "TM",

    "tuvalu": "TV",


    "uganda": "UG",
    "ugandan": "UG",

    "ukraine": "UA",
    "ukrainian": "UA",

    "united arab emirates": "AE",
    "uae": "AE",
    "u.a.e": "AE",
    "emirates": "AE",

    "united kingdom": "GB",
    "uk": "GB",
    "u.k.": "GB",
    "britain": "GB",
    "great britain": "GB",
    "british": "GB",
    "england": "GB",

    "united states": "US",
    "united states of america": "US",
    "usa": "US",
    "u.s.a": "US",
    "u.s.a.": "US",
    "u.s": "US",
    "u.s.": "US",
    "us": "US",
    "america": "US",
    "american": "US",

    "uruguay": "UY",
    "uruguayan": "UY",

    "uzbekistan": "UZ",
    "uzbek": "UZ",

    "vanuatu": "VU",
    "vanuatuan": "VU",

    "vatican city": "VA",
    "holy see": "VA",

    "venezuela": "VE",
    "venezuelan": "VE",

    "vietnam": "VN",
    "viet nam": "VN",
    "vietnamese": "VN",

    "yemen": "YE",
    "yemeni": "YE",

    "zambia": "ZM",
    "zambian": "ZM",

    "zimbabwe": "ZW",
    "zimbabwean": "ZW",
}

COUNTRY_MAIN_AIRPORT = {

    # =========================
    # A
    # =========================

    "AF": "KBL",  # Afghanistan - Kabul
    "AL": "TIA",  # Albania - Tirana
    "DZ": "ALG",  # Algeria - Algiers
    "AD": "LEU",  # Andorra
    "AO": "LAD",  # Angola - Luanda
    "AG": "ANU",  # Antigua and Barbuda
    "AR": "EZE",  # Argentina - Buenos Aires
    "AM": "EVN",  # Armenia - Yerevan
    "AU": "SYD",  # Australia - Sydney
    "AT": "VIE",  # Austria - Vienna
    "AZ": "GYD",  # Azerbaijan - Baku


    # =========================
    # B
    # =========================

    "BS": "NAS",  # Bahamas - Nassau
    "BH": "BAH",  # Bahrain - Manama
    "BD": "DAC",  # Bangladesh - Dhaka
    "BB": "BGI",  # Barbados - Bridgetown
    "BY": "MSQ",  # Belarus - Minsk
    "BE": "BRU",  # Belgium - Brussels
    "BZ": "BZE",  # Belize - Belize City
    "BJ": "COO",  # Benin - Cotonou
    "BT": "PBH",  # Bhutan - Paro
    "BO": "VVI",  # Bolivia - Santa Cruz
    "BA": "SJJ",  # Bosnia and Herzegovina - Sarajevo
    "BW": "GBE",  # Botswana - Gaborone
    "BR": "GRU",  # Brazil - Sao Paulo
    "BN": "BWN",  # Brunei - Bandar Seri Begawan
    "BG": "SOF",  # Bulgaria - Sofia
    "BF": "OUA",  # Burkina Faso - Ouagadougou
    "BI": "BJM",  # Burundi - Bujumbura


    # =========================
    # C
    # =========================

    "CV": "SID",  # Cabo Verde
    "KH": "PNH",  # Cambodia - Phnom Penh
    "CM": "NSI",  # Cameroon - Yaounde
    "CA": "YYZ",  # Canada - Toronto
    "CF": "BGF",  # Central African Republic
    "TD": "NDJ",  # Chad - N'Djamena
    "CL": "SCL",  # Chile - Santiago
    "CN": "PEK",  # China - Beijing
    "CO": "BOG",  # Colombia - Bogota
    "KM": "HAH",  # Comoros
    "CG": "BZV",  # Republic of Congo
    "CD": "FIH",  # DR Congo - Kinshasa
    "CR": "SJO",  # Costa Rica
    "HR": "ZAG",  # Croatia
    "CU": "HAV",  # Cuba - Havana
    "CY": "LCA",  # Cyprus
    "CZ": "PRG",  # Czechia - Prague


    # =========================
    # D
    # =========================

    "DK": "CPH",  # Denmark
    "DJ": "JIB",  # Djibouti
    "DM": "DOM",  # Dominica
    "DO": "SDQ",  # Dominican Republic


    # =========================
    # E
    # =========================

    "EC": "UIO",  # Ecuador - Quito
    "EG": "CAI",  # Egypt - Cairo
    "SV": "SAL",  # El Salvador
    "GQ": "SSG",  # Equatorial Guinea
    "ER": "ASM",  # Eritrea
    "EE": "TLL",  # Estonia
    "SZ": "MTS",  # Eswatini
    "ET": "ADD",  # Ethiopia


    # =========================
    # F
    # =========================

    "FJ": "NAN",  # Fiji
    "FI": "HEL",  # Finland
    "FR": "CDG",  # France - Paris


    # =========================
    # G
    # =========================

    "GA": "LBV",  # Gabon
    "GM": "BJL",  # Gambia
    "GE": "TBS",  # Georgia
    "DE": "FRA",  # Germany - Frankfurt
    "GH": "ACC",  # Ghana
    "GR": "ATH",  # Greece - Athens
    "GD": "GND",  # Grenada
    "GT": "GUA",  # Guatemala
    "GN": "CKY",  # Guinea
    "GW": "OXB",  # Guinea-Bissau
    "GY": "GEO",  # Guyana


    # =========================
    # H
    # =========================

    "HT": "PAP",  # Haiti
    "HN": "SAP",  # Honduras
    "HU": "BUD",  # Hungary


    # =========================
    # I
    # =========================

    "IS": "KEF",  # Iceland
    "IN": "DEL",  # India - Delhi
    "ID": "CGK",  # Indonesia - Jakarta
    "IR": "IKA",  # Iran - Tehran
    "IQ": "BGW",  # Iraq - Baghdad
    "IE": "DUB",  # Ireland - Dublin
    "IL": "TLV",  # Israel - Tel Aviv
    "IT": "FCO",  # Italy - Rome


    # =========================
    # J
    # =========================

    "JM": "KIN",  # Jamaica
    "JP": "HND",  # Japan - Tokyo
    "JO": "AMM",  # Jordan - Amman


    # =========================
    # K
    # =========================

    "KZ": "NQZ",  # Kazakhstan - Astana
    "KE": "NBO",  # Kenya - Nairobi
    "KI": "TRW",  # Kiribati
    "KP": "FNJ",  # North Korea
    "KR": "ICN",  # South Korea - Seoul
    "KW": "KWI",  # Kuwait
    "KG": "FRU",  # Kyrgyzstan


    # =========================
    # L
    # =========================

    "LA": "VTE",  # Laos
    "LV": "RIX",  # Latvia
    "LB": "BEY",  # Lebanon
    "LS": "MSU",  # Lesotho
    "LR": "ROB",  # Liberia
    "LY": "TIP",  # Libya
    "LI": "ZRH",  # Liechtenstein
    "LT": "VNO",  # Lithuania
    "LU": "LUX",  # Luxembourg


    # =========================
    # M
    # =========================

    "MG": "TNR",  # Madagascar
    "MW": "LLW",  # Malawi
    "MY": "KUL",  # Malaysia - Kuala Lumpur
    "MV": "MLE",  # Maldives - Male
    "ML": "BKO",  # Mali
    "MT": "MLA",  # Malta
    "MH": "MAJ",  # Marshall Islands
    "MR": "NKC",  # Mauritania
    "MU": "MRU",  # Mauritius
    "MX": "MEX",  # Mexico
    "FM": "PNI",  # Micronesia
    "MD": "RMO",  # Moldova
    "MC": "NCE",  # Monaco - Nice
    "MN": "UBN",  # Mongolia - Ulaanbaatar
    "ME": "TGD",  # Montenegro
    "MA": "CMN",  # Morocco - Casablanca
    "MZ": "MPM",  # Mozambique
    "MM": "RGN",  # Myanmar


    # =========================
    # N
    # =========================

    "NA": "WDH",  # Namibia
    "NR": "INU",  # Nauru
    "NP": "KTM",  # Nepal - Kathmandu
    "NL": "AMS",  # Netherlands - Amsterdam
    "NZ": "AKL",  # New Zealand - Auckland
    "NI": "MGA",  # Nicaragua
    "NE": "NIM",  # Niger
    "NG": "LOS",  # Nigeria - Lagos
    "MK": "SKP",  # North Macedonia
    "NO": "OSL",  # Norway


    # =========================
    # O
    # =========================

    "OM": "MCT",  # Oman - Muscat


    # =========================
    # P
    # =========================

    "PK": "ISB",  # Pakistan - Islamabad
    "PW": "ROR",  # Palau
    "PA": "PTY",  # Panama
    "PG": "POM",  # Papua New Guinea
    "PY": "ASU",  # Paraguay
    "PE": "LIM",  # Peru - Lima
    "PH": "MNL",  # Philippines - Manila
    "PL": "WAW",  # Poland - Warsaw
    "PT": "LIS",  # Portugal - Lisbon


    # =========================
    # Q
    # =========================

    "QA": "DOH",  # Qatar - Doha


    # =========================
    # R
    # =========================

    "RO": "OTP",  # Romania
    "RU": "SVO",  # Russia - Moscow
    "RW": "KGL",  # Rwanda


    # =========================
    # S
    # =========================

    "KN": "SKB",  # Saint Kitts and Nevis
    "LC": "UVF",  # Saint Lucia
    "VC": "SVD",  # Saint Vincent and the Grenadines
    "WS": "APW",  # Samoa
    "SM": "RMI",  # San Marino - Rimini
    "ST": "TMS",  # Sao Tome and Principe

    "SA": "JED",  # Saudi Arabia
    "SN": "DSS",  # Senegal
    "RS": "BEG",  # Serbia
    "SC": "SEZ",  # Seychelles
    "SL": "FNA",  # Sierra Leone
    "SG": "SIN",  # Singapore
    "SK": "BTS",  # Slovakia
    "SI": "LJU",  # Slovenia
    "SB": "HIR",  # Solomon Islands
    "SO": "MGQ",  # Somalia
    "ZA": "JNB",  # South Africa
    "SS": "JUB",  # South Sudan
    "ES": "MAD",  # Spain
    "LK": "CMB",  # Sri Lanka
    "SD": "KRT",  # Sudan
    "SR": "PBM",  # Suriname
    "SE": "ARN",  # Sweden
    "CH": "ZRH",  # Switzerland
    "SY": "DAM",  # Syria


    # =========================
    # T
    # =========================

    "TJ": "DYU",  # Tajikistan
    "TZ": "JRO",  # Tanzania
    "TH": "BKK",  # Thailand - Bangkok
    "TL": "DIL",  # Timor-Leste
    "TG": "LFW",  # Togo
    "TO": "TBU",  # Tonga
    "TT": "POS",  # Trinidad and Tobago
    "TN": "TUN",  # Tunisia
    "TR": "IST",  # Türkiye - Istanbul
    "TM": "ASB",  # Turkmenistan
    "TV": "FUN",  # Tuvalu


    # =========================
    # U
    # =========================

    "UG": "EBB",  # Uganda
    "UA": "KBP",  # Ukraine
    "AE": "DXB",  # United Arab Emirates - Dubai
    "GB": "LHR",  # United Kingdom - London
    "US": "JFK",  # United States - New York
    "UY": "MVD",  # Uruguay
    "UZ": "TAS",  # Uzbekistan


    # =========================
    # V
    # =========================

    "VU": "VLI",  # Vanuatu
    "VA": "FCO",  # Vatican City - Rome
    "VE": "CCS",  # Venezuela
    "VN": "SGN",  # Vietnam - Ho Chi Minh City


    # =========================
    # Y
    # =========================

    "YE": "SAH",  # Yemen


    # =========================
    # Z
    # =========================

    "ZM": "LUN",  # Zambia
    "ZW": "HRE",  # Zimbabwe
}

CITY_MAIN_AIRPORT = {

    # =========================
    # INDIA
    # =========================

    "delhi": "DEL",
    "new delhi": "DEL",
    "mumbai": "BOM",
    "bombay": "BOM",
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "hyderabad": "HYD",
    "chennai": "MAA",
    "madras": "MAA",
    "kolkata": "CCU",
    "calcutta": "CCU",
    "ahmedabad": "AMD",
    "pune": "PNQ",
    "goa": "GOI",
    "panaji": "GOI",
    "kochi": "COK",
    "cochin": "COK",
    "jaipur": "JAI",
    "lucknow": "LKO",
    "varanasi": "VNS",
    "amritsar": "ATQ",
    "chandigarh": "IXC",
    "srinagar": "SXR",
    "bhubaneswar": "BBI",
    "patna": "PAT",
    "indore": "IDR",
    "nagpur": "NAG",
    "surat": "STV",
    "vadodara": "BDQ",
    "rajkot": "HSR",
    "ranchi": "IXR",
    "guwahati": "GAU",
    "thiruvananthapuram": "TRV",
    "trivandrum": "TRV",
    "visakhapatnam": "VTZ",
    "vizag": "VTZ",
    "coimbatore": "CJB",
    "madurai": "IXM",
    "mangalore": "IXE",
    "mangaluru": "IXE",
    "tiruchirappalli": "TRZ",
    "trichy": "TRZ",
    "calicut": "CCJ",
    "kozhikode": "CCJ",
    "dehradun": "DED",
    "agra": "AGR",
    "aurangabad": "IXU",
    "ayodhya": "AYJ",
    "gaya": "GAY",
    "jodhpur": "JDH",
    "udaipur": "UDR",
    "kanpur": "KNU",
    "mysore": "MYQ",
    "mysuru": "MYQ",
    "port blair": "IXZ",
    "leh": "IXL",
    "siliguri": "IXB",
    "darjeeling": "IXB",


    # =========================
    # UNITED STATES
    # =========================

    "new york": "JFK",
    "nyc": "JFK",
    "manhattan": "JFK",

    "los angeles": "LAX",
    "la": "LAX",

    "san francisco": "SFO",
    "sf": "SFO",

    "chicago": "ORD",

    "houston": "IAH",

    "dallas": "DFW",
    "fort worth": "DFW",

    "miami": "MIA",

    "boston": "BOS",

    "washington": "DCA",
    "washington dc": "DCA",
    "dc": "DCA",

    "las vegas": "LAS",
    "vegas": "LAS",

    "seattle": "SEA",

    "atlanta": "ATL",

    "denver": "DEN",

    "phoenix": "PHX",

    "philadelphia": "PHL",

    "san diego": "SAN",

    "orlando": "MCO",

    "minneapolis": "MSP",

    "detroit": "DTW",

    "charlotte": "CLT",

    "austin": "AUS",

    "nashville": "BNA",

    "portland": "PDX",

    "san jose": "SJC",

    "new orleans": "MSY",

    "tampa": "TPA",

    "honolulu": "HNL",

    "salt lake city": "SLC",

    "baltimore": "BWI",

    "cleveland": "CLE",

    "pittsburgh": "PIT",

    "st louis": "STL",

    "kansas city": "MCI",

    "raleigh": "RDU",

    "indianapolis": "IND",

    "columbus": "CMH",

    "cincinnati": "CVG",

    "memphis": "MEM",

    "birmingham": "BHM",


    # =========================
    # CANADA
    # =========================

    "toronto": "YYZ",

    "vancouver": "YVR",

    "montreal": "YUL",

    "calgary": "YYC",

    "ottawa": "YOW",

    "edmonton": "YEG",

    "winnipeg": "YWG",

    "halifax": "YHZ",

    "quebec city": "YQB",


    # =========================
    # UNITED KINGDOM
    # =========================

    "london": "LHR",

    "manchester": "MAN",

    "birmingham": "BHX",

    "edinburgh": "EDI",

    "glasgow": "GLA",

    "bristol": "BRS",

    "liverpool": "LPL",

    "leeds": "LBA",

    "belfast": "BFS",

    "newcastle": "NCL",

    "cardiff": "CWL",

    "southampton": "SOU",


    # =========================
    # EUROPE
    # =========================

    # France
    "paris": "CDG",
    "nice": "NCE",
    "lyon": "LYS",
    "marseille": "MRS",

    # Germany
    "berlin": "BER",
    "frankfurt": "FRA",
    "munich": "MUC",
    "münchen": "MUC",
    "hamburg": "HAM",
    "dusseldorf": "DUS",
    "düsseldorf": "DUS",
    "cologne": "CGN",
    "cologne germany": "CGN",

    # Italy
    "rome": "FCO",
    "roma": "FCO",
    "milan": "MXP",
    "milano": "MXP",
    "venice": "VCE",
    "venezia": "VCE",
    "florence": "FLR",
    "naples": "NAP",

    # Spain
    "madrid": "MAD",
    "barcelona": "BCN",
    "seville": "SVQ",
    "sevilla": "SVQ",
    "valencia": "VLC",
    "malaga": "AGP",
    "ibiza": "IBZ",
    "palma": "PMI",

    # Portugal
    "lisbon": "LIS",
    "lisboa": "LIS",
    "porto": "OPO",
    "faro": "FAO",

    # Netherlands
    "amsterdam": "AMS",
    "rotterdam": "RTM",

    # Switzerland
    "zurich": "ZRH",
    "geneva": "GVA",
    "basel": "BSL",

    # Austria
    "vienna": "VIE",
    "wien": "VIE",
    "salzburg": "SZG",

    # Greece
    "athens": "ATH",
    "thessaloniki": "SKG",
    "santorini": "JTR",
    "mykonos": "JMK",

    # Ireland
    "dublin": "DUB",
    "cork": "ORK",
    "shannon": "SNN",

    # Belgium
    "brussels": "BRU",
    "antwerp": "ANR",

    # Denmark
    "copenhagen": "CPH",

    # Sweden
    "stockholm": "ARN",
    "gothenburg": "GOT",

    # Norway
    "oslo": "OSL",
    "bergen": "BGO",

    # Finland
    "helsinki": "HEL",

    # Iceland
    "reykjavik": "KEF",

    # Poland
    "warsaw": "WAW",
    "krakow": "KRK",

    # Czechia
    "prague": "PRG",

    # Hungary
    "budapest": "BUD",

    # Romania
    "bucharest": "OTP",

    # Croatia
    "zagreb": "ZAG",
    "dubrovnik": "DBV",

    # Serbia
    "belgrade": "BEG",

    # Bulgaria
    "sofia": "SOF",

    # Ukraine
    "kyiv": "KBP",

    # Russia
    "moscow": "SVO",
    "st petersburg": "LED",
    "saint petersburg": "LED",

    # Türkiye
    "istanbul": "IST",
    "ankara": "ESB",
    "antalya": "AYT",


    # =========================
    # MIDDLE EAST
    # =========================

    # UAE
    "dubai": "DXB",
    "abu dhabi": "AUH",
    "sharjah": "SHJ",

    # Qatar
    "doha": "DOH",

    # Saudi Arabia
    "riyadh": "RUH",
    "jeddah": "JED",
    "dammam": "DMM",
    "medina": "MED",
    "makkah": "JED",
    "mecca": "JED",

    # Oman
    "muscat": "MCT",
    "salalah": "SLL",

    # Bahrain
    "manama": "BAH",

    # Kuwait
    "kuwait city": "KWI",
    "kuwait": "KWI",

    # Jordan
    "amman": "AMM",

    # Israel
    "tel aviv": "TLV",
    "jerusalem": "TLV",

    # Lebanon
    "beirut": "BEY",

    # Iran
    "tehran": "IKA",

    # Iraq
    "baghdad": "BGW",


    # =========================
    # EAST ASIA
    # =========================

    # Japan
    "tokyo": "HND",
    "osaka": "KIX",
    "kyoto": "KIX",
    "kyoto japan": "KIX",
    "nagoya": "NGO",
    "sapporo": "CTS",
    "fukuoka": "FUK",
    "okinawa": "OKA",

    # China
    "beijing": "PEK",
    "shanghai": "PVG",
    "guangzhou": "CAN",
    "shenzhen": "SZX",
    "chengdu": "CTU",
    "chongqing": "CKG",
    "xian": "XIY",
    "xi'an": "XIY",
    "hangzhou": "HGH",
    "nanjing": "NKG",

    # South Korea
    "seoul": "ICN",
    "busan": "PUS",
    "jeju": "CJU",

    # Hong Kong
    "hong kong": "HKG",

    # Taiwan
    "taipei": "TPE",

    # Mongolia
    "ulaanbaatar": "UBN",


    # =========================
    # SOUTHEAST ASIA
    # =========================

    # Thailand
    "bangkok": "BKK",
    "phuket": "HKT",
    "chiang mai": "CNX",
    "pattaya": "BKK",

    # Singapore
    "singapore": "SIN",

    # Malaysia
    "kuala lumpur": "KUL",
    "kl": "KUL",
    "penang": "PEN",
    "langkawi": "LGK",

    # Indonesia
    "jakarta": "CGK",
    "bali": "DPS",
    "denpasar": "DPS",
    "surabaya": "SUB",

    # Vietnam
    "ho chi minh city": "SGN",
    "ho chi minh": "SGN",
    "saigon": "SGN",
    "hanoi": "HAN",
    "da nang": "DAD",

    # Philippines
    "manila": "MNL",
    "cebu": "CEB",

    # Cambodia
    "phnom penh": "PNH",
    "siem reap": "SAI",

    # Myanmar
    "yangon": "RGN",
    "mandalay": "MDL",

    # Laos
    "vientiane": "VTE",

    # Brunei
    "bandar seri begawan": "BWN",


    # =========================
    # SOUTH ASIA
    # =========================

    # Bangladesh
    "dhaka": "DAC",
    "chittagong": "CGP",
    "chattogram": "CGP",
    "sylhet": "ZYL",

    # Nepal
    "kathmandu": "KTM",
    "pokhara": "PKR",

    # Sri Lanka
    "colombo": "CMB",
    "kandy": "CMB",

    # Pakistan
    "islamabad": "ISB",
    "lahore": "LHE",
    "karachi": "KHI",

    # Maldives
    "male": "MLE",
    "malé": "MLE",

    # Bhutan
    "paro": "PBH",


    # =========================
    # AFRICA
    # =========================

    # Egypt
    "cairo": "CAI",
    "sharm el sheikh": "SSH",
    "hurghada": "HRG",

    # South Africa
    "johannesburg": "JNB",
    "cape town": "CPT",
    "durban": "DUR",

    # Kenya
    "nairobi": "NBO",
    "mombasa": "MBA",

    # Nigeria
    "lagos": "LOS",
    "abuja": "ABV",

    # Ethiopia
    "addis ababa": "ADD",

    # Morocco
    "casablanca": "CMN",
    "marrakesh": "RAK",
    "marrakech": "RAK",

    # Tanzania
    "dar es salaam": "DAR",
    "zanzibar": "ZNZ",
    "arusha": "ARK",

    # Ghana
    "accra": "ACC",

    # Rwanda
    "kigali": "KGL",

    # Uganda
    "kampala": "EBB",

    # Senegal
    "dakar": "DSS",

    # Mauritius
    "mauritius": "MRU",
    "port louis": "MRU",


    # =========================
    # OCEANIA
    # =========================

    # Australia
    "sydney": "SYD",
    "melbourne": "MEL",
    "brisbane": "BNE",
    "perth": "PER",
    "adelaide": "ADL",
    "canberra": "CBR",
    "gold coast": "OOL",
    "darwin": "DRW",

    # New Zealand
    "auckland": "AKL",
    "wellington": "WLG",
    "christchurch": "CHC",
    "queenstown": "ZQN",


    # =========================
    # SOUTH AMERICA
    # =========================

    # Brazil
    "sao paulo": "GRU",
    "são paulo": "GRU",
    "rio de janeiro": "GIG",
    "brasilia": "BSB",
    "brasília": "BSB",

    # Argentina
    "buenos aires": "EZE",

    # Chile
    "santiago": "SCL",

    # Peru
    "lima": "LIM",

    # Colombia
    "bogota": "BOG",
    "bogotá": "BOG",
    "medellin": "MDE",
    "cartagena": "CTG",

    # Ecuador
    "quito": "UIO",
    "guayaquil": "GYE",

    # Uruguay
    "montevideo": "MVD",

    # Paraguay
    "asuncion": "ASU",
    "asunción": "ASU",

    # Venezuela
    "caracas": "CCS",

    # Bolivia
    "la paz": "LPB",
    "santa cruz": "VVI",
}


def clean_text(text: str) -> str:
    text = text.lower().strip()

    # Keep letters, numbers, spaces, apostrophes and hyphens
    text = re.sub(r"[^a-z0-9\s'-]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    stop_words = {
        "flight",
        "flights",
        "ticket",
        "tickets",
        "trip",
        "trips",
        "travel",
        "plan",
        "planning",
        "complete",
        "days",
        "day",
        "including",
        "hotel",
        "hotels",
        "sightseeing",
        "under",
        "budget",
        "info",
        "information",
        "please",
        "find",
        "search",
        "show",
        "give",
        "get",
        "book",
        "booking",
        "me",
        "for",
        "the",
        "a",
        "an",
        "to",
        "from",
        "in",
        "on",
        "of",
        "and",
        "with",
    }

    words = [
        word
        for word in text.split()
        if word not in stop_words
    ]

    return " ".join(words).strip()

def country_name_to_code(text: str):
    text = clean_text(text)

    # Direct alias lookup
    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]

    # Direct country-name lookup
    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass

    # Detect country name inside longer text
    for country in pycountry.countries:
        country_name = country.name.lower()

        if country_name in text:
            return country.alpha_2

    # Detect alias inside longer text
    for alias, code in COUNTRY_ALIASES.items():
        if alias in text:
            return code

    return None

def airport_country_matches(airport: dict, country_code: str) -> bool:
    airport_country = str(
        airport.get("country", "")
    ).upper().strip()

    country_code = country_code.upper().strip()

    # Direct ISO-2 country code match
    if airport_country == country_code:
        return True

    try:
        country = pycountry.countries.get(alpha_2=country_code)

        if country and airport_country.lower() == country.name.lower():
            return True

    except (LookupError, AttributeError):
        pass

    return False

def get_best_airport_for_country(country_code: str):
    country_code = country_code.upper().strip()

    # 1. Use manually defined preferred airport first
    preferred = COUNTRY_MAIN_AIRPORT.get(country_code)

    if preferred and preferred in AIRPORTS:
        return preferred

    # 2. Otherwise find the best airport automatically
    candidates = []

    for iata, airport in AIRPORTS.items():
        if not iata:
            continue

        if airport_country_matches(airport, country_code):
            name = str(airport.get("name", "")).lower()
            city = str(airport.get("city", "")).lower()

            score = 0

            if "international" in name:
                score += 50

            if "intl" in name:
                score += 40

            if "capital" in name:
                score += 20

            if city:
                score += 5

            candidates.append((score, iata))

    if not candidates:
        return None

    candidates.sort(reverse=True)

    return candidates[0][1]

def resolve_location_to_iata(location: str):
    """
    Convert country, city, airport, or IATA code into an IATA airport code.

    Examples:
        Bangladesh -> DAC
        Japan      -> NRT
        Dhaka      -> DAC
        Tokyo      -> NRT
        DAC        -> DAC
    """

    if not location:
        return None

    raw_location = location.strip()

    # --------------------------------------------------
    # 1. Direct IATA code
    # --------------------------------------------------
    if re.fullmatch(r"[A-Za-z]{3}", raw_location):
        code = raw_location.upper()

        if code in AIRPORTS:
            return code

    # --------------------------------------------------
    # 2. Clean the location
    # --------------------------------------------------
    location_clean = clean_text(raw_location)

    if not location_clean:
        return None

    # --------------------------------------------------
    # 3. City preferred airport
    # --------------------------------------------------
    if location_clean in CITY_MAIN_AIRPORT:
        return CITY_MAIN_AIRPORT[location_clean]

    # --------------------------------------------------
    # 4. Country preferred airport
    # --------------------------------------------------
    country_code = country_name_to_code(location_clean)

    if country_code:
        airport = get_best_airport_for_country(country_code)

        if airport:
            return airport

    # --------------------------------------------------
    # 5. Search exact city in airport database
    # --------------------------------------------------
    city_matches = []

    for iata, airport in AIRPORTS.items():

        if not iata:
            continue

        city = str(
            airport.get("city", "")
        ).lower().strip()

        name = str(
            airport.get("name", "")
        ).lower().strip()

        score = 0

        # Exact city match
        if city == location_clean:
            score += 100

        # Partial city match
        elif location_clean in city:
            score += 70

        # Airport name contains location
        if location_clean in name:
            score += 50

        # Prefer international airports
        if "international" in name:
            score += 10

        if score > 0:
            city_matches.append((score, iata))

    # --------------------------------------------------
    # 6. Return highest-scoring airport
    # --------------------------------------------------
    if city_matches:
        city_matches.sort(reverse=True)
        return city_matches[0][1]

    # --------------------------------------------------
    # 7. Nothing found
    # --------------------------------------------------
    return None


def find_location_mentions(query: str):
    """
    Finds country or city names inside a natural language query.
    """

    q = query.lower()
    mentions = []

    # Country aliases
    for alias in COUNTRY_ALIASES:
        if re.search(rf"\b{re.escape(alias)}\b", q):
            mentions.append(alias)

    # Country names
    for country in pycountry.countries:
        name = country.name.lower()

        if len(name) >= 4 and re.search(rf"\b{re.escape(name)}\b", q):
            mentions.append(name)

    # City names
    for city in CITY_MAIN_AIRPORT:
        if re.search(rf"\b{re.escape(city)}\b", q):
            mentions.append(city)

    # Remove duplicates
    unique_mentions = []

    for item in mentions:
        if item not in unique_mentions:
            unique_mentions.append(item)

    return unique_mentions


def parse_route(query: str):
    """
    Returns:
        dep_iata, arr_iata

        None, None -> global live flights
        DAC, NRT    -> filtered route
        DAC, None   -> all flights from DAC
        None, NRT   -> all flights to NRT
    """

    q = query.strip()
    q_lower = q.lower()

    # Global query
    global_keywords = [
        "all country",
        "all countries",
        "global flight",
        "global flights",
        "all flight",
        "all flights",
        "worldwide flight",
        "worldwide flights",
    ]

    if any(keyword in q_lower for keyword in global_keywords):
        return None, None

    # Direct IATA route
    codes = re.findall(r"\b[A-Z]{3}\b", q)

    if len(codes) >= 2:
        return codes[0].upper(), codes[1].upper()

    # From X to Y
    match = re.search(
        r"\bfrom\s+(.+?)\s+\bto\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:
        origin_text = match.group(1)
        dest_text = match.group(2)

        dep_iata = resolve_location_to_iata(origin_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # To Y from X
    match = re.search(
        r"\bto\s+(.+?)\s+\bfrom\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at)\b|[.!?]|$)",
        q_lower,
    )

    if match:
        dest_text = match.group(1)
        origin_text = match.group(2)

        dep_iata = resolve_location_to_iata(origin_text)
        arr_iata = resolve_location_to_iata(dest_text)

        return dep_iata, arr_iata

    # From X
    match = re.search(r"\bfrom\s+(.+?)(?:[.!?]|$)", q_lower)

    if match:
        origin_text = match.group(1)
        dep_iata = resolve_location_to_iata(origin_text)

        return dep_iata, None

    # To X
    match = re.search(r"\bto\s+(.+?)(?:[.!?]|$)", q_lower)

    if match:
        dest_text = match.group(1)
        arr_iata = resolve_location_to_iata(dest_text)

        return None, arr_iata

    # Fallback location detection
    mentions = find_location_mentions(q)

    if len(mentions) >= 2:
        dep_iata = resolve_location_to_iata(mentions[0])
        arr_iata = resolve_location_to_iata(mentions[1])

        return dep_iata, arr_iata

    if len(mentions) == 1:
        arr_iata = resolve_location_to_iata(mentions[0])

        return DEFAULT_ORIGIN_IATA, arr_iata

    return None, None


def format_flight(flight: dict):
    airline = flight.get("airline", {}).get("name") or "Unknown airline"
    flight_number = flight.get("flight", {}).get("iata") or "Unknown flight number"
    status = flight.get("flight_status") or "Unknown"

    dep = flight.get("departure", {}) or {}
    arr = flight.get("arrival", {}) or {}

    dep_airport = dep.get("airport") or "Unknown departure airport"
    dep_iata = dep.get("iata") or "Unknown"
    dep_terminal = dep.get("terminal") or "N/A"
    dep_gate = dep.get("gate") or "N/A"
    dep_scheduled = dep.get("scheduled") or "Unknown"
    dep_delay = dep.get("delay")
    dep_delay_text = f"{dep_delay} minutes" if dep_delay is not None else "N/A"

    arr_airport = arr.get("airport") or "Unknown arrival airport"
    arr_iata = arr.get("iata") or "Unknown"
    arr_terminal = arr.get("terminal") or "N/A"
    arr_gate = arr.get("gate") or "N/A"
    arr_scheduled = arr.get("scheduled") or "Unknown"
    arr_delay = arr.get("delay")
    arr_delay_text = f"{arr_delay} minutes" if arr_delay is not None else "N/A"

    return f"""
Airline: {airline}
Flight: {flight_number}
Status: {status}

Departure:
- Airport: {dep_airport}
- IATA: {dep_iata}
- Terminal: {dep_terminal}
- Gate: {dep_gate}
- Scheduled: {dep_scheduled}
- Delay: {dep_delay_text}

Arrival:
- Airport: {arr_airport}
- IATA: {arr_iata}
- Terminal: {arr_terminal}
- Gate: {arr_gate}
- Scheduled: {arr_scheduled}
- Delay: {arr_delay_text}
""".strip()

def search_flights(query: str, limit: int = 10):
    if not API_KEY:
        return (
            "Flight API error: AVIATIONSTACK_API_KEY is missing.\n"
            "Please add this in your .env file:\n"
            "AVIATIONSTACK_API_KEY=your_api_key_here"
        )

    dep_iata, arr_iata = parse_route(query)

    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }

    if dep_iata:
        params["dep_iata"] = dep_iata

    if arr_iata:
        params["arr_iata"] = arr_iata

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )
        data = response.json()

    except requests.exceptions.RequestException as e:
        return f"Flight API request failed: {e}"

    except ValueError:
        return "Flight API returned invalid JSON."

    if "error" in data:
        error = data["error"]

        return (
            "Flight API error:\n"
            f"Code: {error.get('code', 'Unknown')}\n"
            f"Message: {error.get('message', 'Unknown error')}"
        )

    flight_data = data.get("data", [])

    if not flight_data:
        route_text = ""

        if dep_iata and arr_iata:
            route_text = f" for route {dep_iata} to {arr_iata}"
        elif dep_iata:
            route_text = f" from {dep_iata}"
        elif arr_iata:
            route_text = f" to {arr_iata}"

        return (
            f"No live flight data found{route_text}.\n\n"
            "Note: AviationStack provides live/status flight data, "
            "not ticket prices. For actual fare prices, use a "
            "flight-pricing API such as Amadeus."
        )

    route_info = "Global live flights"

    if dep_iata and arr_iata:
        route_info = f"Live flights from {dep_iata} to {arr_iata}"
    elif dep_iata:
        route_info = f"Live flights from {dep_iata}"
    elif arr_iata:
        route_info = f"Live flights to {arr_iata}"

    formatted_flights = [
        format_flight(flight)
        for flight in flight_data[:limit]
    ]

    return f"{route_info}\n\n" + "\n\n---\n\n".join(formatted_flights)


if __name__ == "__main__":
    print(
        search_flights(
            "Plan a 7 days Dubai trip from India " 
        )
    )

    print("\n" + "=" * 80 + "\n")

    print(
        search_flights(
            "all country flight info"
        )
    )