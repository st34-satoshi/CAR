# save the record.read from the file.記録が保存されているファイルから読み込む


import pygame
from pygame.locals import *
import sys
from record import record_data
import constant
from environment import make_environment


def draw_player(screen, s_circle):
    pygame.draw.circle(screen, s_circle.get_color(), s_circle.get_position(), s_circle.get_radius(), 0)


def draw_all_player(screen, list_cops, list_robbers):
    # display all player 全てのプレイヤーを表示する
    for cp in list_cops:
        draw_player(screen, cp.make_circle_me())
        draw_player(screen, cp.make_eye_circle())
    for rob in list_robbers:
        draw_player(screen, rob.make_circle_me())
        draw_player(screen, rob.make_eye_circle())


def play_record():
    count_scene = 0  # replay what scene number 何番目を再現しているか
    size_x = constant.screen_size_x
    size_y = constant.screen_size_y
    record = record_data.Record()
    record.read_from_file("record/CAR-record")
    list_cops = record.record_read[0][0]  # 最初は0番目
    list_robbers = record.record_read[0][1]

    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption("Cops and Robbers play record")
    environment = make_environment.make_environment()
    state_play = 'stop'  # stop,play,back

    while True:
        screen.fill((255, 255, 255, 8))  # color
        environment.draw_environment(screen)
        draw_all_player(screen, list_cops, list_robbers)
        pygame.display.update()
        if state_play == 'play':
            get_scene = record.get_scene_at(count_scene + 1)
            count_scene = get_scene[0]
            list_cops = get_scene[1]
            list_robbers = get_scene[2]
        elif state_play == 'back':
            get_scene = record.get_scene_at(count_scene - 1)
            count_scene = get_scene[0]
            list_cops = get_scene[1]
            list_robbers = get_scene[2]
        for event in pygame.event.get():
            if event.type == QUIT:
                # at the end.終了
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if pygame.key.get_pressed()[K_f]:
                    # move one scene when push f.f一度押すことで一つ進む
                    get_scene = record.get_scene_at(count_scene + 1)
                    count_scene = get_scene[0]
                    list_cops = get_scene[1]
                    list_robbers = get_scene[2]
                elif pygame.key.get_pressed()[K_b]:
                    # back one scene pushing b button.bを一度押すことで一つ戻る
                    get_scene = record.get_scene_at(count_scene - 1)
                    count_scene = get_scene[0]
                    list_cops = get_scene[1]
                    list_robbers = get_scene[2]
                elif pygame.key.get_pressed()[K_s]:
                    # save the scene pushing s button.sを押すことでその場面を保存する
                    record.save_to_file_one(count_scene)
                elif pygame.key.get_pressed()[K_p]:
                    state_play = 'play'
                elif pygame.key.get_pressed()[K_o]:
                    state_play = 'stop'
                elif pygame.key.get_pressed()[K_i]:
                    state_play = 'back'

        if pygame.key.get_pressed()[K_RIGHT]:
            # move next scene if there is next scene.次の場面があれば次の場面に進む
            get_scene = record.get_scene_at(count_scene + 1)
            count_scene = get_scene[0]
            list_cops = get_scene[1]
            list_robbers = get_scene[2]
        elif pygame.key.get_pressed()[K_LEFT]:
            get_scene = record.get_scene_at(count_scene - 1)
            count_scene = get_scene[0]
            list_cops = get_scene[1]
            list_robbers = get_scene[2]


if __name__ == '__main__':
    pygame.init()
    play_record()
