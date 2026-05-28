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

CATS = [
    'Ambiente','Ciudad Inteligente','Deporte y Cultura','Desarrollo Urbano',
    'Educación','Entrevista','General','Gobierno','Mensaje de oyente',
    'Participación','Políticas Sociales','Recursos Tributarios',
    'Salud','Seguridad','Transporte','Tránsito','Tribunal de Faltas'
]

KW_DATA = [
    ('llaryora', ['General']),
    ('passerini', ['General']),
    ('schiaretti', ['General']),
    ('intendente', ['General']),
    ('gobernación', ['General']),
    ('corte', ['Gobierno', 'Desarrollo Urbano']),
    ('olor', ['Ambiente']),
    ('contaminación', ['Ambiente']),
    ('Plaza', ['Ambiente']),
    ('Ambiente', ['Ambiente']),
    ('Basural', ['Ambiente']),
    ('sarria', ['Ambiente', 'Entrevista']),
    ('Pretto', ['General', 'Entrevista']),
    ('Lorenzatti', ['General', 'Entrevista']),
    ('Gei', ['Ciudad Inteligente', 'Entrevista']),
    ('Viola', ['Participación', 'Entrevista']),
    ('Peralta', ['Desarrollo Urbano', 'Entrevista']),
    ('Campana', ['Deporte y Cultura', 'Entrevista']),
    ('Gabriel Martin', ['Ambiente', 'Entrevista']),
    ('La Cava', ['Políticas Sociales', 'Entrevista']),
    ('La Terza', ['Educación', 'Entrevista']),
    ('Aleksandroff', ['Salud', 'Entrevista']),
    ('Rodrigo Fernandez', ['Gobierno', 'Entrevista']),
    ('Tránsito', ['Gobierno']),
    ('Juan Manuel Araoz', ['Tribunal de Faltas', 'Entrevista']),
    ('tasas', ['Recursos Tributarios']),
    ('impuestos', ['Recursos Tributarios']),
    ('presupuesto participativo', ['Participación']),
    ('juntas de participacion', ['Participación']),
    ('CPC', ['Participación']),
    ('Centro operativo', ['Participación']),
    ('bache', ['Desarrollo Urbano']),
    ('obras', ['Desarrollo Urbano']),
    ('plaza', ['Ambiente']),
    ('pasto', ['Ambiente']),
    ('yuyos', ['Ambiente']),
    ('mosquito', ['Salud', 'Ambiente']),
    ('dengue', ['Salud', 'Ambiente']),
    ('dispensario', ['Salud']),
    ('hospital', ['Salud']),
    ('vacuna', ['Salud']),
    ('medico', ['Salud']),
    ('medica', ['Salud']),
    ('medicina', ['Salud']),
    ('fentanilo', ['Salud']),
    ('sanatorio', ['Salud']),
    ('residente', ['Salud']),
    ('enfermero', ['Salud']),
    ('enfermera', ['Salud']),
    ('testeo', ['Salud']),
    ('uber', ['Gobierno', 'Transporte']),
    ('taxi', ['Gobierno', 'Transporte']),
    ('suoem', ['General']),
    ('surbac', ['Ambiente']),
    ('metropolitano', ['Gobierno']),
    ('transporte', ['Gobierno', 'Transporte']),
    ('inspector', ['Gobierno']),
    ('horario extendido', ['Gobierno']),
    ('centros educativos', ['Participación']),
    ('ANMAT', ['Salud']),
    ('Instituto', ['Deporte y Cultura']),
    ('Talleres', ['Deporte y Cultura']),
    ('Belgrano', ['Deporte y Cultura']),
    ('Racing', ['Deporte y Cultura']),
    ('Pichi Campana', ['Deporte y Cultura']),
    ('Kempes', ['Deporte y Cultura']),
    ('sucia', ['Ambiente']),
    ('sucio', ['Ambiente']),
    ('mugre', ['Ambiente']),
    ('asco', ['Ambiente']),
    ('Sube', ['Gobierno']),
    ('Red Bus', ['Gobierno']),
    ('clausura', ['Gobierno']),
    ('Hormaeche', ['Gobierno']),
    ('semáforo', ['Gobierno', 'Tránsito']),
    ('boleto gratuito', ['Gobierno']),
    ('servidores urbanos', ['Participación']),
    ('grupo fem', ['Participación']),
    ('robo', ['Seguridad']),
    ('detenidos', ['Seguridad']),
    ('inseguridad', ['Seguridad']),
    ('arrestados', ['Seguridad']),
    ('investigado', ['Seguridad']),
    ('centros de salud', ['Salud']),
    ('paciente', ['Salud']),
    ('crimen', ['Seguridad']),
    ('muerte', ['Seguridad']),
    ('policia', ['Seguridad']),
    ('sintomas', ['Salud']),
    ('mató', ['Seguridad']),
    ('femicidio', ['Seguridad']),
    ('arresto', ['Seguridad']),
    ('arrestado', ['Seguridad']),
    ('trámites', ['Participación']),
    ('ilegal', ['Seguridad']),
    ('narco', ['Seguridad']),
    ('tiroteo', ['Seguridad']),
    ('asesino', ['Seguridad']),
    ('clases', ['Educación']),
    ('fútbol', ['Deporte y Cultura']),
    ('teatro', ['Deporte y Cultura']),
    ('basquet', ['Deporte y Cultura']),
    ('centro vecinal', ['Deporte y Cultura']),
    ('centros vecinales', ['Deporte y Cultura']),
    ('cultura', ['Deporte y Cultura']),
    ('feria del libro', ['Deporte y Cultura']),
    ('coro', ['Deporte y Cultura']),
    ('tech', ['Ciudad Inteligente']),
    ('cordoba acelera', ['Ciudad Inteligente']),
    ('emprendedor', ['Ciudad Inteligente']),
    ('lgbt', ['Políticas Sociales']),
    ('entrevista', ['Entrevista']),
    ('con nosotros', ['Entrevista']),
    ('hablamos con', ['Entrevista']),
    ('violencia', ['Seguridad']),
    ('oyente', ['Mensaje de oyente']),
    ('Oyente:', ['Mensaje de oyente']),
    ('Oyente', ['Mensaje de oyente']),
    ('oyente:', ['Mensaje de oyente']),
    ('te escribo', ['Mensaje de oyente']),
    ('Comerciante', ['Mensaje de oyente']),
    ('comerciante', ['Mensaje de oyente']),
    ('VA2', ['Mensaje de oyente']),
    ('VA3', ['Mensaje de oyente']),
    ('Basura', ['Ambiente']),
    ('basura', ['Ambiente']),
    ('estacionar', ['Gobierno']),
    ('limpiavidrios', ['Gobierno']),
    ('estacionamiento', ['Gobierno']),
    ('naranjitas', ['Gobierno']),
    ('naranjita', ['Gobierno']),
    ('app', ['Ciudad Inteligente']),
    ('App', ['Ciudad Inteligente']),
    ('Frecuencia', ['Transporte']),
    ('frecuencia', ['Transporte']),
    ('Juan Pablo Quinteros', ['Entrevista']),
    ('Obra pública', ['Desarrollo Urbano']),
    ('infraestructura', ['Desarrollo Urbano']),
    ('Marcelo Valdomero', ['Entrevista']),
    ('Accidentología vial', ['Tránsito']),
    ('Guillermo Pacharoni', ['Tránsito']),
    ('hundimiento', ['Desarrollo Urbano']),
]

