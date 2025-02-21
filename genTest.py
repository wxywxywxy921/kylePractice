import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date

# Function to generate random problems
def generate_problems(num_problems, operation):
    problems = []
    solutions = []

    for _ in range(num_problems):
        if operation == '/':
            num1 = random.randint(2, 9)
            num2 = num1
            while num2 == num1:
                num2 = random.randint(2, 9)
        elif operation == '*':
            num1 = random.randint(2, 99)
            num2 = random.randint(2, 9)
        else:
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)
        
        if operation == '/':
            num1 = num1 * num2
        elif operation == '-':
            if num1 < num2:
                num1, num2 = num2, num1

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1  - num2
        elif operation == '*':
            result = num1 * num2   
        elif operation == '/':
            result = num1 / num2

        problems.append("{} {} {} {}".format(num1, operation, num2, '='))
        solutions.append("{} {} {} {} {}".format(num1, operation, num2, '=', result))
    return problems, solutions

# Function to export problems to a PDF
def export_to_pdf(problems, filename, num_problems):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 12)
    margin = 50
    line_height = 16
    problems_per_row = 4
    x_start, y_start = margin, height - margin
    x, y = x_start, y_start

    today = date.today()
    formatted_date = today.strftime("%B %d, %Y")
    title = "Math Practice Problems: " + formatted_date
    c.drawString(x, y, title)
    y -= line_height * 2

    for i, problem in enumerate(problems, start=1):
        c.drawString(x, y, f"{problem}")
        x += width / problems_per_row - 20
        if i % problems_per_row == 0:
            x = x_start
            y -= line_height
        if y < margin:  # Start a new page if space runs out
            c.showPage()
            c.setFont("Helvetica", 10)
            y = y_start
        if i % num_problems  == 0:
            x = x_start
            y -= line_height * 2

    c.save()

# Generate problems and export
num_problems = 28
operations = ['+', '-', '*', '/']
problems = []
solutions = []

for operation in operations:
    problemsTemp, solutionsTemp = generate_problems(num_problems, operation)
    problems = problems + problemsTemp
    solutions = solutions + solutionsTemp

export_to_pdf(problems, "math_practice.pdf", num_problems)
export_to_pdf(solutions, "math_solutions.pdf", num_problems)

print("PDF with math practice problems has been created.")
