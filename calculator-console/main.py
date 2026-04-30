import sys
from calculator import add, subtract, multiply, divide, format_for_display

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (OSError, ValueError):
        pass


def show_menu() -> None:
    print()
    print("Lütfen yapmak istediğiniz işlemi seçiniz:")
    print()
    print("1 - Toplama")
    print("2 - Çıkarma")
    print("3 - Çarpma")
    print("4 - Bölme")
    print("5 - Çıkış")


def get_operation_choice() -> str:
    valid_choices = frozenset({"1", "2", "3", "4", "5"})
    while True:
        choice = input("Seçiminiz: ").strip()
        if choice in valid_choices:
            return choice
        print("Geçersiz seçim yaptınız. Lütfen 1 ile 5 arasında bir değer giriniz.")
        show_menu()


def get_number(message: str) -> float:
    while True:
        try:
            raw = input(message).strip()
            if not raw:
                print("Hatalı giriş. Lütfen geçerli bir sayı giriniz.")
                continue
            return float(raw)
        except ValueError:
            print("Hatalı giriş. Lütfen geçerli bir sayı giriniz.")


def main() -> None:
    print("Python Console Hesap Makinesi")
    print("-----------------------------")

    while True:
        show_menu()
        choice = get_operation_choice()

        if choice == "5":
            print("Programdan çıkılıyor. Görüşmek üzere.")
            break

        first = get_number("Birinci sayıyı giriniz: ")
        second = get_number("İkinci sayıyı giriniz: ")

        if choice == "1":
            result = add(first, second)
            operator = "+"
        elif choice == "2":
            result = subtract(first, second)
            operator = "-"
        elif choice == "3":
            result = multiply(first, second)
            operator = "*"
        else:
            result = divide(first, second)
            if result is None:
                print("Sıfıra bölme hatası. İkinci sayı 0 olamaz.")
                continue
            operator = "/"

        a_str = format_for_display(first)
        b_str = format_for_display(second)
        res_str = format_for_display(result)
        print()
        print(f"Sonuç: {a_str} {operator} {b_str} = {res_str}")


if __name__ == "__main__":
    main()
