"""
Clipping de Medios — Bot de Telegram
Municipalidad de Córdoba

Enviá el .txt exportado de WhatsApp → el bot lo procesa con IA → te devuelve
el resumen por categoría listo para compartir.

Variables de entorno requeridas:
  TELEGRAM_BOT_TOKEN   — obtenelo con @BotFather en Telegram
  ANTHROPIC_API_KEY    — obtenela en console.anthropic.com
"""

import os, re, json, asyncio, tempfile, logging
from anthropic import Anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
client = Anthropic()

# ══════════════════════════════════════════════════════════
#  DATOS (palabras clave + mapeo de medios)
# ══════════════════════════════════════════════════════════

CATS = [
    "Ambiente","Ciudad Inteligente","Deporte y Cultura","Desarrollo Urbano",
    "Educación","Entrevista","General","Gobierno","Mensaje de oyente",
    "Participación","Políticas Sociales","Recursos Tributarios",
    "Salud","Seguridad","Transporte","Tribunal de Faltas"
]

# (keyword, [categorías])
KW_DATA = [
    ("llaryora",["General"]),("passerini",["General"]),("schiaretti",["General"]),
    ("intendente",["General"]),("gobernación",["General"]),("suoem",["General"]),
    ("corte",["Gobierno","Desarrollo Urbano"]),("tránsito",["Gobierno"]),
    ("sube",["Gobierno"]),("red bus",["Gobierno"]),("clausura",["Gobierno"]),
    ("hormaeche",["Gobierno"]),("semáforo",["Gobierno"]),("boleto gratuito",["Gobierno"]),
    ("metropolitano",["Gobierno"]),("transporte",["Gobierno","Transporte"]),
    ("inspector",["Gobierno"]),("horario extendido",["Gobierno"]),
    ("uber",["Gobierno","Transporte"]),("taxi",["Gobierno","Transporte"]),
    ("olor",["Ambiente"]),("contaminación",["Ambiente"]),("plaza",["Ambiente"]),
    ("ambiente",["Ambiente"]),("basural",["Ambiente"]),("pasto",["Ambiente"]),
    ("yuyos",["Ambiente"]),("surbac",["Ambiente"]),("sucia",["Ambiente"]),
    ("sucio",["Ambiente"]),("mugre",["Ambiente"]),("asco",["Ambiente"]),
    ("sarria",["Ambiente","Entrevista"]),("gabriel martin",["Ambiente","Entrevista"]),
    ("mosquito",["Salud","Ambiente"]),("dengue",["Salud","Ambiente"]),
    ("dispensario",["Salud"]),("hospital",["Salud"]),("vacuna",["Salud"]),
    ("medico",["Salud"]),("medica",["Salud"]),("medicina",["Salud"]),
    ("fentanilo",["Salud"]),("sanatorio",["Salud"]),("residente",["Salud"]),
    ("enfermero",["Salud"]),("enfermera",["Salud"]),("testeo",["Salud"]),
    ("centros de salud",["Salud"]),("paciente",["Salud"]),("sintomas",["Salud"]),
    ("anmat",["Salud"]),("aleksandroff",["Salud","Entrevista"]),
    ("bache",["Desarrollo Urbano"]),("obras",["Desarrollo Urbano"]),
    ("peralta",["Desarrollo Urbano","Entrevista"]),
    ("presupuesto participativo",["Participación"]),
    ("juntas de participacion",["Participación"]),("cpc",["Participación"]),
    ("centro operativo",["Participación"]),("centros educativos",["Participación"]),
    ("servidores urbanos",["Participación"]),("grupo fem",["Participación"]),
    ("trámites",["Participación"]),("viola",["Participación","Entrevista"]),
    ("tasas",["Recursos Tributarios"]),("impuestos",["Recursos Tributarios"]),
    ("instituto",["Deporte y Cultura"]),("talleres",["Deporte y Cultura"]),
    ("belgrano",["Deporte y Cultura"]),("racing",["Deporte y Cultura"]),
    ("pichi campana",["Deporte y Cultura"]),("kempes",["Deporte y Cultura"]),
    ("fútbol",["Deporte y Cultura"]),("teatro",["Deporte y Cultura"]),
    ("basquet",["Deporte y Cultura"]),("centro vecinal",["Deporte y Cultura"]),
    ("centros vecinales",["Deporte y Cultura"]),("cultura",["Deporte y Cultura"]),
    ("feria del libro",["Deporte y Cultura"]),("coro",["Deporte y Cultura"]),
    ("campana",["Deporte y Cultura","Entrevista"]),
    ("tech",["Ciudad Inteligente"]),("cordoba acelera",["Ciudad Inteligente"]),
    ("emprendedor",["Ciudad Inteligente"]),("gei",["Ciudad Inteligente","Entrevista"]),
    ("clases",["Educación"]),("la terza",["Educación","Entrevista"]),
    ("juan manuel araoz",["Tribunal de Faltas","Entrevista"]),
    ("pretto",["General","Entrevista"]),("lorenzatti",["General","Entrevista"]),
    ("rodrigo fernandez",["Gobierno","Entrevista"]),
    ("entrevista",["Entrevista"]),("con nosotros",["Entrevista"]),
    ("hablamos con",["Entrevista"]),
    ("robo",["Seguridad"]),("detenidos",["Seguridad"]),("inseguridad",["Seguridad"]),
    ("arrestados",["Seguridad"]),("investigado",["Seguridad"]),("crimen",["Seguridad"]),
    ("muerte",["Seguridad"]),("policia",["Seguridad"]),("mató",["Seguridad"]),
    ("femicidio",["Seguridad"]),("arresto",["Seguridad"]),("ilegal",["Seguridad"]),
    ("narco",["Seguridad"]),("tiroteo",["Seguridad"]),("asesino",["Seguridad"]),
    ("violencia",["Seguridad"]),
    ("oyente",["Mensaje de oyente"]),("te escribo",["Mensaje de oyente"]),
    ("comerciante",["Mensaje de oyente"]),
    ("lgbt",["Políticas Sociales"]),("la cava",["Políticas Sociales","Entrevista"]),
]

