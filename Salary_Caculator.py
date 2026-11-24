from tkinter import *
from tkinter import messagebox


# -------------------- Main Window --------------------

BG = '#202B3C'
PAGE_BG = '#26364A'
BTN_BG = '#34445B'
ACCENT = '#78C6C3'
TEXT = '#EAF1F7'

EMPLOYEE_FILE = 'employees.csv'
PAYROLL_FILE = 'payroll.csv'

win = Tk()
win.title('Salary Calculator')
win.state('zoomed')
win.resizable(False, False)
win.configure(bg=BG)


# -------------------- Variables --------------------

employee_entries = {}
performance_entries = {}

employee_info = {}
payroll_info = {}

employee_mode = ['new']
payroll_issued = [False]
payroll_calculated = [False]


# -------------------- General Functions --------------------

def show_page(page):

    for item in (home_page, page1, page2, page3):
        item.pack_forget()

    page.pack(fill='both', expand=True)


def set_message(label, message, color=ACCENT):
    label.config(text=message, fg=color)


def read_file(file_name):

    try:
        file = open(file_name, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()
        return lines

    except FileNotFoundError:
        return []

    except OSError:
        return None


def write_file(file_name, lines):

    try:
        file = open(file_name, 'w', encoding='utf-8')

        for line in lines:
            file.write(line.rstrip('\n') + '\n')

        file.close()
        return True

    except OSError:
        return False


def get_employee_data(national_id):

    lines = read_file(EMPLOYEE_FILE)

    if lines is None:
        return None

    for line in lines:

        values = line.strip('\n').split('|')

        if len(values) == 19 and values[0] == national_id:

            data = {}

            data['national_id'] = values[0]
            data['full_name'] = values[1]
            data['birthplace'] = values[2]
            data['birth_year'] = values[3]
            data['gender'] = values[4]
            data['marital_status'] = values[5]
            data['children'] = values[6]
            data['degree'] = values[7]
            data['major'] = values[8]
            data['university'] = values[9]
            data['position'] = values[10]
            data['job_title'] = values[11]
            data['service_group'] = values[12]
            data['service_unit'] = values[13]
            data['insurance_type'] = values[14]
            data['insurance_number'] = values[15]
            data['contract_type'] = values[16]
            data['base_salary'] = values[17]
            data['bonus'] = values[18]

            return data

    return None


def get_payroll_data(national_id, year, month):

    lines = read_file(PAYROLL_FILE)

    if lines is None:
        return None

    month = month.zfill(2)

    for line in lines:

        values = line.strip('\n').split('|')

        if len(values) == 27:

            if values[0] == national_id and values[1] == year and values[2] == month:

                data = {}

                keys = [
                    'national_id', 'year', 'month',
                    'work_days', 'required_hours', 'daily_hours',
                    'normal_hours', 'overtime_hours', 'shortage_hours',
                    'holiday_hours', 'night_hours', 'mission_hours',
                    'overtime_pay', 'night_pay', 'holiday_pay',
                    'housing', 'mission', 'child_allowance',
                    'bonus', 'tax', 'insurance',
                    'base_salary', 'total_benefits',
                    'total_deductions', 'net_salary',
                    'employee_name', 'position'
                ]

                for i in range(len(keys)):
                    data[keys[i]] = values[i]

                return data

    return None


def clear_entries(entries):

    for entry in entries.values():
        entry.config(state='normal')
        entry.delete(0, END)


def add_field(parent, title, key, row, column, target, callback=None):

    lbl = Label(
        parent
        ,text=title
        ,font=('tahoma', 10, 'bold')
        ,bg=PAGE_BG
        ,fg=TEXT
        ,anchor='e'
    )

    lbl.grid(
        row=row
        ,column=column * 2 + 1
        ,sticky='ew'
        ,padx=8
        ,pady=5
    )

    ent = Entry(
        parent
        ,font=('tahoma', 11)
        ,justify='right'
        ,bg='#EAF1F7'
        ,fg=BG
        ,relief='flat'
        ,bd=5
    )

    ent.grid(
        row=row
        ,column=column * 2
        ,sticky='ew'
        ,padx=8
        ,pady=5
    )

    target[key] = ent

    if callback is not None:
        ent.bind('<KeyRelease>', callback)

    return ent


def add_radio(parent, title, variable, options, row, callback=None):

    lbl = Label(
        parent
        ,text=title
        ,font=('tahoma', 10, 'bold')
        ,bg=PAGE_BG
        ,fg=TEXT
        ,anchor='e'
    )

    lbl.grid(row=row, column=1, sticky='ew', padx=8, pady=5)

    radio_frame = Frame(parent, bg=PAGE_BG)
    radio_frame.grid(row=row, column=0, sticky='ew', padx=8, pady=5)

    for value, label in options:

        Radiobutton(
            radio_frame
            ,text=label
            ,value=value
            ,variable=variable
            ,font=('tahoma', 10)
            ,bg=PAGE_BG
            ,fg=TEXT
            ,selectcolor=BG
            ,activebackground=PAGE_BG
            ,activeforeground=TEXT
            ,command=callback
        ).pack(side=RIGHT, padx=5)


def focus_next(event, next_widget):

    if not event.widget.get().strip():
        messagebox.showwarning('Required field', 'این فیلد نمی‌تواند خالی باشد')
        event.widget.focus_set()
        return 'break'

    next_widget.focus_set()
    return 'break'


def bind_enter(entries, last_action):

    entry_list = list(entries.values())

    for i in range(len(entry_list) - 1):

        entry_list[i].bind(
            '<Return>',
            lambda event, next_entry=entry_list[i + 1]:
            focus_next(event, next_entry)
        )

    if entry_list:
        entry_list[-1].bind('<Return>', last_action)


def nav_button(title, command, side=LEFT):

    btn = Button(
        nav
        ,text=title
        ,font=('tahoma', 10, 'bold')
        ,bg=BTN_BG
        ,fg=TEXT
        ,relief='flat'
        ,padx=15
        ,pady=10
        ,command=command
    )

    btn.pack(side=side, padx=5, pady=5)

    btn.bind('<Enter>', lambda event: btn.config(bg=ACCENT, fg=BG))
    btn.bind('<Leave>', lambda event: btn.config(bg=BTN_BG, fg=TEXT))

    return btn


def search_performance(event=None):
    pass


# -------------------- Pages --------------------

nav = Frame(win, bg=BG, height=65)
nav.pack(fill='x', padx=12, pady=10)
nav.pack_propagate(False)

home_page = Frame(win, bg=PAGE_BG)
page1 = Frame(win, bg=PAGE_BG)
page2 = Frame(win, bg=PAGE_BG)
page3 = Frame(win, bg=PAGE_BG)

nav_button('تعریف و مدیریت کارمند', lambda: show_page(page1))
nav_button('عملکرد و محاسبه حقوق', lambda: show_page(page2))
nav_button('مشاهده فیش حقوقی', lambda: show_page(page3))
nav_button('خانه', lambda: show_page(home_page), RIGHT)


# -------------------- Home Page --------------------

Label(
    home_page
    ,text='سیستم مدیریت و محاسبه حقوق'
    ,font=('tahoma', 25, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
).pack(pady=70)

Label(
    home_page
    ,text='Employee Management and Salary Calculator'
    ,font=('tahoma', 14)
    ,bg=PAGE_BG
    ,fg=TEXT
).pack(pady=10)

Label(
    home_page
    ,text='برای شروع، یکی از بخش‌های بالای صفحه را انتخاب کنید'
    ,font=('tahoma', 12)
    ,bg=PAGE_BG
    ,fg=TEXT
).pack(pady=10)


# =====================================================
#                    PAGE 1
#              Employee Management
# =====================================================

gender_var = StringVar()
marital_var = StringVar()

page1.grid_columnconfigure(0, weight=1)
page1.grid_rowconfigure(1, weight=1)

Label(
    page1
    ,text='تعریف و مدیریت کارمند'
    ,font=('tahoma', 18, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
).grid(row=0, column=0, pady=8)


employee_content = Frame(page1, bg=PAGE_BG)
employee_content.grid(row=1, column=0, sticky='nsew', padx=12, pady=5)
employee_content.grid_columnconfigure(0, weight=1)
employee_content.grid_columnconfigure(1, weight=1)
employee_content.grid_rowconfigure(0, weight=1)
employee_content.grid_rowconfigure(1, weight=1)


# -------------------- Personal Information --------------------

personal = LabelFrame(
    employee_content
    ,text='اطلاعات فردی'
    ,font=('tahoma', 11, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=8
    ,pady=5
)

personal.grid(row=0, column=1, sticky='nsew', padx=6, pady=5)
personal.grid_columnconfigure(0, weight=1)
personal.grid_columnconfigure(1, weight=1)

add_field(personal, 'شناسه ملی', 'national_id', 0, 0, employee_entries)
add_field(personal, 'نام و نام خانوادگی', 'full_name', 1, 0, employee_entries)
add_field(personal, 'محل تولد', 'birthplace', 2, 0, employee_entries)
add_field(personal, 'سال تولد', 'birth_year', 3, 0, employee_entries)

add_radio(
    personal,
    'جنسیت',
    gender_var,
    [('male', 'مرد'), ('female', 'زن')],
    4
)


# -------------------- Family Information --------------------

family = LabelFrame(
    employee_content
    ,text='اطلاعات خانوار'
    ,font=('tahoma', 11, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=8
    ,pady=5
)

family.grid(row=0, column=0, sticky='nsew', padx=6, pady=5)
family.grid_columnconfigure(0, weight=1)
family.grid_columnconfigure(1, weight=1)

add_radio(
    family,
    'وضعیت تأهل',
    marital_var,
    [('single', 'مجرد'), ('married', 'متأهل')],
    0
)

add_field(family, 'تعداد فرزندان', 'children', 1, 0, employee_entries)


# -------------------- Education Information --------------------

education = LabelFrame(
    employee_content
    ,text='اطلاعات تحصیلی'
    ,font=('tahoma', 11, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=8
    ,pady=5
)

education.grid(row=1, column=0, sticky='nsew', padx=6, pady=5)
education.grid_columnconfigure(0, weight=1)
education.grid_columnconfigure(1, weight=1)

add_field(education, 'مدرک تحصیلی', 'degree', 0, 0, employee_entries)
add_field(education, 'رشته تحصیلی', 'major', 1, 0, employee_entries)
add_field(education, 'دانشگاه', 'university', 2, 0, employee_entries)


# -------------------- Job Information --------------------

job = LabelFrame(
    employee_content
    ,text='اطلاعات شغلی'
    ,font=('tahoma', 11, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=8
    ,pady=5
)

job.grid(row=1, column=1, sticky='nsew', padx=6, pady=5)

for i in range(4):
    job.grid_columnconfigure(i, weight=1)

add_field(job, 'سمت', 'position', 0, 0, employee_entries)
add_field(job, 'عنوان شغلی', 'job_title', 0, 1, employee_entries)
add_field(job, 'گروه خدمتی', 'service_group', 1, 0, employee_entries)
add_field(job, 'واحد خدمتی', 'service_unit', 1, 1, employee_entries)
add_field(job, 'نوع بیمه', 'insurance_type', 2, 0, employee_entries)
add_field(job, 'شماره بیمه', 'insurance_number', 2, 1, employee_entries)
add_field(job, 'نوع قرارداد', 'contract_type', 3, 0, employee_entries)
add_field(job, 'حقوق پایه (ریال)', 'base_salary', 3, 1, employee_entries)
add_field(job, 'کارانه ثابت (ریال)', 'bonus', 4, 0, employee_entries)


# -------------------- Employee Functions --------------------

def employee_form_complete():

    return (
        all(entry.get().strip() for entry in employee_entries.values())
        and gender_var.get() != ''
        and marital_var.get() != ''
    )


def clear_employee_form(event=None):

    clear_entries(employee_entries)
    gender_var.set('')
    marital_var.set('')
    employee_mode[0] = 'new'
    employee_status.config(text='فرم ثبت کارمند جدید')
    employee_save_btn.config(text='ثبت اطلاعات')
    set_message(employee_message, '')


def load_employee_form(data):

    clear_employee_form()

    for key, entry in employee_entries.items():
        entry.insert(0, data.get(key, ''))

    gender_var.set(data.get('gender', ''))
    marital_var.set(data.get('marital_status', ''))

    employee_mode[0] = 'edit'
    employee_save_btn.config(text='ذخیره ویرایش')
    employee_status.config(text='اطلاعات کارمند برای ویرایش بارگذاری شد')


def search_employee(event=None):

    national_id = employee_entries['national_id'].get().strip()

    if len(national_id) != 10 or not national_id.isascii() or not national_id.isdigit():
        set_message(employee_message, 'شناسه ملی باید ۱۰ رقم انگلیسی باشد', '#FF7777')
        return

    data = get_employee_data(national_id)

    if data is None:
        set_message(employee_message, 'کارمند پیدا نشد', '#FF7777')
        return

    load_employee_form(data)
    set_message(employee_message, 'اطلاعات کارمند پیدا شد', ACCENT)


def save_employee(event=None):

    if not employee_form_complete():
        set_message(employee_message, 'تمام فیلدها را تکمیل کنید', '#FF7777')
        return

    data = {}

    for key, entry in employee_entries.items():
        data[key] = entry.get().strip()

    data['gender'] = gender_var.get()
    data['marital_status'] = marital_var.get()

    national_id = data['national_id']

    if len(national_id) != 10 or not national_id.isascii() or not national_id.isdigit():
        set_message(employee_message, 'شناسه ملی باید ۱۰ رقم انگلیسی باشد', '#FF7777')
        return

    for key in ('birth_year', 'children', 'base_salary', 'bonus'):

        if not data[key].isdigit():
            set_message(employee_message, 'فیلدهای عددی باید عدد صحیح باشند', '#FF7777')
            return

    lines = read_file(EMPLOYEE_FILE)

    if lines is None:
        set_message(employee_message, 'خطا در خواندن فایل کارمندان', '#FF7777')
        return

    new_line = '|'.join([
        data['national_id'],
        data['full_name'],
        data['birthplace'],
        data['birth_year'],
        data['gender'],
        data['marital_status'],
        data['children'],
        data['degree'],
        data['major'],
        data['university'],
        data['position'],
        data['job_title'],
        data['service_group'],
        data['service_unit'],
        data['insurance_type'],
        data['insurance_number'],
        data['contract_type'],
        data['base_salary'],
        data['bonus']
    ])

    found = False
    new_lines = []

    for line in lines:

        values = line.strip('\n').split('|')

        if values and values[0] == national_id:
            found = True

            if employee_mode[0] == 'edit':
                new_lines.append(new_line)
            else:
                set_message(employee_message, 'این شناسه ملی قبلاً ثبت شده است', '#FF7777')
                return

        else:
            new_lines.append(line.strip('\n'))

    if employee_mode[0] == 'edit' and not found:
        set_message(employee_message, 'کارمند برای ویرایش پیدا نشد', '#FF7777')
        return

    if employee_mode[0] == 'new':
        new_lines.append(new_line)

    if write_file(EMPLOYEE_FILE, new_lines):
        set_message(employee_message, 'اطلاعات با موفقیت ذخیره شد', ACCENT)
        employee_mode[0] = 'edit'
        employee_save_btn.config(text='ذخیره ویرایش')
        employee_status.config(text='اطلاعات ثبت شده است')
    else:
        set_message(employee_message, 'خطا در ذخیره اطلاعات', '#FF7777')


def delete_employee(event=None):

    national_id = employee_entries['national_id'].get().strip()

    if len(national_id) != 10:
        set_message(employee_message, 'ابتدا کارمند را جست‌وجو کنید', '#FF7777')
        return

    if not messagebox.askyesno('Delete Employee', 'آیا از حذف این کارمند مطمئن هستید؟'):
        return

    lines = read_file(EMPLOYEE_FILE)

    if lines is None:
        set_message(employee_message, 'خطا در خواندن فایل', '#FF7777')
        return

    new_lines = []
    found = False

    for line in lines:

        values = line.strip('\n').split('|')

        if values and values[0] == national_id:
            found = True
        else:
            new_lines.append(line.strip('\n'))

    if not found:
        set_message(employee_message, 'کارمند پیدا نشد', '#FF7777')
        return

    if write_file(EMPLOYEE_FILE, new_lines):
        clear_employee_form()
        set_message(employee_message, 'کارمند حذف شد', ACCENT)
    else:
        set_message(employee_message, 'خطا در حذف کارمند', '#FF7777')


# -------------------- Employee Buttons --------------------

employee_actions = Frame(page1, bg=PAGE_BG)
employee_actions.grid(row=2, column=0, pady=5)

employee_save_btn = Button(
    employee_actions
    ,text='ثبت اطلاعات'
    ,font=('tahoma', 10, 'bold')
    ,bg=ACCENT
    ,fg=BG
    ,width=15
    ,command=save_employee
)

employee_save_btn.pack(side=RIGHT, padx=5)

Button(
    employee_actions
    ,text='جست‌وجو'
    ,font=('tahoma', 10, 'bold')
    ,bg=BTN_BG
    ,fg=TEXT
    ,width=15
    ,command=search_employee
).pack(side=RIGHT, padx=5)

Button(
    employee_actions
    ,text='حذف کارمند'
    ,font=('tahoma', 10, 'bold')
    ,bg=BTN_BG
    ,fg=TEXT
    ,width=15
    ,command=delete_employee
).pack(side=RIGHT, padx=5)

Button(
    employee_actions
    ,text='فرم جدید'
    ,font=('tahoma', 10, 'bold')
    ,bg=BTN_BG
    ,fg=TEXT
    ,width=15
    ,command=clear_employee_form
).pack(side=RIGHT, padx=5)

employee_status = Label(page1, text='فرم ثبت کارمند جدید', font=('tahoma', 9), bg=PAGE_BG, fg=TEXT)
employee_status.grid(row=3, column=0)

employee_message = Label(page1, text='', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=ACCENT)
employee_message.grid(row=4, column=0, pady=3)

employee_entries['national_id'].bind('<Return>', lambda event=None: employee_entries['full_name'].focus())
employee_entries['full_name'].bind('<Return>', lambda event=None: employee_entries['birthplace'].focus())
employee_entries['birthplace'].bind('<Return>', lambda event=None: employee_entries['birth_year'].focus())
employee_entries['birth_year'].bind('<Return>', lambda event=None: employee_entries['children'].focus())
employee_entries['children'].bind('<Return>', lambda event=None: employee_entries['degree'].focus())
employee_entries['degree'].bind('<Return>', lambda event=None: employee_entries['major'].focus())
employee_entries['major'].bind('<Return>', lambda event=None: employee_entries['university'].focus())
employee_entries['university'].bind('<Return>', lambda event=None: employee_entries['position'].focus())
employee_entries['position'].bind('<Return>', lambda event=None: employee_entries['job_title'].focus())
employee_entries['job_title'].bind('<Return>', lambda event=None: employee_entries['service_group'].focus())
employee_entries['service_group'].bind('<Return>', lambda event=None: employee_entries['service_unit'].focus())
employee_entries['service_unit'].bind('<Return>', lambda event=None: employee_entries['insurance_type'].focus())
employee_entries['insurance_type'].bind('<Return>', lambda event=None: employee_entries['insurance_number'].focus())
employee_entries['insurance_number'].bind('<Return>', lambda event=None: employee_entries['contract_type'].focus())
employee_entries['contract_type'].bind('<Return>', lambda event=None: employee_entries['base_salary'].focus())
employee_entries['base_salary'].bind('<Return>', lambda event=None: employee_entries['bonus'].focus())
employee_entries['bonus'].bind('<Return>', save_employee)


# =====================================================
#                    PAGE 2
#             Monthly Performance / Payroll
# =====================================================

page2.grid_columnconfigure(0, weight=1)
page2.grid_rowconfigure(1, weight=1)

Label(
    page2
    ,text='عملکرد ماهانه و محاسبه حقوق'
    ,font=('tahoma', 18, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
).grid(row=0, column=0, pady=8)

performance_content = Frame(page2, bg=PAGE_BG)
performance_content.grid(row=1, column=0, sticky='nsew', padx=12, pady=5)
performance_content.grid_columnconfigure(0, weight=1)
performance_content.grid_columnconfigure(1, weight=1)


# -------------------- Search Employee / Month --------------------

search_frame = LabelFrame(
    performance_content
    ,text='جست‌وجوی کارمند و دوره حقوق'
    ,font=('tahoma', 10, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=8
    ,pady=5
)

search_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

Label(search_frame, text='شناسه ملی', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=7, padx=5)
search_id_entry = Entry(search_frame, font=('tahoma', 11), width=14, justify='center')
search_id_entry.grid(row=0, column=6, padx=5)

Label(search_frame, text='سال', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=5, padx=5)
year_entry = Entry(search_frame, font=('tahoma', 11), width=8, justify='center')
year_entry.grid(row=0, column=4, padx=5)

Label(search_frame, text='ماه', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=3, padx=5)
month_entry = Entry(search_frame, font=('tahoma', 11), width=5, justify='center')
month_entry.grid(row=0, column=2, padx=5)

search_btn = Button(
    search_frame
    ,text='جست‌وجو'
    ,font=('tahoma', 10, 'bold')
    ,bg=ACCENT
    ,fg=BG
    ,width=12
    ,command=search_performance
)
search_btn.grid(row=0, column=0, padx=10)


# -------------------- Employee Information --------------------

employee_frame = LabelFrame(
    performance_content
    ,text='اطلاعات کارمند'
    ,font=('tahoma', 10, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=8
    ,pady=5
)

employee_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
employee_frame.grid_columnconfigure(0, weight=1)


def employee_label(parent, title, row):

    Label(
        parent
        ,text=title
        ,font=('tahoma', 10, 'bold')
        ,bg=PAGE_BG
        ,fg=TEXT
    ).grid(row=row, column=1, sticky='e', padx=5, pady=4)

    lbl = Label(
        parent
        ,text='-'
        ,font=('tahoma', 10)
        ,bg=PAGE_BG
        ,fg=ACCENT
        ,anchor='e'
    )

    lbl.grid(row=row, column=0, sticky='ew', padx=5, pady=4)
    return lbl


employee_name_lbl = employee_label(employee_frame, 'نام کارمند', 0)
employee_position_lbl = employee_label(employee_frame, 'سمت', 1)
employee_contract_lbl = employee_label(employee_frame, 'نوع قرارداد', 2)
employee_salary_lbl = employee_label(employee_frame, 'حقوق پایه', 3)


# -------------------- Performance Fields --------------------

hours_frame = LabelFrame(
    performance_content
    ,text='عملکرد و ساعت کاری'
    ,font=('tahoma', 10, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=5
    ,pady=3
)

hours_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
hours_frame.grid_columnconfigure(0, weight=1)
hours_frame.grid_columnconfigure(1, weight=1)
hours_frame.grid_columnconfigure(2, weight=1)
hours_frame.grid_columnconfigure(3, weight=1)

add_field(hours_frame, 'روز کارکرد', 'work_days', 0, 0, performance_entries)
add_field(hours_frame, 'ساعت موظفی', 'required_hours', 0, 1, performance_entries)
add_field(hours_frame, 'ساعت کاری روزانه', 'daily_hours', 1, 0, performance_entries)
add_field(hours_frame, 'ساعت کار عادی', 'normal_hours', 1, 1, performance_entries)
add_field(hours_frame, 'ساعت اضافه‌کاری', 'overtime_hours', 2, 0, performance_entries)
add_field(hours_frame, 'ساعت کسری کار', 'shortage_hours', 2, 1, performance_entries)
add_field(hours_frame, 'ساعت تعطیل‌کاری', 'holiday_hours', 3, 0, performance_entries)
add_field(hours_frame, 'ساعت شب‌کاری', 'night_hours', 3, 1, performance_entries)
add_field(hours_frame, 'ساعت مأموریت', 'mission_hours', 4, 0, performance_entries)


# -------------------- Benefits --------------------

benefits_frame = LabelFrame(
    performance_content
    ,text='مزایا و پرداخت‌ها (ریال)'
    ,font=('tahoma', 10, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=5
    ,pady=3
)

benefits_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
benefits_frame.grid_columnconfigure(0, weight=1)
benefits_frame.grid_columnconfigure(1, weight=1)
benefits_frame.grid_columnconfigure(2, weight=1)
benefits_frame.grid_columnconfigure(3, weight=1)

add_field(benefits_frame, 'مبلغ اضافه‌کاری', 'overtime_pay', 0, 0, performance_entries)
add_field(benefits_frame, 'مبلغ شب‌کاری', 'night_pay', 0, 1, performance_entries)
add_field(benefits_frame, 'مبلغ تعطیل‌کاری', 'holiday_pay', 1, 0, performance_entries)
add_field(benefits_frame, 'حق مسکن', 'housing', 1, 1, performance_entries)
add_field(benefits_frame, 'حق مأموریت', 'mission', 2, 0, performance_entries)
add_field(benefits_frame, 'حق اولاد', 'child_allowance', 2, 1, performance_entries)


# -------------------- Deductions --------------------

deductions_frame = LabelFrame(
    performance_content
    ,text='کسورات (ریال)'
    ,font=('tahoma', 10, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=5
    ,pady=3
)

deductions_frame.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
deductions_frame.grid_columnconfigure(0, weight=1)
deductions_frame.grid_columnconfigure(1, weight=1)

add_field(deductions_frame, 'مالیات', 'tax', 0, 0, performance_entries)
add_field(deductions_frame, 'بیمه سهم کارمند', 'insurance', 1, 0, performance_entries)


# -------------------- Calculation Results --------------------

result_frame = LabelFrame(
    performance_content
    ,text='نتیجه محاسبه'
    ,font=('tahoma', 10, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=8
    ,pady=4
)

result_frame.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

total_benefits_lbl = Label(result_frame, text='۰', font=('tahoma', 12, 'bold'), bg=PAGE_BG, fg=ACCENT)
total_deductions_lbl = Label(result_frame, text='۰', font=('tahoma', 12, 'bold'), bg=PAGE_BG, fg=ACCENT)
net_salary_lbl = Label(result_frame, text='۰', font=('tahoma', 12, 'bold'), bg=PAGE_BG, fg=ACCENT)

Label(result_frame, text='مجموع ناخالص و مزایا', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=2, padx=20)
Label(result_frame, text='مجموع کسورات', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=1, padx=20)
Label(result_frame, text='حقوق خالص', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=0, padx=20)

total_benefits_lbl.grid(row=1, column=2, padx=20, pady=3)
total_deductions_lbl.grid(row=1, column=1, padx=20, pady=3)
net_salary_lbl.grid(row=1, column=0, padx=20, pady=3)


# -------------------- Performance Functions --------------------

def performance_form_complete():

    return (
        bool(payroll_info)
        and all(entry.get().strip() for entry in performance_entries.values())
    )


def set_performance_state(state):

    for entry in performance_entries.values():
        entry.config(state=state)


def clear_performance_fields():

    clear_entries(performance_entries)

    payroll_issued[0] = False
    payroll_calculated[0] = False

    total_benefits_lbl.config(text='۰')
    total_deductions_lbl.config(text='۰')
    net_salary_lbl.config(text='۰')

    set_performance_state('normal')


def clear_performance_form(event=None):

    search_id_entry.delete(0, END)
    year_entry.delete(0, END)
    month_entry.delete(0, END)

    payroll_info.clear()
    employee_name_lbl.config(text='-')
    employee_position_lbl.config(text='-')
    employee_contract_lbl.config(text='-')
    employee_salary_lbl.config(text='-')

    clear_performance_fields()
    set_performance_state('disabled')

    set_message(performance_message, '')


def search_performance(event=None):

    national_id = search_id_entry.get().strip()
    year = year_entry.get().strip()
    month = month_entry.get().strip()

    if len(national_id) != 10 or not national_id.isascii() or not national_id.isdigit():
        set_message(performance_message, 'شناسه ملی باید ۱۰ رقم انگلیسی باشد', '#FF7777')
        return

    if len(year) != 4 or not year.isdigit():
        set_message(performance_message, 'سال باید چهار رقم باشد', '#FF7777')
        return

    if not month.isdigit() or not 1 <= int(month) <= 12:
        set_message(performance_message, 'ماه باید بین ۱ تا ۱۲ باشد', '#FF7777')
        return

    employee = get_employee_data(national_id)

    if employee is None:
        payroll_info.clear()
        employee_name_lbl.config(text='-')
        employee_position_lbl.config(text='-')
        employee_contract_lbl.config(text='-')
        employee_salary_lbl.config(text='-')
        clear_performance_fields()
        set_performance_state('disabled')
        set_message(performance_message, 'کارمند پیدا نشد', '#FF7777')
        return

    payroll_info.clear()
    payroll_info.update(employee)

    employee_name_lbl.config(text=employee['full_name'])
    employee_position_lbl.config(text=employee['position'])
    employee_contract_lbl.config(text=employee['contract_type'])
    employee_salary_lbl.config(text=f"{int(employee['base_salary']):,}")

    existing = get_payroll_data(national_id, year, month)

    clear_performance_fields()

    if existing is not None:

        for key, entry in performance_entries.items():
            entry.insert(0, existing.get(key, '0'))

        total_benefits_lbl.config(text=f"{int(existing['total_benefits']):,}")
        total_deductions_lbl.config(text=f"{int(existing['total_deductions']):,}")
        net_salary_lbl.config(text=f"{int(existing['net_salary']):,}")

        payroll_issued[0] = True
        payroll_calculated[0] = True
        set_performance_state('disabled')

        set_message(performance_message, 'فیش این ماه قبلاً صادر شده است', '#FF7777')

    else:

        set_performance_state('normal')
        set_message(performance_message, 'کارمند پیدا شد؛ اطلاعات عملکرد این ماه را وارد کنید', ACCENT)


def calculate_performance(event=None):

    if not performance_form_complete():
        set_message(performance_message, 'ابتدا کارمند را جست‌وجو و تمام فیلدها را تکمیل کنید', '#FF7777')
        return False

    try:

        values = {}

        for key, entry in performance_entries.items():

            value = entry.get().strip()

            if not value.isdigit():
                raise ValueError

            values[key] = int(value)

        if values['work_days'] > 31:
            set_message(performance_message, 'روز کارکرد نمی‌تواند بیشتر از ۳۱ باشد', '#FF7777')
            return False

        base_salary = int(payroll_info['base_salary'])
        fixed_bonus = int(payroll_info['bonus'])

        prorated_salary = base_salary * values['work_days'] // 30

        benefit_keys = [
            'overtime_pay',
            'night_pay',
            'holiday_pay',
            'housing',
            'mission',
            'child_allowance'
        ]

        total_benefits = prorated_salary + fixed_bonus

        for key in benefit_keys:
            total_benefits += values[key]

        total_deductions = values['tax'] + values['insurance']

        if total_deductions > total_benefits:
            set_message(performance_message, 'مجموع کسورات نمی‌تواند از حقوق ناخالص بیشتر باشد', '#FF7777')
            return False

        net_salary = total_benefits - total_deductions

        total_benefits_lbl.config(text=f'{total_benefits:,}')
        total_deductions_lbl.config(text=f'{total_deductions:,}')
        net_salary_lbl.config(text=f'{net_salary:,}')

        payroll_calculated[0] = True
        set_message(performance_message, 'محاسبه حقوق با موفقیت انجام شد', ACCENT)

        return True

    except ValueError:
        set_message(performance_message, 'تمام مقادیر باید عدد صحیح و غیرمنفی باشند', '#FF7777')
        return False


def save_performance(event=None):

    if payroll_issued[0]:
        set_message(performance_message, 'برای این کارمند و ماه قبلاً فیش صادر شده است', '#FF7777')
        return

    if not calculate_performance():
        return

    national_id = search_id_entry.get().strip()
    year = year_entry.get().strip()
    month = month_entry.get().strip().zfill(2)

    values = {}

    for key, entry in performance_entries.items():
        values[key] = entry.get().strip()

    base_salary = int(payroll_info['base_salary'])
    fixed_bonus = int(payroll_info['bonus'])
    prorated_salary = base_salary * int(values['work_days']) // 30

    total_benefits = int(total_benefits_lbl.cget('text').replace(',', ''))
    total_deductions = int(total_deductions_lbl.cget('text').replace(',', ''))
    net_salary = total_benefits - total_deductions

    row = [
        national_id,
        year,
        month,
        values['work_days'],
        values['required_hours'],
        values['daily_hours'],
        values['normal_hours'],
        values['overtime_hours'],
        values['shortage_hours'],
        values['holiday_hours'],
        values['night_hours'],
        values['mission_hours'],
        values['overtime_pay'],
        values['night_pay'],
        values['holiday_pay'],
        values['housing'],
        values['mission'],
        values['child_allowance'],
        str(fixed_bonus),
        values['tax'],
        values['insurance'],
        str(prorated_salary),
        str(total_benefits),
        str(total_deductions),
        str(net_salary),
        payroll_info['full_name'],
        payroll_info['position']
    ]

    lines = read_file(PAYROLL_FILE)

    if lines is None:
        set_message(performance_message, 'خطا در خواندن فایل حقوق', '#FF7777')
        return

    for line in lines:

        old = line.strip('\n').split('|')

        if len(old) >= 3 and old[0] == national_id and old[1] == year and old[2] == month:
            set_message(performance_message, 'این ماه قبلاً ثبت شده است', '#FF7777')
            return

    try:
        file = open(PAYROLL_FILE, 'a', encoding='utf-8')
        file.write('|'.join(row) + '\n')
        file.close()

        payroll_issued[0] = True
        set_performance_state('disabled')

        set_message(performance_message, 'فیش حقوقی با موفقیت ثبت شد', ACCENT)

    except OSError:
        set_message(performance_message, 'خطا در ذخیره فیش حقوقی', '#FF7777')


def focus_performance_next(event, next_widget):

    if not event.widget.get().strip():
        messagebox.showwarning('Required field', 'این فیلد نمی‌تواند خالی باشد')
        event.widget.focus_set()
        return 'break'

    next_widget.focus_set()
    return 'break'


# -------------------- Performance Buttons --------------------

performance_message = Label(page2, text='', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=ACCENT)
performance_message.grid(row=2, column=0, pady=2)

performance_buttons = Frame(page2, bg=PAGE_BG)
performance_buttons.grid(row=3, column=0, pady=5)

Button(
    performance_buttons
    ,text='محاسبه حقوق'
    ,font=('tahoma', 10, 'bold')
    ,bg=ACCENT
    ,fg=BG
    ,width=16
    ,command=calculate_performance
).pack(side=RIGHT, padx=5)

Button(
    performance_buttons
    ,text='صدور و ثبت فیش'
    ,font=('tahoma', 10, 'bold')
    ,bg=ACCENT
    ,fg=BG
    ,width=16
    ,command=save_performance
).pack(side=RIGHT, padx=5)

Button(
    performance_buttons
    ,text='پاک کردن فرم'
    ,font=('tahoma', 10, 'bold')
    ,bg=BTN_BG
    ,fg=TEXT
    ,width=16
    ,command=clear_performance_form
).pack(side=RIGHT, padx=5)

search_id_entry.bind('<Return>', lambda event=None: year_entry.focus())
year_entry.bind('<Return>', lambda event=None: month_entry.focus())
month_entry.bind('<Return>', search_performance)

performance_entry_list = list(performance_entries.values())

for i in range(len(performance_entry_list) - 1):
    performance_entry_list[i].bind(
        '<Return>',
        lambda event, next_entry=performance_entry_list[i + 1]:
        focus_performance_next(event, next_entry)
    )

performance_entry_list[-1].bind('<Return>', calculate_performance)

set_performance_state('disabled')


# =====================================================
#                    PAGE 3
#                 Payslip Search
# =====================================================

page3.grid_columnconfigure(0, weight=1)

Label(
    page3
    ,text='مشاهده و دریافت فیش حقوقی'
    ,font=('tahoma', 20, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
).pack(pady=20)


# -------------------- Payslip Search --------------------

payslip_search = LabelFrame(
    page3
    ,text='جست‌وجوی فیش'
    ,font=('tahoma', 10, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=10
    ,pady=8
)

payslip_search.pack(fill='x', padx=25, pady=10)

Label(payslip_search, text='شناسه ملی', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=7, padx=5)
payslip_id_entry = Entry(payslip_search, font=('tahoma', 11), width=14, justify='center')
payslip_id_entry.grid(row=0, column=6, padx=5)

Label(payslip_search, text='سال', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=5, padx=5)
payslip_year_entry = Entry(payslip_search, font=('tahoma', 11), width=8, justify='center')
payslip_year_entry.grid(row=0, column=4, padx=5)

Label(payslip_search, text='ماه', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=TEXT).grid(row=0, column=3, padx=5)
payslip_month_entry = Entry(payslip_search, font=('tahoma', 11), width=5, justify='center')
payslip_month_entry.grid(row=0, column=2, padx=5)


# -------------------- Payslip Details --------------------

payslip_frame = LabelFrame(
    page3
    ,text='جزئیات فیش حقوقی'
    ,font=('tahoma', 11, 'bold')
    ,bg=PAGE_BG
    ,fg=ACCENT
    ,labelanchor='ne'
    ,padx=15
    ,pady=10
)

payslip_frame.pack(fill='both', expand=True, padx=25, pady=10)

payslip_labels = {}


def payslip_label(title, key, row, column):

    Label(
        payslip_frame
        ,text=title
        ,font=('tahoma', 10, 'bold')
        ,bg=PAGE_BG
        ,fg=TEXT
        ,anchor='e'
    ).grid(row=row, column=column * 2 + 1, sticky='ew', padx=8, pady=7)

    lbl = Label(
        payslip_frame
        ,text='-'
        ,font=('tahoma', 10)
        ,bg=PAGE_BG
        ,fg=ACCENT
        ,anchor='e'
    )

    lbl.grid(row=row, column=column * 2, sticky='ew', padx=8, pady=7)
    payslip_labels[key] = lbl


payslip_label('نام کارمند', 'employee_name', 0, 0)
payslip_label('سمت', 'position', 0, 1)
payslip_label('شناسه ملی', 'national_id', 1, 0)
payslip_label('دوره حقوق', 'period', 1, 1)
payslip_label('روز کارکرد', 'work_days', 2, 0)
payslip_label('حقوق پایه محاسبه‌شده', 'base_salary', 2, 1)
payslip_label('کارانه ثابت', 'bonus', 3, 0)
payslip_label('اضافه‌کاری', 'overtime_pay', 3, 1)
payslip_label('شب‌کاری', 'night_pay', 4, 0)
payslip_label('تعطیل‌کاری', 'holiday_pay', 4, 1)
payslip_label('حق مسکن', 'housing', 5, 0)
payslip_label('حق مأموریت', 'mission', 5, 1)
payslip_label('حق اولاد', 'child_allowance', 6, 0)
payslip_label('مجموع ناخالص و مزایا', 'total_benefits', 6, 1)
payslip_label('مالیات', 'tax', 7, 0)
payslip_label('بیمه سهم کارمند', 'insurance', 7, 1)
payslip_label('مجموع کسورات', 'total_deductions', 8, 0)
payslip_label('حقوق خالص', 'net_salary', 8, 1)


def clear_payslip(event=None):

    for label in payslip_labels.values():
        label.config(text='-')

    set_message(payslip_message, '')


def search_payslip(event=None):

    national_id = payslip_id_entry.get().strip()
    year = payslip_year_entry.get().strip()
    month = payslip_month_entry.get().strip()

    if len(national_id) != 10 or not national_id.isascii() or not national_id.isdigit():
        set_message(payslip_message, 'شناسه ملی باید ۱۰ رقم انگلیسی باشد', '#FF7777')
        return

    if len(year) != 4 or not year.isdigit():
        set_message(payslip_message, 'سال باید چهار رقم باشد', '#FF7777')
        return

    if not month.isdigit() or not 1 <= int(month) <= 12:
        set_message(payslip_message, 'ماه باید بین ۱ تا ۱۲ باشد', '#FF7777')
        return

    data = get_payroll_data(national_id, year, month)

    if data is None:
        clear_payslip()
        set_message(payslip_message, 'فیش حقوقی پیدا نشد', '#FF7777')
        return

    payslip_labels['employee_name'].config(text=data['employee_name'])
    payslip_labels['position'].config(text=data['position'])
    payslip_labels['national_id'].config(text=data['national_id'])
    payslip_labels['period'].config(text=data['year'] + '/' + data['month'])
    payslip_labels['work_days'].config(text=data['work_days'])
    payslip_labels['base_salary'].config(text=f"{int(data['base_salary']):,}")
    payslip_labels['bonus'].config(text=f"{int(data['bonus']):,}")
    payslip_labels['overtime_pay'].config(text=f"{int(data['overtime_pay']):,}")
    payslip_labels['night_pay'].config(text=f"{int(data['night_pay']):,}")
    payslip_labels['holiday_pay'].config(text=f"{int(data['holiday_pay']):,}")
    payslip_labels['housing'].config(text=f"{int(data['housing']):,}")
    payslip_labels['mission'].config(text=f"{int(data['mission']):,}")
    payslip_labels['child_allowance'].config(text=f"{int(data['child_allowance']):,}")
    payslip_labels['total_benefits'].config(text=f"{int(data['total_benefits']):,}")
    payslip_labels['tax'].config(text=f"{int(data['tax']):,}")
    payslip_labels['insurance'].config(text=f"{int(data['insurance']):,}")
    payslip_labels['total_deductions'].config(text=f"{int(data['total_deductions']):,}")
    payslip_labels['net_salary'].config(text=f"{int(data['net_salary']):,}")

    set_message(payslip_message, 'فیش حقوقی پیدا شد', ACCENT)


payslip_buttons = Frame(page3, bg=PAGE_BG)
payslip_buttons.pack(pady=5)

Button(
    payslip_buttons
    ,text='جست‌وجوی فیش'
    ,font=('tahoma', 10, 'bold')
    ,bg=ACCENT
    ,fg=BG
    ,width=16
    ,command=search_payslip
).pack(side=RIGHT, padx=5)

Button(
    payslip_buttons
    ,text='پاک کردن'
    ,font=('tahoma', 10, 'bold')
    ,bg=BTN_BG
    ,fg=TEXT
    ,width=16
    ,command=clear_payslip
).pack(side=RIGHT, padx=5)

payslip_message = Label(page3, text='', font=('tahoma', 10, 'bold'), bg=PAGE_BG, fg=ACCENT)
payslip_message.pack(pady=5)

payslip_id_entry.bind('<Return>', lambda event=None: payslip_year_entry.focus())
payslip_year_entry.bind('<Return>', lambda event=None: payslip_month_entry.focus())
payslip_month_entry.bind('<Return>', search_payslip)


# -------------------- Start --------------------

show_page(home_page)
win.mainloop()
