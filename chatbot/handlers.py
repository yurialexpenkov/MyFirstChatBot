import re

import calendar
import datetime

from generate_ticket import generate_ticket

LIST_SITY = [
    {'санкт-петербург': [
        {'мюнхен': [['нед:', 1, 3, 5], [18, 30]]},
        {'пхукет': [['нед:', 0, 1, 2, 3, 4, 5, 6], [20, 30]]},
        {'сайгон': [['мес:', 5, 15, 25], [16, 30]]},
        {'бали': [['нед:', 0, 1, 2, 3, 4, 5, 6], [14, 30]]}
    ]
    },
    {'мюнхен': [
        {'санкт-петербург': [['нед:', 1, 3, 5], [17, 30]]},
        {'пхукет': [['нед:', 0, 1, 2, 3, 4, 5, 6], [21, 30]]},
        {'сайгон': [['мес:', 5, 15, 25], [15, 30]]},
        {'бали': [['нед:', 0, 1, 2, 3, 4, 5, 6], [11, 30]]}
    ]
    },
    {'пхукет': [
        {'мюнхен': [['нед:', 1, 3, 5], [10, 30]]},
        {'санкт-петербург': [['нед:', 0, 1, 2, 3, 4, 5, 6], [22, 30]]},
        {'сайгон': [['мес:', 5, 15, 25], [23, 30]]},
        {'бали': [['нед:', 0, 1, 2, 3, 4, 5, 6], [17, 30]]}
    ]
    },
    {'сайгон': [
        {'пхукет': [['нед:', 1, 3, 5], [9, 30]]},
        {'санкт-петербург': [['нед:', 0, 1, 2, 3, 4, 5, 6], [7, 30]]},
        {'бали': [['мес:', 5, 15, 25], [8, 30]]}
    ]
    },

    {'бали': [
        {'мюнхен': [['нед:', 1, 3, 5], [17, 30]]},
        {'пхукет': [['нед:', 0, 1, 2, 3, 4, 5, 6], [7, 30]]},
        {'сайгон': [['мес:', 5, 15, 25], [23, 30]]},
        {'санкт-петербург': [['нед:', 1, 3, 5], [10, 30]]}
    ]
    }

]


def handler_sity_of_departyre(text, context):
    for sity in LIST_SITY:
        if text.lower() in sity.keys():
            context['sity_of_departyre'] = text.lower()
            return True
    else:
        return False


def handler_sity_of_arrival(text, context):
    for sity in LIST_SITY:
        if context['sity_of_departyre'] in sity.keys():
            for sity2 in sity[context['sity_of_departyre']]:
                if text.lower() in sity2.keys():
                    context['sity_of_arrival'] = text.lower()
                    return True
                else:
                    continue
    else:
        return False


def handler_selection_of_tickets_on_a_given_date(text, context):
    return selecting_dates(context, text)


def selecting_dates(context, text):
    """
    Подбирает список дат вылета самолетов, исходя из запрошенной даты
    :param context:
    :param text:
    :return:
    """
    flight_schedule = search_for_flight_schedule_data(context)
    departure_date = datetime.datetime.strptime(text, '%d-%m-%Y')
    if departure_date < datetime.datetime.today():
        return False
    i = 0
    current_day = departure_date
    list_aircraft_flight_date = []
    while i < 5:
        print(current_day.weekday(), current_day.weekday() in flight_schedule[0][1:-1])
        if (current_day.weekday() in flight_schedule[0][1:] and 'нед' in flight_schedule[0][0]) or \
                (current_day.day in flight_schedule[0][1:] and 'мес' in flight_schedule[0][0]):
            aircraft_flight_date = datetime.datetime(year=current_day.year, month=current_day.month,
                                                     day=current_day.day, hour=flight_schedule[1][0],
                                                     minute=flight_schedule[1][1])
            list_aircraft_flight_date.append([i + 1, aircraft_flight_date.strftime("вариант - %d-%m-%Y %H:%M")])
            current_day = current_day + datetime.timedelta(days=1)
            i += 1
        else:
            current_day = current_day + datetime.timedelta(days=1)
    context['list_aircraft_flight'] = list_aircraft_flight_date
    print(list_aircraft_flight_date)
    return True


def search_for_flight_schedule_data(context):
    """
    Пасит и возвращает данные о графике полетов, между городами вылета и прилета из списка LIST_SITY
    :param context:
    :return:
    """
    for sity in LIST_SITY:
        if context['sity_of_departyre'] in sity.keys():
            for sity2 in sity[context['sity_of_departyre']]:
                if context['sity_of_arrival'] in sity2.keys():
                    return sity2[context['sity_of_arrival']]


def departure_date_selection(text, context):
    print(context['list_aircraft_flight'])
    for date in context['list_aircraft_flight']:
        if date[0] == int(text):
            context['selected_flight_date'] = date[1]
            return True
        else:
            continue
    else:
        return False


def choice_of_number_of_seats(text, context):
    if str(text) in ['1', '2', '3', '4', '5']:
        context['choice_of_number_of_seats'] = text
        return True
    else:
        return False


def comment_entry(text, context):
    if text:
        context['comment_entry'] = text
        return True
    else:
        context['comment_entry'] = None
        return False


def clarification_of_entered_data(text, context):
    return text.lower() == 'да'


re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_surname = re.compile(r'^[\w\-\s]{3,40}$')


def handler_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handler_surname(text, context):
    match = re.match(re_surname, text)
    if match:
        context['surname'] = text
        return True
    else:
        return False


def generate_ticket_handler(text, context):
    return generate_ticket(name=context['name'],
                           surname=context['surname'],
                           sity_of_departyre=context['sity_of_departyre'],
                           sity_of_arrival=context['sity_of_arrival'],
                           selected_flight_date=context['selected_flight_date'][9:],
                           )
