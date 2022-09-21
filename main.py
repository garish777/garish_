import pygame
import random
import os

#Constans 常量
W,H=200,600     #宽和高
FPS=30          #每秒的的帧率设置为30，Frames Per Second：每秒传输帧数



#Setup 设置

#初始化pygame模块
pygame.init()

#调用pygame里的display模块 ，用set—mode方法把屏幕设置成宽300，高500，其中（300，500）是一个元组
SCREEN=pygame.display.set_mode((W,H))   #python全大写表示常量，这里的SCREE是一个常量

#给弹出窗口定义名字
pygame.display.set_caption('王佳鑫的像素鸟')

#类似于time。sleep，pygame专业的控制帧与帧之间的间隔，即控制刷新频率
CLOCK=pygame.time.Clock()




#Materials 素材
# 导入主角图片
IMAGES = {}       #运用字典的形式，利用循环输出图片,             #最后输出的IMAGE是   如 '7': <Surface(24x36x8 SW)>， 'floor': <Surface(336x112x8 SW)>，由此，图片可以表示成IMAGES['FLOOR']
for image in os.listdir('assets/sprites'):  #listdir列举文件夹的所有文件
    name,extension = os.path.splitext(image)  #将文件名分割成文件+后缀(extension)的形式，如“小鸟”+“png",splittext：分割文本
    path = os.path.join("assets/sprites",image)  #将文件路径拼接成assets/sprites/image的形式，如assets/sprites/bird.png
    IMAGES[name] = pygame.image.load(path)  #字典里的键是文件名字，对应的值是装载的图片

#以下为装载图片的笨方法
# #导入主角图片
# bird_red_up=pygame.image.load('./assets/sprites/red-up.png')
# bird_red_mid=pygame.image.load('./assets/sprites/red-mid.png')
# bird_red_down=pygame.image.load('./assets/sprites/red-down.png')
# bird_yellow_up=pygame.image.load('./assets/sprites/yellow-up.png')
# bird_yellow_mid=pygame.image.load('./assets/sprites/yellow-mid.png')
# bird_yellow_down=pygame.image.load('./assets/sprites/yellow-down.png')
# bird_blue_up=pygame.image.load('./assets/sprites/blue-up.png')
# bird_blue_mid=pygame.image.load('./assets/sprites/blue-mid.png')
# bird_blue_down=pygame.image.load('./assets/sprites/blue-down.png')
# #导入背景图片
# bgpic=pygame.image.load('./assets/sprites/day.png')
# guide=pygame.image.load('./assets/sprites/guide.png')
# floor=pygame.image.load('./assets/sprites/floor.png')
# pipe=pygame.image.load('./assets/sprites/green-pipe.png')
# gameover=pygame.image.load('./assets/sprites/gameover.png')

#由于经常使用FLOOR_Y所以改成常量，便于写代码
# 地面放置的竖直位置等于窗口高度-地板高度，用get_height（）函数得到地板高度
FLOOR_Y = H - IMAGES['floor'].get_height()  # 常量的加减法，这也是为什么设置常量的原因

#导入音效
#利用pygame的mixer扩音器模块导入音效
# start = pygame.mixer.Sound('./assets/audio/start.wav') #开始音效
# die = pygame.mixer.Sound('./assets/audio/die.wav')    #死亡音效
# hit = pygame.mixer.Sound('./assets/audio/hit.wav')    #撞击音效
# score = pygame.mixer.Sound('./assets/audio/score.wav') #得分音效
# flap = pygame.mixer.Sound('./assets/audio/flap.wav')


AUDIO = {}
for audio in os.listdir('assets/audio'):
    name,extension = os.path.splitext(audio)
    path = os.path.join('assets/audio',audio)
    AUDIO[name] = pygame.mixer.Sound(path)