MEDIA_MAP = {k.lower(): {'display': d, 'tipo': t} for k, d, t in [
    ('Radio Mitre', 'Mitre', 'Medio'),
    ('APTT', 'Aquí Petete', 'Programa'),
    ('POP', 'Radio Popular', 'Medio'),
    ('VV', 'Vamos Viendo', 'Programa'),
    ('LV3', 'Cadena 3', 'Medio'),
    ('RADIOINF', 'Radio Informe 3', 'Programa'),
    ('CONTINENTAL', 'Continental', 'Medio'),
    ('AENOT', 'Alassia es noticia', 'Programa'),
    ('Gefinforma', 'Ge Informa', 'Medio'),
    ('HoyDia', 'Hoy Día Córdoba', 'Medio'),
    ('Cba24n', 'CBA 24 Noticias', 'Medio'),
    ('El Doce', 'Canal 12', 'Medio'),
    ('TELEFE', 'Telefe', 'Medio'),
    ('LMZ', 'La mañana con Zuliani', 'Programa'),
    ('C12', 'Canal 12', 'Medio'),
    ('ACBA', 'Arriba Córdoba', 'Programa'),
    ('CanalC', 'Canal C', 'Medio'),
    ('LVeV', 'La Voz en Vivo', 'Programa'),
    ('SJ', 'Siempre Juntos', 'Programa'),
    ('SUQUIA', 'Radio Suquía', 'Medio'),
    ('BDC', 'Bien de Córdoba', 'Programa'),
    ('MEM', 'Mediodía en Mitre', 'Programa'),
    ('SDL', 'Show del Lagarto', 'Programa'),
    ('SUQ', 'Radio Suquía', 'Medio'),
    ('noticierodoce', 'Noticiero Doce', 'Programa'),
    ('informadosalregreso', 'Informados al Regreso', 'Programa'),
    ('TNC', 'Telefe Noticias', 'Programa'),
    ('TelefeNoticias', 'Telefe Noticias', 'Programa'),
    ('siestaanimal', 'Siesta Animal', 'Programa'),
    ('siemprejuntos', 'Siempre Juntos', 'Programa'),
    ('AquiPetete', 'Aquí Petete', 'Programa'),
    ('geninforma', 'Gen Informa', 'Programa'),
    ('lamananaconzuliani', 'La mañana con Zuliani', 'Programa'),
    ('idayvuelta', 'Ida y Vuelta', 'Programa'),
    ('AEN', 'Alassia es noticia', 'Programa'),
    ('alassiaesnoticia', 'Alassia es noticia', 'Programa'),
    ('TFN', 'Telefe Noticias 1ra Ed', 'Programa'),
    ('BM', 'Buen Mediodía', 'Programa'),
    ('SAML', 'Siesta Animal', 'Programa'),
    ('MT', 'Mientras Tanto', 'Programa'),
    ('elshowdellagarto', 'Show del Lagarto', 'Programa'),
    ('NDCE', 'Noticiero Doce', 'Programa'),
    ('C10', 'Canal 10', 'Medio'),
    ('VVLR', 'Viva la Radio', 'Programa'),
    ('‼️LV3', 'Cadena 3', 'Medio'),
    ('cadena3', 'Cadena 3', 'Medio'),
    ('CC', 'Canal C', 'Medio'),
    ('puntalvillamaria', 'Puntal Villa Maria', 'Medio'),
    ('diarioalfil', 'Diario Alfil', 'Medio'),
    ('politicacordobaverdad', 'Política Cordoba Verdad', 'Medio'),
    ('mivalle', 'Mi Valle', 'Medio'),
    ('economixtv', 'Economix TV', 'Medio'),
    ('eldoce', 'El Doce TV', 'Medio'),
    ('elobjetivo', 'El Objetivo', 'Medio'),
    ('eldiariodecarlospaz', 'Diario de Carlos Paz', 'Medio'),
    ('clipgo', 'Clip GO', 'Medio'),
    ('comercioyjusticia', 'Comercio y Justicia', 'Medio'),
    ('laranchada', 'La Ranchada', 'Medio'),
    ('jornadapolitica', 'Jornada Política', 'Medio'),
    ('viapais', 'Vía País', 'Medio'),
    ('lvdos', 'LV 2', 'Medio'),
    ('infonegocios', 'Info Negocios', 'Medio'),
    ('villamariavivo', 'Villa Maria Vivo', 'Medio'),
    ('derechadiario', 'Derecha Diario', 'Medio'),
    ('enredaccion', 'En Redacción', 'Medio'),
    ('lavoz', 'La Voz', 'Medio'),
    ('lmdiario', 'La Nueva Mañana', 'Medio'),
    ('entretenimientoscordoba', 'Entretenimientos Córdoba', 'Medio'),
    ('el-periodico', 'El Periódico', 'Medio'),
    ('cordoba', 'Telefe', 'Medio'),
    ('miraelnorte', 'Mirá el Norte', 'Medio'),
    ('TELEFE TNC', 'Telefe', 'Medio'),
    ('sierraschicasvivo', 'Sierras Chicas Vivo', 'Medio'),
    ('SUQUIA,', 'Suquia', 'Medio'),
    ('SUQ BDC Uber', 'Suquia', 'Medio'),
    ('Telefe Noticias 1ra Ed', 'Telefe Primera Edición', 'Programa'),
    ('Radioinforme 3', 'Radio Informe 3', 'Programa'),
    ('VV Fernando Genesir', 'Vamos Viendo', 'Programa'),
    ('TUP', 'Siesta Animal', 'Programa'),
    ('SDP', 'Secretos del Poder', 'Programa'),
    ('AN', 'Ahora Noticias', 'Programa'),
    ('JP', 'Jornada Política', 'Programa'),
    ('FYC', 'Fuerte y Claro', 'Programa'),
    ('MQH', 'Mirá quien habla', 'Programa'),
    ('FUTIMP', 'Futuro Imperfecto', 'Programa'),
    ('AP', 'La Argentina Posible', 'Programa'),
    ('TND', 'TeleNoche Doce', 'Programa'),
    ('ETL', 'El toque Lalo', 'Programa'),
    ('LSM', 'La Super Mañana', 'Programa'),
    ('IYV', 'Ida y vuelta', 'Programa'),
    ('CN', 'Córdoba Noticias', 'Programa'),
    ('MitreCordoba', 'Mitre', 'Medio'),
    ('IAR', 'Informados al Regreso', 'Programa'),
    ('DF', 'Distrito Federal', 'Programa'),
    ('difusionnoticias', 'Difusión Noticias', 'Medio'),
    ('cordobainteriorinforma', 'Córdoba Interior Informa', 'Medio'),
    ('puntal', 'Puntal', 'Medio'),
    ('CCordoba', 'C Córdoba', 'Medio'),
    ('marcainformativacba', 'Marca Informativa Cba', 'Medio'),
    ('AM700', 'AM 700', 'Medio'),
    ('lavozdesanjusto', 'La Voz de San Justo', 'Medio'),
    ('diariodelasvarillas', 'Diario de Las Varillas', 'Medio'),
    ('valorlocal', 'Valor Local', 'Medio'),
    ('puntoapunto', 'Punto a Punto', 'Medio'),
    ('LV2', 'LV 2', 'Medio'),
    ('ECDV', 'El Club del Vecino', 'Programa'),
]}


