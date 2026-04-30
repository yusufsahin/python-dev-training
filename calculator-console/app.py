from flask import Flask, render_template, request
from calculator import add, subtract, multiply, divide, format_for_display
from calculator.validation import validate_calculator_input

app = Flask(__name__)

OPERATIONS = {
    "add": (add, "+"),
    "subtract": (subtract, "-"),
    "multiply": (multiply, "*"),
    "divide": (divide, "/")
}

@app.route("/", methods=["GET", "POST"])
def index():
    result_text = None
    errors = {}
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()
        is_valid, errors, validated = validate_calculator_input(form_data)

        if is_valid:
            op_name = validated["operation"]
            first = validated["first_number"]
            second = validated["second_number"]
            
            func, symbol = OPERATIONS[op_name]
            result = func(first, second)
            
            if result is None:
                errors["second_number"] = "Sıfıra bölme hatası. İkinci sayı 0 olamaz."
            else:
                a_str = format_for_display(first)
                b_str = format_for_display(second)
                res_str = format_for_display(result)
                result_text = f"{a_str} {symbol} {b_str} = {res_str}"

    return render_template("index.html", result_text=result_text, errors=errors, form_data=form_data)

if __name__ == "__main__":
    app.run(debug=True)
