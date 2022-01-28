import reader.tools as tools
import reader.models as models
import os
import cv2
import threading
import strats

class PokerBot:
    gameState = ""
    playerCards = []
    tableCards = []
    potSize = 0
    # tableName = ""

    def checkGameState(self) -> str:
        if not len(self.tableCards):
            return "Preflop"
        elif len(self.tableCards) == 4:
            return "Turn"
        elif len(self.tableCards) == 5:
            return "River"
        else:
            return "Flop"

    def readData(self, screenshot):
        self.tableCards = tools.readTableCards(screenshot.filename)
        self.playerCards = tools.readPlayerCards(screenshot.filename)
        self.gameState = self.checkGameState()
        self.potSize = tools.readPotSize(screenshot.filename)

        

class ChangesHandler:
    tableName = ""
    def __init__(self, bot: PokerBot, tableName: str):
        self.gameState = bot.gameState
        self.playerCards = bot.playerCards
        self.tableCards = bot.tableCards
        self.potSize = bot.potSize
        self.tableName = tableName
    
    def check(self, bot: PokerBot):
        if self.gameState != bot.gameState or self.playerCards != bot.playerCards or self.tableCards != bot.tableCards:
            self.gameState = bot.gameState
            self.playerCards = bot.playerCards
            self.tableCards = bot.tableCards
            self.potSize = bot.potSize

            self.printData()

        
    def printData(self):
        print (f'Player cards: {self.playerCards}')
        print (f'Cards on table: {self.tableCards}')
        print (f'Game state: {self.gameState}')
        print(f'Pot Size: {self.potSize}')
        print (f'Table: {self.tableName}')
        print(f'Strategy: {strats.simulate_all_possible(self)}')
        print ("########################")


class MultiBot:
    bot_dict = {}
    def __init__(self):
        self.gameWindows = tools.moveAndResizeWindows()
        screenshots = tools.grabScreen(self.gameWindows)

        for img in screenshots:
            bot = PokerBot()

            changesHandler = ChangesHandler(bot, img.tableName)
            self.bot_dict[img.tableName] = [bot, changesHandler]
    
    def run(self):
        screenshots = tools.grabScreen(self.gameWindows)
        for img in screenshots:
            bot, changesHandler = self.bot_dict[img.tableName]
            bot.readData(img)
            changesHandler.check(bot)
