

class InputVerification:

  def verify_correct_data_and_format(self, job_total, down_payment_percentage, materials, ct_split, sub_split, labor_info):
    job_info = {
      'job_total': float(job_total),
      'down_payment_percentage': float(down_payment_percentage), 
      'materials': materials,
      'total_materials': sum(materials),
      'ct_split': float(ct_split),
      'sub_split': float(sub_split),
      'labor_info': labor_info
    }

    splits_add_correctly = self.splits_should_equal_one_hundred(job_info['ct_split'], job_info['sub_split'])

    if splits_add_correctly:
      return job_info

  def splits_should_equal_one_hundred(self, ct_split, sub_split):
    return ct_split + sub_split == 1


    