# ═══════════════════════════════════════════════
#  PARSERS
# ═══════════════════════════════════════════════

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
            if entry['tipo'] == 'Medio' and not medio:      medio    = entry['display']; continue
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
        if kw.lower() in lo:
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
            'title': '', 'cats': cats,
        })
    return items

# ═══════════════════════════════════════════════
#  IA
# ═══════════════════════════════════════════════

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
                'Generá un título periodístico conciso (máx 10 palabras) '
                'para este recorte de medios de Córdoba, Argentina. '
                'Solo el título, sin comillas ni explicaciones.'
            ),
            messages=[{'role': 'user', 'content': content}]
        )
        return resp.content[0].text.strip().strip('"\'')
    except Exception as e:
        log.warning(f'ai_title error: {e}')
        return (item['desc'] or '')[:70] or '(sin título)'

# ═══════════════════════════════════════════════
#  FORMATO
# ═══════════════════════════════════════════════

def format_message(items, cat_label):
    lines = []
    for n in items:
        title = n['title'] or n['desc'][:70] or '(sin título)'
        src   = ' / '.join(p for p in [n['medio'], n['programa']] if p) or 'Sin fuente'
        link  = f"\n\U0001f517 {n['url']}" if n['url'] else ''
        lines.append(f"\u2192 *{title}*\n\u2192 {n['date']} {n['time']}  {src}{link}")
    header = f"\U0001f4cd *RESUMEN DE \"{cat_label.upper()}\"*"
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