# raw.lower() -> {"display": str, "tipo": "Medio"|"Programa"}
MEDIA_MAP = {k.lower(): {"display": d, "tipo": t} for k, d, t in [
    ("radio mitre","Mitre","Medio"),("mitrecordoba","Mitre","Medio"),("mitre","Mitre","Medio"),
    ("aptt","Aquí Petete","Programa"),("aquipetete","Aquí Petete","Programa"),
    ("pop","Radio Popular","Medio"),("vv","Vamos Viendo","Programa"),
    ("lv3","Cadena 3","Medio"),("cadena3","Cadena 3","Medio"),
    ("lv2","LV 2","Medio"),("am700","AM 700","Medio"),
    ("radioinf","Radio Informe 3","Programa"),("radioinforme 3","Radio Informe 3","Programa"),
    ("continental","Continental","Medio"),
    ("aenot","Alassia es Noticia","Programa"),("aen","Alassia es Noticia","Programa"),
    ("alassiaesnoticia","Alassia es Noticia","Programa"),
    ("gefinforma","Ge Informa","Medio"),("geninforma","Gen Informa","Programa"),
    ("hoydia","Hoy Día Córdoba","Medio"),
    ("cba24n","CBA 24 Noticias","Medio"),
    ("el doce","Canal 12","Medio"),("eldoce","El Doce TV","Medio"),("c12","Canal 12","Medio"),
    ("noticierodoce","Noticiero Doce","Programa"),("ndce","Noticiero Doce","Programa"),
    ("tnd","TeleNoche Doce","Programa"),
    ("telefe","Telefe","Medio"),("tnc","Telefe Noticias","Programa"),
    ("telefeNoticias","Telefe Noticias","Programa"),("tfn","Telefe Noticias 1ra Ed","Programa"),
    ("lmz","La mañana con Zuliani","Programa"),("lamananaconzuliani","La mañana con Zuliani","Programa"),
    ("acba","Arriba Córdoba","Programa"),
    ("canalc","Canal C","Medio"),("cc","Canal C","Medio"),("ccordoba","C Córdoba","Medio"),
    ("lvev","La Voz en Vivo","Programa"),
    ("sj","Siempre Juntos","Programa"),("siemprejuntos","Siempre Juntos","Programa"),
    ("suquia","Radio Suquía","Medio"),("suq","Radio Suquía","Medio"),
    ("bdc","Bien de Córdoba","Programa"),
    ("mem","Mediodía en Mitre","Programa"),
    ("sdl","Show del Lagarto","Programa"),("elshowdellagarto","Show del Lagarto","Programa"),
    ("siestaanimal","Siesta Animal","Programa"),("saml","Siesta Animal","Programa"),
    ("idayvuelta","Ida y Vuelta","Programa"),("iyv","Ida y Vuelta","Programa"),
    ("mt","Mientras Tanto","Programa"),("c10","Canal 10","Medio"),
    ("vvlr","Viva la Radio","Programa"),
    ("informadosalregreso","Informados al Regreso","Programa"),("iar","Informados al Regreso","Programa"),
    ("bm","Buen Mediodía","Programa"),
    ("puntalvillamaria","Puntal Villa Maria","Medio"),("puntal","Puntal","Medio"),
    ("diarioalfil","Diario Alfil","Medio"),("lavoz","La Voz","Medio"),
    ("lmdiario","La Nueva Mañana","Medio"),
    ("comercioyjusticia","Comercio y Justicia","Medio"),
    ("jornadapolitica","Jornada Política","Medio"),("jp","Jornada Política","Programa"),
    ("sdp","Secretos del Poder","Programa"),("an","Ahora Noticias","Programa"),
    ("fyc","Fuerte y Claro","Programa"),("mqh","Mirá quién habla","Programa"),
    ("cn","Córdoba Noticias","Programa"),("ecdv","El Club del Vecino","Programa"),
    ("diariocordoba","Diario Córdoba","Medio"),
    ("politicacordobaverdad","Política Córdoba Verdad","Medio"),
]}

