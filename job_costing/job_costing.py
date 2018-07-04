import pprint

from input_verification import InputVerification
from job_algorithm import JobAlgorithm

class JobCosting:

  # TODO: Maybe think about bundling this up?
  def __init__(self, job_total, down_payment_percentage, materials, ct_split, sub_split, labor_info):
    self.job_total = job_total
    self.down_payment_percentage = down_payment_percentage
    self.materials = materials
    self.ct_split = ct_split
    self.sub_split = sub_split
    self.labor_info = labor_info

  def run_algorithm(self):
    job_info = InputVerification().verify_correct_data_and_format(
        self.job_total, self.down_payment_percentage, self.materials, 
        self.ct_split, self.sub_split, self.labor_info)

    result = JobAlgorithm(job_info).calculate_job_cost()
    return result

  def convert_to_file(self):
    return 'convert result to a file'


def main():
    result = {}
    labor_info = [{
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
    job_cost_results = JobCosting(3500, .25, [50, 100, 100, 250], .5, .5, labor_info).run_algorithm()
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint('OVERALL COSTS')
    pp.pprint(job_cost_results['overall_costs'])
    pp.pprint('===================================')
    pp.pprint('PAINTER RATES')
    pp.pprint(job_cost_results['painter_rates'])

if __name__ == "__main__":
  main()
