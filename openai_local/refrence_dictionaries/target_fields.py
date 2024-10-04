moroccan_regions = [
    "Tanger-Tetouan-Al Hoceima",
    "Oriental",
    "Fes-Meknes",
    "Rabat-Sale-Kenitra",
    "Beni Mellal-Khenifra",
    "Casablanca-Settat",
    "Marrakech-Safi",
    "Draa-Tafilalet",
    "Souss-Massa",
    "Guelmim-Oued Noun",
    "Laayoune-Sakia El Hamra",
    "Dakhla-Oued Ed-Dahab"
]





expropriation_data = [
    {
        "field": "Désignation Organisme Expropriant",
        "lookuptext": "text",
        "field_prompt": "What is the designation of the expropriating organization?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Objet",
        "lookuptext": "text",
        "field_prompt": "What is the object or purpose of the expropriation?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Jugement Ref",
        "lookuptext": "table",
        "field_prompt": "What is the reference for the judgment?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Date Jugement",
        "lookuptext": "table",
        "field_prompt": "What is the date of the judgment?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "N° Décision",
        "lookuptext": "table",
        "field_prompt": "What is the decision number?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "N° Bulletin Officiel",
        "lookuptext": "text",
        "field_prompt": "What is the official bulletin number?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Date Bulletin Officiel",
        "lookuptext": "text",
        "field_prompt": "What is the date of the official bulletin?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Référence Loi",
        "lookuptext": "text",
        "field_prompt": "What is the law reference?",
        "dynamic": False,
        "default_value": "7-81"
    },
    {
        "field": "Référence Décret Expropriation",
        "lookuptext": "text",
        "field_prompt": "What is the decree reference for the expropriation?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Région frappée par le projet",
        "lookuptext": "text",
        "field_prompt": "Which Moroccan region is affected by the project?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Commune frappée par le projet",
        "lookuptext": "text",
        "field_prompt": "Which Moroccan community is affected by the project?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Intitulé Projet",
        "lookuptext": "text",
        "field_prompt": "What is the title of the project?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Tranche Projet d'expropriation",
        "lookuptext": "table",
        "field_prompt": "What is the tranche of the expropriation project?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Montant Total Projet",
        "lookuptext": "text",
        "field_prompt": "What is the total cost of the project?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Montant Global consigné",
        "lookuptext": "text",
        "field_prompt": "What is the total deposited amount?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Type Versement",
        "lookuptext": "table",
        "field_prompt": "What is the type of payment?",
        "dynamic": False,
        "default_value": "Chéque"
    },
    {
        "field": "Nom / Prénom and CIN ",
        "lookuptext": "table",
        "field_prompt": "Get all the names in the table, be accurate , if the name is is accompanied by a CIN or a number , get that too  ",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Adresse courrier ",
        "lookuptext": "text",
        "field_prompt": "What is the mailing address of the Organisme Expropriant?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "N° Téléphone",
        "lookuptext": "text",
        "field_prompt": "What is the phone number of the Organisme Expropriant ?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "Localité",
        "lookuptext": "text",
        "field_prompt": "What is the locality of the project ?",
        "dynamic": True,
        "default_value": "N/A"
    },
    {
        "field": "identifiant fiscal",
        "lookuptext": "table",
        "field_prompt": "What is the fiscal identifier (IF) of each company if exists ?",
        "dynamic": True,
        "default_value": "N/A"
    }
]
