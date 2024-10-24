class Node(): ...


class Recipe(): ...


class Node:
    def __init__(self, data: dict = None, children: list = []) -> None:
        self.data = data if type(data) == dict else None
        self.children = tuple(children)

    def addChildren(self, *children: Node) -> None:
        for child, _ in children:
            for item in self.children:
                if child.getData == item.getData:
                    break
            else:
                self.children = self.children + (child,)

    def setChildren(self, *children: Node) -> None:
        self.children = self.children + children

    def getChildren(self) -> Node:
        return self.children

    def addData(self, key: str, value: any):
        self.data[key] = value

    def setData(self, data: dict):
        self.data = data

    def getData(self):
        return self.data

    def debugPrint(self, indent=0, depth=0):
        print(" "*indent, end='')
        print("self = ", self)
        if self.data != None:
            for key, value in self.data.items():
                print(" "*indent, end='')
                print(key, value, sep=": ")
        print(" "*indent, end='')
        print("self.children =", len(self.children))
        if depth > 0:
            for child in self.children:
                child.debugPrint(indent=indent+4, depth=depth-1)


class Recipe:
    def __init__(self, recipe_class=None, name=None, machine=None, rate=None,
                 ingredients=[], products=[]):
        self.recipe_class = recipe_class
        self.name = name
        self.machine = machine
        self.rate = rate

        self.ingredients = ingredients
        self.products = products

        self.redrawNodes()

    def isIngredient(self, comp_ingredient):
        for ingredient, _ in self.ingredients:
            if comp_ingredient == ingredient:
                return True
        return False
    
    def isProduct(self, comp_product):
        for product, _ in self.products:
            if comp_product == product:
                return True
        return False

    def redrawNodes(self):
        for node, _ in self.ingredients:
            for product in self.products:
                node.addChildren(product)

    def addNodes(self, ingredients=[], products=[]):
        self.addIngredients(*ingredients)
        self.addProducts(*products)

    def addIngredients(self, *ingredients):
        for ingredient in ingredients:
            if not ingredient in self.ingredients:
                ingredient[0].addChildren(*self.products)
                self.ingredients.append(ingredient)

    def addProducts(self, *products):
        for product in products:
            if not product in self.products:
                self.products.append(product)

        self.redrawNodes()

    def debugPrint(self, indent=0, depth=0):
        printIndent("self =", self, indent=indent)
        printIndent("self.recipe_class =", self.recipe_class, indent=indent)
        printIndent("self.name =", self.name, indent=indent)
        printIndent("self.machine =", self.machine, indent=indent)
        printIndent("self.rate =", self.rate, indent=indent)
        printIndent("self.ingredients =", len(self.ingredients), indent=indent)
        printIndent("self.products =", len(self.products), indent=indent)
        for ingredient, _ in self.ingredients[:5]:
            printIndent("Ingredient: ", end='', indent=indent)
            ingredient.debugPrint(indent=indent+4, depth=depth)
        for product, _ in self.products[:5]:
            printIndent("Product: ", end='', indent=indent)
            product.debugPrint(indent=indent+4, depth=depth)
        print()


def printIndent(*values, indent=0, **args):
    print(" "*indent, end='')
    print(*values, **args)

