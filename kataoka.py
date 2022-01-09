import manage_number_of_people as ma
import datetime
import time
from multiprocessing import Process
import datetime as dt
import database_sql

def main(start:int, end:int, standard:int, standard_time:int):
    date = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    ser = ma.serial_transmission()
    manage = ma.manage_number_of_people()
    tmp = ma.tmp_database()
    sql = database_sql()
    isDone = False
    while True:
        if dt.datetime.now().strftime('%a') in date:
            if start <= dt.datetime.now().hour < end and not isDone:
                p1 = Process(target = manage.renew_tmp_database, args = (end, standard_time, tmp))
                p1.start()
                if not (ser.keep_waiting_signal(end, tmp, standard, sql)):
                    print('q:interrupt')
                    break
                p1.join()
                tmp.show()
                sql.add_datas(tmp.people_num_list_dict['total_people_list'],
                              tmp.people_num_list_dict['max_people_list'],
                              tmp.people_num_list_dict['count_warning_list'])
                isDone =  True
            else:
                isDone = False
        else:
            isDone = False
    ser.close()

if __name__ == '__main__':
    main(8, 17, 10, 1)