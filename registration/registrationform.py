"""
Registration form for GeoChallenge – built with Panda3D DirectGUI.

Flow
----
1. User fills in Nickname / Email / Password / Confirm Password and clicks
   "Register".
2. On success a 6-character verification code is sent to the supplied email
   address (requires SMTP env-vars; see emailverification.py).
   If the email cannot be sent the code is displayed on-screen so that local
   testing still works.
3. User enters the code on the verification screen and clicks "Verify".
4. On success *on_success(nickname)* is called so the caller can start the
   game.  *on_cancel()* is called when the user dismisses the form.
"""

import re

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel

from registration.emailverification import SendError, send_verification_email
from registration.userstore import create_user, init_db, verify_email

# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------
_EMAIL_RE = re.compile(
    r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
)
_MIN_NICKNAME = 3
_MIN_PASSWORD = 6

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
_FRAME_BG = (0.09, 0.11, 0.21, 0.96)
_TITLE_FG = (1.0, 0.85, 0.30, 1.0)
_LABEL_FG = (0.85, 0.85, 0.95, 1.0)
_ERR_FG   = (1.0, 0.35, 0.35, 1.0)
_OK_FG    = (0.35, 1.0, 0.35, 1.0)
_WARN_FG  = (1.0, 0.80, 0.20, 1.0)
_CLEAR    = (0.0, 0.0, 0.0, 0.0)

_LABEL_SCALE  = 0.045
_TITLE_SCALE  = 0.060
_ENTRY_SCALE  = 0.050
_ENTRY_WIDTH  = 12        # characters visible before scrolling
_BTN_SCALE    = 0.070


class RegistrationForm:
    """
    Two-screen registration overlay (registration → email verification).

    Parameters
    ----------
    on_success : callable(nickname: str) | None
        Called after successful email verification.
    on_cancel : callable() | None
        Called when the user dismisses the form without registering.
    """

    def __init__(self, on_success=None, on_cancel=None):
        self._on_success = on_success
        self._on_cancel  = on_cancel

        self._pending_token    = None
        self._pending_email    = None
        self._pending_nickname = None

        init_db()
        self._build_registration_screen()

    # ------------------------------------------------------------------
    # Screen 1 – Registration
    # ------------------------------------------------------------------

    def _build_registration_screen(self):
        self._reg_frame = DirectFrame(
            frameColor=_FRAME_BG,
            frameSize=(-0.65, 0.65, -0.56, 0.56),
            pos=(0, 0, 0),
        )

        _make_label(
            self._reg_frame,
            'GeoChallenge \u2013 New Registration',
            (0, 0, 0.46),
            scale=_TITLE_SCALE,
            fg=_TITLE_FG,
        )

        self._nickname_entry = _make_field(
            self._reg_frame, 'Nickname:', z_row=0.28
        )
        self._email_entry = _make_field(
            self._reg_frame, 'Email:', z_row=0.12
        )
        self._password_entry = _make_field(
            self._reg_frame, 'Password:', z_row=-0.04, obscured=True
        )
        self._confirm_entry = _make_field(
            self._reg_frame, 'Confirm Password:', z_row=-0.20, obscured=True
        )

        self._reg_status = DirectLabel(
            parent=self._reg_frame,
            text='',
            text_scale=_LABEL_SCALE,
            text_fg=_ERR_FG,
            pos=(0, 0, -0.34),
            frameColor=_CLEAR,
        )

        DirectButton(
            parent=self._reg_frame,
            text='Register',
            scale=_BTN_SCALE,
            pos=(-0.22, 0, -0.46),
            command=self._on_register,
        )
        DirectButton(
            parent=self._reg_frame,
            text='Cancel',
            scale=_BTN_SCALE,
            pos=(0.22, 0, -0.46),
            command=self._on_cancel_clicked,
        )

    # ------------------------------------------------------------------
    # Screen 2 – Email verification
    # ------------------------------------------------------------------

    def _build_verification_screen(self):
        self._verify_frame = DirectFrame(
            frameColor=_FRAME_BG,
            frameSize=(-0.60, 0.60, -0.44, 0.44),
            pos=(0, 0, 0),
        )

        _make_label(
            self._verify_frame,
            'Email Verification',
            (0, 0, 0.34),
            scale=_TITLE_SCALE,
            fg=_TITLE_FG,
        )
        _make_label(
            self._verify_frame,
            f'A verification code was sent to:\n{self._pending_email}',
            (0, 0, 0.19),
            scale=_LABEL_SCALE,
            fg=_LABEL_FG,
        )

        self._token_entry = _make_field(
            self._verify_frame, 'Code:', z_row=0.02
        )

        self._verify_status = DirectLabel(
            parent=self._verify_frame,
            text='',
            text_scale=_LABEL_SCALE,
            text_fg=_ERR_FG,
            pos=(0, 0, -0.14),
            frameColor=_CLEAR,
        )

        DirectButton(
            parent=self._verify_frame,
            text='Verify',
            scale=_BTN_SCALE,
            pos=(-0.20, 0, -0.32),
            command=self._on_verify,
        )
        DirectButton(
            parent=self._verify_frame,
            text='Back',
            scale=_BTN_SCALE,
            pos=(0.20, 0, -0.32),
            command=self._on_back,
        )

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_register(self):
        nickname = self._nickname_entry.get().strip()
        email    = self._email_entry.get().strip()
        password = self._password_entry.get()
        confirm  = self._confirm_entry.get()

        error = _validate(nickname, email, password, confirm)
        if error:
            self._set_reg_status(error, ok=False)
            return

        try:
            token = create_user(nickname, email, password)
        except ValueError as exc:
            self._set_reg_status(str(exc), ok=False)
            return

        self._pending_token    = token
        self._pending_email    = email
        self._pending_nickname = nickname

        email_sent = True
        try:
            send_verification_email(email, nickname, token)
        except SendError:
            email_sent = False

        self._reg_frame.hide()
        self._build_verification_screen()

        if not email_sent:
            self._verify_status['text'] = (
                'Email could not be sent.\nYour code: ' + token
            )
            self._verify_status['text_fg'] = _WARN_FG

    def _on_cancel_clicked(self):
        self._reg_frame.destroy()
        if self._on_cancel:
            self._on_cancel()

    def _on_verify(self):
        code = self._token_entry.get().strip().upper()
        if verify_email(code):
            self._verify_frame.destroy()
            if self._on_success:
                self._on_success(self._pending_nickname)
        else:
            self._verify_status['text'] = (
                'Invalid or expired code. Please try again.'
            )
            self._verify_status['text_fg'] = _ERR_FG

    def _on_back(self):
        self._verify_frame.destroy()
        self._reg_frame.show()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _set_reg_status(self, msg: str, ok: bool = True) -> None:
        self._reg_status['text']    = msg
        self._reg_status['text_fg'] = _OK_FG if ok else _ERR_FG


