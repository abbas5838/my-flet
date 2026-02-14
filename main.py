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

def main(page: ft.Page):

    # -------------------------
    # تنظیمات صفحه
    # -------------------------
    page.title = "آموزش ریاضی پایه اول"
    page.window.width = 500
    page.window.height = 700
    page.bgcolor = "#FFF8E1"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # شمارنده‌ها
    page.correct_answers = 0
    page.wrong_answers = 0
    page.teacher_name = ""
    page.student_name = ""

    # Snackbar
    page.snack_bar = ft.SnackBar(content=ft.Text(""))

    # -------------------------
    # صدا
    # -------------------------
    if getattr(sys, "frozen", False):
        beep_src = resource_path("beep.mp3")
    else:
        beep_src = "beep.mp3"

    page.beep = ft.Audio(src=beep_src)
    page.overlay.append(page.beep)

    def play_beep():
        page.beep.play()
        page.update()

    # -------------------------
    # افکت فواره‌ای ستاره‌ها (نسخه نهایی گزینه ۳)
    # -------------------------
    def show_stars():

        temp_stack = ft.Stack(expand=True)
        page.overlay.append(temp_stack)

        stars = []

        cx = (page.width or page.window.width) / 2
        cy = (page.height or page.window.height) / 2

        for i in range(22):
            star = ft.Container(
                content=ft.Text(
                    random.choice(["⭐", "✨"]),
                    size=random.randint(22, 36),
                ),
                left=cx,
                top=cy,
                opacity=1,
                animate_position=ft.Animation(500, "ease_out"),
                animate_opacity=ft.Animation(600, "ease_out"),
            )

            stars.append(star)
            temp_stack.controls.append(star)

        page.update()

        async def animate():
            await asyncio.sleep(0.05)

            # ------------------
            # مرحله 1 : پرتاب رو به بالا (ستون فواره)
            # ------------------
            mid_points = []

            for s in stars:
                dx = random.randint(-30, 30)
                dy = random.randint(-180, -120)

                mid_x = cx + dx
                mid_y = cy + dy

                mid_points.append((mid_x, mid_y))

                s.left = mid_x
                s.top = mid_y

            page.update()

            await asyncio.sleep(0.55)

            # ------------------
            # مرحله 2 : پخش شدن اطراف
            # ------------------
            for i, s in enumerate(stars):
                spread_x = mid_points[i][0] + random.randint(-140, 140)
                spread_y = mid_points[i][1] + random.randint(-60, 120)

                s.left = spread_x
                s.top = spread_y

            page.update()

            await asyncio.sleep(0.45)

            # ------------------
            # مرحله 3 : افت کوتاه + محو شدن
            # ------------------
            for s in stars:
                s.top += random.randint(30, 60)
                s.opacity = 0

            page.update()

            await asyncio.sleep(0.7)

            if temp_stack in page.overlay:
                page.overlay.remove(temp_stack)

            page.update()

        page.run_task(animate)

    # -------------------------
    # دکمه‌های استاندارد
    # -------------------------
    def btn_menu(text, on_click, color="#FFCC80"):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            bgcolor=color,
            color="black",
            width=260,
        )

    def btn_option(text, on_click, color="#FFCC80", data=None):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            bgcolor=color,
            color="black",
            data=data,
            expand=True,
        )

    # -------------------------
    # کارت استاندارد
    # -------------------------
    def card(content, color="white", width=380):
        return ft.Container(
            content=content,
            padding=20,
            bgcolor=color,
            border_radius=20,
            width=width,
        )

    # -------------------------
    # خروج
    # -------------------------
    def exit_app(e):
        page.window_close()

    # -------------------------
    # صفحه درباره
    # -------------------------
    def show_about():
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Text("درباره برنامه", size=26, weight="bold", color="#6A1B9A"),
                    card(
                        ft.Column(
                            [
                                ft.Text("این برنامه برای آموزش ریاضی پایه اول طراحی شده است.", size=16),
                                ft.Text("تهیه کننده: دکتر عباس حیدری", size=16),
                                ft.Text("تماس: ۰۹۹۴۴۳۹۳۰۱۴", size=14),
                                btn_menu("بازگشت", lambda e: show_main_menu(), "#CE93D8"),
                            ],
                            spacing=10,
                        ),
                        color="#F3E5F5",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()

    # -------------------------
    # صفحه ارزیابی
    # -------------------------
    def show_report():
        page.controls.clear()

        total = page.correct_answers + page.wrong_answers
        percent = int((page.correct_answers / total) * 100) if total > 0 else 0

        page.add(
            ft.Column(
                [
                    ft.Text("نتیجه ارزیابی", size=26, weight="bold", color="#2E7D32"),
                    card(
                        ft.Column(
                            [
                                ft.Text(f"دانش‌آموز: {page.student_name}", size=16),
                                ft.Text(f"معلم: {page.teacher_name}", size=16),
                                ft.Text(f"درست: {to_persian_number(page.correct_answers)}", size=16),
                                ft.Text(f"غلط: {to_persian_number(page.wrong_answers)}", size=16),
                                ft.Text(f"درصد موفقیت: {to_persian_number(percent)}٪", size=18, weight="bold"),
                                btn_menu("بازگشت", lambda e: show_main_menu(), "#C5E1A5"),
                            ],
                            spacing=10,
                        ),
                        color="#E8F5E9",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()

    # -------------------------
    # آموزش شکل‌ها
    # -------------------------
    def show_shapes():
        page.controls.clear()

        shapes = [("دایره", "⚪"), ("مربع", "⬜"), ("مثلث", "🔺"), ("مستطیل", "▭")]

        page.add(
            ft.Column(
                [
                    ft.Text("آموزش شکل‌ها", size=24, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                *[
                                    ft.Row(
                                        [ft.Text(icon, size=28), ft.Text(name, size=20)],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    )
                                    for name, icon in shapes
                                ],
                                btn_menu("بازگشت", lambda e: show_main_menu()),
                            ],
                            spacing=12,
                        ),
                        color="#FFF3E0",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()

    # -------------------------
    # منوی آموزش اعداد
    # -------------------------
    def show_number_menu():
        page.controls.clear()

        page.add(
            ft.Column(
                [
                    ft.Text("آموزش اعداد", size=24, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                btn_menu("نمایش ترتیبی", lambda e: show_numbers("asc")),
                                btn_menu("نمایش تصادفی", lambda e: show_numbers("random")),
                                btn_menu("بازگشت", lambda e: show_main_menu()),
                            ],
                            spacing=12,
                        ),
                        color="#FFF3E0",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()

    def show_numbers(mode):
        page.controls.clear()

        current = {"value": 1}
        num = ft.Text("", size=56, weight="bold", color="#0277BD")

        def update():
            if mode == "asc":
                num.value = to_persian_number(current["value"])
                current["value"] += 1
                if current["value"] > 20:
                    current["value"] = 1
            else:
                num.value = to_persian_number(random.randint(1, 20))
            page.update()

        update()

        page.add(
            ft.Column(
                [
                    ft.Text("آموزش اعداد", size=24, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                num,
                                btn_menu("عدد بعدی", lambda e: update(), "#FFB74D"),
                                btn_menu("بازگشت", lambda e: show_number_menu()),
                            ],
                            spacing=16,
                        ),
                        color="#E3F2FD",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()

    # -------------------------
    # جمع ساده
    # -------------------------
    def show_add():
        page.controls.clear()

        a = random.randint(1, 10)
        b = random.randint(1, 10)
        correct = a + b

        result = ft.Text("", size=18)

        options = [correct, correct + 1, correct - 1, correct + 2]
        options = [o for o in options if o > 0]
        random.shuffle(options)

        def check(e):
            if e.control.data == correct:
                page.correct_answers += 1
                result.value = "آفرین! درست بود"
                result.color = "green"
                show_stars()
            else:
                page.wrong_answers += 1
                result.value = "بیشتر دقت کن"
                result.color = "red"
                play_beep()
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text("جمع ساده", size=24, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                ft.Text(f"{to_persian_number(a)} + {to_persian_number(b)} =", size=28, weight="bold"),
                                ft.Row(
                                    [btn_option(to_persian_number(i), check, data=i) for i in options],
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                ),
                                result,
                                btn_menu("نمونه جدید", lambda e: show_add(), "#FFB74D"),
                                btn_menu("بازگشت", lambda e: show_main_menu()),
                            ],
                            spacing=12,
                        ),
                        color="#FFFDE7",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()

    # -------------------------
    # تفریق ساده
    # -------------------------
    def show_sub():
        page.controls.clear()

        a = random.randint(5, 15)
        b = random.randint(1, a)
        correct = a - b

        result = ft.Text("", size=18)

        options = [correct, correct + 1, correct - 1, correct + 2]
        options = [o for o in options if o >= 0]
        random.shuffle(options)

        def check(e):
            if e.control.data == correct:
                page.correct_answers += 1
                result.value = "آفرین! درست بود"
                result.color = "green"
                show_stars()
            else:
                page.wrong_answers += 1
                result.value = "بیشتر دقت کن"
                result.color = "red"
                play_beep()
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text("تفریق ساده", size=24, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                ft.Text(f"{to_persian_number(a)} - {to_persian_number(b)} =", size=28, weight="bold"),
                                ft.Row(
                                    [btn_option(to_persian_number(i), check, data=i) for i in options],
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                ),
                                result,
                                btn_menu("نمونه جدید", lambda e: show_sub(), "#FFB74D"),
                                btn_menu("بازگشت", lambda e: show_main_menu()),
                            ],
                            spacing=12,
                        ),
                        color="#F3E5F5",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()
    # -------------------------
    # جمع با شکل‌ها
    # -------------------------
    def show_add_shapes():
        page.controls.clear()

        a = random.randint(1, 5)
        b = random.randint(1, 5)
        icon = random.choice(["🍎", "⚽", "⭐", "🍓"])

        result = ft.Text("", size=18)

        options = [a + b, a + b + 1, a + b - 1]
        options = [o for o in options if o >= 0]
        random.shuffle(options)

        def check(e):
            if e.control.data == a + b:
                page.correct_answers += 1
                result.value = "آفرین! درست بود"
                result.color = "green"
                show_stars()
            else:
                page.wrong_answers += 1
                result.value = "بیشتر دقت کن"
                result.color = "red"
                play_beep()
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text("جمع با شکل‌ها", size=24, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                ft.Text(icon * a + "  +  " + icon * b, size=28),
                                ft.Row(
                                    [btn_option(to_persian_number(i), check, data=i) for i in options],
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                ),
                                result,
                                btn_menu("نمونه جدید", lambda e: show_add_shapes(), "#FFB74D"),
                                btn_menu("بازگشت", lambda e: show_main_menu()),
                            ],
                            spacing=12,
                        ),
                        color="#FFFDE7",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()


    # -------------------------
    # تفریق با شکل‌ها
    # -------------------------
    def show_sub_shapes():
        page.controls.clear()

        a = random.randint(3, 7)
        b = random.randint(1, a - 1)
        icon = random.choice(["🍎", "⚽", "⭐", "🍓"])

        result = ft.Text("", size=18)

        options = [a - b, a - b + 1, a - b - 1]
        options = [o for o in options if o >= 0]
        random.shuffle(options)

        def check(e):
            if e.control.data == a - b:
                page.correct_answers += 1
                result.value = "آفرین! درست بود"
                result.color = "green"
                show_stars()
            else:
                page.wrong_answers += 1
                result.value = "بیشتر دقت کن"
                result.color = "red"
                play_beep()
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text("تفریق با شکل‌ها", size=24, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                ft.Text(icon * a + "  -  " + icon * b, size=28),
                                ft.Row(
                                    [btn_option(to_persian_number(i), check, data=i) for i in options],
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                ),
                                result,
                                btn_menu("نمونه جدید", lambda e: show_sub_shapes(), "#FFB74D"),
                                btn_menu("بازگشت", lambda e: show_main_menu()),
                            ],
                            spacing=12,
                        ),
                        color="#F3E5F5",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()


    # -------------------------
    # بازی پیدا کردن عدد
    # -------------------------
    def show_game_find_number():
        page.controls.clear()

        correct = random.randint(1, 20)

        options = [
            correct,
            correct + random.randint(1, 3),
            correct - random.randint(1, 3),
            random.randint(1, 20),
        ]
        options = [o for o in options if o > 0]
        while len(options) < 4:
            options.append(random.randint(1, 20))
        random.shuffle(options)

        result = ft.Text("", size=18, weight="bold")

        def check(e):
            if e.control.data == correct:
                page.correct_answers += 1
                result.value = "آفرین! درست بود"
                result.color = "green"
                show_stars()
            else:
                page.wrong_answers += 1
                result.value = "بیشتر دقت کن"
                result.color = "red"
                play_beep()
            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text("بازی پیدا کردن عدد", size=26, weight="bold", color="#D84315"),
                    card(
                        ft.Column(
                            [
                                ft.Text(
                                    f"کدام عدد «{num_to_word(correct)}» است؟",
                                    size=20,
                                    weight="bold",
                                    color="#0277BD",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Row(
                                    [
                                        btn_option(to_persian_number(i), check, data=i)
                                        for i in options
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                ),
                                result,
                                btn_menu("مرحله بعد", lambda e: show_game_find_number(), "#FFB74D"),
                                btn_menu("بازگشت", lambda e: show_game_menu()),
                            ],
                            spacing=14,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        color="#E3F2FD",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()


    # -------------------------
    # بازی بزرگ‌تر و کوچک‌تر
    # -------------------------
    def show_game_bigger_smaller():
        page.controls.clear()

        a = random.randint(1, 20)
        b = random.randint(1, 20)

        result = ft.Text("", size=18, weight="bold")

        def check(e):
            if a > b:
                correct_choice = "bigger1"
            elif b > a:
                correct_choice = "bigger2"
            else:
                correct_choice = "equal"

            if e.control.data == correct_choice:
                page.correct_answers += 1
                if correct_choice == "bigger1":
                    result.value = "آفرین! عدد اول بزرگ‌تر است"
                elif correct_choice == "bigger2":
                    result.value = "آفرین! عدد دوم بزرگ‌تر است"
                else:
                    result.value = "درسته! دو عدد برابرند"
                result.color = "green"
                show_stars()
            else:
                page.wrong_answers += 1
                result.value = "بیشتر دقت کن"
                result.color = "red"
                play_beep()

            page.update()

        question = ft.Row(
            [
                ft.Text(to_persian_number(a), size=28, weight="bold", color="#0277BD"),
                ft.Text("و", size=22),
                ft.Text(to_persian_number(b), size=28, weight="bold", color="#0277BD"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        page.add(
            ft.Column(
                [
                    ft.Text("بازی بزرگ‌تر و کوچک‌تر", size=26, weight="bold", color="#D84315"),
                    card(
                        ft.Column(
                            [
                                question,
                                btn_option("عدد اول بزرگ‌تر است", lambda e: check(e), data="bigger1"),
                                btn_option("عدد دوم بزرگ‌تر است", lambda e: check(e), data="bigger2"),
                                btn_option("برابرند", lambda e: check(e), data="equal"),
                                result,
                                btn_menu("مرحله بعد", lambda e: show_game_bigger_smaller(), "#FFB74D"),
                                btn_menu("بازگشت", lambda e: show_game_menu()),
                            ],
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        color="#FFE0B2",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()


    # -------------------------
    # منوی بازی‌ها
    # -------------------------
    def show_game_menu():
        page.controls.clear()

        page.add(
            ft.Column(
                [
                    ft.Text("بازی‌ها", size=26, weight="bold", color="#D84315"),
                    card(
                        ft.Column(
                            [
                                btn_menu("بازی پیدا کردن عدد", lambda e: show_game_find_number(), "#FFCC80"),
                                btn_menu("بازی بزرگ‌تر و کوچک‌تر", lambda e: show_game_bigger_smaller(), "#FFCC80"),
                                btn_menu("بازگشت", lambda e: show_main_menu()),
                            ],
                            spacing=12,
                        ),
                        color="#FFE0B2",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()


    # -------------------------
    # منوی اصلی
    # -------------------------
    def show_main_menu():
        page.controls.clear()

        menu = card(
            ft.Column(
                [
                    ft.Text(f"دانش‌آموز: {page.student_name}", size=14),
                    ft.Text(f"معلم: {page.teacher_name}", size=14),
                    ft.Divider(),
                    btn_menu("آموزش اعداد", lambda e: show_number_menu(), "#BBDEFB"),
                    btn_menu("آموزش شکل‌ها", lambda e: show_shapes(), "#B3E5FC"),
                    btn_menu("جمع با شکل‌ها", lambda e: show_add_shapes(), "#FFECB3"),
                    btn_menu("تفریق با شکل‌ها", lambda e: show_sub_shapes(), "#FFECB3"),
                    btn_menu("جمع ساده", lambda e: show_add(), "#FFE082"),
                    btn_menu("تفریق ساده", lambda e: show_sub(), "#FFE082"),
                    btn_menu("بازی‌ها", lambda e: show_game_menu(), "#FFB74D"),
                    btn_menu("نتیجه ارزیابی", lambda e: show_report(), "#C5E1A5"),
                    btn_menu("درباره برنامه", lambda e: show_about(), "#CE93D8"),
                    btn_menu("خروج از برنامه", exit_app, "#FF8A80"),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            color="#FFFFFF",
            width=380,
        )

        page.add(
            ft.Column(
                [
                    ft.Text("آموزش ریاضی پایه اول", size=24, weight="bold", color="#E65100"),
                    menu,
                ],
                spacing=16,
            )
        )
        page.update()


    # -------------------------
    # صفحه ورود
    # -------------------------
    def show_login():
        page.controls.clear()

        teacher = ft.TextField(
            label="نام معلم",
            text_align=ft.TextAlign.RIGHT,
            width=250,
        )
        student = ft.TextField(
            label="نام دانش‌آموز",
            text_align=ft.TextAlign.RIGHT,
            width=250,
        )

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

        page.add(
            ft.Column(
                [
                    ft.Text("🎉 دبستان شاهد پسرانه 🎉", size=28, weight="bold", color="#E65100"),
                    card(
                        ft.Column(
                            [
                                ft.Text("لطفاً اطلاعات را وارد کنید", size=20, weight="bold"),
                                teacher,
                                student,
                                btn_menu("شروع", start, "#FFB74D"),
                            ],
                            spacing=15,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        color="#FFF3E0",
                    ),
                ],
                spacing=20,
            )
        )
        page.update()


    # شروع از صفحه ورود
    show_login()


ft.app(target=main)
