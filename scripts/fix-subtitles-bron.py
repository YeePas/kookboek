from pathlib import Path
import re

recipes_dir = Path("src/recepten")
old_source = "Koksopleiding Midden Nederland"
new_source = "Koksopleiding ROC Midden Nederland"

origin_subtitles = {
    "french-dressing": "De allereerste vinaigrette die je op de koksopleiding leert maken \u2014 een simpele emulsie van azijn, olie en mosterd die de basis vormt voor vrijwel elke salade.",
    "mayonaise": "Zelf mayonaise maken is een van de eerste technieken op de koksopleiding: met geduld, een garde en een stabiele hand leer je de koude emulsie beheersen.",
    "waldorfsalade": "Een klassieke Amerikaanse salade uit 1893, oorspronkelijk bedacht in het Waldorf Hotel in New York. Op de koksopleiding een van de eerste oefeningen in snijtechnieken en salade-opbouw.",
    "aardappelsalade": "Een eerlijke, Nederlandse aardappelsalade zoals je die op de koksopleiding leert \u2014 met vastkokende aardappelen, augurk en een goed afgesmaakte dressing.",
    "amerikaanse-coleslaw": "De Amerikaanse koolsalade die op de koksopleiding wordt gebruikt om snijtechnieken als julienne te oefenen, met een romige dressing van mayonaise en een vleugje zuur.",
    "salade-nicoise": "Een Proven\u00e7aalse klassieker met gegrilde tonijn, haricots verts en olijven. Op de koksopleiding oefen je hiermee het grillen van vis en het opbouwen van een samengestelde salade.",
    "caponata-met-burrata": "Een Siciliaans groentegerecht met gefrituurde aubergine, zoetzure smaken en romige burrata. Via gastdocent Aggy Kan op de koksopleiding op het menu gekomen.",
    "salade-met-geitenkaas-en-frambozendressing": "Een elegante lunchsalade met warme geitenkaas uit de oven en een frisse frambozendressing \u2014 geleerd als onderdeel van de saladetechnieken op de koksopleiding.",
    "slaatje-2-0": "Een eigentijdse salade met aardappelbrunoise, gegrilde courgette en gepocheerd ei. Op de koksopleiding bedoeld om meerdere technieken tegelijk te combineren.",
    "groentebouillon": "De eerste bouillon die je op de koksopleiding trekt: groenten rustig laten trekken in water, zonder te koken, zodat je een helder en zuiver resultaat krijgt.",
    "vleesbouillon": "Een krachtige runderbouillon op basis van gepinceerde botten en mirepoix. Op de koksopleiding leer je hiermee de basis van extractie en smaakopbouw.",
    "tomatenbouillon": "Een heldere tomatenbouillon die op de koksopleiding wordt behandeld als variant op de klassieke bouillontechnieken \u2014 licht, fris en vol tomatensmaak.",
    "tabouleh-met-naanbrood": "Een Midden-Oosterse bulgursalade met veel verse kruiden, geserveerd met warm naanbrood. Op de koksopleiding onderdeel van een les over internationale keukens.",
    "aspergesalade-met-gerookte-zalm-en-cracker": "Een voorjaarsalade met gegrilde asperges, gerookte zalm en een zelfgemaakte lijnzaadcracker. Op de koksopleiding gecombineerd met een les over garnituren.",
    "quinoasalade-met-feta-komkommer-en-hummus": "Een moderne vegetarische salade met quinoa, feta en zelfgemaakte hummus \u2014 op de koksopleiding gebruikt als voorbeeld van een eigentijds groentemenu.",
    "flensje-met-sinaasappelsaus-en-grand-marnier": "Cr\u00eapes Suzette in de dop: dunne flensjes met een sinaasappelbotersaus en een vleugje Grand Marnier. Op de koksopleiding geleerd als onderdeel van de basistechnieken voor desserts.",
    "kippenbouillon": "Een heldere kippenbouillon op basis van kippenpoten en mirepoix. Op de koksopleiding een van de fundamentele bouillons die je van begin tot eind zelf trekt.",
    "champignon-cremesoep": "Een fluwelen champignonsoep gebonden met een roux en afgewerkt met room. Op de koksopleiding gebruikt om roux-techniek en het pur\u00e9ren van soepen te oefenen.",
    "tomatensoep-klassiek": "Een klassieke gebonden tomatensoep met tomatenpuree, roux en verse mirepoix. Op de koksopleiding het standaardrecept bij de les over warme soepen.",
    "geroosterde-bloemkoolsteak-met-chimichurri": "Een stevige bloemkoolsteak uit de oven met een pittige, verse chimichurri. Op de koksopleiding onderdeel van een volledig vegetarisch viergangenmenu.",
    "romige-pompoensoep-met-kokos-en-gember": "Een fluweelzachte pompoensoep met kokosmelk en verse gember. Op de koksopleiding behandeld als voorbeeld van een moderne, plantaardige soep.",
    "klassieke-steak-tartaar": "Handgesneden ossenhaas met kappertjes, cornichons en een rauwe eidooier \u2014 de klassieker onder de koude vleesbereidingen, op de koksopleiding geleerd als oefening in snijtechniek en balans.",
    "gebakken-biefstuk-met-paddenstoelen-en-rode-ui-relish": "Een sappige biefstuk met gebakken paddenstoelen en zoetzure rode-ui-relish. Op de koksopleiding het standaardgerecht om vlees bakken en bijpassende sauzen te oefenen.",
    "gehaktbal-met-piccalilly-en-aardappelsalade": "Een stevige Nederlandse gehaktbal met zelfgemaakte piccalilly en frisse aardappelsalade. Op de koksopleiding een oefening in het bereiden en op smaak brengen van gehakt.",
    "ceviche-van-zeebaars": "Rauwe zeebaars gemarineerd in limoen met rode ui, koriander en avocado. Op de koksopleiding onderdeel van een driegangenmenu met vis als rode draad.",
    "saltimbocca-van-parelhoen-met-wittewijnsaus": "Parelhoenfilet gewikkeld in rauwe ham en salie, afgeblust met witte wijn. Deze Italiaanse klassieker staat op de koksopleiding bij de les over het driegangenmenu.",
    "vanillebavarois-met-karamelsaus-en-bastognepoeder": "Een licht trillende vanillebavarois met blonde karamelsaus en krokant Bastognepoeder. Op de koksopleiding het nagerecht van het driegangenmenu in lesdag 12.",
    "limoencake": "Een sappige citroencake naar recept van Jamie Oliver, op de koksopleiding gebakken als onderdeel van de les over degen en beslagen.",
    "hollandse-appeltaart": "De oer-Hollandse appeltaart met kruimelig deeg, kaneel en schijfjes goudrenet. Op de koksopleiding het recept waarmee je leert werken met zanddeeg.",
    "focaccia": "Een luchtig Italiaans platbrood met olijfolie en rozemarijn. Op de koksopleiding gebakken als onderdeel van de les over gistdegen en broodbereiding.",
    "risotto-al-mare": "Een romige risotto met vis en zeevruchten in de Italiaanse traditie. Op de koksopleiding het hoofdgerecht bij de les over pasta- en rijstbereidingen.",
    "pasta-con-funghi": "Verse pasta met een mengsel van seizoenspaddenstoelen, knoflook en Parmezaan. Op de koksopleiding onderdeel van de Italiaanse les over pasta en risotto.",
    "pad-thai": "Thaise roergebakken rijstnoedels met ei, taug\u00e9 en pinda\u2019s. Op de koksopleiding ge\u00efntroduceerd als streetfoodgerecht bij de les over internationale keukens.",
    "geroosterde-bloemkoolsteak-met-miso-sesamglazuur": "Dikke plakken bloemkool met een umami-rijk glazuur van miso en sesam. Op de koksopleiding onderdeel van een viergangenmenu met Aziatische invloeden.",
    "krokante-polenta-met-paddenstoelen-truffelcreme-en-cavolo-nero": "Krokant gebakken polenta met truffelcr\u00e8me, seizoenspaddenstoelen en cavolo nero. Op de koksopleiding een tussengerecht uit het viergangenmenu.",
    "ravioli-met-geitenkaas-en-citroen": "Zelfgemaakte ravioli gevuld met geitenkaas en citroen, geserveerd met hazelnootboter en krokante salie. Op de koksopleiding het pastaonderdeel van een viergangenmenu.",
    "moelleux-au-chocolat": "Een Frans chocoladecakeje met een vloeibare kern van pure chocolade. Op de koksopleiding het nagerecht van het viergangenmenu \u2014 timing is hier alles.",
    "sticky-chicken": "Kipdijfilet in een kleverig glazuur van honing, sojasaus en ketchup. Op de koksopleiding bereid als onderdeel van de les waarin een hele kip op drie manieren wordt verwerkt.",
    "gevogeltebouillon-met-bladerdeegdakje": "Een dampende gevogeltebouillon afgedekt met een goudbruin bladerdeegdakje. Op de koksopleiding het voorgerecht bij de les over het verwerken van een hele kip.",
    "pasteitje-met-gevogelteragout": "Krokante pasteibakjes gevuld met romige gevogelteragout en champignons. Op de koksopleiding het hoofdgerecht bij de kippenles, met zelfgetrokken bouillon als basis.",
    "kaneelparfait-met-karamelsaus": "Een bevroren parfait met kaneel en vanille, geserveerd met warme karamelsaus. Op de koksopleiding het dessert bij de les over het verwerken van gevogelte.",
    "oosters-gemarineerde-makreel": "Verse makreel gemarineerd in sojasaus en sushiazijn, met zoetzure komkommer en wasabimayonaise. Op de koksopleiding het voorgerecht bij de visles.",
    "rilette-van-gepocheerde-zalm-met-crostini-en-bieslookcreme": "Een rilette van verse en gerookte zalm met cr\u00e8me fra\u00eeche en dille, geserveerd op krokante crostini. Op de koksopleiding het tussengerecht bij de les over vis.",
    "gebakken-sliptong-a-la-meuniere": "Sliptong door de bloem gehaald en gebakken in bruisende boter met citroen en peterselie \u2014 \u00e0 la meuni\u00e8re, de klassieke Franse visbereiding. Op de koksopleiding het hoofdgerecht van de visles.",
    "vitello-tonnato": "Dun gesneden kalfsvlees met een romige tonijnsaus, kappertjes en ansjovis. Een Italiaans-Piemontese klassieker, op de koksopleiding bereid als koud voorgerecht.",
    "lamskoteletjes-met-rode-biet-pastinaak-en-wortel": "Roze gebakken lamskoteletjes met geroosterde wortelgroenten en een fondsaus. Op de koksopleiding het hoofdgerecht bij de les over lam en sauzen op basis van fond.",
    "rabarber-crumble-met-yoghurtijs": "Warme rabarbercrumble met een krokante kruimellaag, geserveerd met fris yoghurtijs. Op de koksopleiding het nagerecht bij de les over vleesbereidingen.",
    "waldorfsalade-met-gerookte-kip": "De Waldorfsalade opnieuw, nu met gerookte kipfilet, knolselderij en walnoten. Op de koksopleiding het voorgerecht van het afsluitende viergangenmenu.",
    "viscremesoep-met-garnalen": "Een fluwelen gebonden vissoep met Noorse garnalen, room en verse dille. Op de koksopleiding bereid als tweede gang van het eindmenu.",
    "entrecote-met-bearnaisesaus": "Een dubbele entrec\u00f4te met klassieke b\u00e9arnaisesaus, pommes saut\u00e9es en haricots verts. Op de koksopleiding het hoofdgerecht van het afsluitende menu \u2014 de ultieme vleestest.",
    "tarte-tatin-van-ananas-met-vanilleparfait": "Gekaramelliseerde ananas op krokant bladerdeeg, geserveerd met vanilleparfait. Op de koksopleiding het nagerecht van het afsluitende viergangenmenu.",
    "omelet": "De eerste praktijkopdracht op de koksopleiding: een luchtige omelet op basis van drie eieren, waarbij kleur en gaarheid allesbepalend zijn.",
    "sinaasappel-met-sabayon": "Uitgesneden sinaasappelpartjes met een luchtige, warm opgeklopte sabayon van eidooier, suiker en witte wijn. Op de koksopleiding geleerd als oefening in het werken met eieren.",
    "tuile-met-vanille-ijs": "Een krokante tuile gevormd over een koffiekopje, gevuld met vanille-ijs en geserveerd met echte vanillesaus. Op de koksopleiding het sluitstuk van de eierenles.",
    "vanillesaus": "Cr\u00e8me anglaise \u2014 de moeder aller dessertsauzen, gebonden door eidooier en geparfumeerd met echt vanillemerg. Op de koksopleiding een onmisbare basistechniek.",
    "aardbeienbavarois": "Een lichte bavarois van aardbeienpuree, slagroom en gelatine. Op de koksopleiding het eerste nagerecht waarbij je de techniek van hangend verwerken leert.",
    "chocolademousse": "Een intense chocolademousse naar recept van patissier Harry Mercuur. Op de koksopleiding het paradepaardje van de les over koude nagerechten.",
    "soezenbeslag": "De basis voor soezen, \u00e9clairs en profiteroles: een warm beslag dat op het vuur wordt geroerd tot het loslaat. Op de koksopleiding gedemonstreerd als kerntechniek bij nagerechten.",
    "banketbakkersroom": "Een romige cr\u00e8me p\u00e2tissi\u00e8re op basis van melk, eidooier en vanille. Op de koksopleiding de standaardvulling voor soezen en \u00e9clairs.",
    "flensjestaart": "Laagjes dunne cr\u00eapes afgewisseld met banketbakkersroom en fruit \u2014 een feestelijk nagerecht dat op de koksopleiding de flensjes- en roomtechniek combineert.",
}

changed_sub = 0
changed_bron = 0
for path in recipes_dir.glob("*.md"):
    text = path.read_text(encoding="utf-8")
    slug = path.stem
    modified = False

    if f'bron: "{old_source}"' in text:
        text = text.replace(f'bron: "{old_source}"', f'bron: "{new_source}"')
        changed_bron += 1
        modified = True

    if slug in origin_subtitles:
        sub_m = re.search(r'^subtitle: "([^"]*)"', text, re.M)
        if sub_m:
            old_sub = sub_m.group(1)
            new_sub = origin_subtitles[slug]
            if old_sub != new_sub:
                text = text.replace(f'subtitle: "{old_sub}"', f'subtitle: "{new_sub}"', 1)
                changed_sub += 1
                modified = True

    if modified:
        path.write_text(text, encoding="utf-8")

print(f"Bron bijgewerkt in {changed_bron} bestanden")
print(f"Subtitles herschreven in {changed_sub} bestanden")
