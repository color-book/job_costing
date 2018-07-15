import json
from flask import Flask, request
from flask import jsonify
from job_costing_algorithm.job_costing import JobCosting

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Job Costing Algorithm'})

@app.route('/job-costing/v1/calculate-job', methods=["POST"])
def calculate_job():
    job_info = request.json
    job_cost_results = JobCosting(job_info).run_algorithm()

    painter_rates = format_painter_results(job_cost_results['painter_rates'])
    result = {
        "overall_costs": json.loads(job_cost_results['overall_costs'].to_json()),
        "painter_rates": painter_rates,
        "costing_errors": job_cost_results['costing_errors']
    }
    return jsonify(result)

def format_painter_results(painter_rates):
    return_values = []
    for painter in painter_rates:
        painter_info = {}
        painter_info['name'] = painter
        painter_info['weight'] = painter_rates[painter]['weight']
        painter_info['hours'] = painter_rates[painter]['hours']
        painter_info['total_hours'] = painter_rates[painter]['total_hours']
        painter_info['payout'] = painter_rates[painter]['payout']
        painter_info['hourly_average'] = painter_rates[painter]['hourly_average']
        return_values.append(painter_info)
    return return_values

if __name__ == '__main__':
    app.run()