import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import xlsxwriter

date = datetime.now()
number_lst = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
task_dict = {"Pipettes": ["1mL", "2mL", "4mL", "5mL", "10mL", "20mL"],
             "Vol. Flasks": ["25mL clear", "50mL clear", "50mL amber", "100mL clear", "100mL amber", "250mL clear"]}

input_analyst: str = input("Enter number of analysts to complete tasks: ")
for letter in input_analyst:
    if letter not in number_lst:
        print('Error: Only numerical values accepted.')
        exit()

input_months: str = input("Enter number of months for task assignment: ")
for letter in input_months:
    if letter not in number_lst:
        print('Error: Only numerical values accepted.')
        exit()

analyst_lst = ["Analyst " + str(num + 1) for num in range(int(input_analyst))]

p_tasks = {}
v_tasks = {}
p_task_count = {}
v_task_count = {}

for analyst in analyst_lst:
    p_tasks[analyst] = []
    v_tasks[analyst] = []
    p_task_count[analyst] = 0
    v_task_count[analyst] = 0


def not_repeated(temp_dict, final_dict):
    bool_response = True
    for key in final_dict.keys():
        if type(final_dict[key]) == list:
            if len(final_dict[key]) == 0:
                break
            else:
                if final_dict[key][-1] in temp_dict[key]:
                    bool_response = False
                    break
    return bool_response


def not_unfairly_assigned(task_count_dict):
    x = True
    maxi = -9999
    mini = 9999
    for value in task_count_dict.values():
        if value > maxi:
            maxi = value
        if value < mini:
            mini = value
    difference = maxi - mini
    if difference > 1:
        x = False
    return x


def equal_task_assigner(lst_of_analysts, lst_of_tasks, output_dict):
    completed = False
    while not completed:
        index = 0
        temp_dict = {}
        random.shuffle(lst_of_analysts)
        for task in lst_of_tasks:
            temp_dict[lst_of_analysts[index]] = task
            index += 1
        completed = not_repeated(temp_dict, output_dict)
        if completed:
            for key, value in temp_dict.items():
                output_dict[key].append(value)


def count_combine_temp(temp, output):
    d = {}
    for k, v in output.items():
        d[k] = v
    for key, value in temp.items():
        d[key] += value
    return d


def count_combine_perm(temp, output):
    d = output
    for key, value in temp.items():
        d[key] += value
    return d


def task_counter_temp(temp_task_dict):
    d = {}
    for key, value in temp_task_dict.items():
        if type(value) == list:
            task_num = len(value)
            d[key] = task_num
    return d


def more_tasks_analysts(lst_of_analysts, lst_of_tasks, output_dict, count_dict):
    completed = False
    fair = False
    while not completed or not fair:
        temp_dict = {}
        for a in lst_of_analysts:
            temp_dict[a] = []
        index = 0
        random.shuffle(lst_of_analysts)
        random.shuffle(lst_of_tasks)
        for task in lst_of_tasks:
            temp_dict[lst_of_analysts[(index % len(lst_of_analysts))]].append(task)
            index += 1
        temp_count_dict = task_counter_temp(temp_dict)
        completed = not_repeated(temp_dict, output_dict)
        fair = not_unfairly_assigned(count_combine_temp(temp_count_dict, count_dict))
        if completed and fair:
            count_combine_perm(temp_count_dict, count_dict)
            for key, value in temp_dict.items():
                if len(value) > 1:
                    output_dict[key].append(value)
                else:
                    output_dict[key].append(value[0])


def less_task_analyst_counter_temp(temp_dict):
    d = {}
    for k, v in temp_dict.items():
        if v == '-':
            d[k] = 0
        else:
            d[k] = 1
    return d


def less_tasks_analysts_repeat_check(temp_dict, output_dict):
    repeat = True
    for k, v in temp_dict.items():
        if v == '-':
            pass
        elif len(output_dict[k]) == 0:
            break
        else:
            if v == output_dict[k][-1]:
                repeat = False
    return repeat


