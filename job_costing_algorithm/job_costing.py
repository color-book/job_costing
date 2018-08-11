import pprint

try:
    # Trying to find module in the parent package
    from .input_verification import InputVerification
    from .job_algorithm import JobAlgorithm
except ImportError:
    print('Relative import not needed')

try:
    # Trying to find module on sys.path
    from input_verification import InputVerification
    from job_algorithm import JobAlgorithm
except ModuleNotFoundError:
    print('Absolute import not needed')

class JobCosting:

  def __init__(self, job_info):
    self.job_info = job_info

  def run_algorithm(self):
    formatted_job_info = InputVerification().verify_correct_data_and_format(self.job_info)

    result = JobAlgorithm(formatted_job_info).calculate_job_cost()
    return result

  def convert_to_file(self):
    return 'convert result to a file'


def main():
    result = {}
    job_info = {
      "job_total": 3500,
      "down_payment_percentage": .25,
      "materials": [50, 100, 100, 250],
      "ct_split": .5,
      "sub_split": .5,
      "labor_info": [{
      'name': 'Eric',
      'weight': .8,
      'hours': 15
    }, {
      'name': 'Sara',
      'weight': .9,
      'hours': 25
    }, {
      'name': 'Jeff',
      'weight': 1,
      'hours': 35
    }]
    }
    job_cost_results = JobCosting(job_info).run_algorithm()
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint('OVERALL COSTS')
    pp.pprint(job_cost_results['overall_costs'])
    pp.pprint('===================================')
    pp.pprint('PAINTER RATES')
    pp.pprint(job_cost_results['painter_rates'])

if __name__ == "__main__":
  main()