def main():

    #将三个界面放到无限循环之中，一旦开始就无法停止，除非关闭
    while True:
        AUDIO['start'].play()
        #随即展示白天黑夜和主角
        IMAGES['bgpic'] = IMAGES[random.choice(['day','night'])]   #令bgpic这个键对应的值为day或者night图片
        #随即展示小鸟的颜色
        color = random.choice(['red','yellow','blue'])  #color是一个随机颜色的字符串
        IMAGES['birds']= [IMAGES[color+'-up'],IMAGES[color+'-mid'],IMAGES[color + '-down']]   #定义键bird的值为IMAGES{}里的三种图片（非随机一种，而是三种，由于color随机，所以每次bird里边只有一个图片可以被找到，其他两种找不到），利用字符串的拼接方式实现了随即元素的抽取
        #随即展示管子颜色
        pipe = IMAGES[random.choice(['green-pipe','red-pipe'])]
        #展示反转的管子
        IMAGES['pipes'] = [pipe,pygame.transform.flip(pipe,False,True)]   #给IMAGES新加入一个键pipes代表反转的管子，令其在竖直方向反转，水平不动
        #播放音乐，加入到无限循环就可以每次都可播放，不会只播放一次


        #定义了三个游戏界面
        menu_window()   #菜单

        result = game_window()   #游戏
        end_window(result)    #结尾
        #设定一旦游戏判输，直接传到result即转到end_window()里队result的设置

def menu_window():

    #让地板动起来1
    #计算地板图片与窗口宽之差，      #由于为了让小鸟动起来，就让背景图片动，由于背景图片地板宽度大于窗口，所以让背景图片左右晃动来达到小鸟往前进的效果
    floor_gap = IMAGES['floor'].get_width() - W
    #地板x坐标为0,作为x坐标的起始值，类似于count=0
    floor_x = 0


    #计算指引图片水平放置位置，除以2是为了居中图片,居中常用除二法
    guide_x = (W-IMAGES['guide'].get_width())/2
    #计算指引图片竖直方向位置，在窗口中，左上角为（0，0），右下角为（W,H),在竖直方向上，y（H）由0增大到H，故guide_y，是一个常数，是在竖直方向的位置
    guide_y = (FLOOR_Y-IMAGES['guide'].get_height())/2
    #小鸟水平位置,即在水平五分之一处
    bird_x = W * 0.2
    #小鸟竖直位置,在竖直正中间
    bird_y = (H - IMAGES['birds'][0].get_height())/2

    #让小鸟上下移动
    bird_y_vel = 1                        #给小鸟一个y方向的速度,值设置为1，即帧与帧之间小鸟上下移动一个像素
    bird_y_range = [bird_y-8,bird_y+8]    #给小鸟上下移动设置一个范围，防止一直上移，暂定为上下8个像素，其中bird_y_range是一个列表

    #让小鸟扇动翅膀
    idx = 0     #index的缩写，代表序号
    frames = [0 , 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2,2 ,1 ,1 ,1 ,1, 1]    #frames:帧   里边的数字就是把小鸟的个个帧造型定义好，0代表up，1代表mid,2代表down,由于完整的拍动翅膀的周期为up-mid-down-mid
    #由于限制的总帧数为30，如果每隔一次换一个，相当于【0，1，0，2，0…………]则会切换的太快，而为什么是五次是因为小鸟完整扇动翅膀的一个周期是上，中 下 中，正好是



    while True:
        # 用enent事件模块，不要断获取当前的事件，事件就是键盘哪个键被按下，鼠标点击，遥感控制，触屏控制，并可以对自己需要的时间进行检查和捕捉
        for event in pygame.event.get():
            #检查窗口的叉号是否被点击,有的话退出游戏
            if event.type == pygame.QUIT:
                quit()
            # 如果事件类型为按下键盘，且按下的是空格的话，进行界面的跳转,一个return，相当于开始下一个游戏界面
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


        #让地板动起来2
        #让每次x的坐标减4，即相当于把地板图片每次左移4个单位，如果不加以控制，地板会移出画面
        floor_x -= 4
        #对图片左移进行控制，防止移出画面
        if floor_x <= -floor_gap:   #如果移出窗口过多，超过图片与窗口之差时，当等于其差时，即图片最右端正好在窗口最右边，刚刚好没有移出画面
            floor_x = 0             #当移到临界点的时候，让x坐标为0，即又开始了一次新的循环，由此地板达到了一直左右移动的目的


        bird_y += bird_y_vel         #小鸟的位置坐标等于每次移动的速度，即每次上移一个像素
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:  #一旦小鸟跑到界外，把他的速度反向，达到来回上下飞的目的
            bird_y_vel *= -1

        idx += 1      #每一帧更换一个图片,帧与帧之间序号加一,若改为5，则为每五帧更换一个图片
        idx %= len(frames)  #限制序号增加，如果超过总帧数（len(frames) ），则idx等于0

        #将图片放置到屏幕上，先写的先放到屏幕上，后写的会覆盖前面的
        SCREEN.blit(IMAGES['bgpic'],(0,0))            #指引图片，把指引图片放到左上角（0，0）处
        # SCREEN.blit(IMAGES['pipes'][0], (W / 2, H / 2))  #管子
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))    #大地
        SCREEN.blit(IMAGES['guide'],(guide_x, guide_y)) #指引
        SCREEN.blit(IMAGES['birds'][frames[idx]], (bird_x, bird_y))  #小鸟           #用IMAGES['bird'][0]，即只用bird键的第一张图片，由于三张图片都是随机的，所以只选择第一张就好了


        # 调用display的update更新方法，将填充好的颜色更新到屏幕上
        pygame.display.update()

        # 操作时间间隔为0.1秒。即颜色停留在屏幕时间是0.1秒，即一秒十帧
        # time.sleep(0.1)
        CLOCK.tick(FPS)  # 控制一秒为十帧，更加专业


