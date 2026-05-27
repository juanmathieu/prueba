"""
Clipping de Medios — Bot de Telegram v2
Municipalidad de Córdoba
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
#  DATOS
# ══════════════════════════════════════════════════════════

CATS = [
    "Ambiente","Ciudad Inteligente","Deporte y Cultura","Desarrollo Urbano",
    "Educación","Entrevista","General","Gobierno","Mensaje de oyente",
    "Participación","Políticas Sociales","Recursos Tributarios",
    "Salud","Seguridad","Transporte","Tribunal de Faltas"
]

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

MEDIA_MAP = {k.lower(): {"display": d, "tipo": t} for k, d, t in [
    ("radio mitre","Mitre","Medio"),("mitrecordoba","Mitre","Medio"),("mitre","Mitre","Medio"),
    ("aptt","Aquí Petete","Programa"),("aquipetete","Aquí Petete","Programa"),
    ("pop","Radio Popular","Medio"),("vv","Vamos Viendo","Programa"),
    ("lv3","Cadena 3","Medio"),("cadena3","Cadena 3","Medio"),
    ("lv2","LV 2","Medio"),("am700","AM 700","Medio"),
    ("radioinf","Radio Informe 3","Programa"),
    ("continental","Continental","Medio"),
    ("aenot","Alassia es Noticia","Programa"),("aen","Alassia es Noticia","Programa"),
    ("alassiaesnoticia","Alassia es Noticia","Programa"),
    ("gefinforma","Ge Informa","Medio"),
    ("hoydia","Hoy Día Córdoba","Medio"),
    ("cba24n","CBA 24 Noticias","Medio"),
    ("el doce","Canal 12","Medio"),("eldoce","El Doce TV","Medio"),("c12","Canal 12","Medio"),
    ("noticierodoce","Noticiero Doce","Programa"),("ndce","Noticiero Doce","Programa"),
    ("tnd","TeleNoche Doce","Programa"),
    ("telefe","Telefe","Medio"),("tnc","Telefe Noticias","Programa"),
    ("tfn","Telefe Noticias 1ra Ed","Programa"),
    ("lmz","La mañana con Zuliani","Programa"),
    ("acba","Arriba Córdoba","Programa"),
    ("canalc","Canal C","Medio"),("cc","Canal C","Medio"),("ccordoba","C Córdoba","Medio"),
    ("lvev","La Voz en Vivo","Programa"),
    ("sj","Siempre Juntos","Programa"),("siemprejuntos","Siempre Juntos","Programa"),
    ("suquia","Radio Suquía","Medio"),("suq","Radio Suquía","Medio"),
    ("bdc","Bien de Córdoba","Programa"),
    ("mem","Mediodía en Mitre","Programa"),
    ("sdl","Show del Lagarto","Programa"),
    ("siestaanimal","Siesta Animal","Programa"),("saml","Siesta Animal","Programa"),
    ("idayvuelta","Ida y Vuelta","Programa"),("iyv","Ida y Vuelta","Programa"),
    ("mt","Mientras Tanto","Programa"),("c10","Canal 10","Medio"),
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
]}

# ══════════════════════════════════════════════════════════
#  PARSERS  (misma lógica que el HTML, con fix de unicode)
# ══════════════════════════════════════════════════════════

USTRIP  = re.compile(r'^[\u200e\u200f\u202f\ufeff\u200b]+')
URL_RE  = re.compile(r'https?://[^\s\n\r]+')
SKIP_RE = re.compile(
    r'cifrado|añadió|quitó|imagen omitida|documento omitido|se editó este mensaje',
    re.I
)

def parse_wa(text):
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
    if cur: msgs.append(cur)
    return msgs

def is_bot(s):
    sl = s.lower()
    return 'media monitoring' in sl or 'cvamedios' in sl

def lookup(tok):
    return MEDIA_MAP.get(tok.lower().strip())

def get_url(text):
    m = URL_RE.search(text)
    return m.group(0).rstrip(')]\'"') if m else None

def domain_label(url):
    try:
        from urllib.parse import urlparse
        host = urlparse(url).hostname.lstrip('www.')
        parts = host.split('.')
        for key in [host, '.'.join(parts[:-1]), parts[0]]:
            e = lookup(key)
            if e: return e['display']
        return parts[0].replace('-', ' ').title()
    except Exception:
        return ''

def parse_mm(content):
    ia_split = re.split(r'\nIA\.TXT:\s*', content, maxsplit=1)
    ia_txt   = ia_split[1].strip() if len(ia_split) > 1 else None
    main     = ia_split[0]
    url      = get_url(main)
    text_part = main[:main.index(url)].strip() if url else main.strip()

    lines      = text_part.split('\n')
    first_line = lines[0] if lines else ''
    rest       = '\n'.join(l for l in lines[1:]
                           if l.strip() and not re.match(r'^\d{2}:\d{2}', l.strip()))

    segs = re.split(r'\.\s+', first_line)
    medio = programa = ''
    desc_p = []
    in_desc = False

    for seg in segs:
        seg = seg.strip()
        if not seg: continue
        if in_desc: desc_p.append(seg); continue
        if re.match(r'^A\s+V\w*', seg, re.I):
            in_desc = True
            avo = re.sub(r'^A\s+V\w*\.?\s*', '', seg, flags=re.I).strip()
            if avo: desc_p.append(avo)
            continue
        entry = lookup(seg)
        if entry:
            if entry['tipo'] == 'Medio' and not medio:   medio    = entry['display']; continue
            if entry['tipo'] == 'Programa' and not programa: programa = entry['display']; continue
        if medio and programa: in_desc = True
        desc_p.append(seg)

    desc = '. '.join(desc_p)
    if rest: desc = (desc + '\n' + rest).strip()
    desc = re.sub(r'\d{2}:\d{2}(:\d{2})?', '', desc).replace('(-)', '').replace('(=)', '').strip()
    return {'medio': medio, 'programa': programa, 'url': url, 'desc': desc, 'ia_txt': ia_txt}

def parse_cva(content):
    url    = get_url(content)
    text   = (content.replace(url, '') if url else content).strip()
    tokens = re.split(r'[\s.]+', text)
    medio = programa = ''
    used = 0
    for i, tok in enumerate(tokens[:4]):
        entry = lookup(tok)
        if entry:
            if entry['tipo'] == 'Medio' and not medio:      medio    = entry['display']; used = i+1
            elif entry['tipo'] == 'Programa' and not programa: programa = entry['display']; used = i+1
        elif i > 0 and not medio and not programa: break
        elif medio and programa: break
    desc = ' '.join(tokens[used:]).rstrip('0123456789. ').strip()
    return {'medio': medio, 'programa': programa, 'url': url, 'desc': desc, 'ia_txt': None}

def score_local(text):
    lo, sc = text.lower(), {}
    for kw, cats in KW_DATA:
        if kw in lo:
            for cat in cats:
                if cat in CATS: sc[cat] = sc.get(cat, 0) + 1
    return sc

def best_cats(sc):
    s = sorted(sc.items(), key=lambda x: x[1], reverse=True)
    return [c for c, _ in s] if s else ['General']

def build_items(text):
    msgs, items = parse_wa(text), []
    for msg in msgs:
        if not is_bot(msg['sender']): continue
        c = msg['content'].replace('\u200e', '').strip()
        if SKIP_RE.search(c) or len(c) < 5: continue
        is_mm  = 'media monitoring' in msg['sender'].lower()
        parsed = parse_mm(c) if is_mm else parse_cva(c)
        medio  = parsed['medio']
        if not is_mm and not medio and parsed['url']:
            medio = domain_label(parsed['url'])
        sc   = score_local(c + ' ' + (parsed['desc'] or ''))
        cats = best_cats(sc)
        items.append({
            'date': msg['date'], 'time': msg['time'],
            'medio': medio, 'programa': parsed['programa'],
            'url': parsed['url'], 'desc': parsed['desc'],
            'ia_txt': parsed['ia_txt'],
            'title': '',
            'cats': cats,
        })
    return items

# ══════════════════════════════════════════════════════════
#  IA
# ══════════════════════════════════════════════════════════

def ai_title(item):
    content = (
        f"Descripción: {item['desc']}\n\nTranscripción:\n{item['ia_txt'][:2000]}"
        if item['ia_txt'] else (item['desc'] or '')[:2000]
    )
    if not content.strip():
        return item['url'] or '(sin título)'
    try:
        resp = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=80,
            system=(
                "Generá un título periodístico conciso (máx 10 palabras) "
                "para este recorte de medios de Córdoba, Argentina. "
                "Solo el título, sin comillas ni explicaciones."
            ),
            messages=[{'role': 'user', 'content': content}]
        )
        return resp.content[0].text.strip().strip('"')
    except Exception as e:
        log.warning(f"ai_title error: {e}")
        return (item['desc'] or '')[:70] or '(sin título)'

# ══════════════════════════════════════════════════════════
#  FORMATO DEL MENSAJE
# ══════════════════════════════════════════════════════════

def format_message(items, cat_label):
    lines = []
    for n in items:
        title = n['title'] or n['desc'][:70] or '(sin título)'
        src   = ' / '.join(p for p in [n['medio'], n['programa']] if p) or 'Sin fuente'
        link  = f"\n🔗 {n['url']}" if n['url'] else ''
        lines.append(f"→ *{title}*\n→ {n['date']} {n['time']}  {src}{link}")
    header = f"📍 *RESUMEN DE \"{cat_label.upper()}\"*"
    return header + '\n\n' + '\n\n'.join(lines)

async def send_long(bot, chat_id, text):
    LIMIT = 4000
    if len(text) <= LIMIT:
        await bot.send_message(chat_id=chat_id, text=text,
                               parse_mode='Markdown', disable_web_page_preview=True)
        return
    parts, chunk, chunks = text.split('\n\n'), '', []
    for part in parts:
        if len(chunk) + len(part) + 2 > LIMIT:
            if chunk: chunks.append(chunk)
            chunk = part
        else:
            chunk = (chunk + '\n\n' + part).strip()
    if chunk: chunks.append(chunk)
    for i, c in enumerate(chunks):
        if i > 0: await asyncio.sleep(0.4)
        await bot.send_message(chat_id=chat_id, text=c,
                               parse_mode='Markdown', disable_web_page_preview=True)

# ══════════════════════════════════════════════════════════
#  TECLADO — helpers
# ══════════════════════════════════════════════════════════

def menu_keyboard(items, active_cats):
    """Teclado principal con todas las categorías activas."""
    cat_counts = {}
    for n in items:
        for cat in n['cats']:
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

    keyboard = [[InlineKeyboardButton(
        f"📋 Todas ({len(items)})", callback_data="show:__all__"
    )]]
    row = []
    for cat in active_cats:
        row.append(InlineKeyboardButton(
            f"{cat} ({cat_counts.get(cat, 0)})",
            callback_data=f"show:{cat}"
        ))
        if len(row) == 2:
            keyboard.append(row); row = []
    if row: keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def cat_keyboard(cat):
    """Teclado de opciones dentro de una categoría."""
    label = "Todas" if cat == "__all__" else cat
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 Generar mensaje",      callback_data=f"gen:{cat}"),
            InlineKeyboardButton("✨ Con IA (títulos)",     callback_data=f"ai:{cat}"),
        ],
        [InlineKeyboardButton("⬅️  Ver categorías",        callback_data="back:menu")],
    ])

def menu_text(n_items, n_cats):
    return (
        f"✅ *{n_items} noticias* encontradas en *{n_cats} categorías*\n\n"
        "Elegí una categoría para generar el resumen:"
    )

# ══════════════════════════════════════════════════════════
#  SESIONES
# ══════════════════════════════════════════════════════════
SESSIONS = {}   # uid -> {"items": [...], "active_cats": [...]}

# ══════════════════════════════════════════════════════════
#  HANDLERS
# ══════════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    # Si ya hay una sesión activa, volver al menú de categorías
    if uid in SESSIONS:
        s = SESSIONS[uid]
        await update.message.reply_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
        return

    await update.message.reply_text(
        "👋 *Clipping de Medios — Municipalidad de Córdoba*\n\n"
        "Enviame el archivo `.txt` exportado de WhatsApp.\n\n"
        "📲 Cómo exportarlo:\n"
        "WhatsApp → chat del bot → ··· → Más → *Exportar chat* → Sin archivos",
        parse_mode='Markdown'
    )


async def handle_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith('.txt'):
        await update.message.reply_text("⚠️ Enviá un archivo `.txt` exportado de WhatsApp.")
        return

    uid    = update.effective_user.id
    status = await update.message.reply_text("⏳ Leyendo el archivo…")

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
            "Verificá que sea un chat con *Media Monitoring* o *CVAMedios IA Monitoreo*.",
            parse_mode='Markdown'
        )
        return

    cat_counts = {}
    for n in items:
        for cat in n['cats']:
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
    active_cats = [c for c in CATS if c in cat_counts]

    SESSIONS[uid] = {'items': items, 'active_cats': active_cats}

    await status.edit_text(
        menu_text(len(items), len(active_cats)),
        reply_markup=menu_keyboard(items, active_cats),
        parse_mode='Markdown'
    )


async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid  = update.effective_user.id
    data = query.data

    # ── Volver al menú ──────────────────────────────────
    if data == "back:menu":
        if uid not in SESSIONS:
            await query.edit_message_text("La sesión expiró. Enviá el archivo nuevamente.")
            return
        s = SESSIONS[uid]
        await query.edit_message_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
        return

    if uid not in SESSIONS:
        await query.edit_message_text("La sesión expiró. Enviá el archivo nuevamente.")
        return

    s = SESSIONS[uid]

    # ── Mostrar opciones de categoría ───────────────────
    if data.startswith("show:"):
        cat = data[5:]
        label = "Todas las noticias" if cat == "__all__" else cat
        filtered = s['items'] if cat == "__all__" else [n for n in s['items'] if cat in n['cats']]
        await query.edit_message_text(
            f"📍 *{label}* — {len(filtered)} noticias\n\n"
            "¿Cómo querés generar el resumen?",
            reply_markup=cat_keyboard(cat),
            parse_mode='Markdown'
        )
        return

    # ── Generar mensaje sin IA ───────────────────────────
    if data.startswith("gen:"):
        cat      = data[4:]
        filtered = s['items'] if cat == "__all__" else [n for n in s['items'] if cat in n['cats']]
        label    = "NOTICIAS" if cat == "__all__" else cat

        await query.edit_message_text(
            f"⏳ Armando *{label}*…",
            parse_mode='Markdown'
        )

        msg_text = format_message(filtered, label)
        await send_long(ctx.bot, update.effective_chat.id, msg_text)

        # Volver al menú automáticamente
        await query.edit_message_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
        return

    # ── Generar mensaje CON IA ───────────────────────────
    if data.startswith("ai:"):
        cat      = data[3:]
        filtered = s['items'] if cat == "__all__" else [n for n in s['items'] if cat in n['cats']]
        label    = "NOTICIAS" if cat == "__all__" else cat
        total    = len(filtered)

        await query.edit_message_text(
            f"✨ Generando títulos con IA para *{label}*…\n"
            f"({total} noticias, ~{total * 2}s)",
            parse_mode='Markdown'
        )

        for i, item in enumerate(filtered, 1):
            if not item['title']:
                item['title'] = ai_title(item)
            if i % 4 == 0:
                try:
                    await query.edit_message_text(
                        f"✨ Procesando {i}/{total} — *{label}*…",
                        parse_mode='Markdown'
                    )
                except Exception:
                    pass
            await asyncio.sleep(0.2)

        msg_text = format_message(filtered, label)
        await send_long(ctx.bot, update.effective_chat.id, msg_text)

        # Volver al menú automáticamente
        await query.edit_message_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
        return


async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in SESSIONS:
        s = SESSIONS[uid]
        await update.message.reply_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "Enviame el `.txt` exportado de WhatsApp para empezar.",
            parse_mode='Markdown'
        )


# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("Falta TELEGRAM_BOT_TOKEN")
    if not os.environ.get('ANTHROPIC_API_KEY'):
        log.warning("ANTHROPIC_API_KEY no encontrada — IA deshabilitada.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', cmd_start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    log.info("Bot iniciado.")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
