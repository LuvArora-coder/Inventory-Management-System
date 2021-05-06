from random import randint as rnd
from models.Item import Item
import xml.etree.ElementTree as et
class Store:
    def __init__(self):
        self.storeItems = []
        self.itemNames = ["HDMI Cable", "Keyboard", "Headphone", "RAM", "Mouse"]
        self.readStoreItems("products.xml")

    def readStoreItems(self, storeFileName):
        try:
            root =  et.parse(storeFileName).getroot()  
            for child in root.findall("product") : 
                self.storeItems.append(Item(  child.find("name").text, float( child.find("price").text) ) )

        except IOError:
            print("Store File Not Exists... Generating Random Store")
            self.generateRandomStoreItems(8)
    def getStoreItems(self):
        return self.storeItems

    
    def listStore(self):
        counter = 0
        print("Store Items : ") 
        for item in self.storeItems:
            print ("%s : %s  $%s" % (counter, item.name,item.price) )   
            counter += 1        
        print("")

    def generateRandomStoreItems(self, amt):
        storedItemCounter = 0
        while (storedItemCounter < amt):
            itemName = self.itemNames[rnd(0, len(self.itemNames) - 1)]
            itemPrice = rnd(10, 100)
            newItem = Item( name=itemName, price=itemPrice)
            self.storeItems.append(newItem)
            storedItemCounter = storedItemCounter + 1