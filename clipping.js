// clipping.js — Port of bot.py parsing/categorization logic to the browser.
// Municipalidad de Córdoba — Clipping de Medios.

export const CATS = [
  'Ambiente','Ciudad Inteligente','Deporte y Cultura','Desarrollo Urbano',
  'Educación','Entrevista','General','Gobierno',
  'Participación','Políticas Sociales','Recursos Tributarios',
  'Salud','Seguridad','Transporte','Tránsito','Tribunal de Faltas'
];

const KW_DATA = [
  ["llaryora", ["General"]],
  ["passerini", ["General"]],
  ["schiaretti", ["General"]],
  ["intendente", ["General"]],
  ["gobernación", ["General"]],
  ["corte", ["Gobierno", "Desarrollo Urbano"]],
  ["contaminación", ["Ambiente"]],
  ["Basural", ["Ambiente"]],
  ["sarria", ["Ambiente", "Entrevista"]],
  ["Pretto", ["General", "Entrevista"]],
  ["Lorenzatti", ["General", "Entrevista"]],
  ["Gei", ["Ciudad Inteligente", "Entrevista"]],
  ["Viola", ["Participación", "Entrevista"]],
  ["Peralta", ["Desarrollo Urbano", "Entrevista"]],
  ["Campana", ["Deporte y Cultura", "Entrevista"]],
  ["Gabriel Martin", ["Ambiente", "Entrevista"]],
  ["La Cava", ["Políticas Sociales", "Entrevista"]],
  ["La Terza", ["Educación", "Entrevista"]],
  ["Aleksandroff", ["Salud", "Entrevista"]],
  ["Rodrigo Fernandez", ["Gobierno", "Entrevista"]],
  ["Tránsito", ["Gobierno"]],
  ["Juan Manuel Araoz", ["Tribunal de Faltas", "Entrevista"]],
  ["tasas", ["Recursos Tributarios"]],
  ["impuestos", ["Recursos Tributarios"]],
  ["presupuesto participativo", ["Participación"]],
  ["juntas de participacion", ["Participación"]],
  ["CPC", ["Participación"]],
  ["Centro operativo", ["Participación"]],
  ["bache", ["Desarrollo Urbano"]],
  ["obras", ["Desarrollo Urbano"]],
  ["pasto", ["Ambiente"]],
  ["yuyos", ["Ambiente"]],
  ["mosquito", ["Salud", "Ambiente"]],
  ["dengue", ["Salud", "Ambiente"]],
  ["dispensario", ["Salud"]],
  ["hospital", ["Salud"]],
  ["vacuna", ["Salud"]],
  ["medico", ["Salud"]],
  ["medica", ["Salud"]],
  ["medicina", ["Salud"]],
  ["fentanilo", ["Salud"]],
  ["sanatorio", ["Salud"]],
  ["residente", ["Salud"]],
  ["enfermero", ["Salud"]],
  ["enfermera", ["Salud"]],
  ["testeo", ["Salud"]],
  ["uber", ["Gobierno", "Transporte"]],
  ["taxi", ["Gobierno", "Transporte"]],
  ["suoem", ["General"]],
  ["surbac", ["Ambiente"]],
  ["metropolitano", ["Gobierno"]],
  ["transporte", ["Gobierno", "Transporte"]],
  ["inspector", ["Gobierno"]],
  ["horario extendido", ["Gobierno"]],
  ["centros educativos", ["Participación"]],
  ["ANMAT", ["Salud"]],
  ["Instituto", ["Deporte y Cultura"]],
  ["Talleres", ["Deporte y Cultura"]],
  ["Belgrano", ["Deporte y Cultura"]],
  ["Racing", ["Deporte y Cultura"]],
  ["Pichi Campana", ["Deporte y Cultura"]],
  ["Kempes", ["Deporte y Cultura"]],
  ["sucia", ["Ambiente"]],
  ["sucio", ["Ambiente"]],
  ["mugre", ["Ambiente"]],
  ["Sube", ["Gobierno"]],
  ["Red Bus", ["Gobierno"]],
  ["clausura", ["Gobierno"]],
  ["Hormaeche", ["Gobierno"]],
  ["semáforo", ["Gobierno", "Tránsito"]],
  ["boleto gratuito", ["Gobierno"]],
  ["servidores urbanos", ["Participación"]],
  ["grupo fem", ["Participación"]],
  ["robo", ["Seguridad"]],
  ["detenidos", ["Seguridad"]],
  ["inseguridad", ["Seguridad"]],
  ["arrestados", ["Seguridad"]],
  ["investigado", ["Seguridad"]],
  ["centros de salud", ["Salud"]],
  ["paciente", ["Salud"]],
  ["crimen", ["Seguridad"]],
  ["muerte", ["Seguridad"]],
  ["policia", ["Seguridad"]],
  ["sintomas", ["Salud"]],
  ["mató", ["Seguridad"]],
  ["femicidio", ["Seguridad"]],
  ["arresto", ["Seguridad"]],
  ["arrestado", ["Seguridad"]],
  ["trámites", ["Participación"]],
  ["ilegal", ["Seguridad"]],
  ["narco", ["Seguridad"]],
  ["tiroteo", ["Seguridad"]],
  ["asesino", ["Seguridad"]],
  ["clases", ["Educación"]],
  ["fútbol", ["Deporte y Cultura"]],
  ["teatro", ["Deporte y Cultura"]],
  ["basquet", ["Deporte y Cultura"]],
  ["centro vecinal", ["Deporte y Cultura"]],
  ["centros vecinales", ["Deporte y Cultura"]],
  ["cultura", ["Deporte y Cultura"]],
  ["feria del libro", ["Deporte y Cultura"]],
  ["coro", ["Deporte y Cultura"]],
  ["tech", ["Ciudad Inteligente"]],
  ["cordoba acelera", ["Ciudad Inteligente"]],
  ["emprendedor", ["Ciudad Inteligente"]],
  ["lgbt", ["Políticas Sociales"]],
  ["entrevista", ["Entrevista"]],
  ["con nosotros", ["Entrevista"]],
  ["hablamos con", ["Entrevista"]],
  ["violencia", ["Seguridad"]],
  ["oyente", ["Mensaje de oyente"]],
  ["Oyente:", ["Mensaje de oyente"]],
  ["Oyente", ["Mensaje de oyente"]],
  ["oyente:", ["Mensaje de oyente"]],
  ["te escribo", ["Mensaje de oyente"]],
  ["Comerciante", ["Mensaje de oyente"]],
  ["comerciante", ["Mensaje de oyente"]],
  ["VA2", ["Mensaje de oyente"]],
  ["VA3", ["Mensaje de oyente"]],
  ["Basura", ["Ambiente"]],
  ["basura", ["Ambiente"]],
  ["estacionar", ["Gobierno"]],
  ["limpiavidrios", ["Gobierno"]],
  ["estacionamiento", ["Gobierno"]],
  ["naranjitas", ["Gobierno"]],
  ["naranjita", ["Gobierno"]],
  ["app", ["Ciudad Inteligente"]],
  ["App", ["Ciudad Inteligente"]],
  ["Frecuencia", ["Transporte"]],
  ["frecuencia", ["Transporte"]],
  ["Juan Pablo Quinteros", ["Entrevista"]],
  ["Obra pública", ["Desarrollo Urbano"]],
  ["infraestructura", ["Desarrollo Urbano"]],
  ["Marcelo Valdomero", ["Entrevista"]],
  ["Accidentología vial", ["Tránsito"]],
  ["Guillermo Pacharoni", ["Tránsito"]],
  ["hundimiento", ["Desarrollo Urbano"]],
];

