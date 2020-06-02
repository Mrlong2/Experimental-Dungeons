class entity:
    def __init__(self, x, y, objtype, sprite, blockpath=False, health=None, inventory=None, ondeath=None, attack=None,
                 ai_persona="none", special=None):
        # moving and location
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

        # object type
        self.type = objtype
        self.blockpath = blockpath
        self.ai_persona = ai_persona

        # Question: what the heck is up with that retarded "self.owner" stuff?
        # Answer: it's a workaround, python doesn't have a proper "parent" reference.  We need to get stuff from other
        # components, so that's the work around.

        # sprite and drawing
        self.sprite = sprite
        if self.sprite:
            self.sprite.owner = self

        # health
        self.health = health
        if self.health:
            self.health.owner = self

        self.attack = attack
        if self.attack:
            self.attack.owner = self

        # inventory
        self.inventory = inventory
        if self.inventory:
            self.inventory.owner = self

        self.ondeath = ondeath
        if self.ondeath:
            self.ondeath.owner = self

        self.special = special
        if self.ondeath:
            self.ondeath.owner = self