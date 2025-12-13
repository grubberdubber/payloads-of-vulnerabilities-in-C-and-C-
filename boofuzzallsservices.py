#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

import argparse
import os
from datetime import datetime

from boofuzz import (
    Session,
    Target,
    SocketConnection,
    FuzzLoggerText,
    s_initialize,
    s_static,
    s_string,
    s_word,
    s_dword,
    s_byte,
    s_delim,
    s_get
)

# =========================
# Crash Logger REAL
# =========================
CRASH_DIR = "crashes"

class CrashLogger(FuzzLoggerText):
    def log_fail(self, description):
        super().log_fail(description)

        if not os.path.exists(CRASH_DIR):
            os.makedirs(CRASH_DIR)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{CRASH_DIR}/crash_{ts}.log"

        with open(filename, "w") as f:
            f.write("=== BOOFUZZ CRASH ===\n")
            f.write(f"Time: {ts}\n")
            f.write(f"Description: {description}\n")

        print(f"[!] Crash guardado en {filename}")

# =========================
# Session
# =========================
def create_session(host, port):
    return Session(
        target=Target(
            connection=SocketConnection(
                host,
                port,
                proto="tcp"
            )
        ),
        sleep_time=0.3,
        restart_threshold=1,
        fuzz_loggers=[CrashLogger()],
    )

# ================= FTP =================
def ftp(session):
    s_initialize("ftp_user")
    s_static("USER ")
    s_string("anonymous")
    s_static("\r\n")

    s_initialize("ftp_pass")
    s_static("PASS ")
    s_string("test")
    s_static("\r\n")

    s_initialize("ftp_cmd")
    s_string("LIST")
    s_static(" ")
    s_string("/")
    s_static("\r\n")

    session.connect(s_get("ftp_user"))
    session.connect(s_get("ftp_user"), s_get("ftp_pass"))
    session.connect(s_get("ftp_pass"), s_get("ftp_cmd"))

# ================= SMTP =================
def smtp(session):
    s_initialize("smtp_helo")
    s_static("HELO ")
    s_string("example.com")
    s_static("\r\n")

    session.connect(s_get("smtp_helo"))

# ================= POP3 =================
def pop3(session):
    s_initialize("pop3_user")
    s_static("USER ")
    s_string("test")
    s_static("\r\n")

    session.connect(s_get("pop3_user"))

# ================= IMAP =================
def imap(session):
    s_initialize("imap_login")
    s_string("A001")
    s_static(" LOGIN ")
    s_string("user")
    s_static(" ")
    s_string("pass")
    s_static("\r\n")

    session.connect(s_get("imap_login"))

# ================= SIP =================
def sip(session):
    s_initialize("sip_invite")
    s_static("INVITE sip:")
    s_string("user@domain.com")
    s_static(" SIP/2.0\r\n\r\n")

    session.connect(s_get("sip_invite"))

# ================= RTSP =================
def rtsp(session):
    s_initialize("rtsp_opt")
    s_static("OPTIONS rtsp://")
    s_string("127.0.0.1")
    s_static("/ RTSP/1.0\r\n\r\n")

    session.connect(s_get("rtsp_opt"))

# ================= HTTP =================
def http(session):
    s_initialize("http_req")
    s_static("GET /")
    s_string("api")
    s_static(" HTTP/1.1\r\nHost: ")
    s_string("localhost")
    s_static("\r\n\r\n")

    session.connect(s_get("http_req"))

# ================= BINARIO =================
def binary(session):
    s_initialize("binary")
    s_dword(0x41414141)
    s_word(0x1337)
    s_byte(0x01)
    s_string("DATA")

    session.connect(s_get("binary"))

# ================= TEXTO =================
def text(session):
    s_initialize("text")
    s_string("CMD")
    s_delim(" ")
    s_string("ARG")
    s_static("\n")

    session.connect(s_get("text"))

# ================= MAIN =================
def main():
    parser = argparse.ArgumentParser(description="Boofuzz Multi-Protocol Framework")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument(
        "--proto",
        required=True,
        choices=[
            "ftp", "smtp", "pop3", "imap",
            "sip", "rtsp", "http",
            "binary", "text"
        ]
    )

    args = parser.parse_args()

    print("[+] Web UI disponible en http://127.0.0.1:26000")

    session = create_session(args.host, args.port)

    protocols = {
        "ftp": ftp,
        "smtp": smtp,
        "pop3": pop3,
        "imap": imap,
        "sip": sip,
        "rtsp": rtsp,
        "http": http,
        "binary": binary,
        "text": text
    }

    protocols[args.proto](session)
    session.fuzz()

if __name__ == "__main__":
    main()
