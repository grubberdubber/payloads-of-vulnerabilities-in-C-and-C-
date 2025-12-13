#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

TARGET_IP = "127.0.0.1"
TARGET_PORT = 21   # CAMBIA SEGÚN SERVICIO

def create_session():
    return Session(
        target=Target(
            connection=SocketConnection(
                TARGET_IP,
                TARGET_PORT,
                proto="tcp"
            )
        ),
        sleep_time=0.3,
        restart_threshold=1,
        fuzz_loggers=[FuzzLoggerText()],
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

# ================= BINARIO TCP =================
def binary(session):
    s_initialize("bin")
    s_dword(0x41414141)
    s_word(0x1337)
    s_byte(0x01)
    s_string("DATA")

    session.connect(s_get("bin"))

# ================= TEXTO =================
def text(session):
    s_initialize("text")
    s_string("CMD")
    s_delim(" ")
    s_string("ARG")
    s_static("\n")

    session.connect(s_get("text"))

# ================= MAIN =================
if __name__ == "__main__":
    session = create_session()

    # ACTIVA SOLO UNO A LA VEZ
    ftp(session)
    # smtp(session)
    # pop3(session)
    # imap(session)
    # sip(session)
    # rtsp(session)
    # http(session)
    # binary(session)
    # text(session)

    session.fuzz()
