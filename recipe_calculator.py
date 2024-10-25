from typing import Tuple
import json
import csv
import os
import sys

RECIPEFILEPATH = os.path.abspath("parsed_recipes.json")
CLASSFILEPATH = os.path.abspath("classes.csv")


class Node(): ...


class Recipe(): ...


class Node:
    def __init__(self, data: dict = None, children: list = [], parents: tuple = []) -> None:
        self.data = data if type(data) == dict else None
        self.children = tuple(children)
        self.parents = tuple(parents)

    def addChildren(self, *children: Node) -> None:
        for child, _ in children:
            for item in self.children:
                if child.getData == item.getData:
                    break
            else:
                self.children = self.children + (child,)

    def setChildren(self, *children: Node) -> None:
        self.children = tuple(children)

    def getChildren(self) -> Tuple[Node]:
        return self.children
    
    def addParents(self, *parents: Node) -> None:
        for parent, _ in parents:
            for item in self.parents:
                if parent.getData == item.getData:
                    break
            else:
                self.parents = self.parents + (parent, )
    
    def setParents(self, *parents: Node) -> None:
        self.parents = tuple(parents)

    def getParents(self) -> Tuple[Node]:
        return self.parents

    def addData(self, key: str, value: any):
        self.data[key] = value

    def setData(self, data: dict):
        self.data = data

    def getData(self):
        return self.data

    def copy(self, data_only=False):
        if data_only:
            return Node(self.data)

    def debugPrint(self, indent=0, depth=0, file=sys.stdout, end='', direction="d"):
        args = {"indent": indent, "file": file}
        printIndent("self =", self, **args)
        if self.data != None:
            for key, value in self.data.items():
                printIndent(key, value, sep=": ", **args)
        printIndent("self.children =", len(self.children), **args)
        printIndent("self.parents =", len(self.parents), **args)
        if direction == "d":
            if depth > 0:
                for child in self.children:
                    child.debugPrint(
                        indent=indent+4, depth=depth-1, file=file, end=end)
        elif direction == "u":
            if depth > 0:
                for parent in self.parents:
                    parent.debugPrint(
                        indent=indent+4, depth=depth-1, file=file, end=end, direction="u")
        print(end, end='', file=file)


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
        for node, n_amount in self.ingredients:
            for product, p_amount in self.products:
                node.addChildren((product, p_amount))
                product.addParents((node, n_amount))

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

    def copy(self, deep=False):
        if deep:
            ingredients = []
            products = []
            for ingredient in self.ingredients:
                ingredients.append((ingredient[0].copy(), ingredient[1]))
            for product in self.products:
                products.append((product[0].copy(), product[1]))

            return Recipe(self.recipe_class, self.name, self.machine,
                          self.rate, ingredients, products)
        return Recipe(self.recipe_class, self.name, self.machine, self.rate,
                      self.ingredients, self.products)

    def debugPrint(self, indent=0, depth=0, file=sys.stdout, end='\n'):
        args = {"indent": indent, "file": file}
        printIndent("self =", self, **args)
        printIndent("self.recipe_class =", self.recipe_class, **args)
        printIndent("self.name =", self.name, **args)
        printIndent("self.machine =", self.machine, **args)
        printIndent("self.rate =", self.rate, **args)
        printIndent("self.ingredients =", len(self.ingredients), **args)
        printIndent("self.products =", len(self.products), **args)
        for ingredient, _ in self.ingredients[:5]:
            printIndent("Ingredient: ", end='', **args)
            ingredient.debugPrint(indent=indent+4, file=file, depth=depth, end='\n')
        for product, _ in self.products[:5]:
            printIndent("Product: ", end='', **args)
            product.debugPrint(indent=indent+4, file=file, depth=depth, end='\n')
        print(end, end='', file=file)


def printIndent(*values, indent=0, **args):
    file = args.get("file")
    print(" "*indent, end='', file=file)
    print(*values, **args)


def getClasses():
    classes = dict()
    with open(CLASSFILEPATH, "r") as file:
        reader = csv.reader(file)
        for row in list(reader)[1:]:
            classes[row[0]] = row[1]

    return classes


def getRecipes():
    recipes = dict()
    with open(RECIPEFILEPATH, "r") as file:
        recipes = json.load(file)

    return recipes


def precompute(classes, recipes):
    item_nodes = dict()
    recipe_nodes = dict()

    for key, value in classes.items():
        item_nodes[key] = Node(data={"class": key, "name": value})

    for key, value in recipes.items():
        recipe_class, name = value.get("recipeInfo").values()
        machine = value.get("machine").get("class")
        machine = machine[0] if machine != [] else "None"
        rate = value.get("rate")
        ingredients = value.get("ingredients")
        products = value.get("products")

        recipe = Recipe(recipe_class, name, machine,
                        rate, ingredients=[], products=[])

        for ingredient in ingredients:
            node = item_nodes[ingredient.get("item")]
            recipe.addIngredients((node, ingredient.get("amount")))

        for product in products:
            node = item_nodes[product.get("item")]
            recipe.addProducts((node, product.get("amount")))

        recipe.redrawNodes()

        recipe_nodes[recipe_class] = recipe

    return item_nodes, recipe_nodes


def search(item, recipes, ingredient=True, product=True):
    found_recipes = dict()
    for key, value in list(recipes.items()):
        if ingredient and value.isIngredient(item):
            found_recipes[key] = value
        if product and value.isProduct(item):
            found_recipes[key] = value

    return found_recipes


def getRecipeByName(recipes, name):
    for recipe in recipes:
        if recipe.name == name:
            return recipe
    return None


def getRecipeByClass(recipes, class_name):
    for recipe in recipes:
        if recipe.class_name == class_name:
            return recipe
    return None


def getItemByName(items, name):
    for item in items:
        if item.data.get("name") == name:
            return item
    return None


def getItemByClass(items, class_name):
    for item in items:
        if item.data.get("class") == class_name:
            return item
    return None


if __name__ == "__main__":
    classes = getClasses()
    recipes = getRecipes()

    item_nodes, recipe_nodes = precompute(classes, recipes)
    item_1 = item_nodes.get("Desc_OreIron_C")
    item_2 = item_nodes.get("Desc_IronIngot_C")

    found_recipes = search(item_2, search(item_1, recipe_nodes, product=False), ingredient=False)

    for name, recipe in found_recipes.items():
        recipe.debugPrint()