def game_window():

    score = 0

    AUDIO['flap'].play()    #游戏优化，进入游戏界面就播放音效
    #让地板动起来1
    #计算地板图片与窗口宽之差，      #由于为了让小鸟动起来，就让背景图片动，由于背景图片地板宽度大于窗口，所以让背景图片左右晃动来达到小鸟往前进的效果
    floor_gap = IMAGES['floor'].get_width() - W
    # 地板x坐标为0,作为x坐标的起始值，类似于count=0
    floor_x = 0

    #让小鸟动起来
    bird = Bird(W*0.2,H*0.4)     #生成一个小鸟对象，并指定了生成地方

    #产生多个水管
    n_pairs = 4  # 水管对数量
    distance = 150   #水管水平之间的距离
    pipe_gap = 100   #水管竖直之间距离
    pipe_group = pygame.sprite.Group()   #用精灵组代替之前的列表,将创建的水管加到精灵组（列表）中
    for i in range(n_pairs):
        #随机生成参差不齐的水管，
        pipe_y = random.randint(int(H*0.3),int(H*0.7))     #在高度H*0.3与高度H*0.7之间生成随机高度
        pipe_up = Pipe(W+i * distance,pipe_y,True)   #生成pipe对象，并规定放置位置，间距每次加上distance,由于是上边的水管，所以翻转，flap参数为True
        pipe_down = Pipe(W+i*distance,pipe_y-pipe_gap,False)
        pipe_group.add(pipe_up)             #将创建的水管对象加到pipe_group  精灵组（pipes列表）里边，用的是add方法（append)
        pipe_group.add(pipe_down)

    while True:
        # 对按键后小鸟扇动翅膀进行操作
        flap = False  # 默认没有扇动翅膀
        # 用enent事件模块，不要断获取当前的事件，事件就是键盘哪个键被按下，鼠标点击，遥感控制，触屏控制，并可以对自己需要的时间进行检查和捕捉
        for event in pygame.event.get():
            # 检查窗口的叉号是否被点击,有的话退出游戏
            if event.type == pygame.QUIT:
                quit()
            # 如果事件类型为按下键盘，进行界面的跳转,一个return，相当于开始下一个游戏界面
            if event.type == pygame.KEYDOWN :
                #如果按下空格，播放撞击和死亡音效
                if event.key == pygame.K_SPACE:
                    flap = True  #如果按下空格，代表扇动，为True,由于flap有两个值True,和Flase
                    AUDIO['flap'].play()   #按下空格，播放拍动翅膀的声音

            #让地板动起来2
        # 让每次x的坐标减4，即相当于把地板图片每次左移4个单位，如果不加以控制，地板会移出画面
        floor_x -= 4
        # 对图片左移进行控制，防止移出画面
        if floor_x <= -floor_gap:  # 如果移出窗口过多，超过图片与窗口之差时，当等于其差时，即图片最右端正好在窗口最右边，刚刚好没有移出画面
            floor_x = 0  # 当移到临界点的时候，让x坐标为0，即又开始了一次新的循环，由此地板达到了一直左右移动的目的


        #调用更新方法
        bird.update(flap)   #调用类对象update方法，让小鸟可以扇动翅膀,并把flap参数导入

        #控制产生的水管移除屏幕就消失
        first_pipe_up = pipe_group.sprites()[0]        #向上的第一个水管,从精灵组里边取出来，用的是sprites方法
        first_pipe_down = pipe_group.sprites()[1]      #向下的第一个水管
        if first_pipe_up.rect.right < 0:     #如果第一张图片的右边界的x坐标小于0，即彻底移出了窗口
            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))  # 在高度H*0.3与高度H*0.7之间生成随机高度
            new_pipe_up = Pipe(first_pipe_up.rect.x+n_pairs*distance,pipe_y,True)  #新产生的水管是Pipe类产生的对象，
            new_pipe_down = Pipe(first_pipe_up.rect.x+n_pairs * distance,pipe_y-pipe_gap,False)
            pipe_group.add(new_pipe_up)        #将新产生的水管填充到列表里边，以此来循环无限产生水管
            pipe_group.add(new_pipe_down)
            #删除移出屏幕的水管，用精灵组的kill（）方法替代del 方法
            first_pipe_up.kill()
            first_pipe_down.kill()


        pipe_group.update()



        #输赢判断
        #出画面判输
        if bird.rect.y > FLOOR_Y or bird.rect.y < 0 or pygame.sprite.spritecollideany(bird,pipe_group):     #小鸟y坐标如果大于地板或者小于0（超出上边界），判为死亡
            bird.dying = True      #小鸟对象死亡
            AUDIO['hit'].play()
            AUDIO['die'].play()

            # 创建结果字典，一旦判为游戏失败，返回result字典，而不是直接传到game over界面,前边设定result为game——window（），并将result作为end_window里的参数
            result = {'bird':bird,'pipe_group':pipe_group,'score':score}
            return result                        #切换界面到game over界面

        if bird.rect.left + first_pipe_up.x_vel < first_pipe_up.rect.centerx < bird.rect.left:   #判断中心线是否在小鸟这一帧前后左边界之间
            #               越线前                         中心线                     越线后
            #              （小鸟在这一帧的实际x坐标）而不是bird.rect.left，这是小鸟上一帧的位置
            #原理：在上下两个管子中间连一个线，判断小鸟在这一帧前后的位置，如果小鸟越过中心线，则代表通过，记一分

            AUDIO['score'].play()
            score += 1

        # #实现碰撞       笨方法
        # for pipe in pipe_group.sprites():
        #     #原理：管和小鸟相当于两个矩形，如果两个矩形上下的边界大于两个矩形的高度之和，则说明发生了碰撞
        #     right_to_left = max(bird.rect.right,pipe.rect.right) - min(bird.rect.left,pipe.rect.left)   #定义水平距离
        #     bottom_to_top = max(bird.rect.bottom,pipe.rect.bottom) - min(bird.rect.top,pipe.rect.top)   #定义竖直距离
        #     #判断是否碰撞
        #     if right_to_left < bird.rect.width + pipe.rect.width and bottom_to_top < bird.rect.height + pipe.rect.height:
        #         AUDIO['hit'].play()      #播放碰撞音效
        #         AUDIO['die'].play()
        #         result = {'bird' : bird,'pipe_group' : pipe_group}    #死亡后展示死亡界面
        #         return result

        # 把天空图片放到左上角
        SCREEN.blit(IMAGES['bgpic'], (0, 0))  #SCREEN.blit 屏幕.画图函数
        #把管子放置到中间
        pipe_group.draw(SCREEN)     #用精灵组里的draw方法代替SCREEN里边的blit将水管组里的水管画到屏幕上
        #把大地放置到下边
        SCREEN.blit(IMAGES['floor'],(floor_x, FLOOR_Y))

        #显示分数
        show_score(score)   #调用show_score函数，显示分数


        #把小鸟放置到中间
        SCREEN.blit(bird.image,bird.rect)   #将小鸟图片传入，并且把宽高导入
        # 调用display的update更新方法，将填充好的颜色更新到屏幕上
        pygame.display.update()

        # 操作时间间隔为0.1秒。即颜色停留在屏幕时间是0.1秒，即一秒十帧
        # time.sleep(0.1)
        CLOCK.tick(FPS)  # 控制一秒为三十帧，更加专业



