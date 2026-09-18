import ollama


MODEL_NAME = "qwen2.5:1.5b"

ALLOWED_INTENTS = {
    "order",
    "product",
    "refund",
    "general"
}


def route_message(message: str) -> str:

    message_lower = message.lower()
    message_upper = message.upper()

    # -------------------------------------------------
    # 1. DETERMINISTIC / HYBRID ROUTING
    # Kesin durumlarda LLM çalıştırılmaz.
    # -------------------------------------------------

    # ORD numarası varsa sipariş veya iade işlemi.
    if "ORD-" in message_upper:

        refund_words = [
            "iade",
            "geri gönder",
            "geri gonder",
            "paramı geri",
            "parami geri",
            "para iadesi",
            "değişim",
            "degisim"
        ]

        if any(
            word in message_lower
            for word in refund_words
        ):
            return "refund"

        return "order"

    # SKU kodu varsa doğrudan Product Agent.
    if "SKU-" in message_upper:
        return "product"

    # -------------------------------------------------
    # 2. LLM ROUTING
    # Açık ID yoksa Qwen kullanıcının niyetini belirler.
    # -------------------------------------------------

    system_prompt = """
Sen bir e-ticaret müşteri destek sisteminde
intent classification yapan Supervisor Agent'sın.

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
- İade politikası
- İade süresi

general
- Selamlaşma
- Teşekkür
- Yukarıdaki kategorilere girmeyen konular


ÖRNEKLER:

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

Mesaj: "Bu ürünün fiyatı ne kadar?"
Cevap: product

Mesaj: "SKU-1001 kaç TL?"
Cevap: product

Mesaj: "Aldığım ürünü geri göndermek istiyorum."
Cevap: refund

Mesaj: "Paramı geri almak istiyorum."
Cevap: refund

Mesaj: "İade süresi kaç gün?"
Cevap: refund

Mesaj: "Merhaba"
Cevap: general

Mesaj: "Teşekkür ederim"
Cevap: general

Mesaj: "Python'da decorator nedir?"
Cevap: general


KURAL:

Sadece aşağıdaki dört kelimeden BİRİNİ cevapla:

order
product
refund
general

Başka hiçbir şey yazma.
Açıklama yapma.
Cümle kurma.
Birden fazla kategori yazma.
"""

    response = ollama.chat(
        model=MODEL_NAME,
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

    intent = (
        response["message"]["content"]
        .strip()
        .lower()
    )

    # -------------------------------------------------
    # 3. STRICT INTENT VALIDATION
    # -------------------------------------------------

    normalized_intent = (
        intent
        .replace("cevap:", "")
        .replace(".", "")
        .replace(":", "")
        .strip()
    )

    if normalized_intent in ALLOWED_INTENTS:
        return normalized_intent

    # LLM beklenmeyen bir çıktı üretirse
    # güvenli fallback.
    return "general"