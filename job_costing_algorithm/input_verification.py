

class InputVerification:

  def __init__(self):
    self.sum = 1+1

  def verify_correct_data_and_format(self, job_info):
    formatted_job_info = {
      'job_total': float(job_info['job_total']),
      'down_payment_percentage': float(job_info['down_payment_percentage']), 
      'materials': job_info['materials'],
      'total_materials': sum(job_info['materials']),
      'ct_split': float(job_info['ct_split']),
      'sub_split': float(job_info['sub_split']),
      'labor_info': job_info['labor_info']
    }

    splits_add_correctly = self.splits_should_equal_one_hundred(formatted_job_info['ct_split'], formatted_job_info['sub_split'])

    if splits_add_correctly:
      return formatted_job_info


  def splits_should_equal_one_hundred(self, ct_split, sub_split):
    return ct_split + sub_split == 1


    