def  end_window(result) :

    #定义高度
    gameover_x = (W - IMAGES['gameover'].get_width())/2
    gameover_y = (FLOOR_Y - IMAGES['gameover'].get_height())/2

    bird = result['bird']  # 从字典里边取出来小鸟bird，用于下边把小鸟放到屏幕
    pipe_group = result['pipe_group']   # 从字典里取出来管子，让死亡后的end界面展示水管

    while True:
        #优化死亡画面跳过bug
        if bird.dying : #如果小鸟死亡
            bird.go_die()    #播放死亡画面
        else:     #用if else语句防止死亡后接受键盘事件
         # 用enent事件模块，不要断获取当前的事件，事件就是键盘哪个键被按下，鼠标点击，遥感控制，触屏控制，并可以对自己需要的时间进行检查和捕捉
             for event in pygame.event.get():
             # 检查窗口的叉号是否被点击,有的话退出游戏
               if event.type == pygame.QUIT:
                  quit()
             # 如果事件类型为按下键盘，且按下的是空格的话，进行界面的跳转,一个return，相当于开始下一个游戏界面
               if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                 return


        bird.go_die()     # 增加一个死亡函数，控制小鸟死亡的过程


        #放置天空
        SCREEN.blit(IMAGES['bgpic'],(0,0))
        #放置水管
        pipe_group.draw(SCREEN)
        #放置地板
        SCREEN.blit(IMAGES['floor'],(0,FLOOR_Y))
        #放置结束图片
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        #放置分数
        show_score(result['score'])
        #放置小鸟
        SCREEN.blit(bird.image,bird.rect)     #bird是一个个对象
        # 调用display的update更新方法，将填充好的颜色更新到屏幕上
        pygame.display.update()

        # 操作时间间隔为0.1秒。即颜色停留在屏幕时间是0.1秒，即一秒十帧
        # time.sleep(0.1)
        CLOCK.tick(FPS)  # 控制一秒为十帧，更加专业

