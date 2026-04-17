from pathlib import Path
import re


recipes_dir = Path("src/recepten")
old_source = "Koksopleiding Midden Nederland"
new_source = "Koksopleiding ROC Midden Nederland"

subtitle_overrides = {
    "aardappelsalade": "Een klassieke aardappelsalade met vastkokende aardappelen, augurk en een frisse, romige dressing.",
    "amerikaanse-coleslaw": "Een romige Amerikaanse koolsalade met fijngesneden kool, wortel en een frisse dressing met een vleugje zuur.",
    "flensjestaart": "Laagjes dunne crepes met banketbakkersroom en fruit maken dit tot een feestelijk nagerecht om van tevoren op te bouwen.",
    "french-dressing": "Een klassieke vinaigrette van azijn, olie en mosterd die als frisse basis past bij vrijwel elke salade.",
    "groentebouillon": "Een heldere groentebouillon die je rustig laat trekken voor een zuivere smaak en een lichte basis in de keuken.",
    "mayonaise": "Een klassieke koude emulsie van eidooier, olie en zuur, romig van structuur en breed inzetbaar in de keuken.",
    "omelet": "Een zachte omelet van drie eieren waarbij kleur, souplesse en een smeuige kern het verschil maken.",
    "saltimbocca-van-parelhoen-met-wittewijnsaus": "Parelhoenfilet met rauwe ham, salie en wittewijnsaus is een verfijnde variant op de klassieke Italiaanse saltimbocca.",
    "salade-met-geitenkaas-en-frambozendressing": "Een elegante lunchsalade met warme geitenkaas uit de oven en een frisse frambozendressing.",
    "tomatenbouillon": "Een heldere tomatenbouillon met een frisse, zuivere tomatensmaak en een verrassend lichte afdronk.",
}

subtitle_cleanup_patterns = (
    (r"\.\s*Op de koksopleiding[^.]*\.", "."),
    (r"\.\s*Via gastdocent Aggy Kan op de koksopleiding[^.]*\.", "."),
    (r",\s*op de koksopleiding[^.]*\.", "."),
    (r"\s+[-\u2014]\s+op de koksopleiding[^.]*\.", "."),
    (r"\s+dat op de koksopleiding[^.]*\.", "."),
)


def clean_subtitle(text: str, slug: str) -> str:
    if slug in subtitle_overrides:
        return subtitle_overrides[slug]

    cleaned = text
    for pattern, replacement in subtitle_cleanup_patterns:
        cleaned = re.sub(pattern, replacement, cleaned)

    cleaned = re.sub(r"\s+\.", ".", cleaned)
    cleaned = re.sub(r"\.\.+", ".", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


changed_sub = 0
changed_bron = 0
changed_tags = 0

for path in recipes_dir.glob("*.md"):
    text = path.read_text(encoding="utf-8")
    slug = path.stem
    modified = False

    if f'bron: "{old_source}"' in text:
        text = text.replace(f'bron: "{old_source}"', f'bron: "{new_source}"')
        changed_bron += 1
        modified = True

    sub_m = re.search(r'^subtitle: "([^"]*)"', text, re.M)
    if sub_m:
        old_sub = sub_m.group(1)
        new_sub = clean_subtitle(old_sub, slug)
        if old_sub != new_sub:
            text = text.replace(f'subtitle: "{old_sub}"', f'subtitle: "{new_sub}"', 1)
            changed_sub += 1
            modified = True

    tag_pattern = '\n  - "koksopleiding"'
    if tag_pattern in text:
        text = text.replace(tag_pattern, "")
        changed_tags += 1
        modified = True

    if modified:
        path.write_text(text, encoding="utf-8")

print(f"Bron bijgewerkt in {changed_bron} bestanden")
print(f"Subtitles herschreven in {changed_sub} bestanden")
print(f"Tags verwijderd in {changed_tags} bestanden")
