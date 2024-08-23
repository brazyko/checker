def format_receipt_text(receipt, char_limit):
    lines = []
    lines.append("      ФОП Джонсонюк Борис       ")
    lines.append("=" * char_limit)

    for product in receipt.products:
        quantity_price = f"{product['quantity']} x {product['price']}"
        total_price = f"{product['total']:.2f}"
        product_name = product["name"]

        lines.append(f"{quantity_price:<15}{total_price:>{char_limit - 15}}")
        if len(product_name) > char_limit:
            lines.extend(split_text_into_lines(product_name, char_limit))
        else:
            lines.append(f"{product_name:<{char_limit}}")

    lines.append("=" * char_limit)
    lines.append(f"СУМА{receipt.total:>{char_limit - 4}.2f}")
    lines.append(f"{receipt.payment_type}{receipt.payment_amount:>{char_limit - 7}.2f}")
    lines.append(f"Решта{receipt.rest:>{char_limit - 5}.2f}")
    lines.append(f"        {receipt.created_at.strftime('%d.%m.%Y %H:%M')}        ")
    lines.append("      Дякуємо за покупку!       ")

    return "\n".join(lines)


def split_text_into_lines(text, char_limit):
    return [text[i: i + char_limit] for i in range(0, len(text), char_limit)]
