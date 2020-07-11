from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, asc
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# session.query(Table).delete()
# session.commit()
while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit

    """)

    choice = int(input())

    if choice == 0:
        print('\nBye!')

        break

    if choice == 5:
        print('Enter task')
        t = input()
        t_raw = input()
        t_task= datetime.strptime(t_raw,  '%Y-%m-%d' )
        new_row = Table(task=t, deadline=t_task)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    if choice == 1:
        today = datetime.today()

        print("""\nToday {} {}:""".format(today.day, today.strftime('%b')))

        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if rows:
            counter = 1
            for x in rows:
                print('{}. {}'.format(counter, x.task))
                # print(x.id)
                # print(x.deadline)
                counter += 1
        else:
            print("Nothing to do!")
        print('\n')
    if choice == 2:
        today = datetime.today()

        for i in range(7):

            d_iter = today + timedelta(days=i)
            print("""\n{} {} {}:""".format(d_iter.strftime('%A'), d_iter.day, d_iter.strftime('%b')))
            rows = session.query(Table).filter(Table.deadline == d_iter.date()).all()
            if rows:
                counter = 1
                for x in rows:
                    print('{}. {}'.format(counter, x.task))
                    # print(x.id)
                    # print(x.deadline)
                    counter += 1
            else:
                print("Nothing to do!")
        print('\n')
    if choice == 3:
        today = datetime.today()

        print("""\nAll tasks:""")

        rows = session.query(Table).order_by(asc(Table.deadline)).all()
        if rows:
            counter = 1
            for x in rows:

                print('{}. {} {} {}'.format(counter, x.task, x.deadline.day, x.deadline.strftime('%b') ))
                # print(x.id)
                # print(x.deadline)
                counter += 1
        else:
            print("Nothing to do!")
        print('\n')
    if choice == 4:
        today = datetime.today()

        print("""\nMissed tasks:""")

        rows = session.query(Table).filter(Table.deadline < today.date()).order_by(asc(Table.deadline)).all()
        if rows:
            counter = 1
            for x in rows:
                print('{}. {} {} {}'.format(counter, x.task, x.deadline.day, x.deadline.strftime('%b')))
                # print(x.id)
                # print(x.deadline)
                counter += 1
        else:
            print("Nothing is missed!")
        print('\n')
    if choice == 6:
        today = datetime.today()
        rows = session.query(Table).order_by(asc(Table.deadline)).all()
        if rows:
            print("""\nChose the number of the task you want to delete:""")
            counter = 1
            for x in rows:
                print('{}. {} {} {}'.format(counter, x.task, x.deadline.day, x.deadline.strftime('%b')))
                # print(x.id)
                # print(x.deadline)
                counter += 1
            del_number = int(input())
            specific_row = rows[del_number-1]
            session.delete(specific_row)
            session.commit()

        else:
            print("Nothing to delete")
        print('\n')