'''These are components'''

# controls an object's health
class health:
    def __init__(self, hp, maxhp=None):
        self.owner = None
        self.hp = hp
        self.dead = False  # allows you to know if you're dead
        if maxhp == None:
            self.maxhp = hp
        else:
            self.maxhp = maxhp


# controls drawing and stuff
class sprite:
    def __init__(self, img, spriteoffsetx=0, spriteoffsety=0, layering=0):
        self.img = img
        self.spriteoffsetx = spriteoffsetx
        self.spriteoffsety = spriteoffsety
        self.layering = layering  # IMPORTANT! Higher numbers makes it go down, not up!
        self.owner = None

    def drawself(self, surf, offset_x, offset_y):
        surf.blit(self.img, (
            (self.owner.x * config.CELL_WIDTH) + (self.spriteoffsetx * config.CELL_WIDTH) + offset_x,
            (self.owner.y * config.CELL_HEIGHT) + (self.spriteoffsety * config.CELL_HEIGHT) + offset_y))


# things have inventories
class inventory:
    def __init__(self):
        self.owner = None


# some objects can be picked up and used as weapons.
class item:
    def __init__(self):
        self.owner = None


class attack:
    def __init__(self, attackdamage):
        self.owner = None
        self.attackdamage = attackdamage


class special:
    def __init__(self, special_data):
        self.owner = None
        self.data = special_data