#得分函数
def show_score(score):
    score_str = str(score)  # 把分数变成字符串，便于拆分，并遍历字符串每一位
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1  # 定义图片宽度，乘以1.1是为了保证分数之间的间隔
    x = (W - n * w) / 2  # 让图片居中展示
    y = H * 0.1  # 定义图片y坐标
    for number in score_str:
        SCREEN.blit(IMAGES[number], (x, y))  # 依次遍历每一个数字，并展示，并且x坐标递加
        x += w


#小鸟加工厂
class Bird:   #声明Bird是一个类，用于生成一个个对象（多个小鸟），即小鸟这个类（Bird)产生小鸟这个对象（bird)
             #可以把self理解成一个个对象bird
    #设置类对象的各个属性
    def __init__(self,x,y):  #用构造方法__init__，说明对象刚产生时做的事情,其中x,和 y是小鸟的放置位置的横纵坐标
        #在每个原来函数前边都加上了self，说明是对一个个类对象的操作
        self.frames = [0]*5+[1]*5+[2]*5+[1]*5     #定义这个类的对象的帧造型
        self.idx = 0          #类对象的当前序号
        self.images = IMAGES['birds']    #定义类对象的图片（帧造型）
        self.image = self.images[self.frames[self.idx]]       #定义类对象不同造型图片的转变（即上中下的切换）
        self.rect = self.image.get_rect()    #由于图片是一个个矩形框，定义rect(矩形框）就是图片框，用get方法获得图片的宽高（x,y)
        self.rect.x = x                    #定义框宽即小鸟放置的横坐标x
        self.rect.y = y                     #定义框高即小鸟放置的纵坐标y
        #控制小鸟上升和下降
        self.y_vel = -10                  #控制小鸟y方向速度，由于pygame里边原点是在左上角，向下为正，故开始有一个向上为10像素的初速度（-10）
        self.max_y_vel = 10
        self.gravity = 1                 #补上向下的重力速度为1像素
        #控制小鸟上下图像倾斜角度
        self.rotate = 45                  #让小鸟初始向上45°  rotate是旋转的意思
        self.max_rotate = -20             #设置最大角度向下的20°
        self.rotate_vel = -3              #每一帧向下改变3°,即重力，阻力扇动效果的影响
        # 设置拍动翅膀后的速度
        self.y_vel_after_flap = -10       # 设置拍动翅膀后的初速度-10，即拍一次翅膀向上10个像素
        self.rotate_after_flap = 45       #拍动翅膀后的初角度，即45°，即拍动翅膀向上仰角,获得能量
        self.dying = False               #为修复死亡画面被空格打断而不可以看见分数的bug，初始值是False表明尚未死亡，True为小鸟死亡

    def update(self,flap=False):     #给update两个参数，一个是self,一个是flap，用于判断是否拍动翅膀

        #判断是否拍动翅膀
        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap      #只要拍动翅膀，角度和速度都被重置



        # 更新速度
        self.y_vel = min(self.y_vel+self.gravity,self.max_y_vel)      # 控制小鸟的速度，控制为向上速度和重力速度的和速度，即再向上的力和向下的力的影响下导致的合速度，但是不会超过最大的y方向速度
        self.rect.y += self.y_vel                     # 让每次小鸟这个图片的y方向的位置就是速度的位置，即速度控制图片的位置，小鸟初始位置是 self.rect.y ，每次改变一次速度，则位置改变大小就是速度大小
        # 比如刚开始向上是-10，重力速度是-1，则刚开始初速度为-9，第二次循环中，向上为-9，重力速度为1，则速度变为-8，以此类推，直到速度为0，这时候速度成了向下的1，小鸟向下，一直到最大速度10，由于速度不可以大于10，所以此后速度一直为10，即以10像素的速度向下坠落

        # 更新角度
        self.rotate = max(self.rotate+self.rotate_vel,self.max_rotate)  # self.rotate+self.rotate_vel 是小鸟的合速度，由最开始的45每次减三取到20（由于取得最大值），



        # 更新图片
        self.idx += 1
        self.idx %= len(self.frames)
        self.image = IMAGES['birds'][self.frames[self.idx]]

        # 更新图片倾斜角度
        self.image = pygame.transform.rotate(self.image, self.rotate)   # 让图片跟据倾斜角度self.rotate来倾斜


        #定义小鸟死亡过程
    def go_die(self):
        if self.rect.y < FLOOR_Y:   #判断小鸟是否在地上
            self.rect.y += self.max_y_vel  #小鸟位置每次加10，达到越落越快的效果
            self.rotate = -90              #小鸟翻转到都九十度，就是头朝下
            self.image = self.images[self.frames[self.idx]]  #传入随机小鸟图片
            self.image = pygame.transform.rotate(self.image,self.rotate)   #让小鸟翻转
        else:
            self.dying = False      #否则的话即小鸟没死。将bird.dying的值改为 False
