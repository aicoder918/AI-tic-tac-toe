import os, ast, matplotlib.pyplot as plt
import copy, random

class TicTacToe:

    """
    The computer uses MiniMax Algorithm to evaluate each state and makes next step accordingly

    x is maxplayer is user
    o is minplayer

    """
    
    state = [[" ", " ", " "],
             [" ", " ", " "], 
             [" ", " ", " "]]
    
    plays_with_util = {}

    randommode = True

    turn = 0

    def utility(self, s=state) -> -1 or 0 or 1:
        # returns the utility of the given state - called when copy.deepcopy(s) called from min-/maxvalue(s) is in a terminated state

        # check horizonatlly 
        for row in s:
            if all(tmp == "x" for tmp in row):
                return 1
            elif all(tmp == "o" for tmp in row):
                return -1

        # check vertcally 
        for row in [*zip(*s)]:
            if all(tmp == "x" for tmp in row):
                return 1
            elif all(tmp == "o" for tmp in row):
                return -1

        # check diagnoally
        if (s[0][0] == "x" and s[1][1] == "x" and s[2][2] == "x") or (s[2][0] == "x" and s[1][1] == "x" and s[2][0] == "x"):
            return 1
        if (s[0][2] == "o" and s[1][1] == "o" and s[2][0] == "o") or s[0][0] == "o" and s[1][1] == "o" and s[2][2] == "o":
            return -1
        
        return 0

    def player(self, s=state) -> "x" or "o":
        # returns which players turn it is  
        x_cnt = 0
        o_cnt = 0

        for row in range(len(s)):
            for tmp in s[row]:
                if tmp == "x": x_cnt += 1
                elif tmp == "o": o_cnt += 1

        if x_cnt == o_cnt: return "x"
        else: return "o" 

    def actions(self, s=state) -> [[], [], [], ...]:
        # returns all possible actions from the current state
        actions = []

        for row in range(len(s)): 
            for col in range(len(s[row])):
                if s[row][col] == " ":
                    actions.append([row, col])

        return actions
    
    def terminated(self, s=state) -> True or False:
        # checks if given state is a goal state (win or all tiles filles) 
        if len(self.actions(s)) == 0: 
            return True

        for row in s:
            if all(tmp == "x" for tmp in row) or all(tmp == "o" for tmp in row):
                return True

        for row in [*zip(*s)]:
            if all(tmp == "x" for tmp in row) or all(tmp == "o" for tmp in row):
                return True

        # check diagnoally
        if (s[0][0] == "x" and s[1][1] == "x" and s[2][2] == "x") or (s[2][0] == "x" and s[1][1] == "x" and s[2][0] == "x") or (s[0][2] == "o" and s[1][1] == "o" and s[2][0] == "o") or (s[0][0] == "o" and s[1][1] == "o" and s[2][2] == "o"):
            return True

        return False

    def eval_winner(self, s=state) -> None:
        # evaluates the given state and prints out who won
        if len(self.actions(s)) == 0: 
            print("\n  Draw\n")
            return
        
        for row in s:
            if all(tmp == "x" for tmp in row):
                print("\n  x won\n")
                return
            elif all(tmp == "o" for tmp in row):
                print("\n  o won\n")
                return 

        for row in [*zip(*s)]:
            if all(tmp == "x" for tmp in row):
                print("\n  x won\n")
                return 
            
            elif all(tmp == "o" for tmp in row):
                print("\n  o won\n")
                return 

        # check diagnoally
        if (s[0][0] == "x" and s[1][1] == "x" and s[2][2] == "x") or (s[2][0] == "x" and s[1][1] == "x" and s[2][0] == "x"):
            print("\n  x won\n")
            return 
        
        if (s[0][2] == "o" and s[1][1] == "o" and s[2][0] == "o") or (s[0][0] == "o" and s[1][1] == "o" and s[2][2] == "o"):
            print("\n  o won\n")
            return 

    def result(self, action, s) -> state:
        # perfoms given action on given tmpstate 
        s[action[0]][action[1]] = self.player(s)
        return s

    def min_value(self, s) -> int:
        # called by ai_play(s) - recursively calls maxvalue to evaluate the best possible play via an decision tree of all possible plays and its possible moves until terminated state
        if self.terminated(s): return self.utility(s)
        
        tmp_plays_with_util = {str(action): float("inf") for action in self.actions(s)}        
        min_ = float("inf")

        for action in self.actions(s):
            tmp_plays_with_util[str(action)] = min(tmp_plays_with_util[str(action)], self.max_value(self.result(action, copy.deepcopy(s))))
            min_ = min(min_, tmp_plays_with_util[str(action)])
        
        self.plays_with_util = tmp_plays_with_util
        
        return min_   

    def max_value(self, s) -> int:
        # similar to min_value(s), it calls min_value(s) and tries to get the best possible move that maximizes the board from current state
        if self.terminated(s): return self.utility(s)
        
        tmp_plays_with_util = {str(action): -float("inf") for action in self.actions(s)}
        max_ = -float("inf")

        for action in self.actions(s):
            tmp_plays_with_util[str(action)] = max(tmp_plays_with_util[str(action)], self.min_value(self.result(action, copy.deepcopy(s))))
            max_ = max(max_, tmp_plays_with_util[str(action)])
        
        return max_   
    
    def user_input(self) -> None:
        # waits for user to make a valid input
        xpos = input("\nX (row) position: ")
        ypos = input("Y (col) position: ")

        while not (0 <= int(xpos) <= 2 and 0 <= int(ypos) <= 2) or self.state[int(xpos)][int(ypos)] != " ":
            print("Invalid input, try agian!")
            xpos = input("X (row) position: ")
            ypos = input("Y (col) position: ")

        self.state[int(xpos)][int(ypos)] = "x"
        self.printboard()

    def ai_play(self, s=state) -> None:
        # after user played, the computer player evaluates the state and tries to make a move that minimizes the board as its the minplayer ("o")
        tmpmin = self.min_value(s)

        # implememnt random if various options exists that are optimal
        if self.randommode:
            tmp_plays_with_util = {str(key):tmpmin for key in self.plays_with_util if self.plays_with_util[key] == tmpmin}
            tmp = ast.literal_eval(random.choice(list(tmp_plays_with_util.items()))[0])
            self.state[tmp[0]][tmp[1]] = "o"
            self.printboard()
            return
        
        else:
            for key in self.plays_with_util:
                if self.plays_with_util[key] == tmpmin:
                    tmp = ast.literal_eval(key)
                    self.state[tmp[0]][tmp[1]] = "o"
                    self.printboard()
                    return

    def printboard(self) -> None:
        # prints current state of the board
        os.system("clear")
        print("\n  Current state: \n")
        print("    0   1   2")
        print("  -------------")
        print(f"0 | {self.state[0][0]} | {self.state[0][1]} | {self.state[0][2]} |")
        print("  -------------")
        print(f"1 | {self.state[1][0]} | {self.state[1][1]} | {self.state[1][2]} |       turn: {self.turn}")
        print("  -------------")
        print(f"2 | {self.state[2][0]} | {self.state[2][1]} | {self.state[2][2]} |")
        print("  -------------")
        self.turn += 1
            

if __name__ == "__main__":
    tik = TikTackToe()

    tik.printboard()
    while not tik.terminated():
        tik.user_input()
        tik.ai_play()
    tik.eval_winner()