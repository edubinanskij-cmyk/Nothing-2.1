import math

N = 18
W, R, G = "#ffffff", "#d4202a", "#8c8c8c"


class Icon:
    def __init__(self):
        self.p = {}

    def px(self, x, y, c=W):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < N and 0 <= y < N:
            self.p[(x, y)] = c

    def line(self, x0, y0, x1, y1, c=W):
        x0, y0, x1, y1 = map(lambda v: int(round(v)), (x0, y0, x1, y1))
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def path(self, pts, c=W, close=False):
        for a, b in zip(pts, pts[1:]):
            self.line(*a, *b, c)
        if close:
            self.line(*pts[-1], *pts[0], c)

    def shape(self, pred, edge=W, fill=None):
        ins = {(x, y) for x in range(N) for y in range(N) if pred(x, y)}
        for (x, y) in ins:
            is_edge = any((x + dx, y + dy) not in ins for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if is_edge:
                self.px(x, y, edge)
            elif fill:
                self.px(x, y, fill)

    def poly(self, pts, edge=W, fill=None):
        def pred(x, y):
            inside = False
            n = len(pts)
            j = n - 1
            for i in range(n):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            return inside
        self.shape(pred, edge, fill)

    def circ(self, cx, cy, r, edge=W, fill=None):
        self.shape(lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 <= r * r, edge, fill)

    def rect(self, x0, y0, x1, y1, c=W, fill=None):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if x in (x0, x1) or y in (y0, y1):
                    self.px(x, y, c)
                elif fill:
                    self.px(x, y, fill)

    def arc(self, cx, cy, r, a0, a1, c=W, th=0.55):
        for x in range(N):
            for y in range(N):
                d = math.hypot(x - cx, y - cy)
                if abs(d - r) <= th:
                    a = math.degrees(math.atan2(y - cy, x - cx)) % 360
                    lo, hi = a0 % 360, a1 % 360
                    ok = lo <= a <= hi if lo <= hi else (a >= lo or a <= hi)
                    if ok:
                        self.px(x, y, c)


def home():
    i = Icon()
    i.path([(1, 9), (9, 2), (17, 9)])
    i.path([(3, 8), (3, 16), (15, 16), (15, 8)])
    i.path([(13, 4), (13, 6)])
    i.rect(8, 11, 10, 16, R, R)
    return i


def heart():
    i = Icon()
    def pred(x, y):
        u, v = (x - 8.5) / 7.2, (8.2 - y) / 7.0
        return (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0
    i.shape(pred, W, R)
    return i


def star():
    i = Icon()
    pts = []
    for k in range(10):
        r = 8.4 if k % 2 == 0 else 3.9
        a = -math.pi / 2 + k * math.pi / 5
        pts.append((8.5 + r * math.cos(a), 9.3 + r * math.sin(a)))
    i.poly(pts, W, W)
    i.px(8, 8, R); i.px(9, 8, R); i.px(8, 9, R); i.px(9, 9, R); i.px(8, 10, R); i.px(9, 10, R)
    return i


def bell():
    i = Icon()
    i.path([(8, 2), (9, 2)])
    i.path([(6, 4), (5, 8), (4, 12), (2, 14), (15, 14), (13, 12), (12, 8), (11, 4), (6, 4)])
    i.path([(8, 3), (9, 3)])
    i.circ(8.5, 16, 1.2, R, R)
    i.px(0, 6, G); i.px(17, 6, G)
    return i


def lock():
    i = Icon()
    i.arc(8.5, 7.5, 4, 180, 360)
    i.line(4, 7, 4, 8); i.line(13, 7, 13, 8)
    i.rect(2, 8, 15, 16, W)
    i.rect(2, 8, 15, 9, W, W)
    i.px(8, 12, R); i.px(9, 12, R); i.px(8, 13, R); i.px(9, 13, R); i.px(8, 14, R); i.px(9, 14, R)
    return i


def cloud():
    i = Icon()
    cs = [(5.5, 10, 3.6), (9.5, 7, 4.6), (13.5, 10, 3.6)]
    def pred(x, y):
        if 10 <= y <= 12 and 5.5 <= x <= 13.5:
            return True
        return any((x - a) ** 2 + (y - b) ** 2 <= r * r for a, b, r in cs) and y <= 12
    i.shape(pred, W, None)
    for x in (5, 9, 13):
        i.line(x, 14, x - 1, 16, R)
    return i


def sun():
    i = Icon()
    i.circ(8.5, 8.5, 3.6, W, R)
    for k in range(8):
        a = k * math.pi / 4
        i.line(8.5 + 6 * math.cos(a), 8.5 + 6 * math.sin(a), 8.5 + 8.4 * math.cos(a), 8.5 + 8.4 * math.sin(a))
    return i


def moon():
    i = Icon()
    i.shape(lambda x, y: (x - 8) ** 2 + (y - 9) ** 2 <= 7.8 ** 2 and (x - 12.6) ** 2 + (y - 6) ** 2 > 6.4 ** 2, W, W)
    i.px(5, 10, R); i.px(6, 10, R); i.px(5, 11, R); i.px(6, 11, R)
    i.px(14, 3, R); i.px(16, 9, G); i.px(13, 14, G)
    return i


def battery():
    i = Icon()
    i.rect(1, 5, 14, 12, W)
    i.rect(15, 7, 16, 10, W, W)
    i.rect(3, 7, 4, 10, R, R)
    i.rect(6, 7, 7, 10, G, G)
    i.rect(9, 7, 10, 10, G, G)
    i.rect(12, 7, 12, 10, G, G)
    return i


def wifi():
    i = Icon()
    for r in (4, 7.5, 11):
        i.arc(8.5, 14, r, 225, 315, W, 0.7)
    i.circ(8.5, 14, 1.2, R, R)
    return i


def download():
    i = Icon()
    i.line(8, 1, 8, 10, R); i.line(9, 1, 9, 10, R)
    i.path([(4, 7), (8, 11)], R); i.path([(13, 7), (9, 11)], R)
    i.path([(2, 11), (2, 16), (15, 16), (15, 11)])
    return i


def trash():
    i = Icon()
    i.line(1, 4, 16, 4)
    i.path([(6, 2), (11, 2)])
    i.path([(6, 2), (6, 4)]); i.path([(11, 2), (11, 4)])
    i.path([(3, 4), (4, 16), (13, 16), (14, 4)])
    for x in (6, 8, 10):
        i.line(x, 7, x, 13, R if x == 8 else W)
    return i


def folder():
    i = Icon()
    i.path([(1, 3), (6, 3), (8, 5), (16, 5), (16, 15), (1, 15), (1, 3)])
    i.line(1, 7, 16, 7)
    for x in range(3, 15):
        i.px(x, 10, G)
    i.px(8, 12, R); i.px(9, 12, R)
    return i


def bookmark():
    i = Icon()
    i.path([(4, 1), (13, 1), (13, 16), (8, 12), (4, 16), (4, 1)])
    i.rect(8, 5, 9, 6, R, R)
    return i


def play():
    i = Icon()
    i.circ(8.5, 8.5, 7.8, W, None)
    i.poly([(6.5, 4.5), (6.5, 13), (13.5, 8.7)], R, R)
    return i


def volume():
    i = Icon()
    i.poly([(1, 6.5), (4.5, 6.5), (8.5, 2.5), (8.5, 15.5), (4.5, 11.5), (1, 11.5)], W, None)
    i.arc(9, 9, 4, 315, 45, R, 0.7)
    i.arc(9, 9, 7.2, 315, 45, W, 0.7)
    return i


def mic():
    i = Icon()
    i.shape(lambda x, y: 6 <= x <= 11 and 1 <= y <= 10 and not ((x in (6, 11)) and y in (1,)) , W, None)
    i.arc(8.5, 8, 5.8, 20, 160, W, 0.6)
    i.line(3, 8, 3, 9); i.line(14, 8, 14, 9)
    i.line(8, 14, 8, 16); i.line(9, 14, 9, 16)
    i.line(5, 16, 12, 16)
    i.line(8, 3, 8, 6, R); i.line(9, 3, 9, 6, R)
    return i


def globe():
    i = Icon()
    i.circ(8.5, 8.5, 7.8, W, None)
    i.arc(8.5, 8.5, 7.8, 0, 360, W, 0.1)
    i.shape(lambda x, y: ((x - 8.5) / 3.6) ** 2 + ((y - 8.5) / 7.8) ** 2 <= 1, W, None)
    for x in range(2, 16):
        i.px(x, 8, R if 7 <= x <= 10 else W)
    return i


def bolt():
    i = Icon()
    i.poly([(10.5, 0.5), (3, 10), (7.6, 10), (6.2, 16.8), (14.5, 7), (9.6, 7)], W, W)
    for p in ((9, 4), (8, 6), (7, 8), (10, 8), (9, 10)):
        i.px(*p, R)
    return i


def eye():
    i = Icon()
    i.shape(lambda x, y: abs(y - 8.5) <= 5.3 * max(0.0, 1 - ((x - 8.5) / 8.4) ** 2) ** 0.9 and abs(x - 8.5) <= 8.4, W, None)
    i.circ(8.5, 8.5, 3.0, W, R)
    return i


def cart():
    i = Icon()
    i.path([(0, 2), (3, 2), (5, 11), (14, 11)])
    i.path([(4, 5), (16, 5), (14, 11)])
    i.circ(6.5, 14.5, 1.3, W, W)
    i.circ(12.5, 14.5, 1.3, W, W)
    i.px(8, 8, R); i.px(9, 8, R); i.px(12, 8, R); i.px(13, 8, R)
    return i


def flag():
    i = Icon()
    i.line(3, 1, 3, 16); i.line(4, 1, 4, 16)
    i.poly([(5, 2), (15, 2), (12, 5.2), (15, 8.5), (5, 8.5)], W, R)
    return i


def pencil():
    i = Icon()
    i.path([(2, 16), (3, 11), (12, 2), (15, 5), (6, 14), (2, 16)])
    i.poly([(2, 16), (3.4, 11.8), (6.2, 14.6)], R, R)
    i.line(10, 4, 13, 7)
    i.line(4, 13, 5, 14, R)
    return i


def chart():
    i = Icon()
    i.line(1, 1, 1, 16); i.line(1, 16, 16, 16)
    i.rect(4, 10, 5, 14, W, W)
    i.rect(8, 7, 9, 14, W, W)
    i.rect(12, 3, 13, 14, R, R)
    for x in range(3, 15, 2):
        i.px(x, 1, G)
    return i




# ---------------------------------------------------------------- extra icons

def phone():
    i = Icon()
    i.arc(14, 3, 11, 90, 180, W, 1.5)
    i.line(3, 3, 7, 3); i.line(3, 4, 6, 4); i.line(2, 5, 5, 5)
    i.line(14, 14, 14, 10); i.line(13, 14, 13, 11); i.line(12, 15, 12, 12)
    i.px(10, 5, R); i.px(12, 7, R); i.px(14, 5, R); i.px(10, 3, G); i.px(14, 1, G); i.px(16, 3, G)
    return i


def chat():
    i = Icon()
    i.path([(1, 2), (16, 2), (16, 11), (8, 11), (4, 15), (4, 11), (1, 11), (1, 2)])
    for x in (5, 8, 11):
        i.px(x, 6, R)
        i.px(x + 1, 6, R)
    return i


def camera():
    i = Icon()
    i.rect(1, 5, 16, 15, W)
    i.path([(5, 5), (6, 3), (11, 3), (12, 5)])
    i.circ(8.5, 10, 3.4, W, None)
    i.px(8, 10, R); i.px(9, 10, R); i.px(8, 9, R); i.px(9, 9, R)
    i.px(14, 7, R)
    return i


def photo():
    i = Icon()
    i.rect(1, 2, 16, 15, W)
    i.path([(2, 14), (6, 9), (9, 12), (12, 7), (15, 12)])
    i.px(4, 5, R); i.px(5, 5, R); i.px(4, 6, R); i.px(5, 6, R)
    for x in range(3, 15):
        i.px(x, 14, G)
    return i


def clock():
    i = Icon()
    i.circ(8.5, 8.5, 7.8, W, None)
    i.line(8, 8, 8, 3, R); i.line(9, 8, 9, 3, R)
    i.line(8, 8, 12, 11, R)
    for a in range(12):
        t = a * math.pi / 6
        i.px(8.5 + 6.2 * math.sin(t), 8.5 - 6.2 * math.cos(t), G)
    return i


def gear():
    i = Icon()
    i.circ(8.5, 8.5, 5.6, W, None)
    for k in range(8):
        a = k * math.pi / 4
        cx, cy = 8.5 + 7.2 * math.cos(a), 8.5 + 7.2 * math.sin(a)
        for dx in (-0.5, 0.5):
            for dy in (-0.5, 0.5):
                i.px(cx + dx, cy + dy)
    i.circ(8.5, 8.5, 2.2, R, R)
    return i


def mail():
    i = Icon()
    i.rect(1, 3, 16, 14, W)
    i.path([(1, 3), (8, 9), (9, 9), (16, 3)])
    i.line(1, 14, 6, 9, G); i.line(16, 14, 11, 9, G)
    i.px(8, 11, R); i.px(9, 11, R)
    return i


def pin():
    i = Icon()
    i.shape(lambda x, y: (x - 8.5) ** 2 + (y - 6.5) ** 2 <= 5.6 ** 2 or (y > 6.5 and abs(x - 8.5) <= (14.5 - y) * 0.7 and y <= 14.5), W, None)
    i.circ(8.5, 6.5, 2.0, R, R)
    for x in range(4, 14):
        i.px(x, 16, G)
    return i


def calendar():
    i = Icon()
    i.rect(1, 3, 16, 16, W)
    for x in range(2, 16):
        i.px(x, 4, R); i.px(x, 5, R)
    i.px(5, 1, W); i.px(5, 2, W); i.px(12, 1, W); i.px(12, 2, W)
    for yy in (8, 11, 14):
        for xx in (4, 7, 10, 13):
            i.px(xx, yy, W if (xx, yy) != (10, 11) else R)
    return i


def calc():
    i = Icon()
    i.rect(3, 1, 14, 16, W)
    i.rect(5, 3, 12, 5, R, R)
    for yy in (8, 11, 14):
        for xx in (5, 8, 11):
            i.px(xx, yy, W)
            i.px(xx + 1, yy, W)
    return i


def note():
    i = Icon()
    i.circ(5, 14, 2.4, W, W)
    i.line(7, 14, 7, 3); i.line(8, 14, 8, 3)
    i.line(8, 3, 14, 5, R); i.line(8, 4, 14, 6, R); i.line(14, 5, 14, 9, R)
    i.px(14, 10, R)
    return i


ICONS = [phone, chat, camera, photo, clock, gear,
         mail, pin, calendar, calc, note, home,
         heart, star, bell, lock, cloud, sun,
         moon, battery, wifi, download, trash, folder,
         bookmark, play, volume, mic, globe, bolt,
         eye, cart, flag, pencil, chart]
# names used for drawable ids
NAMES = [f.__name__ for f in ICONS]


# ---------------------------------------------------------------- project writer
import os
import sys
import zipfile
from PIL import Image, ImageDraw

PKG = "com.dotpack.icons"

# best-guess launcher activities of common apps -> icon name
MAP = {
    "phone": ["com.android.dialer/com.android.dialer.DialtactsActivity",
              "com.google.android.dialer/com.google.android.dialer.extensions.GoogleDialtactsActivity",
              "com.samsung.android.dialer/com.samsung.android.dialer.DialtactsActivity"],
    "chat": ["com.google.android.apps.messaging/com.google.android.apps.messaging.ui.ConversationListActivity",
             "com.android.mms/com.android.mms.ui.ConversationList"],
    "camera": ["com.android.camera/com.android.camera.Camera",
               "com.google.android.GoogleCamera/com.android.camera.CameraLauncher",
               "com.sec.android.app.camera/com.sec.android.app.camera.Camera"],
    "photo": ["com.google.android.apps.photos/com.google.android.apps.photos.home.HomeActivity",
              "com.sec.android.gallery3d/com.samsung.android.gallery.app.activity.GalleryActivity",
              "com.android.gallery3d/com.android.gallery3d.app.GalleryActivity"],
    "clock": ["com.google.android.deskclock/com.android.deskclock.DeskClock",
              "com.android.deskclock/com.android.deskclock.DeskClock",
              "com.sec.android.app.clockpackage/com.sec.android.app.clockpackage.ClockPackage"],
    "gear": ["com.android.settings/com.android.settings.Settings"],
    "mail": ["com.google.android.gm/com.google.android.gm.ConversationListActivityGmail"],
    "pin": ["com.google.android.apps.maps/com.google.android.maps.MapsActivity"],
    "calendar": ["com.google.android.calendar/com.android.calendar.AllInOneActivity"],
    "calc": ["com.google.android.calculator/com.android.calculator2.Calculator",
             "com.sec.android.app.popupcalculator/com.sec.android.app.popupcalculator.Calculator"],
    "note": ["com.google.android.apps.youtube.music/com.google.android.apps.youtube.music.activities.MusicActivity"],
    "globe": ["com.android.chrome/com.google.android.apps.chrome.Main"],
    "play": ["com.google.android.youtube/com.google.android.youtube.HomeActivity"],
    "folder": ["com.google.android.apps.nbu.files/com.google.android.apps.nbu.files.home.HomeActivity"],
    "cart": ["com.android.vending/com.android.vending.AssetBrowserActivity"],
}


def render(ic, size=192, S=4):
    big = size * S
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, big - 1, big - 1], radius=int(big * 0.23), fill="#0c0c0c")
    pitch = big / 20.0
    off = (big - (N - 1) * pitch) / 2
    for x in range(N):
        for y in range(N):
            cx, cy = off + x * pitch, off + y * pitch
            c = ic.p.get((x, y))
            r, col = (pitch * 0.42, c) if c else (pitch * 0.12, "#2f2f2f")
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return im.resize((size, size), Image.LANCZOS)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build_project(out):
    a = os.path.join(out, "app", "src", "main")
    write(os.path.join(out, "settings.gradle"),
          "pluginManagement {\n    repositories { google(); mavenCentral(); gradlePluginPortal() }\n}\n"
          "dependencyResolutionManagement {\n    repositories { google(); mavenCentral() }\n}\n"
          "rootProject.name = \"DotIcons\"\ninclude ':app'\n")
    write(os.path.join(out, "build.gradle"),
          "plugins {\n    id 'com.android.application' version '8.5.2' apply false\n}\n")
    write(os.path.join(out, "gradle.properties"),
          "org.gradle.jvmargs=-Xmx2g\nandroid.useAndroidX=true\n")
    write(os.path.join(out, "app", "build.gradle"),
          "plugins {\n    id 'com.android.application'\n}\n\n"
          "android {\n    namespace '" + PKG + "'\n    compileSdk 34\n\n"
          "    defaultConfig {\n        applicationId '" + PKG + "'\n        minSdk 21\n"
          "        targetSdk 34\n        versionCode 1\n        versionName '1.0'\n    }\n\n"
          "    buildTypes {\n        release {\n            minifyEnabled false\n        }\n    }\n}\n")

    intents = ""
    for action, cat in (("com.novalauncher.THEME", "com.novalauncher.category.CUSTOM_ICON_PICKER"),
                        ("org.adw.launcher.THEMES", "android.intent.category.DEFAULT"),
                        ("org.adw.launcher.icons.ACTION_PICK_ICON", "android.intent.category.DEFAULT"),
                        ("com.anddoes.launcher.THEME", "android.intent.category.DEFAULT"),
                        ("com.teslacoilsw.launcher.THEME", "android.intent.category.DEFAULT")):
        intents += ('            <intent-filter>\n                <action android:name="%s" />\n'
                    '                <category android:name="%s" />\n            </intent-filter>\n' % (action, cat))
    write(os.path.join(a, "AndroidManifest.xml"),
          '<?xml version="1.0" encoding="utf-8"?>\n'
          '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n'
          '    <application\n        android:allowBackup="false"\n        android:icon="@drawable/ic_launcher"\n'
          '        android:label="Dot Icons">\n'
          '        <activity\n            android:name=".MainActivity"\n            android:exported="true">\n'
          '            <intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n'
          '                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>\n'
          + intents +
          '        </activity>\n    </application>\n</manifest>\n')
    write(os.path.join(a, "java", *PKG.split("."), "MainActivity.java"),
          "package " + PKG + ";\n\n"
          "import android.app.Activity;\nimport android.graphics.Color;\nimport android.os.Bundle;\n"
          "import android.view.Gravity;\nimport android.widget.TextView;\n\n"
          "public class MainActivity extends Activity {\n"
          "    @Override\n    protected void onCreate(Bundle b) {\n        super.onCreate(b);\n"
          "        TextView t = new TextView(this);\n"
          "        t.setText(\"Dot Icons\\n\\nВідкрий налаштування лаунчера і вибери пак іконок Dot Icons.\");\n"
          "        t.setTextColor(Color.WHITE);\n        t.setTextSize(18);\n        t.setPadding(48, 48, 48, 48);\n"
          "        t.setGravity(Gravity.CENTER);\n        t.setBackgroundColor(Color.parseColor(\"#0c0c0c\"));\n"
          "        setContentView(t);\n    }\n}\n")

    res = os.path.join(a, "res", "drawable-nodpi")
    os.makedirs(res, exist_ok=True)
    for fn in ICONS:
        render(fn()).save(os.path.join(res, "ic_%s.png" % fn.__name__))
    render(star()).save(os.path.join(res, "ic_launcher.png"))

    items = ""
    for name, comps in MAP.items():
        for c in comps:
            items += '    <item component="ComponentInfo{%s}" drawable="ic_%s" />\n' % (c, name)
    appfilter = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <scale factor="1.0" />\n' + items + '</resources>\n'
    write(os.path.join(a, "res", "xml", "appfilter.xml"), appfilter)
    write(os.path.join(a, "assets", "appfilter.xml"), appfilter)
    dr = ('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <version>1</version>\n'
          '    <category title="All" />\n'
          + "".join('    <item drawable="ic_%s" />\n' % n for n in NAMES) + '</resources>\n')
    write(os.path.join(a, "res", "xml", "drawable.xml"), dr)
    write(os.path.join(a, "assets", "drawable.xml"), dr)


def zip_dir(src, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(src):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, os.path.dirname(src)))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "project"
    build_project(out)
    print("project written to", out, "with", len(ICONS), "icons")
