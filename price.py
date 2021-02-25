import sys
from random import choice, randrange

import pygame as pg

from binance.client import Client
from binance.websockets import BinanceSocketManager


# init
api_key = your_key
api_secret = your_secret

client = Client(api_key, api_secret)
coin_price = {'error':False}

priceGlob = 0
def coin_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    global priceGlob
    if msg['e'] != 'error':
        # print(msg['c'])
        # print(msg['c'][0:7])
        priceGlob = msg['c'][0:7]
        coin_price['last'] = msg['c']
        coin_price['bid'] = msg['b']
        coin_price['last'] = msg['a']
    else:
        coin_price['error'] = True
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', coin_trade_history)
bsm.start()


def main():
    global priceGlob
    info = pg.display.Info()
    screen = pg.display.set_mode((info.current_w, info.current_h), pg.FULLSCREEN)
    screen_rect = screen.get_rect()
    font = pg.font.Font(None, 600)
    clock = pg.time.Clock()
    color = (randrange(256), randrange(256), randrange(256))
    txt = font.render("BTC", True, color)
    timer = 10
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    done = True

        timer -= 1
        # Update the text surface and color every 10 frames.
        if timer <= 0:
            timer = 10
            color = (randrange(256), randrange(256), randrange(256))
            txt = font.render(str(priceGlob), True, color)

        screen.fill((30, 30, 30))
        screen.blit(txt, txt.get_rect(center=screen_rect.center))

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
    sys.exit()


