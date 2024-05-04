import pygame

import ujson

from scripts.game_structure.game_essentials import game

class Sprites():
    cat_tints = {}
    white_patches_tints = {}

    def __init__(self, size=None):
        """Class that handles and hold all spritesheets. 
        Size is normall automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None
        
        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except:
            print("ERROR: Reading White Patches Tints")
            
    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=6,
                   sprites_y=8):  # pos = ex. (2, 3), no single pixels
        """
        Divide sprites on a sprite-sheet into groups of sprites that are easily accessible.

        Parameters:
        spritesheet -- Name of spritesheet.
        pos -- (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites.
        name -- Name of group to make.
        
        Keyword Arguments
        sprites_x -- Number of sprites horizontally (default: 3)
        sprites_y -- Number of sprites vertically (default: 3)
        """

        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0


        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )
                except ValueError:
                    # Fallback for non-existent sprites
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite
                self.sprites[f'{name}{i}'] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 6 == height / 8:
            self.size = width / 6
        else:
            self.size = 50 # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and do a search for 'if width / 3 == height / 7:'")

        del width, height # unneeded

        for x in [
            'lineart', 'singlecolours', 'speckledcolours', 'tabbycolours', 'tortiesmoss',
            'whitepatches', 'whitepatches2', 'whitepatchesmoss', 'eyes', 'eyes2', 'skin', 'scars', 'missingscars',
            'collars', 'bellcollars', 'bowcollars', 'nyloncollars',
            'bengalcolours', 'marbledcolours', 'rosettecolours', 'smokecolours', 'tickedcolours',
            'mackerelcolours', 'classiccolours', 'sokokecolours', 'agouticolours', 'singlestripecolours', 'maskedcolours',
            'shadersnewwhite', 'lineartdead', 'tortiepatchesmasks',
            'medcatherbs', 'lineartdf', 'lightingnew', 'fademask',
            'fadestarclan', 'fadedarkforest', 'abyssiancolours', 'braidedcolours', 'brindlecolours',
            'fadedcolours', 'sabercolours', 'splotchcolours', 'mossherbs', 'bloodcollars', 'fogcolours', 'mistcolours'

        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')

        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        for a, i in enumerate(
                ['YELLOW', 'AMBER', 'HAZEL', 'PALE GREEN', 'GREEN', 'BLUE']):
            self.make_group('eyes', (a, 0), f'eyes{i}')

        for a, i in enumerate(
                ['DARK BLUE', 'GREY', 'CYAN', 'EMERALD', 'HEATHER BLUE', 'SUN-LIT ICE']):
            self.make_group('eyes', (a, 1), f'eyes{i}')

        for a, i in enumerate(
                ['COPPER', 'SAGE', 'BRIGHT BLUE', 'PALE BLUE', 'LAVENDER', 'DARK GREY']):
            self.make_group('eyes', (a, 2), f'eyes{i}')

        for a, i in enumerate(
                ['PALE YELLOW', 'GOLD', 'LIME', 'HAZELNUT', 'DARK AMBER', 'SLATE']):
            self.make_group('eyes', (a, 3), f'eyes{i}')

        for a, i in enumerate(
                ['RUBY', 'LILAC', 'LIGHT GREY', 'PINK', 'DARK HAZEL', 'CHOCOLATE']):
            self.make_group('eyes', (a, 4), f'eyes{i}')

        for a, i in enumerate(['TRUE', 'CENTRAL', 'QUARTER', 'SLIVER', 'SPECKLES', 'FROSTED']):
            self.make_group('eyes2', (a, 0), f'eyes2{i}')
        for a, i in enumerate(['RING', 'HALFCENTRAL', 'HALFRING', 'BUBBLE', 'OUTRING', 'SWAP']):
            self.make_group('eyes2', (a, 1), f'eyes2{i}')

        # white patches
        for a, i in enumerate(['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO',
                               'MOON', 'PHANTOM', 'POWDER', 'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE']):
            self.make_group('whitepatches', (a, 0), f'white{i}')
        for a, i in enumerate(['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL',
                               'LIGHTSONG', 'VITILIGO', 'BLACKSTAR', 'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL']):
            self.make_group('whitepatches', (a, 1), f'white{i}')
        # ryos white patches
        for a, i in enumerate(['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO',
                               'PAWS', 'MITAINE', 'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD']):
            self.make_group('whitepatches', (a, 2), f'white{i}')
        for a, i in enumerate(['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY',
                               'FAROFA', 'DAMIEN', 'MISTER', 'BELLY', 'TAILTIP', 'TOES', 'TOPCOVER']):
            self.make_group('whitepatches', (a, 3), f'white{i}')
        for a, i in enumerate(
                ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW',
                 'PANTS', 'REVERSEPANTS', 'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW']):
            self.make_group('whitepatches', (a, 4), f'white{i}')


        # beejeans white patches + perrio's point marks, painted, and heart2 + anju's new marks + key's blackstar
        for a, i in enumerate(['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT',
            'MAO', 'LUNA', 'CHESTSPECK', 'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER']):
            self.make_group('whitepatches2', (a, 0), f'white{i}')

        # acorn's white patches + ryos' bub + fable lovebug + frankie trixie
        for a, i in enumerate(['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART',
            'SPARROW', 'VEST', 'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE']):
            self.make_group('whitepatches2', (a, 1), f'white{i}')

        # acorn's white patches: the sequel
        for a, i in enumerate(['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE',
            'FADEBELLY', 'FRONT', 'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS']):
            self.make_group('whitepatches2', (a, 2), f'white{i}')
        for a, i in enumerate(['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR',
            'BUSTER', 'SMOKEY', 'HAWKBLAZE', 'CAKE', 'ROSINA', 'PRINCESS']):
            self.make_group('whitepatches2', (a, 3), f'white{i}')
        for a, i in enumerate(['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']):
            self.make_group('whitepatches2', (a, 4), 'white' + i)

        # moss patches
        for a, i in enumerate(
                ['CHANCE', 'MOSSY', 'MOTH', 'NIGHTMIST', 'FALCON', 'VENUS', 'RETSUKO', 'TIDAL', 'DIAMOND',
                 'ECLIPSE', 'SNOWSTORM', 'PEPPER', 'COWTHREE', 'COWFOUR']):
            self.make_group('whitepatchesmoss', (a, 0), f'white{i}')
        for a, i in enumerate(
                ['COWFIVE', 'COWSIX', 'COWSEVEN', 'COWEIGHT', 'COWNINE', 'COWTEN',
                 'COWELEVEN', 'FRECKLEMASK', 'SPLAT', 'BATWING']):
            self.make_group('whitepatchesmoss', (a, 1), f'white{i}')

        # single (solid)
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('singlecolours', (a, 0), f'single{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('singlecolours', (a, 1), f'single{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('singlecolours', (a, 2), f'single{i}')
        # tabby
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('tabbycolours', (a, 0), f'tabby{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('tabbycolours', (a, 1), f'tabby{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('tabbycolours', (a, 2), f'tabby{i}')
        # marbled
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('marbledcolours', (a, 0), f'marbled{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('marbledcolours', (a, 1), f'marbled{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('marbledcolours', (a, 2), f'marbled{i}')
        # rosette
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('rosettecolours', (a, 0), f'rosette{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('rosettecolours', (a, 1), f'rosette{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('rosettecolours', (a, 2), f'rosette{i}')
        # smoke
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('smokecolours', (a, 0), f'smoke{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('smokecolours', (a, 1), f'smoke{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('smokecolours', (a, 2), f'smoke{i}')
        # ticked
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('tickedcolours', (a, 0), f'ticked{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('tickedcolours', (a, 1), f'ticked{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('tickedcolours', (a, 2), f'ticked{i}')
        # speckled
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('speckledcolours', (a, 0), f'speckled{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('speckledcolours', (a, 1), f'speckled{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('speckledcolours', (a, 2), f'speckled{i}')
        # bengal
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('bengalcolours', (a, 0), f'bengal{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('bengalcolours', (a, 1), f'bengal{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('bengalcolours', (a, 2), f'bengal{i}')
        # mackerel
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('mackerelcolours', (a, 0), f'mackerel{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('mackerelcolours', (a, 1), f'mackerel{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('mackerelcolours', (a, 2), f'mackerel{i}')
        # classic
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('classiccolours', (a, 0), f'classic{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('classiccolours', (a, 1), f'classic{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('classiccolours', (a, 2), f'classic{i}')
        # sokoke
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('sokokecolours', (a, 0), f'sokoke{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('sokokecolours', (a, 1), f'sokoke{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('sokokecolours', (a, 2), f'sokoke{i}')
        # agouti
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('agouticolours', (a, 0), f'agouti{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('agouticolours', (a, 1), f'agouti{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('agouticolours', (a, 2), f'agouti{i}')
        # singlestripe
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('singlestripecolours', (a, 0), f'singlestripe{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('singlestripecolours', (a, 1), f'singlestripe{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('singlestripecolours', (a, 2), f'singlestripe{i}')
        # brindle
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('brindlecolours', (a, 0), f'brindle{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('brindlecolours', (a, 1), f'brindle{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('brindlecolours', (a, 2), f'brindle{i}')
        # Abyssinian
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('abyssiancolours', (a, 0), f'abyssinian{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('abyssiancolours', (a, 1), f'abyssinian{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('abyssiancolours', (a, 2), f'abyssinian{i}')
        # braided
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('braidedcolours', (a, 0), f'braided{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('braidedcolours', (a, 1), f'braided{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('braidedcolours', (a, 2), f'braided{i}')
        # splotch
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('splotchcolours', (a, 0), f'splotch{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('splotchcolours', (a, 1), f'splotch{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('splotchcolours', (a, 2), f'splotch{i}')
        # saber
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('sabercolours', (a, 0), f'saber{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('sabercolours', (a, 1), f'saber{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('sabercolours', (a, 2), f'saber{i}')
        # faded
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('fadedcolours', (a, 0), f'faded{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('fadedcolours', (a, 1), f'faded{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('fadedcolours', (a, 2), f'faded{i}')
        # masked
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('maskedcolours', (a, 0), f'masked{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('maskedcolours', (a, 1), f'masked{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('maskedcolours', (a, 2), f'masked{i}')
        # mist
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('mistcolours', (a, 0), f'mist{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('mistcolours', (a, 1), f'mist{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('mistcolours', (a, 2), f'mist{i}')
        # fog
        for a, i in enumerate(['WHITE', 'SNOW WHITE', 'GRAY', 'SLATE', 'DARK GRAY', 'DARK SLATE',
                               'PALE BLUE', 'BLUE', 'PALE LILAC', 'LILAC', 'SILVER',
                               'BLACK', 'SOOT BLACK', 'OBSIDIAN', 'GHOST']):
            self.make_group('fogcolours', (a, 0), f'fog{i}')
        for a, i in enumerate(['PALE BROWN', 'ALMOND', 'ACORN', 'LIGHT BROWN', 'BROWN', 'DARK BROWN',
                               'PALE CINNAMON', 'CINNAMON', 'SABLE', 'DARK SABLE', 'BIRCH',
                               'PALE LAVENDER', 'LAVENDER', 'DARK LAVENDER', 'DARK ORANGE']):
            self.make_group('fogcolours', (a, 1), f'fog{i}')
        for a, i in enumerate(['PALE FIRE', 'FIRE', 'DARK FIRE', 'PALE GINGER', 'GINGER', 'DARK GINGER',
                               'PALE GOLD', 'YELLOW', 'GOLD', 'BRONZE', 'ROSE',
                               'LIGHT CREAM', 'CREAM', 'DARK CREAM', 'DARK GOLD']):
            self.make_group('fogcolours', (a, 2), f'fog{i}')

        # new new torties
        for a, i in enumerate(['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE']):
            self.make_group('tortiepatchesmasks', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL', 'GRUMPYFACE']):
            self.make_group('tortiepatchesmasks', (a, 1), f"tortiemask{i}")
        for a, i in enumerate(['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE']):
            self.make_group('tortiepatchesmasks', (a, 2), f"tortiemask{i}")
        for a, i in enumerate(['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY']):
            self.make_group('tortiepatchesmasks', (a, 3), f"tortiemask{i}")
        for a, i in enumerate(['SHILOH']):
            self.make_group('tortiepatchesmasks', (a, 4), f"tortiemask{i}")

        for a, i in enumerate(['VIPER', 'SKULL', 'POINTS', 'DITTO', 'TABBY', 'SPECKLED', 'BENGAL', 'CLASSIC', 'MACKEREL', 'MARBLED']):
            self.make_group('tortiesmoss', (a, 0), f"tortiemask{i}")
        for a, i in enumerate(['SABER', 'ROSETTE', 'MASKED', 'DUST']):
            self.make_group('tortiesmoss', (a, 1), f"tortiemask{i}")

        # SKINS
        for a, i in enumerate(['BLACK', "RED", 'PINK', 'DARKBROWN', 'BROWN', 'LIGHTBROWN']):
            self.make_group('skin', (a, 0), f"skin{i}")
        for a, i in enumerate(['DARK', 'DARKGREY', 'GREY', 'DARKSALMON', 'SALMON', 'PEACH']):
            self.make_group('skin', (a, 1), f"skin{i}")
        for a, i in enumerate(['DARKMARBLED', 'MARBLED', 'LIGHTMARBLED', 'DARKBLUE', 'BLUE', 'LIGHTBLUE']):
            self.make_group('skin', (a, 2), f"skin{i}")

        self.load_scars()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """
        for a, i in enumerate(
                ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", 
                 "BRIDGE", "RIGHTBLIND", "LEFTBLIND", "BOTHBLIND", "BURNPAWS", "BURNTAIL"]):
            self.make_group('scars', (a, 0), f'scars{i}')
        for a, i in enumerate(
                ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE",
                 "FROSTFACE", "FROSTTAIL", "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"]):
            self.make_group('scars', (a, 1), f'scars{i}')
        for a, i in enumerate(
                ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE",
                 "LEGBITE", "NECKBITE", "FACE"]):
            self.make_group('scars', (a, 2), f'scars{i}')
        for a, i in enumerate(
                ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]):
            self.make_group('scars', (a, 3), f'scars{i}')
        # missing parts
        for a, i in enumerate(
                ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW"]):
            self.make_group('missingscars', (a, 0), f'scars{i}')

            # Accessories
        for a, i in enumerate([
            "MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "LAUREL"]):
            self.make_group('medcatherbs', (a, 0), f'acc_herbs{i}')
        for a, i in enumerate([
            "BLUEBELLS", "NETTLE", "POPPY", "LAVENDER", "HERBS", "PETALS"]):
            self.make_group('medcatherbs', (a, 1), f'acc_herbs{i}')
        for a, i in enumerate([
            "OAK LEAVES", "CATMINT", "MAPLE SEED", "JUNIPER"]):
            self.make_group('medcatherbs', (a, 3), f'acc_herbs{i}')
        self.make_group('medcatherbs', (5, 2), 'acc_herbsDRY HERBS')

        for a, i in enumerate([
            "RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "MOTH WINGS", "CICADA WINGS"]):
            self.make_group('medcatherbs', (a, 2), f'acc_wild{i}')

         #Moss
        for a, i in enumerate([
            "LUNA MOTH", "ATLAS MOTH", "BIRD SKULL", "IVY", "DAISY", "BUTTERFLIES"]):
            self.make_group('mossherbs', (a, 0), f'acc_moss{i}')
        for a, i in enumerate([
            "CLOVER", "ANTLERS", "STICK", "FIREFLIES", "WREATH", "FLOWER WREATH"]):
            self.make_group('mossherbs', (a, 1), f'acc_moss{i}')
        for a, i in enumerate([
            "SPROUT", "MUSHROOM", "LILAC", "SEAWEED", "LILY PAD", "MONSTERA"]):
            self.make_group('mossherbs', (a, 2), f'acc_moss{i}')
        for a, i in enumerate([
            "WILD FLOWERS", "TWIGS", "SHELL", "CRYSTAL", "SERPENT", "MOSS BALL"]):
            self.make_group('mossherbs', (a, 3), f'acc_moss{i}')

        for a, i in enumerate(["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"]):
            self.make_group('collars', (a, 0), f'collars{i}')
        for a, i in enumerate(["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"]):
            self.make_group('collars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINK", "PURPLE", "MULTI", "INDIGO"]):
            self.make_group('collars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL",
            "LIMEBELL"
        ]):
            self.make_group('bellcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"]):
            self.make_group('bellcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]):
            self.make_group('bellcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW",
            "LIMEBOW"
        ]):
            self.make_group('bowcollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"]):
            self.make_group('bowcollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]):
            self.make_group('bowcollars', (a, 2), f'collars{i}')
        for a, i in enumerate([
            "CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON",
            "LIMENYLON"
        ]):
            self.make_group('nyloncollars', (a, 0), f'collars{i}')
        for a, i in enumerate(
                ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"]):
            self.make_group('nyloncollars', (a, 1), f'collars{i}')
        for a, i in enumerate(["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]):
            self.make_group('nyloncollars', (a, 2), f'collars{i}')

        for a, i in enumerate(["CRIMSONFANG", "BLUEFANG", "YELLOWFANG", "CYANFANG", "REDFANG", "LIMEFANG"]):
            self.make_group('bloodcollars', (a, 0), f'dogcollars{i}')
        for a, i in enumerate(["GREENFANG", "RAINBOWFANG", "BLACKFANG", "SPIKESFANG", "WHITEFANG"]):
            self.make_group('bloodcollars', (a, 1), f'dogcollars{i}')
        for a, i in enumerate(["PINKFANG", "PURPLEFANG", "MULTIFANG", "INDIGOFANG"]):
            self.make_group('bloodcollars', (a, 2), f'dogcollars{i}')

# CREATE INSTANCE 
sprites = Sprites()
