import pygame


def get_inputs():
    global RUN_GAME, SELECTED
    for event in pygame.event.get():
        # if exit is pressed
        if event.type == pygame.QUIT:
            RUN_GAME = False  # set to false

        if event.type == pygame.KEYDOWN:  # if the event is a key down press
            # player controls
            if event.key == pygame.K_w:
                SELECTED.dy = -1

            if event.key == pygame.K_s:
                SELECTED.dy = 1

            if event.key == pygame.K_a:
                SELECTED.dx = -1

            if event.key == pygame.K_d:
                SELECTED.dx = 1
            # debug/fps menu
            if event.key == pygame.K_F1:
                DEBUG["showfps"] = not (DEBUG["showfps"])

            if event.key == pygame.K_UP:
                STATE['camera pos'] = (STATE['camera pos'][0], STATE['camera pos'][1] + 32)

            if event.key == pygame.K_DOWN:
                STATE['camera pos'] = (STATE['camera pos'][0], STATE['camera pos'][1] - 32)

            if event.key == pygame.K_LEFT:
                STATE['camera pos'] = (STATE['camera pos'][0] + 32, STATE['camera pos'][1])

            if event.key == pygame.K_RIGHT:
                STATE['camera pos'] = (STATE['camera pos'][0] - 32, STATE['camera pos'][1])

        # mouse controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.button)
            # if (pygame.mouse.get_pressed() == 1):
            xm, ym = pygame.mouse.get_pos()
            itemsfound = query_click_location(xm, ym)
            for thing in itemsfound:
                print(thing.type)
            # print(xm, ym)
