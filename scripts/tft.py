"""TFT (云顶之弈) input helper.

Coordinates are in the 1456x819 screenshot frame (the frame the computer-use
screenshot tool reports when the game fills the screen). They are mapped onto
the TFT window's client area, so clicks land correctly at any resolution.

Usage:  py -3.14 tft.py "CMD ; CMD ; ..."
Commands:
  r X Y [ms]        right press-hold-release (default 100ms; use 150-400)
  l X Y [ms]        left press-hold-release
  d X1 Y1 X2 Y2     left drag (units, items, anvils, selling)
  dh X1 Y1 X2 Y2 MS left drag, hovering MS over the target before release (Sprykin rider)
  m X Y             move mouse (hover for tooltips)
  k KEY             tap a key (w = field/bench the hovered unit, d = reroll, f = XP)
  w MS              wait MS milliseconds
  fit               resize the TFT window so its client area covers the whole screen
  info              print screen size and TFT window/client rects
"""
import ctypes, sys, time
from ctypes import wintypes

u = ctypes.windll.user32
k32 = ctypes.windll.kernel32
u.SetProcessDPIAware()
IW, IH = 1456.0, 819.0

ULONG_PTR = ctypes.c_size_t
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]
class INPUT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("pad", ctypes.c_byte * 32)]
    _anonymous_ = ("u",)
    _fields_ = [("type", wintypes.DWORD), ("u", _U)]

def mouse(flags, ax=0, ay=0):
    i = INPUT(type=0); i.mi = MOUSEINPUT(ax, ay, 0, flags, 0, 0)
    u.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))

def key(vk, up=False):
    scan = u.MapVirtualKeyW(vk, 0)
    i = INPUT(type=1); i.ki = KEYBDINPUT(0, scan, 0x8 | (0x2 if up else 0), 0, 0)
    u.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))

def find_tft():
    # The game window title is "TFT" padded with spaces; FindWindow on "TFT" misses it.
    found = []
    P = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    def cb(h, l):
        n = u.GetWindowTextLengthW(h)
        if n and u.IsWindowVisible(h):
            b = ctypes.create_unicode_buffer(n + 1); u.GetWindowTextW(h, b, n + 1)
            if b.value.strip() == "TFT": found.append(h)
        return True
    u.EnumWindows(P(cb), 0)
    return found[0] if found else 0

def client_rect(hwnd):
    r = wintypes.RECT(); u.GetClientRect(hwnd, ctypes.byref(r))
    pt = wintypes.POINT(0, 0); u.ClientToScreen(hwnd, ctypes.byref(pt))
    return pt.x, pt.y, r.right, r.bottom

def move(x, y):
    sw, sh = u.GetSystemMetrics(0), u.GetSystemMetrics(1)
    left, top, cw, ch = 0, 0, sw, sh
    hwnd = find_tft()
    if hwnd:
        l, t, w, h = client_rect(hwnd)
        if w > 0 and h > 0:
            left, top, cw, ch = l, t, w, h
    px, py = left + x * cw / IW, top + y * ch / IH
    # SendInput mouse *moves* are sometimes rejected (returns 0, error 87) while
    # button events still go through; SetCursorPos always works, so use it.
    u.SetCursorPos(int(px), int(py))

def focus():
    # Other apps (e.g. the Claude desktop app) steal focus; input sent while TFT is
    # in the background is silently dropped. Force TFT to the foreground first.
    hwnd = find_tft()
    if not hwnd:
        return
    for i in range(5):
        if u.GetForegroundWindow() == hwnd:
            if i > 0:
                time.sleep(2.0)  # the game may switch display mode on focus
            return
        fg = u.GetForegroundWindow()
        cur = k32.GetCurrentThreadId()
        fgt = u.GetWindowThreadProcessId(fg, None)
        u.AttachThreadInput(cur, fgt, True)
        u.keybd_event(0x12, 0, 0, 0); u.keybd_event(0x12, 0, 2, 0)
        u.BringWindowToTop(hwnd)
        u.SetForegroundWindow(hwnd)
        u.AttachThreadInput(cur, fgt, False)
        time.sleep(0.15)

def fit():
    hwnd = find_tft()
    if not hwnd:
        print("TFT window not found"); return
    sw, sh = u.GetSystemMetrics(0), u.GetSystemMetrics(1)
    u.ShowWindow(hwnd, 9); time.sleep(0.5)  # restore from maximized
    wr = wintypes.RECT(); u.GetWindowRect(hwnd, ctypes.byref(wr))
    l, t, w, h = client_rect(hwnd)
    bl, bt = l - wr.left, t - wr.top                      # border/title offsets
    br, bb = wr.right - (l + w), wr.bottom - (t + h)
    u.SetWindowPos(hwnd, 0, -bl, -bt, sw + bl + br, sh + bt + bb, 0x0004 | 0x0020)
    time.sleep(2.0)

def info():
    sw, sh = u.GetSystemMetrics(0), u.GetSystemMetrics(1)
    hwnd = find_tft()
    print("screen", sw, sh, "tft_hwnd", hwnd)
    if hwnd:
        print("client(left,top,w,h)", client_rect(hwnd), "foreground", u.GetForegroundWindow() == hwnd)

def autofit():
    # The game drops out of fullscreen whenever it loses focus and comes back as a
    # small window; coordinates still map, but refit so screenshots match 1456x819.
    hwnd = find_tft()
    if not hwnd:
        return
    sw, sh = u.GetSystemMetrics(0), u.GetSystemMetrics(1)
    l, t, w, h = client_rect(hwnd)
    if (l, t, w, h) != (0, 0, sw, sh):
        fit()

VK = {"space": 0x20, "esc": 0x1B, "enter": 0x0D}
focus()
autofit()
for cmd in " ".join(sys.argv[1:]).split(";"):
    a = cmd.split()
    if not a:
        continue
    c, v = a[0], a[1:]
    if c != "w":
        focus()
    if c in ("r", "l"):
        move(float(v[0]), float(v[1])); time.sleep(0.12)
        move(float(v[0]) + 0.5, float(v[1])); time.sleep(0.12)  # game drops clicks that arrive right after a jump
        dn, up = (0x8, 0x10) if c == "r" else (0x2, 0x4)
        mouse(dn); time.sleep(int(v[2]) / 1000 if len(v) > 2 else 0.1); mouse(up)
    elif c in ("d", "dh"):
        # dh X1 Y1 X2 Y2 MS: drag and hover over the target for MS before releasing
        # (needed e.g. to set a Sprykin as the rider of the Big Furry Friend).
        x1, y1, x2, y2 = map(float, v[:4])
        hold = int(v[4]) / 1000 if c == "dh" and len(v) > 4 else 0.12
        move(x1, y1); time.sleep(0.08); mouse(0x2); time.sleep(0.12)
        for s in range(1, 11):
            move(x1 + (x2 - x1) * s / 10, y1 + (y2 - y1) * s / 10); time.sleep(0.02)
        time.sleep(hold); mouse(0x4)
    elif c == "m":
        move(float(v[0]), float(v[1]))
    elif c == "k":
        vk = VK[v[0].lower()] if v[0].lower() in VK else ord(v[0].upper())
        key(vk); time.sleep(0.06); key(vk, True)
    elif c == "w":
        time.sleep(int(v[0]) / 1000)
    elif c == "fit":
        fit()
    elif c == "info":
        info()
    time.sleep(0.12)
print("ok fg_is_tft", u.GetForegroundWindow() == find_tft())
