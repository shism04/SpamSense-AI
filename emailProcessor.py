import pandas as pd
import re 

class EmailProcessor:
    """
    EmailProcessor Class: 
    1. Extracts header and body from raw email strings.
    2. Performs feature engineering on headers.
    3. Generates text embeddings for the email body.
    """
    def __init__(self, embedding_model):
        self.__embedding_model = embedding_model
    
    def transform_raw_email(self, raw_input):
        """Main pipeline to transform raw string into a feature dictionary."""
        email_split = self.__dividir_correo(raw_input)
        header = email_split["header"]
        body = email_split["body"]

        # Add the new engineered features
        transformed_email = {
            "num_received_headers": self.__num_received_headers(header),
            "received_first_ip_is_private": self.__received_first_ip_is_private(header),
            "from_returnpath_match": self.__from_returnpath_match(header),
            "reply_to_differs_from_from": self.__reply_to_differs_from_from(header),
            "message_id_missing": self.__message_id_missing(header),
            "message_id_matches_from": self.__message_id_matches_from(header),
            "message_id_is_random": self.__message_id_is_random(header),
            "subject_length": self.__subject_length(header),
            "subject_starts_with_re_fwd": self.__subject_starts_with_re_fwd(header),
            "num_recipients": self.__num_recipients(header),
            "to_contains_undisclosed_recipients": self.__to_contains_undisclosed_recipients(header),
            "is_html": self.__is_html(header),
            "is_multipart": self.__is_multipart(header),
            "num_list_headers": self.__num_list_headers(header)
        }

        # Add the body embedding
        emb_vector = self.__embed_correo(body)
        for i in range(len(emb_vector)):
            transformed_email[f"emb_{i}"] = emb_vector[i]
        
        return pd.DataFrame([transformed_email])

    # --- Internal Utilities ---

    def __dividir_correo(self, raw_input):
        # Splits based on the first double newline (standard RFC 822 separator)
        parts = raw_input.split("\n\n", 1)
        return {
            "header": parts[0],
            "body": parts[1] if len(parts) > 1 else ""
        }

    def __get_cabecera(self, cabecera_str, nombre_cabecera):
        patron = rf"^{nombre_cabecera}:\s*(.*)$"
        match = re.search(patron, cabecera_str, flags=re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else None

    # --- Header Feature Engineering ---

    def __num_received_headers(self, header):
        return len(re.findall(r'^Received:', header, flags=re.IGNORECASE | re.MULTILINE))

    def __received_first_ip_is_private(self, header):
        patrones_privados = [r'^10\.', r'^192\.168\.', r'^172\.(1[6-9]|2\d|3[0-1])\.']
        received_headers = re.findall(r'^Received: (.*)$', header, flags=re.IGNORECASE | re.MULTILINE)
        if not received_headers:
            return 0
        first_hop = received_headers[-1]
        ip_match = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", first_hop)
        if not ip_match:
            return 0
        ip = ip_match.group(1)
        return int(any(re.match(p, ip) for p in patrones_privados))

    def __from_returnpath_match(self, header):
        from_c = self.__get_cabecera(header, "From")
        rpath = self.__get_cabecera(header, "Return-Path")
        if not from_c or not rpath: return 0
        d_from = re.findall(r"@([\w\.-]+)", from_c)
        d_rp = re.findall(r"@([\w\.-]+)", rpath)
        if not d_from or not d_rp: return 0
        return int(d_from[0].lower() != d_rp[0].lower())

    def __reply_to_differs_from_from(self, header):
        from_c = self.__get_cabecera(header, "From")
        reply_to = self.__get_cabecera(header, "Reply-To")
        if not from_c or not reply_to: return 0
        d_from = re.findall(r"@([\w\.-]+)", from_c)
        d_rt = re.findall(r"@([\w\.-]+)", reply_to)
        if not d_from or not d_rt: return 0
        return int(d_from[0].lower() != d_rt[0].lower())

    def __message_id_missing(self, header):
        return int(self.__get_cabecera(header, 'Message-ID') is None)

    def __message_id_matches_from(self, header):
        from_c = self.__get_cabecera(header, "From")
        msgid = self.__get_cabecera(header, "Message-ID")
        if not from_c or not msgid: return 0
        d_from = re.findall(r"@([\w\.-]+)", from_c)
        d_msg = re.findall(r"@([\w\.-]+)", msgid)
        if not d_from or not d_msg: return 0
        return int(d_from[0].lower() != d_msg[0].lower())

    def __message_id_is_random(self, header):
        msgid = self.__get_cabecera(header, "Message-ID")
        if not msgid: return 0
        local = msgid.split("@")[0]
        return int(bool(len(local) > 25 and re.search(r"[A-Za-z]", local) and re.search(r"\d", local)))

    def __subject_length(self, header):
        sub = self.__get_cabecera(header, "Subject")
        return len(sub) if sub else 0

    def __subject_starts_with_re_fwd(self, header):
        sub = self.__get_cabecera(header, "Subject") or ""
        return int(bool(re.match(r"^(re:|fwd:)", sub, flags=re.IGNORECASE)))

    def __num_recipients(self, header):
        to = self.__get_cabecera(header, "To") or ""
        cc = self.__get_cabecera(header, "CC") or ""
        return len(re.findall(r"@[\w\.-]+", to)) + len(re.findall(r"@[\w\.-]+", cc))

    def __to_contains_undisclosed_recipients(self, header):
        to = self.__get_cabecera(header, "To") or ""
        return int("undisclosed" in to.lower())

    def __is_html(self, header):
        ct = self.__get_cabecera(header, "Content-Type") or ""
        return int("text/html" in ct.lower())

    def __is_multipart(self, header):
        ct = self.__get_cabecera(header, "Content-Type") or ""
        return int("multipart/" in ct.lower())

    def __num_list_headers(self, header):
        return len(re.findall(r"^List-[A-Za-z\-]+:", header, flags=re.IGNORECASE | re.MULTILINE))

    # --- Body Feature Engineering ---

    def __limpiar_texto(self, texto):
        texto = re.sub(r"<.*?>", "", texto)
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()
    
    def __embed_correo(self, body):
        cuerpo_limpio = self.__limpiar_texto(body)
        return self.__embedding_model.encode(cuerpo_limpio, convert_to_numpy=True).tolist()