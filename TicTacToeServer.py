import socket
import threading
import argparse

playground = [' '] * 9
symboGame = 'X'

argparser = argparse.ArgumentParser(description="Proxy server")
argparser.add_argument("port", type=int, help="Port to listen on")
parsargs = argparser.parse_args()

def cli_info(cnc,elses, IDuser):

    global symboGame
    global playground
    
    cnc.sendall(b" 'Turn Info' : When server says it is your turn, you can make your move \n")
    cnc.sendall(b" 'Board Info' : To view the state of board at any time, you can write command 'board' \n")
    cnc.sendall(b" You can enter values 0 to 8 \n")
    cnc.sendall(b"Game is beginning\n")
    if (symboGame == 'X' and IDuser == 1) or (symboGame == 'O' and IDuser == 2):
        
        cnc.sendall(b"\n" + boardlook(playground).encode() + b"\n")
        cnc.sendall(b"It is your time to turn! \n")
        
    if (symboGame == 'X' and IDuser == 2) or ( symboGame == 'O' and IDuser == 1):
        cnc.sendall(b"\n" + boardlook(playground).encode() + b"\n")    
        cnc.sendall(b"Please wait your opponent! \n")
            
    while True:
        
        packag = cnc.recv(1024).decode().strip()

        
        if (symboGame == 'X' and IDuser == 2) or ( symboGame == 'O' and IDuser == 1):

            if packag.lower() == "board":
                cnc.sendall(b"\n" + boardlook(playground).encode() + b"\n")

            elif packag.lower() == "turn":
                cnc.sendall(b"It's not your turn! \n")
            else:
                cnc.sendall(b"You shall wait your opponent due to rule of turns! \n")
                    
                    
        if (symboGame == 'X' and IDuser == 1) or (symboGame == 'O' and IDuser == 2):
            
            if packag.lower() == "board":
                cnc.sendall(b"\n" + boardlook(playground).encode() + b"\n")
                continue
            
            if packag.lower() == "turn":
                cnc.sendall(b"It's your turn! \n")
                cnc.sendall(b"Enter move for your turn (0-8), board or turn: ")
                continue
            
            if not packag:
                cnc.sendall(b"False statement. Please try again.\n")
                
                continue
            try:
                drv = int(packag)
            except ValueError:
                cnc.sendall(b"False statement. Please try again.\n")
                continue

            if drv < 0 or drv > 8:
                cnc.sendall(b"Illegal. Try again.\n")
                print('Received illegal move!')
                continue
            

            
            if playground[drv] == ' ':
                playground[drv] = symboGame
                if symboGame == 'X':
                    print('Player 1s position is:' + str(drv) +' .Player 2s turn!')
                else:
                    print('Player 2s position is' + str(drv) +' .Player 1s turn!')
                    
                if how2win(playground, symboGame):
                    elses.sendall(b"\n" + boardlook(playground).encode() + b"\n")
                    cnc.sendall(b"\n" + boardlook(playground).encode() + b"\n")
                    cnc.sendall(b"Winner!\n")
                    elses.sendall(b"Lose!\n")
                    print('End of the game!')
                    
                    if symboGame == 'X':
                        print('Player 1 won!')
                    else:
                        print('Player 2 won!')
                    break
                elif ' ' not in playground:
                    elses.sendall(b"\n" + boardlook(playground).encode() + b"\n")
                    cnc.sendall(b"\n" + boardlook(playground).encode() + b"\n")
                    cnc.sendall(b"Draw!\n")
                    elses.sendall(b"Draw!\n")
                    print('Game of draw.')
                    break
                else:
                    symboGame = 'O' if symboGame == 'X' else 'X'
                    elses.sendall(b"\n" + boardlook(playground).encode() + b"\n")
                    elses.sendall(b"It's your turn! \n")
                    cnc.sendall(b"\n" + boardlook(playground).encode() + b"\n")
                    cnc.sendall(b"You've already played, please wait the opponent! \n")
            else:
                 cnc.sendall(b"Illeagel move. Please do legal move.\n")
        

    cnc.close()

def how2win(brd, usr):
    stateofwinning = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]               
    ]
    for comb in stateofwinning:
        if all(brd[i] == usr for i in comb):
            return True
    return False

def boardlook(brd):
    drw = []
    drw.append("                  ")
    drw.append("(" + brd[0] + ")" +" | " + "(" + brd[1] + ")" + " | " + "(" + brd[2] + ")")
    drw.append("                  ")
    drw.append("(" + brd[3] + ")" + " | " + "(" +  brd[4] + ")" + " | " + "(" + brd[5] + ")")
    drw.append("                  ")
    drw.append("(" + brd[6] + ")" +  " | " + "(" + brd[7] + ")" + " | " + "(" + brd[8] + ")")
    drw.append("                  ")
    return "\n".join(drw)

def main():
    hst = '127.0.0.1'
    prt = parsargs.port

    soc_srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc_srv.bind((hst, prt))
    soc_srv.listen(2)
    print("Waiting...")

    frst_cnc, frst_add = soc_srv.accept()
    print("Player 1 connected for (X):", frst_add)

    frst_cnc.sendall(b"You are player 1 (X)\n")
    scnd_cnc, scnd_add = soc_srv.accept()
    print("Player 2 connected for (O):", scnd_add)

    scnd_cnc.sendall(b"You are player 2 (O)\n")
    print("Its beginning...")
    print('Player 1 starts the game!')


    frst_thr = threading.Thread(target=cli_info, args=(frst_cnc,scnd_cnc, 1))
    scnd_thr = threading.Thread(target=cli_info, args=(scnd_cnc,frst_cnc, 2))

    frst_thr.start()
    scnd_thr.start()

    frst_thr.join()
    scnd_thr.join()


    frst_cnc.close()
    scnd_cnc.close()
    soc_srv.close()

if __name__ == '__main__':
    main()