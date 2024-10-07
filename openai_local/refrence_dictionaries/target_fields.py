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


class FieldPrompts:
    Désignation_Organisme_Expropriant_prompt = (
        "Please provide the official name or designation of the organization responsible for the expropriation. "
        "This is typically the government entity or company leading the project."
    )

    Objet_prompt = (
        "What is the specific purpose or object of the expropriation? "
        "Describe the reason or justification behind the project in detail."
    )

    Jugement_Ref_prompt = (
        "Enter the official reference for the judgment associated with the expropriation. "
        "This field's name in Arabic is either 'حكم' or 'مقرر حكم'. "
        "Only return the field if one of these two terms is present in the text; otherwise, return 'N/A'."
    )

    Date_Jugement_prompt = (
        "Provide the date when the judgment related to the expropriation was issued. "
        "Ensure the format is DD/MM/YYYY. '"
        "Only return the field if one of these two terms : حكم' or 'مقرر حكم'.  "
        "is present in the text; otherwise, return 'N/A'."

    )

    Num_Décision_prompt = (
        "What is the official decision number for this expropriation process? "
        "This field's name in Arabic 'قرار '"
        "Only return the field if this term is present in the text; otherwise, return 'N/A'."
        "This is a legal identifier found in official documents."
    )

    Num_Bulletin_Officiel_prompt = (
        "Please enter the number of the official bulletin where this expropriation was published. "
        "This field's name in Arabic is 'الجريدة الرسمية' "
        "Only return the field if the term is present in the text; otherwise, return 'N/A'."
        "This is a legal identifier found in official documents.The expected format is '2.22.645'."
        "This field's name in Arabic is 'مرسوم'. The sentence format you are looking for is 'x.x.xxx مرسوم رقم'. "
        "If you find a sentence such as 'تبعا للمرسوم رقم 2.22.645', extract and return '2.22.645' as the value for this field."

    )

    Date_Bulletin_Officiel_prompt = (
        "Provide the date when the expropriation was published in the official bulletin."
        "Ensure the format is DD/MM/YYYY.  this field's name in arabic is 'الجريدة الرسمية ')"
        "Only return the field if the term is present in the text ***example**  if teh sentence : الصادر بالجريدة الرسمية رقم 6545 بتاريخ 23/02/2023"
        "is found : then the answer should be 23/02/2023"

    )

    Référence_Loi_prompt = (
        "What is the law reference associated with the expropriation process? "
        "For example, '7-81' could be a reference number for the relevant legislation."
    )

    Référence_Décret_Expropriation_prompt = (
        "Enter the decree reference number for the expropriation. The expected format is '2.22.645'. "
        "This field's name in Arabic is 'مرسوم'. The sentence format you are looking for is 'x.x.xxx مرسوم رقم'. "
        "If you find a sentence such as 'تبعا للمرسوم رقم 2.22.645', extract and return '2.22.645' as the value for this field."
    )

    Région_frappée_par_le_projet_prompt = (
        f"Which Moroccan region is affected by the expropriation project? "
        f"Provide the name of the region in which the project is taking place. the answer must be in this list {moroccan_regions}"

    )

    Commune_frappée_par_le_projet_prompt = (
        "Which Moroccan community is affected by the project? "
        "Provide the name of the specific commune involved in the expropriation."
    )

    Intitulé_Projet_prompt = (
        "What is the official title or name of the expropriation project? "
        "This is the project's designated title as mentioned in the documents."
    )

    Tranche_Projet_d_expropriation_prompt = (
        "What is the tranche or phase of the expropriation project? "
        "Provide details about the specific phase or segment of the project."
    )

    Montant_Total_Projet_prompt = (
        "What is the total financial cost of the expropriation project? "
        "Enter the amount as specified in the official documents."
    )

    Montant_Global_consigné_prompt = (
        "What is the total amount of money deposited for the expropriation? "
        "Provide the value as it appears in the financial records."
    )

    Type_Versement_prompt = (
        "What is the type of payment used in the expropriation process? "
        "For example, specify if it's a 'Chéque' or other form of payment."
    )

    Nom_Prénom_and_CIN_prompt = (
        "Get all the names in the table accurately. "
        "If a name is accompanied by a CIN (National ID) or a number, include that as well."
    )

    Adresse_courrier_prompt = (
        "What is the mailing address of the expropriating organization? "
        "Provide the full address as specified in the documents."
    )

    Num_Téléphone_prompt = (
        "What is the phone number of the expropriating organization? "
        "Ensure the phone number format includes the international code if applicable."
    )

    Localité_prompt = (
        "What is the locality or area where the project is situated? "
        "Provide the name of the locality as specified in the documents."
    )

    Identifiant_Fiscal_prompt = (
        "What is the fiscal identifier (IF) of each company involved in the project, if available? "
        "Provide the identifier numbers as listed in the records."
    )