# ---------------------------------------------------------------------------
# Validation helper (module-level)
# ---------------------------------------------------------------------------

def _validate(nickname: str, email: str,
              password: str, confirm: str) -> str | None:
    """Return an error message string, or None if all inputs are valid."""
    if len(nickname) < _MIN_NICKNAME:
        return f'Nickname must be at least {_MIN_NICKNAME} characters.'
    if not _EMAIL_RE.match(email):
        return 'Please enter a valid email address.'
    if len(password) < _MIN_PASSWORD:
        return f'Password must be at least {_MIN_PASSWORD} characters.'
    if password != confirm:
        return 'Passwords do not match.'
    return None


# ---------------------------------------------------------------------------
# Layout helpers (module-level to keep the class concise)
# ---------------------------------------------------------------------------

def _make_label(parent, text, pos, scale=_LABEL_SCALE, fg=_LABEL_FG):
    """Create a transparent-background DirectLabel."""
    return DirectLabel(
        parent=parent,
        text=text,
        text_scale=scale,
        text_fg=fg,
        pos=pos,
        frameColor=_CLEAR,
    )


def _make_field(parent, label_text: str, z_row: float,
                obscured: bool = False) -> DirectEntry:
    """
    Create a right-aligned label above a DirectEntry and return the entry.

    The label sits slightly above the entry baseline (*z_row* + 0.055).
    """
    _make_label(
        parent,
        label_text,
        (-0.55, 0, z_row + 0.055),
        scale=_LABEL_SCALE,
        fg=_LABEL_FG,
    )
    # Override the default left-align so label text anchors to the left edge
    # of the X position given above.
    entry = DirectEntry(
        parent=parent,
        text='',
        scale=_ENTRY_SCALE,
        pos=(-0.55, 0, z_row),
        width=_ENTRY_WIDTH,
        numLines=1,
        obscured=obscured,
    )
    return entry
