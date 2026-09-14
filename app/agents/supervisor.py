import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def route_message(message: str) -> str:
    response = client.responses.create(
        model="gpt-5.6",
        instructions="""
You are the supervisor of an e-commerce customer support system.

Classify the customer's message into exactly one category:

order
product
refund
general

Definitions:

order:
Questions about order status, shipping, delivery or tracking.

product:
Questions about products, stock, price, color or product information.

refund:
Questions about returns, exchanges or refunds.

general:
Anything that does not fit the categories above.

Return ONLY the category name.
""",
        input=message
    )

    intent = response.output_text.strip().lower()

    allowed_intents = {
        "order",
        "product",
        "refund",
        "general"
    }

    if intent not in allowed_intents:
        return "general"

    return intent