const PHRASE_RULES = [
  [["transitoinforme"], "Gobierno", 12],
  [["tránsito","informe"], "Gobierno", 12],
  [["transito","informe"], "Gobierno", 12],
  [["accidentetransito"], "Gobierno", 11],
  [["accidentologiavial"], "Gobierno", 11],
  [["accidente","tránsito"], "Gobierno", 10],
  [["accidente","transito"], "Gobierno", 10],
  [["atropello"], "Gobierno", 10],
  [["choque"], "Gobierno", 8],
  [["seguridadvial"], "Gobierno", 11],
  [["tupcolectivos"], "Gobierno", 12],
  [["colectivos","frecuencia"], "Gobierno", 11],
  [["colectivos","recorrido"], "Gobierno", 11],
  [["transporteurbanopasajeros"], "Gobierno", 12],
  [["famempresa"], "Gobierno", 11],
  [["transporteaplicaciones"], "Gobierno", 11],
  [["estacionamientocontrolado"], "Gobierno", 12],
  [["estacionamiento","controlado"], "Gobierno", 12],
  [["estacionamiento","medido"], "Gobierno", 12],
  [["semmsistemadeestacionamiento"], "Gobierno", 12],
  [["semm"], "Gobierno", 10],
  [["estacionamiento"], "Gobierno", 7],
  [["naranjitasilegales"], "Gobierno", 12],
  [["naranjitas"], "Gobierno", 10],
  [["limpiavidrios"], "Gobierno", 10],
  [["policialdesaparicion"], "Gobierno", 12],
  [["policialrobo"], "Gobierno", 12],
  [["policialdetencion"], "Gobierno", 11],
  [["policialagresion"], "Gobierno", 11],
  [["policiallesionesgraves"], "Gobierno", 11],
  [["inseguridadrobo"], "Gobierno", 12],
  [["inseguridadlesionesgraves"], "Gobierno", 11],
  [["desaparición"], "Gobierno", 8],
  [["alerta","sofía"], "Gobierno", 12],
  [["alerta","sofia"], "Gobierno", 12],
  [["empleado","municipal"], "Gobierno", 10],
  [["uberregulacion"], "Gobierno", 12],
  [["taxistasreclamo"], "Gobierno", 12],
  [["taxisremis"], "Gobierno", 11],
  [["uber"], "Gobierno", 8],
  [["guardiaurbana"], "Gobierno", 11],
  [["ruidosmolesto"], "Gobierno", 10],
  [["caminera","multa"], "Gobierno", 10],
  [["carnetconducir"], "Gobierno", 11],
  [["higieneurbanareclamo"], "Ambiente", 12],
  [["higieneurbanatareas"], "Ambiente", 12],
  [["basuralreclamo"], "Ambiente", 12],
  [["recicladoderesiduos"], "Ambiente", 12],
  [["espaciosverdesreclamo"], "Ambiente", 12],
  [["carrerosreclamo"], "Ambiente", 12],
  [["urbacor"], "Ambiente", 12],
  [["surbac"], "Ambiente", 11],
  [["basural"], "Ambiente", 11],
  [["basura"], "Ambiente", 8],
  [["residuos"], "Ambiente", 7],
  [["mugre"], "Ambiente", 8],
  [["recolección","residuos"], "Ambiente", 10],
  [["higiene","urbana"], "Ambiente", 9],
  [["poda"], "Ambiente", 8],
  [["descacharreo"], "Ambiente", 10],
  [["bachereclamomc"], "Desarrollo Urbano", 12],
  [["alumbradopublicoreclamo"], "Desarrollo Urbano", 12],
  [["pavimentoreclamo"], "Desarrollo Urbano", 12],
  [["semaforosreclamo"], "Desarrollo Urbano", 11],
  [["aguascordobesascanoroto"], "Desarrollo Urbano", 12],
  [["aguascordobesasreclamo"], "Desarrollo Urbano", 11],
  [["callesreclamo"], "Desarrollo Urbano", 11],
  [["obrasvialesreclamo"], "Desarrollo Urbano", 12],
  [["veredasreclamo"], "Desarrollo Urbano", 12],
  [["desaguesreclamo"], "Desarrollo Urbano", 12],
  [["callehundimiento"], "Desarrollo Urbano", 12],
  [["obraspublicas"], "Desarrollo Urbano", 11],
  [["obrapublica"], "Desarrollo Urbano", 11],
  [["bache"], "Desarrollo Urbano", 10],
  [["alumbrado"], "Desarrollo Urbano", 9],
  [["pavimento"], "Desarrollo Urbano", 9],
  [["semáforo"], "Desarrollo Urbano", 8],
  [["semaforo"], "Desarrollo Urbano", 8],
  [["caño","roto"], "Desarrollo Urbano", 10],
  [["cloacas"], "Desarrollo Urbano", 9],
  [["hundimiento","calle"], "Desarrollo Urbano", 10],
  [["llaryora"], "General", 9],
  [["llaryoragestion"], "General", 12],
  [["danielpasserini"], "General", 11],
  [["suoem"], "General", 10],
  [["suoemsindicato"], "General", 12],
  [["milei"], "General", 9],
  [["concejodeliberante"], "General", 11],
  [["concejo"], "General", 7],
  [["eleccionintendente"], "General", 12],
  [["intendentes"], "General", 8],
  [["gobernador"], "General", 7],
  [["campanavacunacion"], "Salud", 12],
  [["vacunación","campaña"], "Salud", 11],
  [["dispensario"], "Salud", 11],
  [["vacunas"], "Salud", 10],
  [["salud","mental"], "Salud", 11],
  [["dengue","muertos"], "Salud", 10],
  [["dengue","casos"], "Salud", 9],
  [["personassituaciondecalle"], "Políticas Sociales", 12],
  [["comedoresreclamo"], "Políticas Sociales", 12],
  [["personas","situación","calle"], "Políticas Sociales", 11],
  [["comedor"], "Políticas Sociales", 9],
  [["transporteescolar"], "Educación", 12],
  [["transporte","escolar"], "Educación", 11],
  [["docentes","paro"], "Educación", 11],
  [["nochedeloscpc"], "Participación", 12],
  [["cpcdescentralizacion"], "Participación", 12],
  [["horario","extendido"], "Participación", 10],
  [["teatrocomedia"], "Deporte y Cultura", 12],
  [["nochedelaslecturas"], "Deporte y Cultura", 12],
  [["noche","lecturas"], "Deporte y Cultura", 11],
  [["teatro"], "Deporte y Cultura", 8],
  [["cultura"], "Deporte y Cultura", 8],
  [["musica"], "Deporte y Cultura", 9],
  [["gardel","premios"], "Deporte y Cultura", 11],
  [["inmuebles","alquiler"], "Recursos Tributarios", 11],
  [["vacíos","inmuebles"], "Recursos Tributarios", 12],
  [["tasas","municipales"], "Recursos Tributarios", 11],
  [["cargos","ocultos"], "Recursos Tributarios", 12],
  [["tasas"], "Recursos Tributarios", 7],
  [["juicio","audiencia"], "Tribunal de Faltas", 11],
  [["tribunal","faltas"], "Tribunal de Faltas", 12],
  [["appdenuncias"], "Ciudad Inteligente", 12],
  [["vedi"], "Ciudad Inteligente", 10],
  [["midocta"], "Ciudad Inteligente", 12],
  [["govtech"], "Ciudad Inteligente", 12],
  [["smartcity"], "Ciudad Inteligente", 12],
  [["app","trámites"], "Ciudad Inteligente", 10],
];

