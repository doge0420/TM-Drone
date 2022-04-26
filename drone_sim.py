from DroneBlocksTelloSimulator.DroneBlocksSimulatorContextManager import DroneBlocksSimulatorContextManager

if __name__ == '__main__':

    sim_key = '73f3fd18-88b1-4b11-9697-cccae7c62efd'
    distance = 40
    with DroneBlocksSimulatorContextManager(simulator_key=sim_key) as drone:
        drone.takeoff()
        drone.fly_forward(distance, 'cm')
        drone.fly_left(distance, 'cm')
        drone.fly_backward(distance, 'cm')
        drone.fly_right(distance, 'cm')
        drone.flip_backward()
        drone.land()