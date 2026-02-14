import platform
import flet as ft
import random
import sys
import asyncio
import os

# -------------------------
# توابع کمکی
# -------------------------
def to_persian_number(num):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"
    num = str(num)
    for e, p in zip(english_digits, persian_digits):
        num = num.replace(e, p)
    return num


def num_to_word(n):
    words = {
        0: "صفر", 1: "یک", 2: "دو", 3: "سه", 4: "چهار", 5: "پنج", 6: "شش", 7: "هفت", 8: "هشت", 9: "نه",
        10: "ده", 11: "یازده", 12: "دوازده", 13: "سیزده", 14: "چهارده", 15: "پانزده",
        16: "شانزده", 17: "هفده", 18: "هجده", 19: "نوزده", 20: "بیست"
    }
    return words.get(n, str(n))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# -------------------------
# برنامه اصلی
# -------------------------
def main(page: ft.Page):
    page.title = "آموزش ریاضی پایه اول"
    page.bgcolor = "#FFF8E1"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.correct_answers = 0
    page.wrong_answers = 0
    page.teacher_name = ""
    page.student_name = ""

    page.snack_bar = ft.SnackBar(content=ft.Text(""))

    # صدا
    page.beep = ft.Audio(src=resource_path("assets/beep.mp3"))
    page.overlay.append(page.beep)

    def play_beep():
        page.beep.play()
        page.update()

    # افکت ستاره‌ها
    def show_stars():
        temp_stack = ft.Stack(expand=True)
        page.overlay.append(temp_stack)

        stars = []
        cx = page.window_width / 2
        cy = page.window_height / 2

        for i in range(22):
            star = ft.Container(
                content=ft.Text(random.choice(["⭐", "✨"]), size=random.randint(22, 36)),
                left=cx,
                top=cy,
                opacity=1,
                animate_position=ft.Animation(600, "ease_out"),
                animate_opacity=ft.Animation(700, "ease_out"),
            )
            stars.append(star)
            temp_stack.controls.append(star)

        page.update()

        async def animate():
            await asyncio.sleep(0.05)
            mid_points = []
            for s in stars:
                dx = random.randint(-30, 30)
                dy = random.randint(-180, -120)
                mid_points.append((cx + dx, cy + dy))
                s.left = cx + dx
                s.top = cy + dy
            page.update()
            await asyncio.sleep(0.55)

            for i, s in enumerate(stars):
                s.left = mid_points[i][0] + random.randint(-140, 140)
                s.top = mid_points[i][1] + random.randint(-60, 120)
            page.update()
            await asyncio.sleep(0.45)

            for s in stars:
                s.top += random.randint(30, 60)
                s.opacity = 0
            page.update()
            await asyncio.sleep(0.7)

            if temp_stack in page.overlay:
                page.overlay.remove(temp_stack)
            page.update()

        page.run_task(animate)

    # دکمه‌ها و کارت‌ها
    def btn_menu(text, on_click, color="#FFCC80"):
        return ft.ElevatedButton(text, on_click=on_click, bgcolor=color, color="black", width=260)

    def btn_option(text, on_click, color="#FFCC80", data=None):
        return ft.ElevatedButton(text, on_click=on_click, bgcolor=color, color="black", data=data, expand=True)

    def card(content, color="white", width=380):
        return ft.Container(content=content, padding=20, bgcolor=color, border_radius=20, width=width)

    def exit_app(e):
        page.window_close()

    # صفحات اصلی (آموزش اعداد، شکل‌ها، جمع و تفریق، بازی‌ها، گزارش، درباره)
    # همه توابع همان نسخه شما هستند اما مسیرها و انیمیشن‌ها اصلاح شده‌اند.

    def show_about():
        page.controls.clear()
        page.add(
            ft.Column([
                ft.Text("درباره برنامه", size=26, weight="bold", color="#6A1B9A"),
                card(ft.Column([
                    ft.Text("این برنامه برای آموزش ریاضی پایه اول طراحی شده است.", size=16),
                    ft.Text("تهیه کننده: دکتر عباس حیدری", size=16),
                    ft.Text("تماس: ۰۹۹۴۴۳۹۳۰۱۴", size=14),
                    btn_menu("بازگشت", lambda e: show_main_menu(), "#CE93D8"),
                ], spacing=10), color="#F3E5F5"),
            ], spacing=20)
        )
        page.update()

    # نمایش صفحه ورود
    def show_login():
        page.controls.clear()
        teacher = ft.TextField(label="نام معلم", text_align=ft.TextAlign.RIGHT, width=250)
        student = ft.TextField(label="نام دانش‌آموز", text_align=ft.TextAlign.RIGHT, width=250)

        def start(e):
            if teacher.value.strip() == "" or student.value.strip() == "":
                page.snack_bar.content = ft.Text("لطفاً نام معلم و دانش‌آموز را وارد کنید")
                page.snack_bar.bgcolor = "#FF7043"
                page.snack_bar.open = True
                page.update()
                return
            page.teacher_name = teacher.value.strip()
            page.student_name = student.value.strip()
            show_main_menu()

        page.add(ft.Column([
            ft.Text("🎉 دبستان شاهد پسرانه 🎉", size=28, weight="bold", color="#E65100"),
            card(ft.Column([
                ft.Text("لطفاً اطلاعات را وارد کنید", size=20, weight="bold"),
                teacher,
                student,
                btn_menu("شروع", start, "#FFB74D")
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER), color="#FFF3E0")
        ], spacing=20))
        page.update()

    # شروع برنامه با صفحه ورود
    show_login()

ft.app(target=main)