const MEDIA_TUPLES = [
  ["Radio Mitre", "Mitre", "Medio"],
  ["APTT", "Aquí Petete", "Programa"],
  ["POP", "Radio Popular", "Medio"],
  ["VV", "Vamos Viendo", "Programa"],
  ["LV3", "Cadena 3", "Medio"],
  ["RADIOINF", "Radio Informe 3", "Programa"],
  ["CONTINENTAL", "Continental", "Medio"],
  ["AENOT", "Alassia es noticia", "Programa"],
  ["Gefinforma", "Ge Informa", "Medio"],
  ["HoyDia", "Hoy Día Córdoba", "Medio"],
  ["Cba24n", "CBA 24 Noticias", "Medio"],
  ["El Doce", "Canal 12", "Medio"],
  ["TELEFE", "Telefe", "Medio"],
  ["LMZ", "La mañana con Zuliani", "Programa"],
  ["C12", "Canal 12", "Medio"],
  ["ACBA", "Arriba Córdoba", "Programa"],
  ["CanalC", "Canal C", "Medio"],
  ["LVeV", "La Voz en Vivo", "Programa"],
  ["SJ", "Siempre Juntos", "Programa"],
  ["SUQUIA", "Radio Suquía", "Medio"],
  ["BDC", "Bien de Córdoba", "Programa"],
  ["MEM", "Mediodía en Mitre", "Programa"],
  ["SDL", "Show del Lagarto", "Programa"],
  ["SUQ", "Radio Suquía", "Medio"],
  ["noticierodoce", "Noticiero Doce", "Programa"],
  ["informadosalregreso", "Informados al Regreso", "Programa"],
  ["TNC", "Telefe Noticias", "Programa"],
  ["TelefeNoticias", "Telefe Noticias", "Programa"],
  ["siestaanimal", "Siesta Animal", "Programa"],
  ["siemprejuntos", "Siempre Juntos", "Programa"],
  ["AquiPetete", "Aquí Petete", "Programa"],
  ["geninforma", "Gen Informa", "Programa"],
  ["lamananaconzuliani", "La mañana con Zuliani", "Programa"],
  ["idayvuelta", "Ida y Vuelta", "Programa"],
  ["AEN", "Alassia es noticia", "Programa"],
  ["alassiaesnoticia", "Alassia es noticia", "Programa"],
  ["TFN", "Telefe Noticias 1ra Ed", "Programa"],
  ["BM", "Buen Mediodía", "Programa"],
  ["SAML", "Siesta Animal", "Programa"],
  ["MT", "Mientras Tanto", "Programa"],
  ["elshowdellagarto", "Show del Lagarto", "Programa"],
  ["NDCE", "Noticiero Doce", "Programa"],
  ["C10", "Canal 10", "Medio"],
  ["VVLR", "Viva la Radio", "Programa"],
  ["‼️LV3", "Cadena 3", "Medio"],
  ["cadena3", "Cadena 3", "Medio"],
  ["CC", "Canal C", "Medio"],
  ["puntalvillamaria", "Puntal Villa Maria", "Medio"],
  ["diarioalfil", "Diario Alfil", "Medio"],
  ["politicacordobaverdad", "Política Cordoba Verdad", "Medio"],
  ["mivalle", "Mi Valle", "Medio"],
  ["economixtv", "Economix TV", "Medio"],
  ["eldoce", "El Doce TV", "Medio"],
  ["elobjetivo", "El Objetivo", "Medio"],
  ["eldiariodecarlospaz", "Diario de Carlos Paz", "Medio"],
  ["clipgo", "Clip GO", "Medio"],
  ["comercioyjusticia", "Comercio y Justicia", "Medio"],
  ["laranchada", "La Ranchada", "Medio"],
  ["jornadapolitica", "Jornada Política", "Medio"],
  ["viapais", "Vía País", "Medio"],
  ["lvdos", "LV 2", "Medio"],
  ["infonegocios", "Info Negocios", "Medio"],
  ["villamariavivo", "Villa Maria Vivo", "Medio"],
  ["derechadiario", "Derecha Diario", "Medio"],
  ["enredaccion", "En Redacción", "Medio"],
  ["lavoz", "La Voz", "Medio"],
  ["lmdiario", "La Nueva Mañana", "Medio"],
  ["entretenimientoscordoba", "Entretenimientos Córdoba", "Medio"],
  ["el-periodico", "El Periódico", "Medio"],
  ["cordoba", "Telefe", "Medio"],
  ["miraelnorte", "Mirá el Norte", "Medio"],
  ["TELEFE TNC", "Telefe", "Medio"],
  ["sierraschicasvivo", "Sierras Chicas Vivo", "Medio"],
  ["SUQUIA,", "Suquia", "Medio"],
  ["SUQ BDC Uber", "Suquia", "Medio"],
  ["Telefe Noticias 1ra Ed", "Telefe Primera Edición", "Programa"],
  ["Radioinforme 3", "Radio Informe 3", "Programa"],
  ["VV Fernando Genesir", "Vamos Viendo", "Programa"],
  ["TUP", "Siesta Animal", "Programa"],
  ["SDP", "Secretos del Poder", "Programa"],
  ["AN", "Ahora Noticias", "Programa"],
  ["JP", "Jornada Política", "Programa"],
  ["FYC", "Fuerte y Claro", "Programa"],
  ["MQH", "Mirá quien habla", "Programa"],
  ["FUTIMP", "Futuro Imperfecto", "Programa"],
  ["AP", "La Argentina Posible", "Programa"],
  ["TND", "TeleNoche Doce", "Programa"],
  ["ETL", "El toque Lalo", "Programa"],
  ["LSM", "La Super Mañana", "Programa"],
  ["IYV", "Ida y vuelta", "Programa"],
  ["CN", "Córdoba Noticias", "Programa"],
  ["MitreCordoba", "Mitre", "Medio"],
  ["IAR", "Informados al Regreso", "Programa"],
  ["DF", "Distrito Federal", "Programa"],
  ["difusionnoticias", "Difusión Noticias", "Medio"],
  ["cordobainteriorinforma", "Córdoba Interior Informa", "Medio"],
  ["puntal", "Puntal", "Medio"],
  ["CCordoba", "C Córdoba", "Medio"],
  ["marcainformativacba", "Marca Informativa Cba", "Medio"],
  ["AM700", "AM 700", "Medio"],
  ["lavozdesanjusto", "La Voz de San Justo", "Medio"],
  ["diariodelasvarillas", "Diario de Las Varillas", "Medio"],
  ["valorlocal", "Valor Local", "Medio"],
  ["puntoapunto", "Punto a Punto", "Medio"],
  ["LV2", "LV 2", "Medio"],
  ["ECDV", "El Club del Vecino", "Programa"],
];

