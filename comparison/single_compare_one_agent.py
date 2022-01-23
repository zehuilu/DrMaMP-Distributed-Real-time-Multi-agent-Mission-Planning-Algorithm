#!/usr/bin/env python3
import os
import time
import matplotlib.pyplot as plt
import pathmagic
with pathmagic.context():
    from Simulator import Simulator
    import DrMaMP
    import CBBA_Path_Finding
    from compute_path_distance import compute_path_distance_one_agent


if __name__ == "__main__":
    # a json configuration file for CBBA
    cbba_config_file_name = os.getcwd() + "/example/cbba_config.json"

    # define the world
    map_width_meter = 25.0
    map_height_meter = 25.0
    map_resolution = 2
    value_non_obs = 0  # the cell is empty
    value_obs = 255  # the cell is blocked
    # create a simulator
    Simulator = Simulator(map_width_meter, map_height_meter, map_resolution, value_non_obs, value_obs)
    # number of obstacles
    num_obs = 120
    # [width, length] size of each obstacle [meter]
    size_obs = [1, 1]
    # generate random obstacles
    Simulator.generate_random_obs(num_obs, size_obs)
    # convert 2D numpy array to 1D list
    world_map = Simulator.map_array.flatten().tolist()

    # my algorithm
    num_agents = 1
    num_targets = 20
    agent_position, targets_position = Simulator.generate_agents_and_targets(num_agents, num_targets)
    t0 = time.time()
    # solve it
    path_many_result, task_allocation_result = DrMaMP.SolveOneAgent(agent_position, targets_position, world_map, Simulator.map_width, Simulator.map_height)
    t1 = time.time()
    print("My algorithm time used [sec]:" + str(t1 - t0))
    distance_my = compute_path_distance_one_agent(path_many_result)
    print("my distance", distance_my)
    # visualization
    Simulator.plot_path_multi_agent([path_many_result], agent_position, targets_position, [task_allocation_result], [], [])
    print("my task_allocation_result")
    print(task_allocation_result)

    # CBBA + path finding
    t0 = time.time()
    agent_position_list, task_position_list, path_all_agents, task_allocation_list, AgentList, TaskList =\
        CBBA_Path_Finding.Solve(agent_position, targets_position, Simulator, cbba_config_file_name, plot_flag=False)
    t1 = time.time()
    print("CBBA + path finding time used [sec]:" + str(t1 - t0))
    distance_cbba = compute_path_distance_one_agent(path_all_agents[0])
    print("CBBA distance", distance_cbba)
    # plot
    Simulator.plot_path_multi_agent(path_all_agents, agent_position, targets_position, task_allocation_list, [], [])
    print("CBBA task_allocation_list")
    print(task_allocation_list[0])

    plt.show()
