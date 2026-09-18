import ollama


ALLOWED_INTENTS = {"order", "product", "refund", "general"}


def route_message(message: str) -> str:

    # -------------------------------------------------
    # 1. HYBRID ROUTING
    # Kesin durumlarda LLM'i boşuna çalıştırmıyoruz.
    # -------------------------------------------------

    message_lower = message.lower()
    message_upper = message.upper()

    # ORD numarası varsa sipariş veya iade işlemi.
    if "ORD-" in message_upper:

        refund_words = [
            "iade",
            "geri gönder",
            "geri gonder",
            "paramı geri",
            "parami geri"
        ]

        if any(word in message_lower for word in refund_words):
            return "refund"

        return "order"

    # SKU kodu varsa doğrudan Product Agent.
    if "SKU-" in message_upper:
        return "product"

    # -------------------------------------------------
    # 2. LLM ROUTING
    # Mesaj açık bir ID içermiyorsa Qwen niyeti belirler.
    # -------------------------------------------------

    system_prompt = """
Sen bir e-ticaret müşteri destek sisteminde intent classification yapan
Supervisor Agent'sın.

Görevin kullanıcının ASIL NİYETİNİ belirlemektir.

KATEGORİLER:

order
- Sipariş nerede?
- Kargo ve teslimat
- Teslimat gecikmesi
- Kargo takip
- Satın alınan bir şeyin henüz ulaşmaması

product
- Ürün fiyatı
- Ürün stoğu
- Ürün özellikleri
- Ürün kullanımı
- Renk, boyut veya ürün hakkında bilgi

refund
- İade etmek istemek
- Para iadesi
- Ürün değişimi
- Satın alınan ürünü geri göndermek

general
- Selamlaşma
- Teşekkür
- Yukarıdaki kategorilere girmeyen konular


ÖNEMLİ ÖRNEKLER:

Mesaj: "Siparişim nerede?"
Cevap: order

Mesaj: "Üç gündür aldığım şey hâlâ gelmedi."
Cevap: order

Mesaj: "Geçen hafta aldım ama hâlâ elime ulaşmadı."
Cevap: order

Mesaj: "Kargom ne zaman gelir?"
Cevap: order

Mesaj: "Siparişler kaç günde kargoya veriliyor?"
Cevap: order

Mesaj: "Bu serum stokta var mı?"
Cevap: product

Mesaj: "C vitamini serumunu nasıl kullanmalıyım?"
Cevap: product

Mesaj: "SKU-1001 kaç TL?"
Cevap: product

Mesaj: "Aldığım ürünü geri göndermek istiyorum."
Cevap: refund

Mesaj: "Paramı geri almak istiyorum."
Cevap: refund

Mesaj: "İade süresi kaç gün?"
Cevap: refund

Mesaj: "Merhaba, nasılsınız?"
Cevap: general

Mesaj: "Python'da decorator nedir?"
Cevap: general


KURAL:

Sadece aşağıdaki dört kelimeden BİRİNİ cevapla:

order
product
refund
general

Açıklama yapma.
Cümle kurma.
Noktalama işareti kullanma.
"""

    response = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        options={
            "temperature": 0
        }
    )

    intent = response["message"]["content"].strip().lower()

    # Küçük modeller bazen "order." veya
    # "Cevap: order" gibi çıktı verebilir.
    for allowed_intent in ALLOWED_INTENTS:
        if allowed_intent in intent:
            return allowed_intent

    # Tanınmayan cevaplarda güvenli fallback.
    return "general"