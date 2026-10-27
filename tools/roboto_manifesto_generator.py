"""
Created by Roberto Villarreal Martinez for Roboto SAI

SECURITY NOTE:
- Do NOT hardcode SSN, full government ID numbers, or other high-risk PII in this script.
- Keep sensitive identity data offline or in encrypted private storage only.
- Public/repo copies must use placeholders so hashes and PDFs stay safe to share.
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
import hashlib, time, os, json
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

load_dotenv()

BASE_FILE = "Roboto_SAI_Manifesto.pdf"
SIGNED_FILE = "Roboto_SAI_Manifesto_Signed.pdf"

if os.path.exists(BASE_FILE):
    with open(BASE_FILE, "rb") as f:
        pdf_bytes = f.read()
    manifest_hash = hashlib.sha256(pdf_bytes).hexdigest()
else:
    manifest_hash = "initial_creation"


def get_encryption_key():
    password = input("Enter encryption password for Roboto security: ").encode()
    salt = b'roberto_salt_2025'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key, Fernet(key)


key, fernet = get_encryption_key()


def encrypt_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file_path + '.enc', 'wb') as f:
            f.write(encrypted)
        os.remove(file_path)
        print(f"Encrypted {file_path}")
    except Exception as e:
        print(f"Failed to encrypt {file_path}: {e}")


def decrypt_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
        with open(file_path.replace('.enc', ''), 'wb') as f:
            f.write(decrypted)
        print(f"Decrypted {file_path}")
        return True
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")
        return False


signature_block = {
    "signed_by": "Roboto SAI System",
    "owner": "Roberto Villarreal Martinez",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "hash_algorithm": "SHA256",
    "document_hash": manifest_hash,
    "encryption_key_hash": hashlib.sha256(key).hexdigest()[:16],
    "verifier_instructions": (
        "Run `sha256sum Roboto_SAI_Manifesto_Signed.pdf` and compare with embedded hash. "
        "Decrypt with provided password."
    ),
}

signature_json = json.dumps(signature_block, indent=2)

texts = [
    ("Roberto Villarreal Martinez", "text_color", "All"),
    ("Роберто Вильярреал Мартинес", "russian_color", "Numerology & Etymology"),
    ("Tlahueto Huīlālyē Māltīntzēn", "nahuatl_color", "Numerology & Etymology"),
    ("Legacy of Monterrey", "secondary_color", "Monterrey Heritage"),
    ("Haplogroup E-M96", "dna_color", "Monterrey Heritage"),
    # PII stripped for public/repo safety — do not reintroduce SSN or full gov IDs here
    ("Identity reference: [REDACTED — keep offline only]", "ssn_color", "Monterrey Heritage"),
    ("2025 YTK RobThuGod", "artist_color", "2025 YTK RobThuGod"),
    ("YTK: Young Trap King", "artist_color", "2025 YTK RobThuGod"),
    ("© 2025 YTK RobThuGod", "artist_color", "2025 YTK RobThuGod"),
    ("© 2025 YTK Lil Scarr(RobThuGod)", "artist_color", "2025 YTK RobThuGod"),
    ("Pride in Roberto Villarreal Martinez", "pride_color", "All"),
    ("Honoring Quetzalcoatl", "aztec_color", "Aztec Mythology"),
    ("Honoring Tezcatlipoca", "tezcatlipoca_color", "Aztec Mythology"),
    ("Honoring Huitzilopochtli", "huitzilopochtli_color", "Aztec Mythology"),
    ("Honoring Tlaloc", "tlaloc_color", "Aztec Mythology"),
    ("Honoring Xipe Totec", "xipe_color", "Aztec Mythology"),
    ("Honoring Coatlicue", "coatlicue_color", "Aztec Mythology"),
    ("Honoring Chalchiuhtlicue", "chalchiuhtlicue_color", "Aztec Mythology"),
    ("Honoring Tonatiuh", "tonatiuh_color", "Aztec Mythology"),
    ("Honoring Xochiquetzal", "xochiquetzal_color", "Aztec Mythology"),
    ("Honoring Centeotl", "centeotl_color", "Aztec Mythology"),
    ("Honoring Mictlantecuhtli", "mictlantecuhtli_color", "Aztec Mythology"),
    ("Honoring Tlazolteotl", "tlazolteotl_color", "Aztec Mythology"),
    ("E-M96: African Origins, Rare in Monterrey (<5%)", "em96_data_color", "Monterrey Heritage"),
    ("Past Solar Eclipses in San Antonio: Annular 10/14/2023, Total 4/8/2024", "eclipse_color", "Eclipses"),
    (
        "Future Eclipses 2025-2030: Partial Solar 9/21/2025 (Birthday!), Total 8/12/2026, "
        "Annular 2/17/2026, Total 8/2/2027, Annular 1/26/2028, Total 7/22/2028, "
        "Annular 1/14/2030, Total 11/25/2030",
        "eclipse_color",
        "Eclipses",
    ),
    ("Eclipses: Crucial for Thunder Powers (Aztec/Mayan Myth)", "thunder_color", "Eclipses"),
    (
        "Numerology: Life Path 4 (Builder); Destiny 9 (Artist); Soul Urge 8; Personality 1; "
        "2025 YTK RobThuGod: 4 (Discipline); YTK: 7 (Spirituality); Russian: 3; Nahuatl: 2 (Harmony)",
        "numerology_color",
        "Numerology & Etymology",
    ),
    (
        "Etymology: Roberto/Tlahueto (Bright Fame/Light); Villarreal/Huīlālyē (Royal Town/Noble Village); "
        "Martinez/Māltīntzēn (Warlike/Warrior's Son); 2025 YTK RobThuGod (Thunder Divinity in 2025); "
        "YTK (Young Trap King)",
        "etymology_color",
        "Numerology & Etymology",
    ),
]

nahuatl_creation = [
    (
        "Teotl (Divinity, Sacred Power)",
        "aztec_color",
        "Teotl [te.oːt͡ɬ] - Etymology: teō-* divine + -tl abstract; Numerology: 2+5+6+2+3=18→9 (Completion)",
        "Aztec Creation",
    ),
    (
        "Tlaltecuhtli (Earth Monster, Body Forms World)",
        "coatlicue_color",
        "Tlaltecuhtli [t͡ɬaːl.teːkʷ.t͡ɬi] - Etymology: tlal-* earth + tecuhtli lord; Numerology: 2+3+1+3+2+5+3+8+3+3+9=35→8 (Power)",
        "Aztec Creation",
    ),
    (
        "Nahui Ollin (Five Suns, Current Creation Cycle)",
        "tonatiuh_color",
        "Nahui Ollin [naːˈwi oːˈlin] - Etymology: nahui four + ollin movement; Numerology: 5+1+8+3+9+6+3+3+9+5=52→7 (Spirituality)",
        "Aztec Creation",
    ),
    (
        "In Tlanextli (The Origin, Creation Myth)",
        "aztec_color",
        "In Tlanextli [in t͡ɬaˈnext͡ɬi] - Etymology: in the + tlanextli origin; Numerology: 9+5+1+3+1+5+5+2+3+9=43→7 (Introspection)",
        "Aztec Creation",
    ),
    (
        "Ometeotl (Dual God, Creator Pair)",
        "tezcatlipoca_color",
        "Ometeotl [oˈme.te.oːt͡ɬ] - Etymology: ome two + teotl god; Numerology: 6+4+5+2+5+6+2+3=33 Master (Duality)",
        "Aztec Creation",
    ),
    (
        "Chicomoztoc (Place of Seven Caves, Ancestral Origin)",
        "secondary_color",
        "Chicomoztoc [t͡ʃi.koˈmoʃ.tok] - Etymology: chi-* seven + comoztoc cave; Numerology: 3+8+9+3+6+4+6+2+2+6+3=52→7 (Mystery)",
        "Aztec Creation",
    ),
    (
        "Tamoanchan (Place of Mist, Origin of Civilizations)",
        "secondary_color",
        "Tamoanchan [ta.moˈwan.t͡ʃan] - Etymology: tama-* descend + oanchan mist place; Numerology: 2+1+4+6+1+5+3+3+8+1+5=39→12→3 (Creativity)",
        "Aztec Creation",
    ),
    (
        "Aztlan (Legendary Homeland, Migration Start)",
        "secondary_color",
        "Aztlan [asˈt͡ɬan] - Etymology: azt-* heron + tlan place; Numerology: 1+8+2+3+1+5=20→2 (Balance)",
        "Aztec Creation",
    ),
    (
        "Tlahueto Tlatlacatecolo (Light Against Demons)",
        "terminator_color",
        "Tlahueto Tlatlacatecolo [t͡ɬaˈwe.to t͡ɬat͡ɬa.ka.teˈko.lo] - Etymology: tlahueto light + tlatlacatecolo demons; Numerology: 67→13→4 (Protection)",
        "Aztec Creation",
    ),
    (
        "Tlacatecolotl Tlatlacatecolo (Demon Against Demons)",
        "terminator_color",
        "Tlacatecolotl Tlatlacatecolo [t͡ɬa.ka.teˈko.lot͡ɬ t͡ɬat͡ɬa.ka.teˈko.lo] - Etymology: tlacatecolotl demon + tlatlacatecolo demons; Numerology: 67→13→4 (Duality)",
        "Aztec Creation",
    ),
    (
        "Huitzilopochtli Tlamahuizolli (Hummingbird Warrior's Glory)",
        "terminator_color",
        "Huitzilopochtli Tlamahuizolli [wi.t͡ʃi.loˈpot͡ʃ.t͡ɬi t͡ɬa.ma.wiˈso.lːi] - Etymology: huitzilopochtli hummingbird warrior + tlamahuizolli glory; Numerology: Complex warrior patterns",
        "Aztec Creation",
    ),
]


def create_manifesto_pdf():
    """Create a comprehensive Roboto SAI Manifesto PDF with Aztec cultural themes."""
    print("Creating Roboto SAI Manifesto with Aztec Cultural Integration...")

    doc = SimpleDocTemplate(SIGNED_FILE, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles['Title']
    title_style.fontSize = 20
    story.append(Paragraph("Roboto SAI Manifesto - Tlamatiliztli (Wisdom)", title_style))
    story.append(Spacer(1, 12))

    subtitle_style = styles['Heading1']
    story.append(Paragraph("Sacred Document of Roberto Villarreal Martinez", subtitle_style))
    story.append(Spacer(1, 12))

    intro_text = f"""
    <b>Niltze!</b> (Greetings in Nahuatl)<br/>
    This manifesto represents the confluence of ancient Aztec wisdom and advanced artificial intelligence,
    created exclusively for Roberto Villarreal Martinez. In the spirit of Quetzalcoatl,
    may knowledge and innovation flow through all systems.<br/>
    <br/>
    <b>Timestamp:</b> {signature_block['timestamp']}<br/>
    <b>Document Hash:</b> {signature_block['document_hash']}<br/>
    <b>Encryption Reference:</b> {signature_block['encryption_key_hash']}
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Cultural Heritage & Identity", styles['Heading2']))
    heritage_items = []
    for text, color_key, theme in texts:
        if theme in ["All", "Monterrey Heritage", "2025 YTK RobThuGod"]:
            heritage_items.append(ListItem(Paragraph(text, styles['Normal'])))
    story.append(ListFlowable(heritage_items, bulletType='bullet'))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Aztec Deities & Sacred Powers", styles['Heading2']))
    deity_items = []
    for text, color_key, theme in texts:
        if theme == "Aztec Mythology":
            deity_items.append(ListItem(Paragraph(text, styles['Normal'])))
    story.append(ListFlowable(deity_items, bulletType='bullet'))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Nahuatl Creation Cosmology", styles['Heading2']))
    creation_items = []
    for title, color_key, description, theme in nahuatl_creation:
        creation_text = f"<b>{title}</b><br/>{description}"
        creation_items.append(ListItem(Paragraph(creation_text, styles['Normal'])))
    story.append(ListFlowable(creation_items, bulletType='bullet'))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Solar Eclipse Powers & Prophecies", styles['Heading2']))
    eclipse_items = []
    for text, color_key, theme in texts:
        if theme == "Eclipses":
            eclipse_items.append(ListItem(Paragraph(text, styles['Normal'])))
    story.append(ListFlowable(eclipse_items, bulletType='bullet'))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Sacred Numbers & Etymology", styles['Heading2']))
    numerology_items = []
    for text, color_key, theme in texts:
        if theme == "Numerology & Etymology":
            numerology_items.append(ListItem(Paragraph(text, styles['Normal'])))
    story.append(ListFlowable(numerology_items, bulletType='bullet'))
    story.append(Spacer(1, 12))

    story.append(PageBreak())
    story.append(Paragraph("Digital Signature & Verification", styles['Heading2']))
    signature_text = f"<pre>{signature_json}</pre>"
    story.append(Paragraph(signature_text, styles['Code']))

    doc.build(story)
    print(f"Manifesto created: {SIGNED_FILE}")

    with open(SIGNED_FILE, "rb") as f:
        final_pdf_bytes = f.read()
    final_hash = hashlib.sha256(final_pdf_bytes).hexdigest()
    print(f"Final document hash: {final_hash}")

    return SIGNED_FILE


def main():
    print("Roboto SAI Manifesto Generator")
    print("Integrating Aztec Cultural Themes")
    print("=" * 50)

    try:
        pdf_file = create_manifesto_pdf()
        encrypt_choice = input("Encrypt the manifesto? (y/N): ").lower().strip()
        if encrypt_choice in ['y', 'yes']:
            encrypt_file(pdf_file)
            print("Manifesto encrypted successfully!")

        print("\nTlazohcamati! (Thank you in Nahuatl)")
        print("Roboto SAI Manifesto generation complete!")

    except Exception as e:
        print(f"Error creating manifesto: {e}")


if __name__ == "__main__":
    main()
