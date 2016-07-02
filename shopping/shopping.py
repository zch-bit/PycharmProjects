from random import randint

done = False

store = []

items = ["Water", "milk", "apple", "banana", "bread"]


class ShoppingCart:
    def __init__(self):
        self.items = []

    def addToCart(self, item):
        self.items.append(item)

    def removeFromCart(self, item):
        self.items.pop(item)

    def priceItemInCart(self):
        price = 0
        for x in self.items:
            price = price + x.price
        return price

    def listCart(self):
        cid = 0
        print "Cart: \n"
        for x in self.items:
            print cid, x.name, "$", x.price
            cid += 1
        print ""


class CartItem:
    def __init__(self, price):
        self.price = price
        self.name = ""


def makeStoreItems(amt):
    storeItems = 0
    while storeItems <= amt:
        ci = CartItem(randint(1, 25))
        ci.name = items[randint(0, len(items) - 1)]
        store.append(ci)
        storeItems += 1


def openStore(storeFile):
    str1 = ""
    try:
        fx = open(storeFile, "r")
        str1 = fx.read()
    except IOError:
        print "No store file, generating one.."
        makeStoreItems(5)
    return str1


def prInstructions():
    print "Type C to view your cart items"
    print "Type R to remove a cart item"
    print "Type an item number to buy it"
    print "Type P to get the total price of your cart"


def listStore():
    iid = 0
    for name in store:
        print iid, ".", name.price, name.name
        iid += 1


def removeItem(item, cart):
    cart.removeFromCart(item)
    print "%s has been removed from cart." % item


def handleInput(inv, cart):
    chars = ["c", "C", "R", "r", "x", "X", "p", "P"]
    if (inv == "C" or inv == "c"):
        cart.listcart()
    if (inv == "R" or inv == "r"):
        removeItem(inv, cart)
    if (inv == "X" or inv == "x"):
        global done
        done = True
    if (inv == "P" or inv == "p"):
        print "Your cart currently is priced at "
        print cart.pricecart()
    if inv not in chars:
        try:
            cart1.addToCart(store[int(inv)])
        except:
            print "You have specified an illegal character!"


if __name__ == "__main__":
    cart1 = ShoppingCart()
    openStore("cart.cartfile")

    while (done == False):
        listStore()
        prInstructions()
        cart1.listCart()
        input_var = raw_input("Choose an item to buy!")
        handleInput(input_var, cart1)