# ══════════════════════════════════════════════════════════
#  PARSERS
# ══════════════════════════════════════════════════════════

USTRIP   = re.compile(r'^[\u200e\u200f\u202f\ufeff\u200b]+')
URL_RE   = re.compile(r'https?://[^\s\n\r]+')
SKIP_RE  = re.compile(r'cifrado|añadió|quitó|imagen omitida|documento omitido|se editó este mensaje', re.I)
TIME_RE  = re.compile(r'\d{2}:\d{2}(:\d{2})?')


def parse_wa(text: str) -> list:
    msgs, cur = [], None
    for raw in text.split('\n'):
        line = USTRIP.sub('', raw).rstrip('\r')
        m = (re.match(r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+?):\s*(.*)$', line)
             or re.match(r'^(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2})\s*[-–]\s*(.+?):\s*(.*)$', line))
        if m:
            if cur: msgs.append(cur)
            cur = {'date': m.group(1), 'time': m.group(2)[:5],
                   'sender': m.group(3).strip(), 'content': m.group(4)}
        elif cur and line.strip():
            cur['content'] += '\n' + line
    if cur:
        msgs.append(cur)
    return msgs


def is_bot(sender: str) -> bool:
    s = sender.lower()
    return 'media monitoring' in s or 'cvamedios' in s


def lookup(token: str):
    return MEDIA_MAP.get(token.lower().strip())


def get_url(text: str):
    m = URL_RE.search(text)
    return m.group(0).rstrip(')]\'"') if m else None


def domain_label(url: str) -> str:
    try:
        from urllib.parse import urlparse
        host = urlparse(url).hostname or ''
        host = host.lstrip('www.')
        parts = host.split('.')
        for key in [host, '.'.join(parts[:-1]), parts[0]]:
            e = lookup(key)
            if e:
                return e['display']
        return parts[0].replace('-', ' ').title()
    except Exception:
        return ''


