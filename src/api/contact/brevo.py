import html
import httpx

from src.core.config import settings
from src.core.exceptions import AppError
from src.core.logger import logger

# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENTACIÓN: versión mínima y funcional (sin estilos) de los 2 envíos.
# Es lo único necesario para mandar estos correos con la REST API de Brevo:
# POST https://api.brevo.com/v3/smtp/email
# Headers: "api-key: <BREVO_API_KEY>", "accept: application/json"
#
# 1) Correo al sitio (llega a BREVO_FROM_EMAIL). replyTo = quien escribió:
#
#   async def send_contact_email(reply_to_email, reply_to_name, reason, message):
#     payload = {
#       "sender": {"email": settings.BREVO_FROM_EMAIL, "name": settings.BREVO_FROM_NAME},
#       "to": [{"email": settings.BREVO_FROM_EMAIL, "name": settings.BREVO_FROM_NAME}],
#       "replyTo": {"email": reply_to_email, "name": reply_to_name},
#       "subject": f"[Contacto] {reason}",
#       "htmlContent": f"<p><strong>{reply_to_name}</strong> ({reply_to_email})</p><p>{message}</p>",
#     }
#
# 2) Correo de confirmación al remitente (llega a user_email):
#
#   async def send_confirmation_email(user_email, user_name):
#     payload = {
#       "sender": {"email": settings.BREVO_FROM_EMAIL, "name": settings.BREVO_FROM_NAME},
#       "to": [{"email": user_email, "name": user_name}],
#       "subject": "Recibimos tu mensaje - Game Guides",
#       "htmlContent": f"<p>Hola <strong>{user_name}</strong>,</p>"
#                      "<p>Recibimos tu mensaje y te responderemos a la brevedad.</p>"
#                      "<p>Gracias por escribirnos.</p>"
#                      "<p>El equipo de Game Guides</p>",
#     }
#
# En ambos casos, enviar con:
#   async with httpx.AsyncClient() as client:
#     response = await client.post(
#       BREVO_API_URL,
#       json=payload,
#       headers={"api-key": settings.BREVO_API_KEY, "accept": "application/json"},
#       timeout=15,
#     )
#   # response.status_code 201 == envío exitoso
# ─────────────────────────────────────────────────────────────────────────────

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"

# Brand palette
BRAND_PRIMARY = "#f97316"
BRAND_PRIMARY_DARK = "#ea580c"
BG_APP = "#13111c"
BG_CARD = "#1f1b2e"
BG_SECTION = "#2a2440"
BORDER = "#3a3354"
TEXT = "#eceaf3"
TEXT_MUTED = "#a49fc0"