expropriation_data = [
    {
        "field": "Désignation Organisme Expropriant",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Désignation_Organisme_Expropriant_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "Official name or title of the organization responsible for the expropriation.",
        "regex": r"^[A-Za-z\s]+$"
    },
    {
        "field": "Objet",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Objet_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "Purpose or reason behind the expropriation project.",
        "regex": r"^[A-Za-z\s]+$"
    },
    {
        "field": "Jugement Ref",
        "lookuptext": "table",
        "field_prompt": FieldPrompts.Jugement_Ref_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "Official reference number or ID associated with the judgment.",
        "regex": r"^\d+\/\d+$"
    },
    {
        "field": "Date Jugement",
        "lookuptext": "table",
        "field_prompt": FieldPrompts.Date_Jugement_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The official date on which the judgment was issued.",
        "regex": r"^\d{2}\/\d{2}\/\d{4}$"
    },
    {
        "field": "N° Décision",
        "lookuptext": "table",
        "field_prompt": FieldPrompts.Num_Décision_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The official decision number related to the expropriation process.",
        "regex": r"^\d+$"
    },
    {
        "field": "N° Bulletin Officiel",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Num_Bulletin_Officiel_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The number assigned to the official bulletin where the expropriation information is published.",
        "regex": r"^\d+$"
    },
    {
        "field": "Date Bulletin Officiel",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Date_Bulletin_Officiel_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The date of publication of the official bulletin.",
        "regex": r"^\d{2}\/\d{2}\/\d{4}$"
    },
    {
        "field": "Référence Loi",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Référence_Loi_prompt,
        "dynamic": False,
        "default_value": "7-81",
        "description": "The legal reference governing the expropriation.",
        "regex": r"^\d{1,3}-\d{2}$"
    },
    {
        "field": "Référence Décret Expropriation",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Référence_Décret_Expropriation_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The reference of the decree authorizing the expropriation process.",
        "regex": r"^\d+$"
    },
    {
        "field": "Région frappée par le projet",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Région_frappée_par_le_projet_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The Moroccan region impacted by the expropriation project.",
        "regex": r"^[A-Za-z\s\-]+$"
    },
    {
        "field": "Commune frappée par le projet",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Commune_frappée_par_le_projet_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The specific community impacted by the project.",
        "regex": r"^[A-Za-z\s\-]+$"
    },
    {
        "field": "Intitulé Projet",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Intitulé_Projet_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The official name or title of the expropriation project.",
        "regex": r"^[A-Za-z0-9\s\-]+$"
    },
    {
        "field": "Tranche Projet d'expropriation",
        "lookuptext": "table",
        "field_prompt": FieldPrompts.Tranche_Projet_d_expropriation_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The tranche or phase of the expropriation project.",
        "regex": r"^\d+$"
    },
    {
        "field": "Montant Total Projet",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Montant_Total_Projet_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The total financial cost of the expropriation project.",
        "regex": r"^\d+(\.\d{2})?$"
    },
    {
        "field": "Montant Global consigné",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Montant_Global_consigné_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The total amount of money deposited for the expropriation.",
        "regex": r"^\d+(\.\d{2})?$"
    },
    {
        "field": "Type Versement",
        "lookuptext": "table",
        "field_prompt": FieldPrompts.Type_Versement_prompt,
        "dynamic": False,
        "default_value": "Chéque",
        "description": "The payment method used for the expropriation (e.g., Cheque).",
        "regex": r"^[A-Za-z\s]+$"
    },
    {
        "field": "Nom / Prénom and CIN ",
        "lookuptext": "table",
        "field_prompt": FieldPrompts.Nom_Prénom_and_CIN_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The names of individuals involved, along with their CIN (national ID) if available.",
        "regex": r"^[A-Za-z\s]+(\s\d+)?$"
    },
    {
        "field": "Adresse courrier ",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Adresse_courrier_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The official mailing address of the expropriating organization.",
        "regex": r"^[A-Za-z0-9\s,]+$"
    },
    {
        "field": "N° Téléphone",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Num_Téléphone_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The contact phone number of the expropriating organization.",
        "regex": r"^\+?\d{10,15}$"
    },
    {
        "field": "Localité",
        "lookuptext": "text",
        "field_prompt": FieldPrompts.Localité_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The locality or area where the project is located.",
        "regex": r"^[A-Za-z\s]+$"
    },
    {
        "field": "identifiant fiscal",
        "lookuptext": "table",
        "field_prompt": FieldPrompts.Identifiant_Fiscal_prompt,
        "dynamic": True,
        "default_value": "N/A",
        "description": "The fiscal identifier (IF) associated with companies involved in the project.",
        "regex": r"^\d{5,12}$"
    }
]