def parse_mm(content: str) -> dict:
    ia_split = re.split(r'\nIA\.TXT:\s*', content, maxsplit=1)
    ia_txt   = ia_split[1].strip() if len(ia_split) > 1 else None
    main     = ia_split[0]

    url       = get_url(main)
    text_part = main[:main.index(url)].strip() if url else main.strip()

    lines      = text_part.split('\n')
    first_line = lines[0] if lines else ''
    rest_lines = [l for l in lines[1:]
                  if l.strip() and not re.match(r'^\d{2}:\d{2}', l.strip())]
    rest       = '\n'.join(rest_lines)

    segs    = re.split(r'\.\s+', first_line)
    medio   = programa = ''
    desc_p  = []
    in_desc = False

    for seg in segs:
        seg = seg.strip()
        if not seg:
            continue
        if in_desc:
            desc_p.append(seg)
            continue
        if re.match(r'^A\s+V\w*', seg, re.I):
            in_desc = True
            rest_avo = re.sub(r'^A\s+V\w*\.?\s*', '', seg, flags=re.I).strip()
            if rest_avo:
                desc_p.append(rest_avo)
            continue
        entry = lookup(seg)
        if entry:
            if entry['tipo'] == 'Medio' and not medio:
                medio = entry['display']
                continue
            if entry['tipo'] == 'Programa' and not programa:
                programa = entry['display']
                continue
        if medio and programa:
            in_desc = True
        desc_p.append(seg)

    desc = '. '.join(desc_p)
    if rest:
        desc = (desc + '\n' + rest).strip()
    desc = TIME_RE.sub('', desc).strip()

    return {'medio': medio, 'programa': programa, 'url': url, 'desc': desc, 'ia_txt': ia_txt}


def parse_cva(content: str) -> dict:
    url      = get_url(content)
    text     = (content.replace(url, '') if url else content).strip()
    tokens   = re.split(r'[\s.]+', text)
    medio    = programa = ''
    used     = 0

    for i, tok in enumerate(tokens[:4]):
        entry = lookup(tok)
        if entry:
            if entry['tipo'] == 'Medio' and not medio:
                medio = entry['display']
                used  = i + 1
            elif entry['tipo'] == 'Programa' and not programa:
                programa = entry['display']
                used     = i + 1
        elif i > 0 and not medio and not programa:
            break
        elif medio and programa:
            break

    desc = ' '.join(tokens[used:]).rstrip('0123456789. ').strip()
    return {'medio': medio, 'programa': programa, 'url': url, 'desc': desc, 'ia_txt': None}


def score_local(text: str) -> dict:
    lo     = text.lower()
    scores = {}
    for kw, cats in KW_DATA:
        if kw in lo:
            for cat in cats:
                if cat in CATS:
                    scores[cat] = scores.get(cat, 0) + 1
    return scores


def best_cats(scores: dict) -> list:
    s = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [c for c, _ in s] if s else ['General']


def build_items(text: str) -> list:
    msgs  = parse_wa(text)
    items = []
    for msg in msgs:
        if not is_bot(msg['sender']):
            continue
        c = msg['content'].replace('\u200e', '').strip()
        if SKIP_RE.search(c) or len(c) < 5:
            continue

        is_mm  = 'media monitoring' in msg['sender'].lower()
        parsed = parse_mm(c) if is_mm else parse_cva(c)

        medio = parsed['medio']
        if not is_mm and not medio and parsed['url']:
            medio = domain_label(parsed['url'])

        scores = score_local(c + ' ' + (parsed['desc'] or ''))
        cats   = best_cats(scores)

        items.append({
            'n':        len(items) + 1,
            'date':     msg['date'],
            'time':     msg['time'],
            'tipo':     'audio' if is_mm else 'web',
            'medio':    medio,
            'programa': parsed['programa'],
            'url':      parsed['url'],
            'desc':     parsed['desc'],
            'ia_txt':   parsed['ia_txt'],
            'raw':      c,
            'title':    '',
            'cats':     cats,
        })
    return items


# ══════════════════════════════════════════════════════════
#  IA: generar título desde descripción
# ══════════════════════════════════════════════════════════

