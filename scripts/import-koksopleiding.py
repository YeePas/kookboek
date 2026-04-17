from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RECIPES_DIR = ROOT / "src" / "recepten"
PHOTOS_DIR = ROOT / "fotos"
PEXELS_API_KEY = "aMq3g2BlsaWaTYEPsK9UKpBaH89dJkAzZE3OQHWATS5QQgWU8QRs6vqF"
SOURCE_NAME = "Koksopleiding ROC Midden Nederland"

RECIPES = [
    {
        "title": "French dressing",
        "category": "sauzen",
        "source": "Koksopleiding — lesdag 1",
        "ingredients": ["2 el wittewijnazijn", "6 el zonnebloemolie", "1 tl fijne mosterd", "bladpeterselie", "sjalot", "zout en peper"],
        "tags": ["dressing", "saus", "salade", "klassiek"],
        "photo_query": "vinaigrette salad dressing bowl",
    },
    {
        "title": "Mayonaise",
        "category": "sauzen",
        "source": "Koksopleiding — lesdag 1",
        "ingredients": ["1 eidooier", "mosterd", "azijn", "zonnebloemolie", "zout", "peper"],
        "tags": ["saus", "basis", "mayonaise", "emulsie"],
        "photo_query": "mayonnaise sauce bowl",
    },
    {
        "title": "Waldorfsalade",
        "category": "overig",
        "source": "Koksopleiding — lesdag 1",
        "ingredients": ["appel", "knolselderij", "walnoten", "mayonaise", "citroensap", "peper en zout"],
        "tags": ["salade", "lunch", "appel", "walnoten"],
        "photo_query": "waldorf salad plated",
    },
    {
        "title": "Aardappelsalade",
        "category": "overig",
        "source": "Koksopleiding — lesdag 1",
        "ingredients": ["vastkokende aardappelen", "augurk", "sjalot", "mayonaise of dressing", "bieslook", "mosterd"],
        "tags": ["salade", "aardappel", "bijgerecht", "klassiek"],
        "photo_query": "potato salad bowl",
    },
    {
        "title": "Amerikaanse coleslaw",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 1",
        "ingredients": ["witte kool", "wortel", "mayonaise", "azijn", "suiker", "peper en zout"],
        "tags": ["coleslaw", "koolsalade", "groente", "bijgerecht"],
        "photo_query": "coleslaw salad bowl",
    },
    {
        "title": "Salade Niçoise",
        "category": "vis",
        "source": "Koksopleiding — lesdag 2",
        "ingredients": ["tonijnfilet", "tomaat", "haricots verts", "aardappel", "ei", "zwarte olijven", "french dressing"],
        "tags": ["salade", "tonijn", "frans", "nicoise"],
        "photo_query": "salade nicoise tuna plate",
    },
    {
        "title": "Caponata met burrata",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 2",
        "ingredients": ["aubergine", "courgette", "bleekselderij", "kerstomaat", "kappertjes", "rozijnen", "burrata"],
        "tags": ["caponata", "burrata", "italiaans", "groentes"],
        "photo_query": "caponata burrata plate",
    },
    {
        "title": "Salade met geitenkaas en frambozendressing",
        "category": "overig",
        "source": "Koksopleiding — lesdag 2",
        "ingredients": ["geitenkaas", "mesclun", "kerstomaten", "spekjes", "frambozen", "frambozenazijn", "honing"],
        "tags": ["salade", "geitenkaas", "dressing", "framboos"],
        "photo_query": "goat cheese salad raspberry dressing",
    },
    {
        "title": "Slaatje 2.0",
        "category": "overig",
        "source": "Koksopleiding — lesdag 2",
        "ingredients": ["aardappelbrunoise", "courgette", "sjalot", "cornichons", "appel", "cottage cheese", "gepocheerd ei"],
        "tags": ["salade", "aardappel", "modern", "ei"],
        "photo_query": "modern plated salad poached egg",
    },
    {
        "title": "Groentebouillon",
        "category": "technieken",
        "source": "Koksopleiding — lesdag 3",
        "ingredients": ["wortel", "ui", "prei", "bleekselderij", "knoflook", "kruiden", "piment"],
        "tags": ["bouillon", "basis", "groente", "techniek"],
        "photo_query": "vegetable stock pot",
    },
    {
        "title": "Vleesbouillon",
        "category": "technieken",
        "source": "Koksopleiding — lesdag 3",
        "ingredients": ["runderbotten", "rundvlees", "wortel", "ui", "prei", "bleekselderij", "laurier en tijm"],
        "tags": ["bouillon", "vlees", "basis", "techniek"],
        "photo_query": "beef stock pot kitchen",
    },
    {
        "title": "Tomatenbouillon",
        "category": "technieken",
        "source": "Koksopleiding — lesdag 3",
        "ingredients": ["tomaten", "ui", "selderij", "kruiden", "bouillon", "zout en peper"],
        "tags": ["bouillon", "tomaat", "helder", "techniek"],
        "photo_query": "tomato consommé bowl",
    },
    {
        "title": "Tabouleh met naanbrood",
        "category": "overig",
        "source": "Koksopleiding — lesdag 3",
        "ingredients": ["bulgur", "peterselie", "munt", "tomaat", "komkommer", "citroen", "naanbrood"],
        "tags": ["tabouleh", "salade", "midden-oosters", "naan"],
        "photo_query": "tabbouleh naan bread plate",
    },
    {
        "title": "Aspergesalade met gerookte zalm en cracker",
        "category": "vis",
        "source": "Koksopleiding — lesdag 3",
        "ingredients": ["groene asperges", "gerookte zalm", "komkommer", "lijnzaadcracker", "frisse dressing", "kruiden"],
        "tags": ["asperge", "zalm", "salade", "voorgerecht"],
        "photo_query": "asparagus smoked salmon salad",
    },
    {
        "title": "Quinoasalade met feta, komkommer en hummus",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 3",
        "ingredients": ["quinoa", "feta", "komkommer", "hummus", "citroen", "olijfolie", "verse kruiden"],
        "tags": ["quinoa", "salade", "feta", "vegetarisch"],
        "photo_query": "quinoa salad feta cucumber bowl",
    },
    {
        "title": "Flensje met sinaasappelsaus en Grand Marnier",
        "category": "desserts",
        "source": "Koksopleiding — lesdag 3",
        "ingredients": ["flensjes", "sinaasappelsap", "suiker", "boter", "Grand Marnier", "sinaasappelrasp"],
        "tags": ["dessert", "flensje", "sinaasappel", "klassiek"],
        "photo_query": "crepe orange sauce dessert",
    },
    {
        "title": "Kippenbouillon",
        "category": "technieken",
        "source": "Koksopleiding — lesdag 6",
        "ingredients": ["kippenpoten", "mirepoix", "foelie", "lavas", "water", "peper en zout"],
        "tags": ["bouillon", "kip", "basis", "techniek"],
        "photo_query": "chicken stock pot kitchen",
    },
    {
        "title": "Champignon-crèmesoep",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 6",
        "ingredients": ["champignons", "boter", "bloem", "bouillon", "room", "ui", "peper en zout"],
        "tags": ["soep", "champignon", "romig", "klassiek"],
        "photo_query": "mushroom cream soup bowl",
    },
    {
        "title": "Tomatensoep klassiek",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 6",
        "ingredients": ["boter", "bloem", "tomatenpuree", "mirepoix", "groentebouillon", "tomatensap", "room"],
        "tags": ["soep", "tomaat", "klassiek", "basis"],
        "photo_query": "classic tomato soup bowl",
    },
    {
        "title": "Geroosterde bloemkoolsteak met chimichurri",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 10",
        "ingredients": ["bloemkool", "olijfolie", "knoflook", "peterselie", "rode wijnazijn", "chilivlokken"],
        "tags": ["bloemkool", "chimichurri", "vegetarisch", "roosteren"],
        "photo_query": "roasted cauliflower steak chimichurri",
    },
    {
        "title": "Romige pompoensoep met kokos en gember",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 10",
        "ingredients": ["pompoen", "ui", "gember", "kokosmelk", "bouillon", "limoen"],
        "tags": ["soep", "pompoen", "kokos", "gember"],
        "photo_query": "pumpkin soup coconut ginger bowl",
    },
    {
        "title": "Klassieke steak tartaar",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 11",
        "ingredients": ["ossenhaas of biefstuk", "kappertjes", "cornichons", "rode ui", "mosterd", "Worcestershiresaus", "eidooier"],
        "tags": ["steak tartaar", "klassiek", "rauw", "voorgerecht"],
        "photo_query": "steak tartare plated",
    },
    {
        "title": "Gebakken biefstuk met paddenstoelen en rode-ui-relish",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 11",
        "ingredients": ["biefstuk", "paddenstoelen", "rode ui", "boter", "jus", "seizoensgroenten"],
        "tags": ["biefstuk", "paddenstoelen", "vlees", "hoofdgerecht"],
        "photo_query": "steak mushrooms plated",
    },
    {
        "title": "Gehaktbal met piccalilly en aardappelsalade",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 11",
        "ingredients": ["half-om-halfgehakt", "ei", "paneermeel", "mosterd", "piccalilly", "aardappelsalade"],
        "tags": ["gehaktbal", "piccalilly", "nederlands", "klassiek"],
        "photo_query": "meatballs potato salad plate",
    },
    {
        "title": "Ceviche van zeebaars",
        "category": "vis",
        "source": "Koksopleiding — lesdag 12",
        "ingredients": ["zeebaars", "limoen", "rode ui", "rode peper", "knoflook", "avocado", "koriander"],
        "tags": ["ceviche", "zeebaars", "fris", "vis"],
        "photo_query": "sea bass ceviche plated",
    },
    {
        "title": "Saltimbocca van parelhoen met wittewijnsaus",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 12",
        "ingredients": ["parelhoenfilet", "rauwe ham", "salie", "boter", "gevogeltefond", "witte wijn"],
        "tags": ["parelhoen", "saltimbocca", "witte wijn", "klassiek"],
        "photo_query": "guinea fowl white wine sauce plated",
    },
    {
        "title": "Vanillebavarois met karamelsaus en Bastognepoeder",
        "category": "desserts",
        "source": "Koksopleiding — lesdag 12",
        "ingredients": ["melk", "slagroom", "gelatine", "vanille", "suiker", "eidooier", "Bastognekoek"],
        "tags": ["bavarois", "karamel", "dessert", "vanille"],
        "photo_query": "vanilla bavarois dessert plated",
    },
    {
        "title": "Limoencake",
        "category": "desserts",
        "source": "Koksopleiding — lesdag 13",
        "ingredients": ["boter", "lichtbruine basterdsuiker", "eieren", "limoen of citrusrasp", "zelfrijzend bakmeel", "bakpoeder"],
        "tags": ["cake", "limoen", "bakken", "dessert"],
        "photo_query": "lime cake loaf slice",
    },
    {
        "title": "Hollandse appeltaart",
        "category": "patisserie",
        "source": "Koksopleiding — lesdag 13",
        "ingredients": ["bloem", "boter", "suiker", "appel", "kaneel", "ei"],
        "tags": ["appeltaart", "bakken", "klassiek", "nederlands"],
        "photo_query": "dutch apple pie slice",
    },
    {
        "title": "Focaccia",
        "category": "brood",
        "source": "Koksopleiding — lesdag 13",
        "ingredients": ["bloem", "gist", "water", "olijfolie", "zout", "rozemarijn"],
        "tags": ["brood", "focaccia", "italiaans", "gistdeeg"],
        "photo_query": "focaccia bread rosemary",
    },
    {
        "title": "Risotto al mare",
        "category": "vis",
        "source": "Koksopleiding — lesdag 14",
        "ingredients": ["risottorijst", "vis of schaal- en schelpdieren", "witte wijn", "bouillon", "ui", "Parmezaan"],
        "tags": ["risotto", "vis", "italiaans", "rijst"],
        "photo_query": "seafood risotto bowl",
    },
    {
        "title": "Pasta con funghi",
        "category": "overig",
        "source": "Koksopleiding — lesdag 14",
        "ingredients": ["pasta", "gemengde paddenstoelen", "knoflook", "room of boter", "peterselie", "Parmezaan"],
        "tags": ["pasta", "funghi", "paddenstoel", "italiaans"],
        "photo_query": "mushroom pasta plate",
    },
    {
        "title": "Pad Thai",
        "category": "overig",
        "source": "Koksopleiding — lesdag 14",
        "ingredients": ["rijstnoedels", "vissaus", "sojasaus", "rijstazijn", "ei", "taugé", "pinda's"],
        "tags": ["pad thai", "streetfood", "aziatisch", "noedels"],
        "photo_query": "pad thai noodles plate",
    },
    {
        "title": "Geroosterde bloemkoolsteak met miso-sesamglazuur",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 16",
        "ingredients": ["bloemkool", "witte miso", "sojasaus", "sesamolie", "gember", "bosui", "sesam"],
        "tags": ["bloemkool", "miso", "sesam", "vegetarisch"],
        "photo_query": "miso cauliflower steak plated",
    },
    {
        "title": "Krokante polenta met paddenstoelen, truffelcrème en cavolo nero",
        "category": "groentes",
        "source": "Koksopleiding — lesdag 16",
        "ingredients": ["polenta", "paddenstoelen", "truffelcrème", "cavolo nero", "Parmezaan", "boter"],
        "tags": ["polenta", "paddenstoelen", "truffel", "vegetarisch"],
        "photo_query": "crispy polenta mushrooms plated",
    },
    {
        "title": "Ravioli met geitenkaas en citroen",
        "category": "overig",
        "source": "Koksopleiding — lesdag 16",
        "ingredients": ["verse ravioli", "geitenkaas", "citroen", "hazelnootboter", "salie", "spinazie"],
        "tags": ["ravioli", "geitenkaas", "citroen", "pasta"],
        "photo_query": "goat cheese ravioli plate",
    },
    {
        "title": "Moelleux au chocolat",
        "category": "desserts",
        "source": "Koksopleiding — lesdag 16",
        "ingredients": ["pure chocolade", "boter", "suiker", "eieren", "bloem", "snuf zout"],
        "tags": ["chocolade", "lava cake", "dessert", "frans"],
        "photo_query": "molten chocolate cake dessert",
    },
    {
        "title": "Sticky chicken",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 17",
        "ingredients": ["kipdijfilet", "honing", "sojasaus", "bruine suiker", "rijstazijn", "ketchup", "knoflook"],
        "tags": ["kip", "sticky", "aziatisch", "glaze"],
        "photo_query": "sticky chicken glazed plate",
    },
    {
        "title": "Gevogeltebouillon met bladerdeegdakje",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 17",
        "ingredients": ["gevogeltebouillon", "kip of parelhoen", "groenten", "bladerdeeg", "ei", "kruiden"],
        "tags": ["bouillon", "gevogelte", "bladerdeeg", "soep"],
        "photo_query": "chicken soup puff pastry bowl",
    },
    {
        "title": "Pasteitje met gevogelteragout",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 17",
        "ingredients": ["pasteibakjes", "gevogelte", "room", "bouillon", "champignons", "boter", "bloem"],
        "tags": ["ragout", "pasteitje", "kip", "klassiek"],
        "photo_query": "chicken vol au vent plate",
    },
    {
        "title": "Kaneelparfait met karamelsaus",
        "category": "desserts",
        "source": "Koksopleiding — lesdag 17",
        "ingredients": ["slagroom", "eidooier", "suiker", "kaneel", "vanille", "karamelsaus"],
        "tags": ["parfait", "kaneel", "dessert", "karamel"],
        "photo_query": "cinnamon parfait dessert",
    },
    {
        "title": "Oosters gemarineerde makreel",
        "category": "vis",
        "source": "Koksopleiding — lesdag 18",
        "ingredients": ["makreel", "komkommer", "radijs", "sjalot", "sushiazijn", "bier", "wasabimayonaise"],
        "tags": ["makreel", "oosters", "vis", "voorgerecht"],
        "photo_query": "mackerel cucumber plated appetizer",
    },
    {
        "title": "Rilette van gepocheerde zalm met crostini en bieslookcrème",
        "category": "vis",
        "source": "Koksopleiding — lesdag 18",
        "ingredients": ["verse zalm", "gerookte zalm", "crème fraîche", "dille", "citroen", "crostini", "bieslook"],
        "tags": ["rilette", "zalm", "crostini", "vis"],
        "photo_query": "salmon rillette crostini plated",
    },
    {
        "title": "Gebakken sliptong à la meunière",
        "category": "vis",
        "source": "Koksopleiding — lesdag 18",
        "ingredients": ["sliptong", "bloem", "boter", "citroen", "peterselie", "krieltjes", "zeekraal"],
        "tags": ["sliptong", "meuniere", "vis", "klassiek"],
        "photo_query": "sole meuniere fish plated",
    },
    {
        "title": "Vitello tonnato",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 19",
        "ingredients": ["kalfsvlees", "tonijn uit blik", "mayonaise", "kappertjes", "ansjovis", "citroen"],
        "tags": ["vitello tonnato", "kalf", "italiaans", "voorgerecht"],
        "photo_query": "vitello tonnato plated",
    },
    {
        "title": "Lamskoteletjes met rode biet, pastinaak en wortel",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 19",
        "ingredients": ["lamsrack", "rode biet", "pastinaak", "wortel", "lamsfond", "boter"],
        "tags": ["lam", "biet", "hoofdgerecht", "klassiek"],
        "photo_query": "lamb chops root vegetables plated",
    },
    {
        "title": "Rabarber crumble met yoghurtijs",
        "category": "desserts",
        "source": "Koksopleiding — lesdag 19",
        "ingredients": ["rabarber", "suiker", "bloem", "boter", "havermout of kruimels", "yoghurtijs"],
        "tags": ["rabarber", "crumble", "dessert", "yoghurtijs"],
        "photo_query": "rhubarb crumble ice cream dessert",
    },
    {
        "title": "Waldorfsalade met gerookte kip",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 20",
        "ingredients": ["knolselderij", "appel", "walnoten", "gerookte kip", "mayonaise", "citroensap"],
        "tags": ["waldorf", "gerookte kip", "salade", "lunch"],
        "photo_query": "smoked chicken waldorf salad",
    },
    {
        "title": "Viscrèmesoep met garnalen",
        "category": "vis",
        "source": "Koksopleiding — lesdag 20",
        "ingredients": ["boter", "bloem", "visbouillon", "room", "garnalen", "dille"],
        "tags": ["vissoep", "garnalen", "romig", "klassiek"],
        "photo_query": "shrimp cream soup bowl",
    },
    {
        "title": "Entrecôte met bearnaisesaus",
        "category": "vlees",
        "source": "Koksopleiding — lesdag 20",
        "ingredients": ["entrecôte", "bearnaisesaus", "haricots verts", "pommes sautées", "tomaat", "boter"],
        "tags": ["entrecote", "bearnaise", "vlees", "klassiek"],
        "photo_query": "entrecote bearnaise plated steak",
    },
    {
        "title": "Tarte tatin van ananas met vanilleparfait",
        "category": "desserts",
        "source": "Koksopleiding — lesdag 20",
        "ingredients": ["ananas", "bladerdeeg", "suiker", "boter", "vanilleparfait", "karamel"],
        "tags": ["tarte tatin", "ananas", "dessert", "vanille"],
        "photo_query": "pineapple tarte tatin dessert",
    },
]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().replace("&", " en ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_existing_state():
    max_page = 0
    category_orders = {}
    existing_slugs = set()
    for path in RECIPES_DIR.glob("*.md"):
        if path.name == "recepten.json":
            continue
        existing_slugs.add(path.stem)
        content = path.read_text(encoding="utf-8")
        m_page = re.search(r"^pageNumber:\s*(\d+)", content, re.M)
        if m_page:
            max_page = max(max_page, int(m_page.group(1)))
        m_cat = re.search(r'^category:\s*"([^"]+)"', content, re.M)
        m_order = re.search(r"^order:\s*(\d+)", content, re.M)
        if m_cat and m_order:
            cat = m_cat.group(1)
            category_orders[cat] = max(category_orders.get(cat, 0), int(m_order.group(1)))
    return max_page, category_orders, existing_slugs


def meta_for(category: str, title: str):
    low = title.lower()
    if any(k in low for k in ["cake", "taart", "bavarois", "parfait", "crumble", "tatin", "moelleux", "flensje"]):
        return [
            ("Personen", "4"),
            ("Voorber.", "20 min"),
            ("Bereiding", "30 min"),
            ("Niveau", "gemiddeld"),
        ]
    if any(k in low for k in ["dressing", "mayonaise", "saus"]):
        return [
            ("Opbrengst", "±250 ml"),
            ("Voorber.", "10 min"),
            ("Bereiding", "10 min"),
            ("Niveau", "makkelijk"),
        ]
    if "bouillon" in low or "soep" in low:
        return [
            ("Personen", "4"),
            ("Voorber.", "15 min"),
            ("Bereiding", "45 min"),
            ("Niveau", "gemiddeld"),
        ]
    return [
        ("Personen", "2"),
        ("Voorber.", "20 min"),
        ("Bereiding", "30 min"),
        ("Niveau", "gemiddeld"),
    ]


def subtitle_for(title: str, category: str, ingredients: list[str] | None = None):
    low = title.lower()
    items = ingredients or []
    top = ", ".join(items[:3]) if items else "mooie smaakmakers"

    if "salade" in low:
        return f"Een frisse en smaakvolle salade met {top}, perfect als lichte lunch of verfijnd voorgerecht."
    if "dressing" in low:
        return f"Een klassieke vinaigrette met {top} die bijna elke salade direct meer diepte geeft."
    if "mayonaise" in low:
        return f"Een romige basissaus met {top}, onmisbaar in de koude keuken."
    if "soep" in low:
        return f"Een volle, verwarmende soep op basis van {top}, mooi in balans en prettig van structuur."
    if "bouillon" in low:
        return f"Een heldere en smaakvolle bouillon getrokken van {top}, ideaal als basis voor verdere bereidingen."
    if any(k in low for k in ["bavarois", "parfait", "crumble", "cake", "taart", "tatin", "moelleux", "sabayon", "flensje"]):
        return f"Een verzorgd dessert met {top}, waarin smaak en textuur mooi samenkomen."
    if any(k in low for k in ["saus", "hollandaise", "bearnaise"]):
        return f"Een klassieke saus met {top}, bedoeld om een gerecht glans, frisheid en diepte te geven."
    if any(k in low for k in ["risotto", "pasta", "ravioli", "pad thai", "focaccia"]):
        return f"Een karaktervol gerecht met {top}, waarbij techniek en timing het verschil maken."
    return f"Een smaakvol gerecht met {top}, uitgewerkt tot een helder en goed navolgbaar recept."


def steps_for(title: str, category: str):
    low = title.lower()
    if "salade" in low or "ceviche" in low or "tonnato" in low or "rilette" in low:
        return [
            "**Voorbereiden:** Snijd en weeg alle ingrediënten af. Zorg dat koude componenten goed gekoeld zijn en breng alvast een basisdressing of marinade op smaak.",
            "**Hoofdcomponent maken:** Bereid het belangrijkste element volgens de techniek van het gerecht, zoals pocheren, marineren, grillen of mengen.",
            "**Afwerken:** Meng de garnituren voorzichtig door of leg ze los op het bord zodat kleur en structuur behouden blijven.",
            "**Serveren:** Proef nogmaals op zuur, zout en frisheid en serveer direct op gekoelde of passende borden.",
        ]
    if "soep" in low or "bouillon" in low:
        return [
            "**Basis opzetten:** Snijd de groenten of andere basisproducten klein en zet ze rustig aan in boter of olie zonder te donker te kleuren.",
            "**Trekkracht opbouwen:** Voeg vloeistof en kruiden toe, breng aan de kook en laat daarna zacht trekken zodat de smaken helder blijven.",
            "**Afwerken:** Zeef of pureer indien nodig en breng zorgvuldig op smaak met zout, peper en eventueel een klein beetje zuur of room.",
            "**Serveren:** Verwarm voor doorgifte goed door en werk af met een passende garnering.",
        ]
    if category == "desserts" or any(k in low for k in ["cake", "taart", "bavarois", "parfait", "crumble", "tatin", "moelleux", "flensje"]):
        return [
            "**Mise en place:** Weeg alle ingrediënten nauwkeurig af en bereid vormen, bakpapier of serveerglazen voor.",
            "**Basis maken:** Klop, meng of kook de hoofdcomponent tot een gladde en luchtige basis volgens de techniek van het gerecht.",
            "**Garen of opstijven:** Bak het dessert goudbruin of laat het voldoende koelen en opstijven voor de juiste textuur.",
            "**Afwerking:** Serveer netjes opgemaakt met saus, krokant element of vers fruit voor contrast.",
        ]
    if category == "sauzen" or any(k in low for k in ["dressing", "mayonaise", "saus"]):
        return [
            "**Basis mengen:** Doe de smaakmakers in een kom en roer of klop los tot alles goed is opgenomen.",
            "**Emulgeren of reduceren:** Voeg vet of vloeistof gecontroleerd toe en werk tot de juiste binding of concentratie.",
            "**Op smaak brengen:** Corrigeer met zuur, zout en peper tot de saus mooi in balans is.",
            "**Gebruiken:** Serveer direct of bewaar gekoeld in een schone afgesloten pot of fles.",
        ]
    if any(k in low for k in ["pasta", "risotto", "ravioli", "pad thai", "focaccia"]):
        return [
            "**Voorbereiden:** Zorg dat alle componenten klaarstaan, want deze gerechten vragen om een vlotte afwerking.",
            "**Hoofdbereiding:** Kook, bak of rooster de basiscomponent tot deze precies gaar is en voeg daarna de smaakmakers toe.",
            "**Binden en afmaken:** Voeg op het einde boter, kaas, saus of verse kruiden toe voor glans en samenhang.",
            "**Serveren:** Presenteer direct zodat textuur en temperatuur optimaal blijven.",
        ]
    return [
        "**Voorbereiden:** Maak alle ingrediënten schoon, snijd ze op maat en kruid het hoofdbestanddeel alvast licht.",
        "**Bakken of garen:** Bereid het hoofdproduct met aandacht voor kleur, garing en sappigheid.",
        "**Saus en garnituur:** Werk ondertussen de saus of bijgerechten af en proef alles goed door.",
        "**Serveren:** Laat indien nodig kort rusten, snijd aan en maak het bord verzorgd op.",
    ]


def tips_for(title: str):
    low = title.lower()
    if "risotto" in low:
        return ["Blijf regelmatig roeren en voeg de bouillon in delen toe voor een romige korrel."]
    if "mayonaise" in low or "dressing" in low:
        return ["Zorg dat alle ingrediënten op ongeveer dezelfde temperatuur zijn voor een stabiele emulsie."]
    if "bouillon" in low:
        return ["Laat bouillon trekken en niet hard koken; zo blijft de smaak helder en zuiver."]
    if any(k in low for k in ["cake", "taart", "moelleux"]):
        return ["Open de oven niet te vroeg zodat structuur en volume mooi behouden blijven."]
    return ["Proef aan het einde altijd nogmaals op zout, zuur, textuur en temperatuur."]


def download_photo(query: str, slug: str) -> str:
    PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    photo_path = PHOTOS_DIR / f"{slug}.jpg"
    if photo_path.exists():
        return photo_path.name
    try:
        api_url = f"https://api.pexels.com/v1/search?query={quote(query)}&per_page=1&orientation=landscape"
        req = Request(api_url, headers={"Authorization": PEXELS_API_KEY})
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        photos = data.get("photos") or []
        if not photos:
            return ""
        img_url = photos[0]["src"].get("large") or photos[0]["src"].get("medium")
        if not img_url:
            return ""
        img_req = Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(img_req, timeout=60) as response:
            photo_path.write_bytes(response.read())
        return photo_path.name
    except Exception:
        return ""


def render_recipe(recipe: dict, page_number: int, order: int, photo: str) -> str:
    ingredients = recipe["ingredients"]
    subtitle = recipe.get("subtitle") or subtitle_for(recipe["title"], recipe["category"], ingredients)
    meta = recipe.get("meta") or meta_for(recipe["category"], recipe["title"])
    steps = recipe.get("steps") or steps_for(recipe["title"], recipe["category"])
    tips = recipe.get("tips") or tips_for(recipe["title"])
    tags = recipe["tags"]

    lines = [
        "---",
        f'title: "{recipe["title"]}"',
        f'subtitle: "{subtitle}"',
        f'category: "{recipe["category"]}"',
        f'foto: "{photo}"',
        f"pageNumber: {page_number}",
        f"order: {order}",
        "",
        "meta:",
    ]
    for label, value in meta:
        lines.append(f'  - label: "{label}"')
        lines.append(f'    value: "{value}"')

    lines.extend(["", "ingredienten:", '  - groep: ""', "    items:"])
    for item in ingredients:
        lines.append(f'      - "{item}"')

    lines.extend(["", "stappen:"])
    for step in steps:
        lines.append(f'  - "{step}"')

    lines.extend(["", "tips:"])
    for tip in tips:
        lines.append(f'  - "{tip}"')

    lines.extend(["", f'bron: "{SOURCE_NAME}"', "", "tags:"])
    for tag in tags:
        lines.append(f'  - "{tag}"')
    lines.extend(["---", ""])
    return "\n".join(lines)


def main():
    max_page, category_orders, existing_slugs = parse_existing_state()
    created = 0
    skipped = 0
    for recipe in RECIPES:
        slug = recipe.get("slug") or slugify(recipe["title"])
        out_path = RECIPES_DIR / f"{slug}.md"
        if slug in existing_slugs or out_path.exists():
            skipped += 1
            print(f"SKIP  {slug}")
            continue

        category = recipe["category"]
        max_page += 1
        category_orders[category] = category_orders.get(category, 0) + 1
        photo = download_photo(recipe.get("photo_query") or recipe["title"], slug)
        content = render_recipe(recipe, max_page, category_orders[category], photo)
        out_path.write_text(content, encoding="utf-8")
        created += 1
        print(f"CREATE {slug}  photo={'yes' if photo else 'no'}")

    print(f"\nKlaar. Nieuwe recepten: {created}, overgeslagen: {skipped}")


if __name__ == "__main__":
    main()
