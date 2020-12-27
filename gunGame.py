# Edgar
import random

class CPU:
    def __init__(self):
        self.score = 0
        self.gun = GunStance()
   
    def getScore(self):
        return self.score
 
    def incrementScore(self):
        self.score += 1

    def getAction(self, p1_bullets):
        print("CPU ", end="")
        if(self.gun.getBullet() > 0):
            num = random.randint(0,2)
            return self.gun.setAction(num)
        elif(self.gun.getBullet() == 0):
            if(p1_bullets == 0):
                return self.gun.setAction(2)
            else:
                return self.gun.setAction(0 if random.choice([True, False]) else 2)
        else:
            return 0
# Sam 
class GameEngine:

    def __init__(self, _winningScore, _p1, _p2):
        self.winningScore = _winningScore
        self.p1 = _p1
        self.p2 = _p2
        
    def startGame(self):
        cpuAction = 0
        playerAction = 0
        gameStates = [[0,0,0],[0,0,-1],[0,1,0]]
        
        while (self.p2.getScore() != self.winningScore and self.p1.getScore() != self.winningScore):
            print("Player Bullets =" + str(self.p1.gun.getBullet()))
            print("Player Bullets =" + str(self.p2.gun.getBullet()))
            playerAction = self.p1.getAction()
            cpuAction = self.p2.getAction(self.p1.gun.getBullet())
            if gameStates[cpuAction][playerAction] == 1:
                self.p1.incrementScore()
            elif gameStates[cpuAction][playerAction] == -1:
                self.p2.incrementScore()
            print("")
        if self.p2.getScore()>self.p1.getScore():
            print("LOSER!!!")
        else:
            print("WINNER!!!")
            
# Brayam
class GunStance:
    def __init__(self):
        self.bullet = 1
        
    def setAction(self, _action) -> int:
        if _action == 0:
            print('chose block')           
            return self.block()
        elif _action == 1:
            print('chose shoot')
            return self.shoot()
        elif _action == 2:
            print('chose reload')
            return self.reload()

    def getBullet(self):
        return self.bullet
        
    def shoot(self) -> int:
        self.bullet -= 1
        return 1

    def block(self) -> int:
        return 0

    def reload(self) -> int:
        self.bullet += 1
        return 2
        
# Brayam
class Player:
    def __init__(self):
        self.input = 0
        self.score = 0
        self.gun = GunStance()

    def getAction(self) -> int:
        actions = ['shield', 'shoot', 'reload']
        print("0:" + actions[0] + " 1:" + actions[1] + " 2:" + actions[2] + "\n" + "Choose Action: ")

        while(True):
            # check user input is correct
            try:
                self.input = input()
                val = int(self.input)
                if(int(self.input) < 0 or int(self.input) > 2 or (self.gun.getBullet() == 0 and int(self.input) == 1)):
                    print("Invalid action.")
                    print("0:" + actions[0] + " 1:" + actions[1] + " 2:" + actions[2] + "\n" + "Choose Action: ")
                    continue
                break
            except ValueError:
                print("That's not an int!")
                print("0:" + actions[0] + " 1:" + actions[1] + " 2:" + actions[2] + "\n" + "Choose Action: ")

        print('You ',end="") 
        return self.gun.setAction(int(self.input))
        
    def checkInt(self, input):
        while(True):
            try:
                val = int(self.input)
                break
            except ValueError:
                print("That's not an int!")
                

    def getScore(self) -> int:
        return self.score

    def incrementScore(self):
        self.score += 1
        
# Everyone
def main():
    p1 = Player()
    p2 = CPU()
    gunGame = GameEngine(1, p1, p2)
    gunGame.startGame()

if __name__ == "__main__":
    # execute only if run as a script
    main()