def ai_title(item: dict) -> str:
    """Genera un título corto para una noticia usando la API de Anthropic."""
    content = (
        f"Descripción: {item['desc']}\n\nTranscripción:\n{item['ia_txt'][:2000]}"
        if item['ia_txt']
        else (item['desc'] or item['raw'])[:2000]
    )
    try:
        resp = client.messages.create(
            model='claude-haiku-4-5-20251001',   # modelo rápido y económico
            max_tokens=80,
            system=(
                "Generá un título periodístico muy conciso (máx 10 palabras) "
                "para este recorte de medios de Córdoba, Argentina. "
                "Solo el título, sin comillas ni explicaciones."
            ),
            messages=[{'role': 'user', 'content': content}]
        )
        return resp.content[0].text.strip().strip('"')
    except Exception as e:
        log.warning(f"ai_title error: {e}")
        return item['desc'][:70] if item['desc'] else '(sin título)'


# ══════════════════════════════════════════════════════════
#  FORMATEADOR DE MENSAJES
# ══════════════════════════════════════════════════════════

def format_message(items: list, cat_label: str) -> str:
    lines = []
    for n in items:
        title = n['title'] or n['desc'][:70] or '(sin título)'
        src   = ' / '.join(p for p in [n['medio'], n['programa']] if p) or 'Sin fuente'
        link  = f"\n🔗 {n['url']}" if n['url'] else ''
        lines.append(f"→ *{title}*\n→ {n['date']} {n['time']}  {src}{link}")

    header = f"📍 RESUMEN DE \"{cat_label.upper()}\""
    return header + '\n\n' + '\n\n'.join(lines)


async def send_long(bot, chat_id: int, text: str):
    """Envía un mensaje largo dividiéndolo en chunks si supera el límite de Telegram."""
    LIMIT = 4000
    if len(text) <= LIMIT:
        await bot.send_message(chat_id=chat_id, text=text,
                               parse_mode='Markdown', disable_web_page_preview=True)
        return

    parts  = text.split('\n\n')
    chunk  = ''
    chunks = []
    for part in parts:
        if len(chunk) + len(part) + 2 > LIMIT:
            if chunk:
                chunks.append(chunk)
            chunk = part
        else:
            chunk = (chunk + '\n\n' + part).strip()
    if chunk:
        chunks.append(chunk)

    for i, c in enumerate(chunks):
        if i > 0:
            await asyncio.sleep(0.4)
        await bot.send_message(chat_id=chat_id, text=c,
                               parse_mode='Markdown', disable_web_page_preview=True)


# ══════════════════════════════════════════════════════════
#  SESIONES EN MEMORIA
# ══════════════════════════════════════════════════════════
# user_id -> {"items": [...], "active_cats": [...]}
SESSIONS: dict = {}


# ══════════════════════════════════════════════════════════
#  HANDLERS DE TELEGRAM
# ══════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Clipping de Medios — Municipalidad de Córdoba*\n\n"
        "Enviame el archivo `.txt` exportado de WhatsApp con los recortes.\n\n"
        "El bot va a:\n"
        "1️⃣  Detectar y clasificar todas las noticias\n"
        "2️⃣  Mostrarte botones por categoría\n"
        "3️⃣  Generar el mensaje listo para compartir\n\n"
        "¡Mandá el archivo cuando quieras!",
        parse_mode='Markdown'
    )


