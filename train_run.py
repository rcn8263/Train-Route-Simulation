"""
file: train_run.py
author: Ryan Nowak
Simulates a train following a route of stations and unloading
train cars at specified stations
"""

from dataclasses import dataclass
from linked_list_type import LinkedList
from node_types import MutableNode
import sys


@dataclass
class Train:
    """
    Represents the train with its speed, cars, and route
    """
    speed: float
    route: LinkedList
    cars: LinkedList


class TrainCar:
    """
    Represents the trains car with its contents and destination
    """
    content: str
    destination: str


def add_station(train, arg):
    """
    Add a station to the end of a train's route with the distance being
    from that station to the home station
    :param train: dataclass to add the route to
    :param arg: list containing station name and distance from home station
    :return: True if the command has no errors, False if it does
    """
    if not len(arg) == 2:
        print('Incorrect number of arguments.')
        return False
    elif not arg[1].replace('.', '', 1).isdigit():
        print('Distance is not a number')
        return False
    elif float(arg[1]) < 0:
        print('Distance cannot be negative')
        return False
    elif train.route.head is None and not float(arg[1]) == 0.0:
        print('First station must be home with distance of 0.')
        return False

    station = (arg[0], float(arg[1]))
    node = train.route.head
    if node is None:
        train.route.head = MutableNode(station, None)
    else:
        while node.next is not None:
            curr_station = node.value
            if curr_station[1] == station[1]:
                print('Two stations cannot have same distance.')
                return False
            node = node.next
        node.next = MutableNode(station, None)
    return True


def set_speed(train, arg):
    """
    Sets the speed of the train
    :param train: Train dataclass
    :param arg: list containing speed of train
    :return: True if the command has no errors, False if it does
    """
    if not len(arg) == 1:
        print('Incorrect number of arguments.')
        return False
    elif not arg[0].replace('.', '', 1).isdigit():
        print('Argument is not a number')
        return False
    else:
        train.speed = float(arg[0])
        return True


def add_car(train, arg):
    """
    Adds a car to a location in the train based on destination
    :param train: Train dataclass
    :param arg: list containing car contents and destination
    :return: True if the command has no errors, False if it does
    """
    if not len(arg) == 2:
        print('Incorrect number of arguments.')
        return False
    elif train.route.head is None:
        print('No stations in route.')
        return False
    elif train.route.head.value[0] == arg[1]:
        print('Cannot have cars destined for home station')
        return False
    else:
        node = train.route.head
        is_station = False
        while node is not None:
            if node.value[0] == arg[1]:
                is_station = True
            node = node.next
        if not is_station:
            print('Station is not in route.')
            return False

    car = TrainCar()
    car.content = arg[0]
    car.destination = arg[1]
    node_cars = train.cars.head
    if node_cars is None:
        train.cars.head = MutableNode(car, None)
    else:
        node_station = train.route.head
        stations = []
        while node_station is not None:
            stations.append(node_station.value[0])
            node_station = node_station.next
        for station in stations:
            if car.destination == station:
                node_cars.next = MutableNode(node_cars.value, node_cars.next)
                node_cars.value = car
                break
            elif node_cars.value.destination == station:
                if node_cars.next is None:
                    node_cars.next = MutableNode(car, None)
                    break
                else:
                    node_cars = node_cars.next
    return True


def show_route(train):
    """
    Prints train route and distance between each station
    :param train: Train dataclass
    """
    node = train.route.head
    while node is not None:
        if node.next is None:
            print(node.value[0])
        else:
            distance = node.value[1]
            print(node.value[0], '---', node.next.value[1] - distance, '--> ', end='')
        node = node.next


def show_train(train):
    """
    Prints train speed and the contents and destination of each train car
    :param train: Train dataclass
    """
    print('engine(', train.speed, ')')
    node = train.cars.head
    while node is not None:
        print('Contents:', node.value.content,
              ', Destination:', node.value.destination)
        node = node.next


def start(train):
    """
    Runs the simulation of the train traveling to its stations and
    unloading cars
    :param train: Train dataclass
    :return: True if the command has no errors, False if it does
    """
    if train.speed == 0:
        print('Train speed not set.')
        return False
    elif train.route.head is None:
        print('Home station not set.')
        return False

    node_route = train.route.head.next
    distance = train.route.head.value[1]
    time = 0.0
    while node_route is not None:
        print('Moving on to', node_route.value[0])
        time += 0.5
        print('0.50 hours taken to separate cars.')
        travel_time = (node_route.value[1]-distance) / train.speed
        time += travel_time
        print('This segment took', '%0.2f' % travel_time, 'hours to travel.')
        while train.cars.head.value.destination == node_route.value[0]:
            print('Unloading', train.cars.head.value.content,
                  'in', node_route.value[0])
            train.cars.head = train.cars.head.next
        distance = node_route.value[1]
        node_route = node_route.next
    print('Total time for trip was', '%0.2f' % time, 'hours.')
    return True


def help():
    """
    Prints all valid commands for user
    """
    print('add_car <content> <station>')
    print('set_speed <speed>')
    print('add_station <station> <distance>')
    print('show_route')
    print('show_train')
    print('start')
    print('help')
    print('quit')


def quit():
    """
    Prints a goodbye message and exits the program
    """
    print('Train yard simulation ending.')
    sys.exit()


def process_commands(train):
    """
    User enters commands and then calls certain functions for each
    command. Prints an error if command is incorrect
    :param train: Train dataclass
    """
    command = ''
    while not command == 'quit':
        arguments = input('> ')
        arguments = arguments.split()
        command = arguments[0]
        arguments = arguments[1:]
        is_valid_command = True
        if command == 'add_station':
            is_valid_command = add_station(train, arguments)
        elif command == 'set_speed':
            is_valid_command = set_speed(train, arguments)
        elif command == 'add_car':
            is_valid_command = add_car(train, arguments)
        elif command == 'show_route' and arguments == []:
            show_route(train)
        elif command == 'show_train' and arguments == []:
            show_train(train)
        elif command == 'start' and arguments == []:
            is_valid_command = start(train)
        elif command == 'help' and arguments == []:
            help()
        elif command == 'quit' and arguments == []:
            quit()
        else:
            print('Illegal command name.')
        if not is_valid_command:
            print('Illegal use or form for this command.')


def main():
    """
    Prints welcome message, creates a Train object, and calls
    process_commands function to start simulation
    """
    print('Welcome to the train yard.')
    train = Train(0.0, LinkedList(None, 0), LinkedList(None, 0))
    process_commands(train)


if __name__ == '__main__':
    main()