#水管加工厂，生成pipe这个类，用于生产水管对象
class Pipe(pygame.sprite.Sprite):     #让水管继承精灵类，方便用精灵组管理代码
    def __init__(self,x,y,upwards=True):     #upwards=True 水管向上为真，True和False是两个值
        pygame.sprite.Sprite.__init__(self)   #调用精灵类__init__方法，对精灵进行管理
        #定义上下的水管属性
        if upwards:    #如果水管朝上
            self.image = IMAGES['pipes'][0]   #定义图像

            self.rect = self.image.get_rect()  #定义图像矩形框
            self.rect.x = x
            self.rect.top = y   #水管朝上，让y表示水管顶部的y坐标
        else:          #如果水管朝下
            self.image = IMAGES['pipes'][1]  # 定义图像
            self.rect = self.image.get_rect()  # 定义图像矩形框
            self.rect.x = x
            self.rect.bottom = y      #水管朝下，让y表示水管底部的y坐标，达到翻转目的
        self.x_vel = -4    #定义水管向左移动速度
    def update(self):
        self.rect.x += self.x_vel   #更新水管x坐标



main()


































# while True:
#     # 用enent事件模块，不要断获取当前的事件，事件就是键盘哪个键被按下，鼠标点击，遥感控制，触屏控制，并可以对自己需要的时间进行检查和捕捉
#     for event in pygame.event.get():
#         # 如果事件类型为按下键盘，且按下的是空格的话
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#             # 运用transform模块中的flip翻转方法，将像素鸟进行翻转，True代表水平方向翻转，Flase代表竖直方向不反转
#             bird = pygame.transform.flip(bird, True, False)
#
#     # 定义一个死循环，生成随机颜色
#     color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # 由于三原色，定义三个随机数，范围在0-255
#
#     # 让屏幕填充满这个颜色
#     SCREEN.fill(color)
#
#     # 用blit方法，把小鸟放到画幅中，这个方法支持定义位置
#     SCREEN.blit(bird, (150, 250))
#
#     # 调用display的update更新方法，将填充好的颜色更新到屏幕上
#     pygame.display.update()
#
#     # 操作时间间隔为0.1秒。即颜色停留在屏幕时间是0.1秒，即一秒十帧
#     # time.sleep(0.1)
#     CLOCK.tick(10)  # 控制一秒为十帧，更加专业






































