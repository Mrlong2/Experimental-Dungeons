class actor:

    def __init__(self, x, y, health=None, inventory=None):

        self.x = x
        self.y = y

        if health:
            self.health = health

        if inventory:
            self.inventory = inventory


class com_health:

    def __init__(self, maxhp, currenthp=None):
        self.maxhp = maxhp
        if currenthp:
            self.currenthp = currenthp
        else:
            self.currenthp = maxhp


class com_inventory:
    def __init__(self, items):
        self.items = items


class item:
    def __init__(self, name):
        self.name = name
