import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import date
import argparse

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
def export_to_pdf(problems, pdfFile, num_problems, pageIndex):
    width, height = letter

    pdfFile.setFont("Helvetica", 12)
    margin = 50
    line_height = 16
    problems_per_row = 4
    x_start, y_start = margin, height - margin
    x, y = x_start, y_start

    today = date.today()
    formatted_date = today.strftime("%B %d, %Y")
    title = "Math Practice Problems: " + formatted_date + " : page: {}".format(pageIndex)
    pdfFile.drawString(x, y, title)
    y -= line_height * 2

    for i, problem in enumerate(problems, start=1):
        pdfFile.drawString(x, y, f"{problem}")
        x += width / problems_per_row - 20
        if i % problems_per_row == 0:
            x = x_start
            y -= line_height
        if y < margin:  # Start a new page if space runs out
            pdfFile.showPage()
            pdfFile.setFont("Helvetica", 10)
            y = y_start
        if i % num_problems  == 0:
            x = x_start
            y -= line_height * 2

    pdfFile.showPage()

def generate_problem_one_page(pageIndex, pdfQuiz, pdfSolution):
    # Generate problems and export
    num_problems = 28
    operations = ['+', '-', '*', '/']
    problems = []
    solutions = []

    for operation in operations:
        problemsTemp, solutionsTemp = generate_problems(num_problems, operation)
        problems = problems + problemsTemp
        solutions = solutions + solutionsTemp

    export_to_pdf(problems, pdfQuiz, num_problems, pageIndex)
    export_to_pdf(solutions, pdfSolution, num_problems, pageIndex)

    print("PDF with math practice problems has been created. page: {}".format(pageIndex))

def main():
    parser = argparse.ArgumentParser(description="generating math quiz for Kyle")
    parser.add_argument("-p", "--pageCount", type=int, help="how mane pages to generate", default=1)
    args = parser.parse_args()

    pdfQuizName = "math_practice.pdf"
    pdfSolutionName = "math_solution.pdf"

    pdfQuiz = canvas.Canvas(pdfQuizName, pagesize=letter)
    pdfSolution = canvas.Canvas(pdfSolutionName, pagesize=letter)

    for pageIndex in range(args.pageCount):
        generate_problem_one_page(pageIndex, pdfQuiz, pdfSolution)

    pdfQuiz.save()
    pdfSolution.save()


if __name__ == "__main__":
    main()