# ═══════════════════════════════════════════════
#  TECLADOS
# ═══════════════════════════════════════════════

def menu_keyboard(items, active_cats):
    cat_counts = {}
    for n in items:
        for cat in n['cats']:
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
    keyboard = [[InlineKeyboardButton(
        f"\U0001f4cb Todas ({len(items)})", callback_data='show:__all__'
    )]]
    row = []
    for cat in active_cats:
        row.append(InlineKeyboardButton(
            f"{cat} ({cat_counts.get(cat,0)})",
            callback_data=f'show:{cat}'
        ))
        if len(row) == 2:
            keyboard.append(row); row = []
    if row: keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def cat_keyboard(cat):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('\U0001f4c4 Generar mensaje',  callback_data=f'gen:{cat}'),
            InlineKeyboardButton('\u2728 Con IA (t\u00edtulos)', callback_data=f'ai:{cat}'),
        ],
        [InlineKeyboardButton('\u2b05\ufe0f  Ver categor\u00edas', callback_data='back:menu')],
    ])

def menu_text(n_items, n_cats):
    return (
        f"\u2705 *{n_items} noticias* en *{n_cats} categor\u00edas*\n\n"
        "Eleg\u00ed una categor\u00eda para generar el resumen:"
    )

# ═══════════════════════════════════════════════
#  SESIONES
# ═══════════════════════════════════════════════

SESSIONS = {}

