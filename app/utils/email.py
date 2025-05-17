import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

def send_order_confirmation_email(
    recipient_email: str,
    customer_name: str,
    order_id: int,
    items: list,
    total_price: float
):
    # Email content
    subject = f"Order Confirmation - Order #{order_id}"
    items_text = "".join(
        [f"\n\t- {item['name']}: {item['quantity']} x ${item['price']:.2f}" for item in items]
    )
    body = f"""
    Dear {customer_name},

    Thank you for your order! Here are the details:

    Order ID: {order_id}
    Items:{items_text}
    Total Price: ${total_price:.2f}

    We will notify you once your order is shipped.

    Best regards,
    Auto Parts Shop
    """

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_SENDER
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        with smtplib.SMTP(settings.EMAIL_SERVER, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise
