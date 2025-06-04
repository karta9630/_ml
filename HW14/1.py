import gymnasium as gym
env = gym.make("CartPole-v1", render_mode="human") # 若改用這個，會畫圖
# env = gym.make("CartPole-v1", render_mode="rgb_array")


# action=0車子向左
# action=1車子向右
# observation[0]座標
# observation[1]車子速度
# observation[2]桿子角度  -0.2095 < x <0.2095
# observation[3]桿子角速度 
# 起始狀態為 -0.05 < y <0.05 random
# 大於500過關 
step=0
observation, info = env.reset(seed=42)
while 1:
   env.render()
   #action = env.action_space.sample()  # 把這裡改成你的公式，看看能撐多久
   if observation[2]>0 and observation[3]>0: # + + 向右倒
        action=0
        observation, reward, terminated, truncated, info = env.step(action)
        step+=1
   elif observation[2]<0 and observation[3]<0:
        action=1
        observation, reward, terminated, truncated, info = env.step(action)
        step+=1    
    
   if terminated or truncated: # 這裡要加入程式，紀錄你每次撐多久
      observation, info = env.reset()
      print(f'step = {step}')
   if step==500:
       print("success")
       break
env.close()