const MEDIA_MAP = {};
for (const [k, d, t] of MEDIA_TUPLES) {
  MEDIA_MAP[k.toLowerCase()] = { display: d, tipo: t };
}

// ── Regexes ──────────────────────────────────
const USTRIP  = /^[\u200e\u200f\u202f\ufeff\u200b]+/;
const URL_RE  = /https?:\/\/[^\s\n\r]+/;
const SKIP_RE = /cifrado|añadió|quitó|imagen omitida|documento omitido|se editó este mensaje/i;

// ── Parsers ──────────────────────────────────
export function parse_wa(text) {
  const msgs = [];
  let cur = null;
  for (const raw of text.split('\n')) {
    const line = raw.replace(USTRIP, '').replace(/\r$/, '');
    const m =
      line.match(/^\[(\d{1,2}\/\d{1,2}\/\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+?):\s*(.*)$/) ||
      line.match(/^(\d{1,2}\/\d{1,2}\/\d{2,4}),?\s+(\d{1,2}:\d{2})\s*[-–]\s*(.+?):\s*(.*)$/);
    if (m) {
      if (cur) msgs.push(cur);
      cur = { date: m[1], time: m[2].slice(0, 5), sender: m[3].trim(), content: m[4] };
    } else if (cur && line.trim()) {
      cur.content += '\n' + line;
    }
  }
  if (cur) msgs.push(cur);
  return msgs;
}

function is_bot(s) {
  const sl = s.toLowerCase();
  return sl.includes('media monitoring') || sl.includes('cvamedios');
}

function lookup(tok) {
  return MEDIA_MAP[tok.toLowerCase().trim()];
}

function get_url(text) {
  const m = text.match(URL_RE);
  return m ? m[0].replace(/[)\]'"]+$/, '') : null;
}

function domain_label(url) {
  try {
    const u = new URL(url);
    let host = u.hostname.replace(/^www\./, '');
    const parts = host.split('.');
    const keys = [host, parts.slice(0, -1).join('.'), parts[0]];
    for (const key of keys) {
      const e = lookup(key);
      if (e) return e.display;
    }
    return parts[0].replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  } catch (e) {
    return '';
  }
}

function parse_mm(content) {
  const ia_match = content.match(/\nIA\.TXT:\s*/);
  let ia_txt = null;
  let main = content;
  if (ia_match) {
    const idx = ia_match.index;
    ia_txt = content.slice(idx + ia_match[0].length).trim();
    main = content.slice(0, idx);
  }
  const url = get_url(main);
  const text_part = url ? main.slice(0, main.indexOf(url)).trim() : main.trim();
  const lines = text_part.split('\n');
  const first_line = lines.length ? lines[0] : '';
  const rest = lines.slice(1)
    .filter(l => l.trim() && !/^\d{2}:\d{2}/.test(l.trim()))
    .join('\n');
  const segs = first_line.split(/\.\s+/);
  let medio = '', programa = '';
  const desc_p = [];
  let in_desc = false;
  for (let seg of segs) {
    seg = seg.trim();
    if (!seg) continue;
    if (in_desc) { desc_p.push(seg); continue; }
    if (/^A\s+V\w*/i.test(seg)) {
      in_desc = true;
      const avo = seg.replace(/^A\s+V\w*\.?\s*/i, '').trim();
      if (avo) desc_p.push(avo);
      continue;
    }
    const entry = lookup(seg);
    if (entry) {
      if (entry.tipo === 'Medio' && !medio) { medio = entry.display; continue; }
      if (entry.tipo === 'Programa' && !programa) { programa = entry.display; continue; }
    }
    if (medio && programa) in_desc = true;
    desc_p.push(seg);
  }
  let desc = desc_p.join('. ');
  if (rest) desc = (desc + '\n' + rest).trim();
  desc = desc.replace(/\d{2}:\d{2}(:\d{2})?/g, '').replace(/\(-\)/g, '').replace(/\(=\)/g, '').trim();
  return { medio, programa, url, desc, ia_txt };
}

function parse_cva(content) {
  const url = get_url(content);
  const text = (url ? content.split(url).join('') : content).trim();
  const tokens = text.split(/[\s.]+/);
  let medio = '', programa = '';
  let used = 0;
  for (let i = 0; i < Math.min(4, tokens.length); i++) {
    const tok = tokens[i];
    const entry = lookup(tok);
    if (entry) {
      if (entry.tipo === 'Medio' && !medio) { medio = entry.display; used = i + 1; }
      else if (entry.tipo === 'Programa' && !programa) { programa = entry.display; used = i + 1; }
    } else if (i > 0 && !medio && !programa) break;
    else if (medio && programa) break;
  }
  let desc = tokens.slice(used).join(' ').replace(/[0-9.\s]+$/, '').trim();
  return { medio, programa, url, desc, ia_txt: null };
}

function score_local(text) {
  const lo = text.toLowerCase();
  const sc = {};
  for (const [kw, cats] of KW_DATA) {
    if (lo.includes(kw.toLowerCase())) {
      for (const cat of cats) {
        if (CATS.includes(cat)) sc[cat] = (sc[cat] || 0) + 1;
      }
    }
  }
  for (const [words, cat, pts] of PHRASE_RULES) {
    if (words.every(w => lo.includes(w.toLowerCase()))) {
      sc[cat] = (sc[cat] || 0) + pts;
    }
  }
  return sc;
}

function best_cats(sc) {
  const entries = Object.entries(sc);
  if (!entries.length) return ['General'];
  entries.sort((a, b) => b[1] - a[1]);
  const top = entries[0][1];
  return entries.filter(([c, v]) => v >= top * 0.6).map(([c]) => c);
}

export function build_items(text) {
  const msgs = parse_wa(text);
  const items = [];
  for (const msg of msgs) {
    if (!is_bot(msg.sender)) continue;
    const c = msg.content.replace(/\u200e/g, '').trim();
    if (SKIP_RE.test(c) || c.length < 5) continue;
    const is_mm = msg.sender.toLowerCase().includes('media monitoring');
    const parsed = is_mm ? parse_mm(c) : parse_cva(c);
    let medio = parsed.medio;
    if (!is_mm && !medio && parsed.url) medio = domain_label(parsed.url);
    const sc = score_local(c + ' ' + (parsed.desc || ''));
    const cats = best_cats(sc);
    items.push({
      date: msg.date, time: msg.time,
      medio, programa: parsed.programa,
      url: parsed.url, desc: parsed.desc,
      ia_txt: parsed.ia_txt,
      title: '', cats,
    });
  }
  return items;
}

// ── Output formatting (mirrors bot.format_message) ──
export function format_message(items, cat_label) {
  const lines = [];
  for (const n of items) {
    const title = n.title || (n.desc || '').slice(0, 70) || '(sin título)';
    const src = [n.medio, n.programa].filter(Boolean).join(' / ') || 'Sin fuente';
    const link = n.url ? `\n\u{1f517} ${n.url}` : '';
    lines.push(`\u2192 *${title}*\n\u2192 ${n.date} ${n.time}  ${src}${link}`);
  }
  const header = `\u{1f4cd} *RESUMEN DE "${cat_label.toUpperCase()}"*`;
  return header + '\n\n' + lines.join('\n\n');
}

if (typeof window !== 'undefined') {
  window.Clipping = { CATS, parse_wa, build_items, format_message };
}
