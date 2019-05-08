import prettytable 

from schedule import Schedule
from genetic import GeneticOptimize


def vis(schedule):
    """visualization Class Schedule.

    Arguments:
        schedule: List, Class Schedule
    """
    col_labels = ['week/slot', '1', '2', '3', '4', '5']
    table_vals = [[i + 1, '', '', '', '', ''] for i in range(5)]

    table = prettytable.PrettyTable(col_labels, hrules=prettytable.ALL)

    for s in schedule:
        weekDay = s.weekDay
        slot = s.slot
        text = 'course: {} \n class: {} \n room: {} \n teacher: {}'.format(s.courseId, s.classId, s.roomId, s.teacherId)
        table_vals[weekDay - 1][slot] = text

    for row in table_vals:
        table.add_row(row)

    print(table)


if __name__ == '__main__':
    schedules = []

    # add schedule
    schedules.append(Schedule(201, 1201, 11101))
    schedules.append(Schedule(201, 1201, 11101))
    schedules.append(Schedule(202, 1201, 11102))
    schedules.append(Schedule(202, 1201, 11102))
    schedules.append(Schedule(203, 1201, 11103))
    schedules.append(Schedule(203, 1201, 11103))
    schedules.append(Schedule(206, 1201, 11106))
    schedules.append(Schedule(206, 1201, 11106))

    schedules.append(Schedule(202, 1202, 11102))
    schedules.append(Schedule(202, 1202, 11102))
    schedules.append(Schedule(204, 1202, 11104))
    schedules.append(Schedule(204, 1202, 11104))
    schedules.append(Schedule(206, 1202, 11106))
    schedules.append(Schedule(206, 1202, 11106))

    schedules.append(Schedule(203, 1203, 11103))
    schedules.append(Schedule(203, 1203, 11103))
    schedules.append(Schedule(204, 1203, 11104))
    schedules.append(Schedule(204, 1203, 11104))
    schedules.append(Schedule(205, 1203, 11105))
    schedules.append(Schedule(205, 1203, 11105))
    schedules.append(Schedule(206, 1203, 11106))
    schedules.append(Schedule(206, 1203, 11106))

    # optimization
    ga = GeneticOptimize(popsize=50, elite=10, maxiter=500)
    res = ga.evolution(schedules, 3)

    # visualization
    vis_res = []
    for r in res:
        if r.classId == 1203:
            vis_res.append(r)
    vis(vis_res)
