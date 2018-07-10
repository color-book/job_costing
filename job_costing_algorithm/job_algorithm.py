import pandas as pd

class JobAlgorithm:

  '''
    Job Info is the data that has been checked
    and packaged by the InputVerification class
  '''
  def __init__(self, job_info):
    self.job_info = job_info

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
      payout = initial_sub_split * weight * (hours / total_hours)
      hourly_average = payout / hours

      if self.sub_split > 0 and self.sub_split > payout:
        self.sub_split = self.sub_split - payout
      elif self.ct_split_final_payout > 0 and self.ct_split_final_payout > payout:
        self.ct_split_final_payout = self.ct_split_final_payout - payout
      else:
        self.sub_split = 0
        self.ct_split_final_payout = 0
        print('ERROR ERROR ERROR Payouts are greater than splits')

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


    return result

  