def _email_template(body: str) -> str:
  return f"""<!DOCTYPE html>
<html lang="es">
  <head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
  <body style="margin:0;padding:0;background-color:{BG_APP};">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{BG_APP};padding:32px 16px;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background-color:{BG_CARD};border-radius:14px;overflow:hidden;border:1px solid {BORDER};">
            <tr>
              <td style="background-color:{BRAND_PRIMARY};padding:22px 28px;text-align:center;border-bottom:4px solid {BRAND_PRIMARY_DARK};">
                <span style="font-family:Georgia,serif;font-size:22px;font-weight:bold;color:#ffffff;letter-spacing:1px;">Game Guides</span>
              </td>
            </tr>
            <tr>
              <td style="padding:28px 28px 8px 28px;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:{TEXT};">
                {body}
              </td>
            </tr>
            <tr>
              <td style="padding:8px 28px 24px 28px;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.6;color:{TEXT_MUTED};border-top:1px solid {BORDER};">
                Este es un correo automático de Game Guides. No respondas a este mensaje.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""


def _info_block(label: str, value: str, last: bool = False) -> str:
  bottom = "border-bottom:1px solid " + BORDER if not last else ""
  return f"""
    <tr><td style="padding:7px 14px;background-color:{BG_SECTION};border-radius:8px 8px 0 0;font-size:11px;color:{BRAND_PRIMARY};text-transform:uppercase;letter-spacing:1px;font-weight:bold;">{label}</td></tr>
    <tr><td style="padding:10px 14px;background-color:{BG_CARD};{bottom}font-size:14px;color:{TEXT};">{value}</td></tr>
  """


async def _send_email(to_email: str, to_name: str, subject: str, html: str, reply_to: tuple[str, str] | None = None) -> None:
  payload = {
    "sender": {"email": settings.BREVO_FROM_EMAIL, "name": settings.BREVO_FROM_NAME},
    "to": [{"email": to_email, "name": to_name}],
    "subject": subject,
    "htmlContent": html,
  }

  if reply_to:
    payload["replyTo"] = {"email": reply_to[0], "name": reply_to[1]}

  async with httpx.AsyncClient() as client:
    response = await client.post(
      BREVO_API_URL,
      json=payload,
      headers={"api-key": settings.BREVO_API_KEY, "accept": "application/json"},
      timeout=15,
    )

  if response.status_code < 400:
    message_id = response.json().get("messageId")
    logger.info("Contact email sent", extra={"props": {"to": to_email, "subject": subject, "brevo_message_id": message_id}})
    return

  logger.error(
    "Brevo send failed",
    extra={"props": {"status": response.status_code, "body": response.text[:500]}},
  )
  _raise_brevo_error(response.status_code)


def _raise_brevo_error(status: int) -> None:
  if status in (401, 403):
    raise AppError(message="Brevo configuration error (invalid API key)", status_code=500)
  if status == 429:
    raise AppError(message="Brevo rate limit exceeded", status_code=429)
  raise AppError(message="Could not send contact email", status_code=502)


async def send_contact_email(reply_to_email: str, reply_to_name: str, reason: str, message: str) -> None:
  name = html.escape(reply_to_name)
  email = html.escape(reply_to_email)
  reason_label = html.escape(reason)
  body = html.escape(message).replace("\n", "<br>")

  content = f"""
    <h2 style="margin:0 0 18px 0;font-size:16px;font-weight:bold;color:#ffffff;">Nuevo mensaje de contacto</h2>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:14px;">
      {_info_block("Remitente", f"{name} &lt;<a href=\"mailto:{email}\" style=\"color:{BRAND_PRIMARY};text-decoration:none;\">{email}</a>&gt;")}
      {_info_block("Motivo", reason_label)}
      {_info_block("Mensaje", body, last=True)}
    </table>
    <p style="margin:16px 0 0 0;font-size:12px;color:{TEXT_MUTED};">Podes responderle directamente a {name} haciendo clic en "Responder".</p>
  """

  await _send_email(
    settings.BREVO_FROM_EMAIL,
    settings.BREVO_FROM_NAME,
    f"[Contacto] {reason}",
    _email_template(content),
    reply_to=(reply_to_email, reply_to_name),
  )


async def send_confirmation_email(user_email: str, user_name: str) -> None:
  name = html.escape(user_name)

  content = f"""
    <h2 style="margin:0 0 16px 0;font-size:16px;font-weight:bold;color:#ffffff;">¡Gracias por escribirnos, {name}!</h2>
    <p style="margin:0 0 12px 0;">Recibimos tu mensaje y el equipo te responderá a la brevedad.</p>
    <p style="margin:0 0 24px 0;">Mientras tanto, seguí explorando las guías de tus juegos favoritos.</p>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center">
          <a href="https://game-guides-astro.vercel.app/" style="display:inline-block;padding:13px 32px;background-color:{BRAND_PRIMARY};color:#ffffff;text-decoration:none;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;border-radius:10px;border-bottom:3px solid {BRAND_PRIMARY_DARK};">Visitar Game Guides</a>
        </td>
      </tr>
    </table>
  """

  await _send_email(
    user_email,
    user_name,
    "Recibimos tu mensaje - Game Guides",
    _email_template(content),
  )