# ═══════════════════════════════════════════════
#  HANDLERS
# ═══════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in SESSIONS:
        s = SESSIONS[uid]
        await update.message.reply_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
        return
    await update.message.reply_text(
        "\U0001f44b *Clipping de Medios \u2014 Municipalidad de C\u00f3rdoba*\n\n"
        "Enviam\u00e9 el archivo `.txt` exportado de WhatsApp.\n\n"
        "\U0001f4f2 *C\u00f3mo exportarlo:*\n"
        "WhatsApp \u2192 chat del bot \u2192 \u00b7\u00b7\u00b7 \u2192 M\u00e1s \u2192 *Exportar chat* \u2192 Sin archivos",
        parse_mode='Markdown'
    )

async def handle_document(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith('.txt'):
        await update.message.reply_text("\u26a0\ufe0f Envi\u00e1 un archivo `.txt` exportado de WhatsApp.")
        return
    uid    = update.effective_user.id
    status = await update.message.reply_text("\u23f3 Leyendo el archivo\u2026")
    try:
        tg_file = await ctx.bot.get_file(doc.file_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            await tg_file.download_to_drive(tmp.name)
            with open(tmp.name, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
    except Exception as e:
        await status.edit_text(f"\u274c Error al leer el archivo: {e}")
        return
    items = build_items(text)
    if not items:
        await status.edit_text(
            "\u274c No encontr\u00e9 noticias.\n"
            "Verific\u00e1 que sea un chat con *Media Monitoring* o *CVAMedios IA Monitoreo*.",
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

    if data == 'back:menu':
        if uid not in SESSIONS:
            await query.edit_message_text("La sesi\u00f3n expir\u00f3. Envi\u00e1 el archivo nuevamente.")
            return
        s = SESSIONS[uid]
        await query.edit_message_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
        return

    if uid not in SESSIONS:
        await query.edit_message_text("La sesi\u00f3n expir\u00f3. Envi\u00e1 el archivo nuevamente.")
        return

    s = SESSIONS[uid]

    if data.startswith('show:'):
        cat      = data[5:]
        label    = 'Todas las noticias' if cat == '__all__' else cat
        filtered = s['items'] if cat == '__all__' else [n for n in s['items'] if cat in n['cats']]
        await query.edit_message_text(
            f"\U0001f4cd *{label}* \u2014 {len(filtered)} noticias\n\n\u00bfC\u00f3mo quer\u00e9s generar el resumen?",
            reply_markup=cat_keyboard(cat),
            parse_mode='Markdown'
        )
        return

    if data.startswith('gen:'):
        cat      = data[4:]
        filtered = s['items'] if cat == '__all__' else [n for n in s['items'] if cat in n['cats']]
        label    = 'NOTICIAS' if cat == '__all__' else cat
        await query.edit_message_text(f"\u23f3 Armando *{label}*\u2026", parse_mode='Markdown')
        await send_long(ctx.bot, update.effective_chat.id, format_message(filtered, label))
        await query.edit_message_text(
            menu_text(len(s['items']), len(s['active_cats'])),
            reply_markup=menu_keyboard(s['items'], s['active_cats']),
            parse_mode='Markdown'
        )
        return

    if data.startswith('ai:'):
        cat      = data[3:]
        filtered = s['items'] if cat == '__all__' else [n for n in s['items'] if cat in n['cats']]
        label    = 'NOTICIAS' if cat == '__all__' else cat
        total    = len(filtered)
        await query.edit_message_text(
            f"\u2728 Generando t\u00edtulos con IA \u2014 *{label}* ({total} noticias)\u2026",
            parse_mode='Markdown'
        )
        for i, item in enumerate(filtered, 1):
            if not item['title']:
                item['title'] = ai_title(item)
            if i % 4 == 0:
                try:
                    await query.edit_message_text(
                        f"\u2728 Procesando {i}/{total}\u2026", parse_mode='Markdown'
                    )
                except Exception:
                    pass
            await asyncio.sleep(0.2)
        await send_long(ctx.bot, update.effective_chat.id, format_message(filtered, label))
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
            "Enviam\u00e9 el `.txt` exportado de WhatsApp para empezar.",
            parse_mode='Markdown'
        )

# ═══════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError('Falta TELEGRAM_BOT_TOKEN')
    if not os.environ.get('ANTHROPIC_API_KEY'):
        log.warning('ANTHROPIC_API_KEY no encontrada.')
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', cmd_start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    log.info('Bot iniciado.')
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