def less_tasks_analysts(lst_of_analysts, lst_of_tasks, output_dict, count_dict):
    completed = False
    fair = False
    while not completed or not fair:
        temp_dict = {}
        index = 0
        random.shuffle(lst_of_analysts)
        random.shuffle(lst_of_tasks)
        for anlst in analyst_lst:
            if index < len(lst_of_tasks):
                temp_dict[anlst] = lst_of_tasks[index]
                index += 1
            elif index >= len(lst_of_tasks):
                temp_dict[anlst] = '-'
        temp_count_dict = less_task_analyst_counter_temp(temp_dict)
        completed = less_tasks_analysts_repeat_check(temp_dict, output_dict)
        fair = not_unfairly_assigned(count_combine_temp(temp_count_dict, count_dict))
        if completed and fair:
            count_combine_perm(temp_count_dict, count_dict)
            for key, value in temp_dict.items():
                output_dict[key].append(value)


for month in range(int(input_months)):
    num_v_tasks_to_assign = len(task_dict["Vol. Flasks"])
    if int(input_analyst) == num_v_tasks_to_assign:
        equal_task_assigner(analyst_lst, task_dict['Vol. Flasks'], v_tasks)
    elif int(input_analyst) < num_v_tasks_to_assign:
        more_tasks_analysts(analyst_lst, task_dict['Vol. Flasks'], v_tasks, v_task_count)
    elif int(input_analyst) > num_v_tasks_to_assign:
        less_tasks_analysts(analyst_lst, task_dict['Vol. Flasks'], v_tasks, v_task_count)
    else:
        print('Error')

for month in range(int(input_months)):
    num_p_tasks_to_assign = len(task_dict["Pipettes"])
    if int(input_analyst) == num_p_tasks_to_assign:
        equal_task_assigner(analyst_lst, task_dict["Pipettes"], p_tasks)
    elif int(input_analyst) < num_p_tasks_to_assign:
        more_tasks_analysts(analyst_lst, task_dict["Pipettes"], p_tasks, p_task_count)
    elif int(input_analyst) > num_p_tasks_to_assign:
        less_tasks_analysts(analyst_lst, task_dict["Pipettes"], p_tasks, p_task_count)
    else:
        print('Error')


def analyst_task_printer(task_dic):
    for pers, tasks in task_dic.items():
        month_count = 1
        global date
        print('\n' '---- ' + pers + ' ----')
        for task in tasks:
            task_month = date + relativedelta(months=month_count)
            print(task_month.strftime('%B') + ': ' + str(task))
            month_count += 1


end_month = date + relativedelta(months=int(input_months))
workbook = xlsxwriter.Workbook('Monthly_task_assignment_workbook.xlsx')
worksheet = workbook.add_worksheet('Tasks ' + date.strftime('%m' + '_' + '%y') + ' '
                                   + end_month.strftime('%m' + '_' + '%y'))


def formatting_workbook():
    head = workbook.add_format()
    head.set_font_size(16)
    head.set_bold(True)
    title = workbook.add_format()
    title.set_font_size(12)
    title.set_bold(True)
    return head, title


def workbook_creation(task_d: dict, type_of_task: str, starting_column: int):
    head, title = formatting_workbook()
    worksheet.write(0, starting_column, type_of_task, head)
    row = 1
    col = starting_column

    for pers, t_l in task_d.items():
        mnth_count = 1
        row += 1
        worksheet.write(row, 1, pers, title)
        row += 1

        for months_task_s in t_l:

            tsk_month = date + relativedelta(months=mnth_count)
            worksheet.write(row, 0, tsk_month.strftime('%B' + ' %y'))
            mnth_count += 1

            if type(months_task_s) == list:
                combined_tasks = ''
                for single_task in months_task_s:
                    combined_tasks += str(single_task) + ', '
                worksheet.write(row, col, combined_tasks[:-2])
                row += 1
            else:
                worksheet.write(row, col, months_task_s)
                row += 1


workbook_creation(p_tasks, 'Pipette Tasks', 1)
workbook_creation(v_tasks, 'Volumetric Tasks', 3)

worksheet.set_column(0, 1, 18)
worksheet.set_column(3, 3, 22)

workbook.close()
