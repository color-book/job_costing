import pandas as pd

class JobAlgorithm:

  '''
    Job Info is the data that has been checked
    and packaged by the InputVerification class
  '''
  def __init__(self, job_info):
    self.job_info = job_info
    self.errors_present = False
    self.error_message = ''

  def calculate_overall_costs(self):
    # result = pd.Series()

    job_total = self.job_info['job_total']
    down_payment_percentage = self.job_info['down_payment_percentage']
    down_payment = job_total * down_payment_percentage
    materials = self.job_info['materials']
    materials_total = sum(self.job_info['materials'])
    labor = job_total - materials_total
    ct_split_percentage = self.job_info['ct_split']
    ct_split = labor * ct_split_percentage
    ct_split_final_payout = ct_split - down_payment
    sub_split_percentage = self.job_info['sub_split']
    sub_split = labor * sub_split_percentage
    
    self.ct_split_final_payout = ct_split_final_payout
    self.sub_split = sub_split

    # TODO: I think this would be better as a dataframe?
    result = pd.Series(
      [job_total, down_payment_percentage, down_payment, materials, materials_total, labor, ct_split_percentage, 
      ct_split, ct_split_final_payout, sub_split_percentage, sub_split],
      index=['job_total', 'down_payment_percentage', 'down_payment', 'materials', 'materials_total', 'labor', 'ct_split_percentage',
      'ct_split', 'ct_split_final_payout', 'sub_split_percentage', 'sub_split'])
    return result

  def calculate_painter_rates(self):
    initial_sub_split = self.sub_split
    labor_info = self.job_info['labor_info']
    row_labels = pd.Index(["weight", "hours", "total_hours", "payout", "hourly_average"], name="rows")
    painter_names = []
    total_hours = sum([i['hours'] for i in labor_info])
    final = {}
    for painter in labor_info:
      painter_data = []
      painter_name = painter['name']
      weight = painter['weight']
      hours = painter['hours']
      earnings = initial_sub_split * weight * (hours / total_hours)
      payout = earnings + painter['reimbursement'] - painter['rental']
      hourly_average = earnings / hours

      if self.sub_split > 0 and self.sub_split > payout:
        self.sub_split = self.sub_split - payout
      elif self.ct_split_final_payout > 0 and (self.ct_split_final_payout > payout or self.ct_split_final_payout > (payout - self.sub_split)):
        self.ct_split_final_payout = self.ct_split_final_payout - (payout - self.sub_split)
        if self.sub_split > 0:
          self.sub_split = 0
      else:
        self.ct_split_final_payout = self.ct_split_final_payout - (payout - self.sub_split)
        self.sub_split = 0
        self.errors_present = True
        self.error_message = '''ERROR: Payout totals are greater than the split totals. The contractor split is now negative.
        Sub Contractor Payouts are first subtracted from the Sub Contractor split. Once that reaches zero
        they're then taken from the Contractor split. If possible, please adjust accordingly.'''

      painter_data.append(weight)
      painter_data.append(hours)
      painter_data.append(total_hours)
      painter_data.append(payout)
      painter_data.append(hourly_average)

      painter_names.append(painter_name)
      final[painter_name] = painter_data

    column_labels = pd.Index(painter_names, name="columns")
    result = pd.DataFrame(data=final, index=row_labels, columns=column_labels)
    return result

  def calculate_job_cost(self):
    result = {}
    overall_costs = self.calculate_overall_costs()
    # sub_split = overall_costs['sub_split']
    # result['overall_costs'] = overall_costs
    result['painter_rates'] = self.calculate_painter_rates()

    overall_costs['ct_split_final_payout'] = self.ct_split_final_payout
    overall_costs['sub_split_left_over'] = self.sub_split
    # overall_costs['sub_split'] = self.sub_split

    result['overall_costs'] = overall_costs
    result['costing_errors'] = {
      "errors": self.errors_present,
      "error_message": self.error_message
    }


    return result

  

