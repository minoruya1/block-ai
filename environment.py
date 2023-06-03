import gym
import numpy as np
import pygame
import math
import random
from pygame.locals import *

class MyEnv(gym.Env):
    def __init__(self):
        
        #初期化
        pygame.init() 
        #ウィンドウサイズ
        self.window_x=1280
        self.window_y=720
        
        screen = pygame.display.set_mode((self.window_x, self.window_y)) # ウィンドウサイズの指定
        pygame.display.set_caption('反射球') # ウィンドウタイトルの指定
        font = pygame.font.Font(None, 55) 
        
        self.rect_width=150#プレーヤーの幅
        self.rect_height=5#プレーヤーの高さ
         
        self.spped=10#球のスピード
        
        # アクション数定義
        ACTION_NUM=3 #アクションの数が3つの場合
        self.action_space = gym.spaces.Discrete(ACTION_NUM) 
        
        # 状態の範囲を定義
        LOW = np.array([0,0,0,-135.06847396007072])
        HIGH = np.array([self.window_x,self.window_y,self.window_x-self.rect_width,135.06847396007072])
        self.observation_space = gym.spaces.Box(low=LOW, high=HIGH)
        
        self.reset()
       
    def reset(self):

        #ブロック
        self.block       = {}                                # 領域
        self.block_rect  = {}                                # Rect(位置情報)
        self.target      = {}                                # ブロックの表示の有無を指定する変数

        for i in range(8):
            self.block[i] = pygame.Surface((80,25))                      # 領域を確保
            self.block[i].set_colorkey((0,0,0))                      # 透過色の設定
            pygame.draw.rect(self.block[i],(255,255,255),(0,0,80,25))    # 領域内を描画する
            self.block_rect[i] = self.block[i].get_rect()                 # blockのRect(位置情報)の取得       
            self.block_rect[i].topleft=(130+(i*130),50)  # blockの左上位置を決める
            self.target[i] = True                                    # ブロックはすべて表示するため、全部Trueとする




        #ボール位置初期化
        self.ball_x=random.randint(20,1260)
        self.ball_y=random.randint(20,200)

        # ボール
        #self.circ = pygame.Surface((500,500))                      # 領域を確保
        #self.circ.set_colorkey((0,0,0))                      # 透過色の設定
        #pygame.draw.circle(self.circ,(255,255,255),(self.ball_x,self.ball_y),50)   # 領域内を描画する
        #self.circ_rect = self.circ.get_rect()                     # circのRect(位置情報)の取得
        #self.circ_rect.topleft=(self.ball_x,self.ball_y)  # blockの左上位置を決める
        #pygame.draw.circle(screen, (0,95,0), (self.ball_x,self.ball_y), 10, width=0)#ボールの描画
        
        #球の進む方向をランダムで決める
        rand=random.randint(0,3)
        if rand==0:
            self.ball_x_direction=1
            self.ball_y_direction=1
        elif rand==1:
            self.ball_x_direction=-1
            self.ball_y_direction=1
        elif rand==2:
            self.ball_x_direction=1
            self.ball_y_direction=-1
        elif rand==3:
            self.ball_x_direction=-1
            self.ball_y_direction=-1
        
        #プレーヤーの位置
        self.rect_x=10
        self.rect_y=self.window_y-self.rect_height
        
        #ボールが次に進む位置
        self.ball_x_next=self.ball_x+self.spped*self.ball_x_direction
        self.ball_y_next=self.ball_y+self.spped*self.ball_y_direction
        
        #ボールの角度
        self.angle=math.atan2(self.ball_y-self.ball_y_next,self.ball_x_next-self.ball_x)*(180/3.14)
        
        observation=[self.ball_x,self.ball_y,self.rect_x,self.angle]
        #breakpoint()
        
        return observation

    def step(self, action_index):
        done=False
        #アクションによってプレーヤーを移動する
        if action_index==0:
            self.rect_x-=20
        if action_index==1:
            self.rect_x+=20
        if self.rect_x<0:
            self.rect_x=0
        if self.rect_x>self.window_x-self.rect_width:
            self.rect_x=self.window_x-self.rect_width
        
        self.circ_rect = Rect(self.ball_x,self.ball_y,20,20)

        #ボールとブロックの衝突
        for i in self.target:
            if self.target[i]:                           # ++ targetがTrueのときだけ衝突判定する
                if self.block_rect[i].colliderect(self.circ_rect):
                    if self.circ_rect.left < self.block_rect[i].left or self.circ_rect.right > self.block_rect[i].right:
                        self.ball_x_direction*=-1
                    if self.circ_rect.top < self.block_rect[i].top or self.circ_rect.bottom > self.block_rect[i].bottom:
                        self.ball_y_direction*=-1
                    self.target[i] = False
                    break
        
        #全てのブロックを壊したら終了フラグ
        if not any (self.target):
            done = True
        
        
        #ボール位置計算
        self.ball_x+=self.spped*self.ball_x_direction
        self.ball_y+=self.spped*self.ball_y_direction
        
        #ボールがプレーヤに当たったら反転
        if self.ball_x>self.rect_x and self.ball_x<self.rect_x+self.rect_width and self.ball_y>self.window_y:
            self.ball_y_direction*=-1    
        elif (self.ball_y>self.window_y):#ボールがプレーヤに当たらずに画面下に当たったら終了フラグ
            done=True
            
        #画面端に当たったら反転
        if(self.ball_x<0):
            self.ball_x_direction*=-1
        if(self.ball_x>self.window_x):
            self.ball_x_direction*=-1
        if(self.ball_y<0):
            self.ball_y_direction*=-1
        
        #ボールが次に進む位置
        self.ball_x_next=self.ball_x+self.spped*self.ball_x_direction
        self.ball_y_next=self.ball_y+self.spped*self.ball_y_direction
        
        #ボールの角度
        self.angle=math.atan2(self.ball_y-self.ball_y_next,self.ball_x_next-self.ball_x)*(180/3.14)
        
        #状態の保存
        observation=[self.ball_x,self.ball_y,self.rect_x,self.angle]
        
        #ゲームが続くと報酬
        reward=1
        return observation, reward, done, {}

    def render(self,mode):
        screen = pygame.display.set_mode((self.window_x, self.window_y)) # ウィンドウサイズの指定
        pygame.time.wait(2)#更新時間間隔
        pygame.display.set_caption("Pygame Test") # ウィンドウの上の方に出てくるアレの指定
        screen.fill((0,0,0,)) # 背景色の指定。RGBだと思う

        for i in self.target:                             # ブロックを配置する
            if self.target[i]:
                screen.blit(self.block[i],self.block_rect[i])

        pygame.draw.rect(screen, (255,0,0), (self.rect_x,self.rect_y,self.rect_width,self.rect_height))#的の描画
        pygame.draw.circle(screen, (255,255,255), (self.ball_x,self.ball_y), 10, width=0)#ボールの描画
        pygame.draw.aaline(screen, (255,0,255), (self.ball_x,self.ball_y), (self.ball_x_next,self.ball_y_next), 0)#バーの描画
        pygame.display.update() # 画面更新
    
    def close(self):
        pygame.quit()