import os
import shutil

def copy_all_files(source_dir, dest_dir, exclude_files=None):
    """
    کپی تمام فایل‌های موجود در source_dir و زیرپوشه‌های آن به dest_dir
    و ذخیره نقشه پوشه‌بندی در یک فایل متنی
    """
    if exclude_files is None:
        exclude_files = set()
    else:
        exclude_files = {os.path.abspath(f) for f in exclude_files}

    # ساخت پوشه مقصد اگر وجود ندارد
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"پوشه مقصد ساخته شد: {dest_dir}")

    dest_abs = os.path.abspath(dest_dir)
    count = 0
    report_lines = []  # خطوط فایل گزارش

    for root, dirs, files in os.walk(source_dir):
        # از ورود به پوشه مقصد جلوگیری کن
        dirs[:] = [d for d in dirs if os.path.abspath(os.path.join(root, d)) != dest_abs]

        for file in files:
            src_file = os.path.abspath(os.path.join(root, file))

            # فایل‌های مستثنی (مثل خود اسکریپت) را رد کن
            if src_file in exclude_files:
                continue

            # مسیر نسبی نسبت به پوشه مبدأ
            rel_path = os.path.relpath(src_file, source_dir)
            rel_dir = os.path.dirname(rel_path)  # پوشه نسبی

            # نام فایل مقصد - اگر تکراری بود شماره اضافه کن
            dest_file = os.path.join(dest_dir, file)
            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(dest_file):
                dest_file = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                counter += 1

            try:
                shutil.copy2(src_file, dest_file)
                count += 1

                # ثبت در گزارش
                if rel_dir and rel_dir != ".":
                    report_lines.append(f"{os.path.basename(dest_file)}  <--  {rel_dir}/{file}")
                else:
                    report_lines.append(f"{os.path.basename(dest_file)}  <--  {file}")

                print(f"کپی شد: {rel_path}  ->  {os.path.basename(dest_file)}")
            except Exception as e:
                print(f"خطا در کپی {src_file}: {e}")

    # نوشتن فایل گزارش
    report_path = os.path.join(dest_dir, "_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("گزارش کپی فایل‌ها\n")
        f.write("=" * 60 + "\n")
        f.write(f"پوشه مبدأ: {source_dir}\n")
        f.write(f"تعداد کل فایل‌ها: {count}\n")
        f.write("=" * 60 + "\n\n")
        f.write("نقشه پوشه‌بندی (فایل مقصد  <--  مسیر اصلی):\n")
        f.write("-" * 60 + "\n")
        for line in sorted(report_lines):
            f.write(line + "\n")

    print(f"\n✅ مجموع {count} فایل کپی شد.")
    print(f"📄 گزارش در فایل ذخیره شد: {report_path}")


if __name__ == "__main__":
    # پوشه‌ای که اسکریپت در آن قرار دارد
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    # پوشه مقصد: files در کنار اسکریپت
    destination = os.path.join(script_dir, "files")

    # خود فایل پایتون از عملیات خارج بماند
    copy_all_files(script_dir, destination, exclude_files=[script_path])
