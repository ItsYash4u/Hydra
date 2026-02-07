from __future__ import annotations

from typing import Iterable

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def _normalize_recipients(to_emails: str | Iterable[str]) -> list[str]:
    if isinstance(to_emails, str):
        return [to_emails]
    return [email for email in to_emails if email]


def send_templated_email(
    *,
    subject: str,
    to_emails: str | Iterable[str],
    template_name: str,
    context: dict,
    from_email: str | None = None,
    reply_to: Iterable[str] | None = None,
    text_template_name: str | None = None,
) -> None:
    recipients = _normalize_recipients(to_emails)
    if not recipients:
        return

    html_body = render_to_string(template_name, context)
    if text_template_name:
        text_body = render_to_string(text_template_name, context)
    else:
        text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=recipients,
        reply_to=list(reply_to) if reply_to else None,
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)
