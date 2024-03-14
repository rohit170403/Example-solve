from flask import Flask, render_template, request
import numpy as np
from scipy.optimize import linear_sum_assignment

app = Flask(__name__, static_url_path='/static', static_folder='static')

def hungarian_algorithm(cost_matrix):
    row_indices, col_indices = linear_sum_assignment(cost_matrix)
    total_cost = cost_matrix[row_indices, col_indices].sum()
    assignment = [(row, col) for row, col in zip(row_indices, col_indices)]
    return assignment, total_cost

@app.route('/', methods=['GET', 'POST'])
def index():
    assignment = None
    total_cost = None
    cost_matrix = None
    if request.method == 'POST':
        cost_matrix = parse_input(request.form['cost_matrix'])
        assignment, total_cost = hungarian_algorithm(cost_matrix)
    return render_template('index.html', assignment=assignment, total_cost=total_cost, cost_matrix=cost_matrix)

def parse_input(input_text):
    rows = input_text.strip().split('\n')
    matrix = [list(map(int, row.strip().split())) for row in rows]
    return np.array(matrix)

if __name__ == '__main__':
    app.run(debug=True)
