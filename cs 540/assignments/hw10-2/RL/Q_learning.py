import gym
import random
import numpy as np
import time
from collections import deque
import pickle
from collections import defaultdict


EPISODES =  20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)

    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning

        while not done:
             # Implementing ε-greedy policy
            if random.uniform(0, 1) < EPSILON:
                response = env.action_space.sample()  # doing exploration------no need for argmax as we explore rather than exploit
            else:
                 # doing exploitation
                
                v_list = [Q_table[(obs, a)] for a in range(env.action_space.n)]
                
                
                response = np.argmax(v_list)#find best policy-given the formula,find value of a by using argmax rather than using simple max

            
            changed_response, reward, done,info = env.step(response)

        
            if not done:
    
                max_next_q = max([Q_table[(changed_response, a)] for a in range(env.action_space.n)])
                
                Q_table[(obs, response)] =      LEARNING_RATE * (DISCOUNT_FACTOR * max_next_q+reward  )+  Q_table[(obs, response)] *(1 - LEARNING_RATE)  
            else:
                
                
                 Q_table[(obs, response)] = LEARNING_RATE *     reward+ Q_table[(obs, response)]*(1 - LEARNING_RATE)     #alpha of slides--learning rate
        
            obs = changed_response

    
            episode_reward += reward#changing rewards for episodes

        
        EPSILON = max(EPSILON_DECAY*EPSILON , 0.01)  #keep hold of bounds of epsilon according to slides(bound is 0.01 fixed)


        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 
     
        if i % 100 == 0 and i > 0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################