async def handle_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith('.txt'):
        await update.message.reply_text(
            "⚠️ Por favor enviá un archivo `.txt`.\n"
            "Exportalo desde WhatsApp → ··· → Más → Exportar chat → Sin archivos."
        )
        return

    uid = update.effective_user.id
    status = await update.message.reply_text("⏳ Leyendo el archivo...")

    # Descargar y parsear
    try:
        tg_file = await ctx.bot.get_file(doc.file_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            await tg_file.download_to_drive(tmp.name)
            with open(tmp.name, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
    except Exception as e:
        await status.edit_text(f"❌ Error al leer el archivo: {e}")
        return

    items = build_items(text)

    if not items:
        await status.edit_text(
            "❌ No encontré noticias.\n"
            "Verificá que sea un chat exportado de WhatsApp con mensajes de "
            "*Media Monitoring* o *CVAMedios IA Monitoreo*.",
            parse_mode='Markdown'
        )
        return

    # Contar por categoría
    cat_counts: dict = {}
    for item in items:
        for cat in item['cats']:
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
    active_cats = [c for c in CATS if c in cat_counts]

    SESSIONS[uid] = {'items': items, 'active_cats': active_cats}

    # Construir teclado inline
    keyboard = [[InlineKeyboardButton(
        f"📋 Todas ({len(items)})", callback_data="cat:__all__"
    )]]
    row: list = []
    for cat in active_cats:
        btn = InlineKeyboardButton(
            f"{cat} ({cat_counts[cat]})",
            callback_data=f"cat:{cat}"
        )
        row.append(btn)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Botón para generar títulos con IA
    keyboard.append([InlineKeyboardButton(
        "✨ Generar títulos con IA (todas)", callback_data="ai:__all__"
    )])

    await status.edit_text(
        f"✅ Encontré *{len(items)} noticias* en *{len(active_cats)} categorías*.\n\n"
        f"Tocá una categoría para generar el mensaje:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id

    if uid not in SESSIONS:
        await query.edit_message_text(
            "⚠️ La sesión expiró. Enviá el archivo `.txt` nuevamente.",
            parse_mode='Markdown'
        )
        return

    data    = query.data
    session = SESSIONS[uid]
    items   = session['items']

    # ── Generar mensaje por categoría ──
    if data.startswith('cat:'):
        cat = data[4:]
        if cat == '__all__':
            filtered  = items
            cat_label = 'NOTICIAS'
        else:
            filtered  = [n for n in items if cat in n['cats']]
            cat_label = cat

        if not filtered:
            await query.answer("No hay noticias en esa categoría.", show_alert=True)
            return

        await query.edit_message_text(
            f"⏳ Armando resumen de *{cat_label}* ({len(filtered)} noticias)…",
            parse_mode='Markdown'
        )

        msg_text = format_message(filtered, cat_label)
        await send_long(ctx.bot, update.effective_chat.id, msg_text)

        await query.edit_message_text(
            f"✅ Resumen de *{cat_label}* enviado — {len(filtered)} noticias.\n\n"
            "Podés pedir otra categoría o enviar un nuevo archivo.",
            parse_mode='Markdown'
        )

    # ── Generar títulos con IA ──
    elif data.startswith('ai:'):
        cat = data[3:]
        if cat == '__all__':
            to_process = items
            cat_label  = 'NOTICIAS'
        else:
            to_process = [n for n in items if cat in n['cats']]
            cat_label  = cat

        total = len(to_process)
        await query.edit_message_text(
            f"✨ Generando títulos con IA para *{cat_label}* ({total} noticias)…\n"
            f"Esto puede tardar ~{total * 2} segundos.",
            parse_mode='Markdown'
        )

        for i, item in enumerate(to_process, 1):
            if not item['title']:
                item['title'] = ai_title(item)
            if i % 5 == 0:
                try:
                    await query.edit_message_text(
                        f"✨ Procesando {i}/{total}…",
                        parse_mode='Markdown'
                    )
                except Exception:
                    pass
            await asyncio.sleep(0.3)   # evitar rate-limit

        msg_text = format_message(to_process, cat_label)
        await send_long(ctx.bot, update.effective_chat.id, msg_text)

        await query.edit_message_text(
            f"✅ Listo con IA — *{cat_label}*, {total} noticias.",
            parse_mode='Markdown'
        )


async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Cualquier mensaje de texto recibe un recordatorio."""
    await update.message.reply_text(
        "Enviame el archivo `.txt` exportado de WhatsApp para empezar.",
        parse_mode='Markdown'
    )


# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("Falta la variable de entorno TELEGRAM_BOT_TOKEN")

    if not os.environ.get('ANTHROPIC_API_KEY'):
        log.warning("ANTHROPIC_API_KEY no encontrada — la función IA estará deshabilitada.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', cmd_start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    log.info("Bot iniciado. Esperando mensajes...")
    app.run_polling(drop_pending_updates=True)


if __name__ == '__main__':
    main()
