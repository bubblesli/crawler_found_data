data=[['\n\n\n净值日期\n单位净值\n累计净值\n日增长率\n申购状态\n赎回状态\n分红送配\n\n\n\n\n2024-03-22\n1.9630\n                            \n                      \n2.7190\n4.53%\n开放申购\n开放赎回\n\n\n\n2024-03-21\n1.8780\n                            \n                      \n2.6340\n2.62%\n开放申购\n开放赎回\n\n\n\n2024-03-20\n1.8300\n                            \n                      \n2.5860\n4.93%\n开放申购\n开放赎回\n\n\n\n2024-03-19\n1.7440\n                            \n                      \n2.5000\n0.16%\n限制大额申购\n开放赎回\n每份派现金0.0860元\n\n\n2024-03-18\n1.8270\n                            \n                      \n2.4970\n3.34%\n限制大额申购\n开放赎回\n\n\n\n2024-03-15\n1.7680\n                            \n                      \n2.4380\n0.97%\n限制大额申购\n开放赎回\n\n\n\n2024-03-14\n1.7510\n                            \n                      \n2.4210\n-2.07%\n开放申购\n开放赎回\n\n\n\n2024-03-13\n1.7880\n                            \n                      \n2.4580\n2.58%\n开放申购\n开放赎回\n\n\n\n2024-03-12\n1.7430\n                            \n                      \n2.4130\n-0.17%\n开放申购\n开放赎回\n\n\n\n2024-03-11\n1.7460\n                            \n                      \n2.4160\n2.34%\n开放申购\n开放赎回\n\n\n\n2024-03-08\n1.7060\n                            \n                      \n2.3760\n1.07%\n开放申购\n开放赎回\n\n\n\n2024-03-07\n1.6880\n                            \n                      \n2.3580\n-1.92%\n开放申购\n开放赎回\n\n\n\n2024-03-06\n1.7210\n                            \n                      \n2.3910\n-1.15%\n开放申购\n开放赎回\n\n\n\n2024-03-05\n1.7410\n                            \n                      \n2.4110\n-1.47%\n开放申购\n开放赎回\n\n\n\n2024-03-04\n1.7670\n                            \n                      \n2.4370\n2.32%\n开放申购\n开放赎回\n\n\n\n2024-03-01\n1.7270\n                            \n                      \n2.3970\n3.04%\n开放申购\n开放赎回\n\n\n\n2024-02-29\n1.6760\n                            \n                      \n2.3460\n3.39%\n开放申购\n开放赎回\n\n\n\n2024-02-28\n1.6210\n                            \n                      \n2.2910\n-4.87%\n开放申购\n开放赎回\n\n\n\n2024-02-27\n1.7040\n                            \n                      \n2.3740\n3.65%\n开放申购\n开放赎回\n\n\n\n2024-02-26\n1.6440\n                            \n                      \n2.3140\n0.24%\n开放申购\n开放赎回\n\n\n\n']]
# 定义列名
column_names = ['净值日期', '单位净值', '累计净值', '日增长率']
result_data = []
# 将原始数据转换为整洁格式
cleaned_data = []
data_date = []
data_Net_unit_value = []
data_Cumulative_net_worth = []
data_Daily_growth_rate = []
for sublist in data[0]:
    lines = sublist.split('\n')
    for i in lines:
        if i == '':
            continue
        elif i =='净值日期':
            continue
        elif i == '单位净值':
            continue
        elif i =='累计净值':
            continue
        elif i == '日增长率':
            continue
        elif i =='申购状态':
            continue
        elif i == '赎回状态':
            continue
        elif i == '红送配':
            continue
        elif i == '                            ':
            continue
        elif i == '开放申购':
            continue
        elif i == '开放赎回':
            continue
        elif i == '限制大额申购':
            continue
        elif i == '每份派现金0.0860元':
            continue
        elif i == '分红送配':
            continue
        elif i == '                      ':
            continue

        else:
            result_data.append(i)
step = 0
for i in result_data:
    if step % 4 == 0:
        data_date.append(i)
    if step % 4 == 1:
        data_Net_unit_value.append(i)
    if step % 4 == 2:
        data_Cumulative_net_worth.append(i)
    if step % 4 == 3:
        data_Daily_growth_rate.append(i)
        if i == '--':
            break
    step += 1
print(data_date)
print(data_Net_unit_value)
print(data_Cumulative_net_worth)
print(data_Daily_growth_rate)

#print(result_data)
