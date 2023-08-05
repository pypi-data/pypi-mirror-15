""" Name: steinitz.py
    Description: This module is responsible by setting up steinitz interface.
"""

from Tkinter import *

from socket import *

# Basic untwisted imports.
from untwisted.network import *
from untwisted.utils.stdio import *

# As fics protocol is token based we use Shrug to tokenize msgs.
from untwisted.utils.shrug import *

# This is a basic implementation for fics protocol.
# It basically splits msgs into fields. These fields
# are delimited by space.
from steinitz import fics

# We use it to show info.
from tkMessageBox import showinfo
from tkSimpleDialog import askstring, askinteger

# This module contains the Seek class 
# that is used to seek games.
from seek import *

# Our board class. It is the abstraction of a chess board.
from steinitz.board import *

# The clock class that will mark the time between moves.
from steinitz.clock import *
from steinitz.chat import *
from steinitz.askrating import *
from steinitz.utils import fenstring, init, rsc, stockfish


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        # It is interesting to hold the root instance
        # though most of times you will not need it.

        # At this point we have no connection initialized
        # we just assign None to self.con to map this state.
        self.con = None

        self.title('Steinitz')
        self.menubar = Menu(master=self)
        self.config(menu=self.menubar)

        self.menu1 = Menu(self.menubar, tearoff = 0)

        self.submenu1 = Menu(self.menubar, tearoff = 0)
        self.menu1.add_cascade(label='Rated White', menu=self.submenu1)

        self.submenu1.add_command(label='Blitz 3 0', 
                                  command=lambda: self.con.dump('seek 3 0 rated white formula\r\n'))
        self.submenu1.add_command(label='Blitz 5 0', 
                                  command=lambda: self.con.dump('seek 5 0 rated white formula\r\n'))
        self.submenu1.add_separator()
        self.submenu1.add_command(label='Standard 10 0', 
                                  command=lambda: self.con.dump('seek 10 0 rated white formula\r\n'))
        self.submenu1.add_command(label='Standard 15 0', 
                                  command=lambda: self.con.dump('seek 15 0 rated white formula\r\n'))
        self.submenu1.add_command(label='Standard 20 0',
                                  command=lambda: self.con.dump('seek 20 0 rated white formula\r\n'))
        self.submenu1.add_command(label='Standard 30 0',
                                  command=lambda: self.con.dump('seek 30 0 rated white formula\r\n'))
        self.submenu1.add_command(label='Standard 60 0', 
                                  command=lambda: self.con.dump('seek 60 0 rated white formula\r\n'))
        self.submenu2 = Menu(self.menubar, tearoff = 0)
        self.menu1.add_cascade(label='Unrated White', menu=self.submenu2)
        self.submenu2.add_command(label='Blitz 3 0', 
                                  command=lambda: self.con.dump('seek 3 0 unrated white formula\r\n'))
        self.submenu2.add_command(label='Blitz 5 0', 
                                  command=lambda: self.con.dump('seek 5 0 unrated white formula\r\n'))
        self.submenu2.add_separator()
        self.submenu2.add_command(label='Standard 10 0', 
                                  command=lambda: self.con.dump('seek 10 0 unrated white formula\r\n'))
        self.submenu2.add_command(label='Standard 15 0',
                                  command=lambda: self.con.dump('seek 15 0 unrated white formula\r\n'))
        self.submenu2.add_command(label='Standard 20 0',
                                  command=lambda: self.con.dump('seek 20 0 unrated white formula\r\n'))
        self.submenu2.add_command(label='Standard 30 0', 
                                  command=lambda: self.con.dump('seek 30 0 unrated white formula\r\n'))
        self.submenu2.add_command(label='Standard 60 0',
                                  command=lambda: self.con.dump('seek 60 0 unrated white formula\r\n'))
        self.menu1.add_separator()
        self.submenu3 = Menu(self.menubar, tearoff = 0)
        self.menu1.add_cascade(label='Rated Black', menu=self.submenu3)
        self.submenu3.add_command(label='Blitz 3 0', 
                                  command=lambda: self.con.dump('seek 3 0 rated black formula\r\n'))
        self.submenu3.add_command(label='Blitz 5 0', 
                                  command=lambda: self.con.dump('seek 5 0 rated black formula\r\n'))
        self.submenu3.add_separator()
        self.submenu3.add_command(label='Standard 10 0', 
                                  command=lambda: self.con.dump('seek 10 0 rated black formula\r\n'))
        self.submenu3.add_command(label='Standard 15 0',
                                  command=lambda: self.con.dump('seek 15 0 rated black formula\r\n'))
        self.submenu3.add_command(label='Standard 20 0', 
                                  command=lambda: self.con.dump('seek 20 0 rated black formula\r\n'))
        self.submenu3.add_command(label='Standard 30 0', 
                                  command=lambda: self.con.dump('seek 30 0 rated black formula\r\n'))
        self.submenu3.add_command(label='Standard 60 0', 
                                  command=lambda: self.con.dump('seek 60 0 rated black formula\r\n'))


        self.submenu4 = Menu(self.menubar, tearoff = 0)
        self.menu1.add_cascade(label='Unrated Black', menu=self.submenu4)

        self.submenu4.add_command(label='Blitz 3 0', 
                                  command=lambda: self.con.dump('seek 3 0 unrated black formula\r\n'))
        self.submenu4.add_command(label='Blitz 5 0', 
                                  command=lambda: self.con.dump('seek 5 0 unrated black formula\r\n'))
        self.submenu4.add_separator()
        self.submenu4.add_command(label='Standard 10 0', 
                                  command=lambda: self.con.dump('seek 10 0 unrated black formula\r\n'))
        self.submenu4.add_command(label='Standard 15 0',
                                  command=lambda: self.con.dump('seek 15 0 unrated black formula\r\n'))
        self.submenu4.add_command(label='Standard 20 0', 
                                  command=lambda: self.con.dump('seek 20 0 unrated black formula\r\n'))
        self.submenu4.add_command(label='Standard 30 0', 
                                  command=lambda: self.con.dump('seek 30 0 unrated black formula\r\n'))
        self.submenu4.add_command(label='Standard 60 0', 
                                  command=lambda: self.con.dump('seek 60 0 unrated black formula\r\n'))

        self.menu1.add_separator()

        self.menu1.add_command(label='Set Rating Range', command=self.set_rating_range)

        self.menu1.add_separator()
        self.menu1.add_command(label='Specific Seek', command=self.find)
        self.menubar.add_cascade(label='Seek', menu=self.menu1)
        self.menu2 = Menu(self.menubar, tearoff = 0)
        self.menu2.add_command(label='Shouts', command=self.open_shouts_channel)
        self.menu2.add_command(label='Private Message', command=self.open_private_message)
        self.menu2.add_command(label='Channel', command=self.open_channel_message)
        self.menu2.add_separator()
        self.menu2.add_command(label='Friend Notify', command=self.unplug)
        self.menu2.add_command(label='Game Notify', command=self.unplug)
        self.menubar.add_cascade(label='Utils', menu=self.menu2)
        self.menu3 = Menu(self.menubar, tearoff = 0)
        self.menu3.add_command(label='Examine Game', command=self.examine_game)
        self.menu3.add_command(label='Examine User Game', command=self.examine_user_game)
        self.menu3.add_command(label='Unexamine Game', command=self.unexamine_game)
        self.menu3.add_separator()
        self.menu3.add_command(label='Observe Game', command=self.observe_game)
        self.menu3.add_command(label='Unobserve Game', command=self.unobserve_game)
        self.menu3.add_separator()
        self.menu3.add_command(label='View Statiscs', command=self.view_statistics)
        self.menu3.add_command(label='View User Statistics', command=self.view_user_statistics)
        self.menu3.add_separator()
        self.menu3.add_command(label='View History', command=self.view_history)
        self.menu3.add_command(label='View User History', command=self.view_user_history)
        self.menubar.add_cascade(label='Tools', menu=self.menu3)

        self.menu4 = Menu(self.menubar, tearoff = 0)
        self.menu4.add_command(label='Connect', command=self.plug)
        self.menu4.add_separator()
        self.menu4.add_command(label='Quit', command=lambda: self.con.dump('quit\r\n'))
        self.menubar.add_cascade(label='Server', menu=self.menu4)

        self.menu5 = Menu(self.menubar, tearoff = 0)
        self.menu5.add_command(label='White Best Move', command=self.white_best_move)
        self.menu5.add_command(label='Black Best Move', command=self.black_best_move)
        self.menu5.add_separator()
        self.menu5.add_command(label='Play Best Move', command=self.play_best_move)
        self.menu5.add_separator()
        self.menu5.add_command(label='Black Last Move Score', command=self.black_last_move_score)
        self.menu5.add_command(label='White Last Move Score', command=self.white_last_move_score)
        self.menu5.add_separator()
        self.menu5.add_command(label='Engine Setup', command=self.setup_engine)
        self.menubar.add_cascade(label='Engine', menu=self.menu5)


        # This frame will contain the board.
        # I use relief=RAISED to give a cuter look and feel.
        self.frame1 = Frame(self, border=3, padx=5, pady=5, relief=RAISED)

        # It initializes board and pass self.frame1 as instance
        # it means it will stay inside frame1.
        self.board = Board(self.frame1, send_move=lambda data: self.con.dump(data))

        # We want it to expand.
        self.board.pack(expand=True)

        self.menu6 = Menu(self.menubar, tearoff = 0)
        self.menu6.add_command(label='Inc Width  <Shift-Right>', command=self.board.incwidth)
        self.menu6.add_command(label='Inc Height <Shift-Up>', command=self.board.incheight)
        self.menu6.add_separator()
        self.menu6.add_command(label='Dec Width <Shift-Left>', command=self.board.decwidth)
        self.menu6.add_command(label='Dec Height <Shift-Down>', command=self.board.decheight)
        self.menu6.add_separator()
        self.menu6.add_command(label='Inc Shape <F1>', command=self.board.incshape)
        self.menu6.add_command(label='Dec Shapet <F2>', command=self.board.decshape)
        self.menubar.add_cascade(label='Appearence', menu=self.menu6)


        
        # We pack it to the left and make it fill in both
        # directions.
        self.frame1.pack(side='left', expand=True, fill=BOTH)

        # We bind key press events to the board functions
        # incheight, decheight, incwidth, decwidth 
        # these functions are responsible by increasing
        # the board size.
        self.bind('<Shift-Up>', lambda widget: self.board.incheight())
        self.bind('<Shift-Down>', lambda widget: self.board.decheight())

        self.bind('<Shift-Right>', lambda widget: self.board.incwidth())
        self.bind('<Shift-Left>', lambda widget: self.board.decwidth())

        # This frame will contain most widgets.
        self.frame2 = Frame(self)
        
        # We instantiate our clock as though it were a frame.
        # Since it inherits from Frame class.
        self.clock = Clock(self.frame2, border=3, relief=RAISED)

        self.clock.pack(side='top', fill=BOTH)

        # This frame contains options relative to game.
        self.frame3 = Frame(self.frame2, border=3, relief=RAISED, padx=5, pady=5)

        self.img1 = PhotoImage(file=rsc('icon', 'take-one.gif'))
        self.img2 = PhotoImage(file=rsc('icon', 'take-two.gif'))
        self.img3 = PhotoImage(file=rsc('icon', 'draw.gif'))
        self.img4 = PhotoImage(file=rsc('icon', 'resign.gif'))
        self.img5 = PhotoImage(file=rsc('icon', 'abort.gif'))
        
        # Whenever one clicks on it it sends a takeback 1
        # to fics.
        self.button1 = Button(self.frame3, image=self.img1, 
                              command = lambda :self.con.dump('takeback 1\r\n'))

        # It asks for take back two moves.
        self.button2 = Button(self.frame3, image=self.img2, 
                              command = lambda :self.con.dump('takeback 2\r\n'))

        # It suggests draw to your opponent.
        self.button3 = Button(self.frame3, image=self.img3, 
                              command = lambda :self.con.dump('draw\r\n'))

        
        # You just resign.
        self.button4 = Button(self.frame3, image=self.img4,
                              command = lambda :self.con.dump('resign\r\n'))
        
        # You got in a bad position maybe it is time to abort
        # it sends request for aborting the game.
        self.button5 = Button(self.frame3, image=self.img5, 
                              command = lambda :self.con.dump('abort\r\n'))

        self.button1.pack(side='left', expand=True, fill=BOTH)
        self.button2.pack(side='left', expand=True, fill=BOTH)
        self.button3.pack(side='left', expand=True, fill=BOTH)
        self.button4.pack(side='left', expand=True, fill=BOTH)
        self.button5.pack(side='left', expand=True, fill=BOTH)
        self.frame3.pack(fill=X)

        # This frame contains buttons that are useful when examining games.
        self.frame4 = Frame(self.frame2, padx=5, pady=5, border=3, relief=RAISED)
        self.img6 = PhotoImage(file=rsc('icon', 'start.gif'))
        self.img7 = PhotoImage(file=rsc('icon', 'back.gif'))
        self.img8 = PhotoImage(file=rsc('icon', 'foward.gif'))
        self.img9 = PhotoImage(file=rsc('icon', 'end.gif'))

        # It goes back to the beginning of a game.
        self.button6 = Button(self.frame4, text='Start', image=self.img6,     
                              command = lambda :self.con.dump('backward 999\r\n'))

        # It goes back one move.
        self.button7  = Button(self.frame4, text='Back', image=self.img7,
                               command = lambda :self.con.dump('backward\r\n'))

        # It goes ahead one move.
        self.button8    = Button(self.frame4, text='Go', image=self.img8, 
                                 command = lambda : self.con.dump('forward\r\n'))

        # It goes to the end.
        self.button9   = Button(self.frame4, text='End', image=self.img9, 
                                command = lambda :self.con.dump('forward 999\r\n'))

        self.button6.pack(side='left', expand=True, fill=X) 
        self.button7.pack(side='left', expand=True, fill=X) 
        self.button8.pack(side='left', expand=True, fill=X) 
        self.button9.pack(side='left', expand=True, fill=X) 
        self.frame4.pack(side='bottom',  fill=X)

        # This frame contains the console widgets.
        self.frame5 = Frame(self.frame2)

        # It contains the text console widget.
        self.frame6 = Frame(master=self.frame5,  border=3,  relief=RAISED,  
                            padx=5,  pady=5)

        # It contains the entry console widget.
        self.frame7 = Frame(master=self.frame5,  border=3,  relief=RAISED,  
                            padx=5,  pady=5)

        self.scrollbar = Scrollbar(master=self.frame6)
        self.scrollbar.pack(side='right', fill=Y)

        # We dump all what comes in this text widget.
        self.text = Text(self.frame6, background='black',foreground='green',width=60, 
                         yscrollcommand=self.scrollbar.set, font=('Helvetica', 8))

        self.scrollbar.config(command=self.text.yview)

        # We use it to send commands.
        self.entry = Entry(self.frame7)
        self.entry.pack(fill=X)

        self.frame7.pack(side='bottom', fill=X)
        self.frame6.pack(side='top', expand=True, fill=BOTH)
        self.text.pack(side='top', expand=True, fill=Y)

        # Whenever you press enter it dumps the command.
        self.entry.bind('<KeyPress-Return>', self.send_cmd)
        self.frame5.pack(side='top', expand=True, fill=Y)
        self.frame2.pack(side='right', fill=Y)

        self.bind('<Shift-Up>', lambda widget: self.board.incheight())
        self.bind('<Shift-Down>', lambda widget: self.board.decheight())
        self.bind('<Shift-Right>', lambda widget: self.board.incwidth())
        self.bind('<Shift-Left>', lambda widget: self.board.decwidth())
        self.bind('<F1>', lambda widget: self.board.incshape())
        self.bind('<F2>', lambda widget: self.board.decshape()) 

        self.stockfish_depth = 20
        # We initialize the process of reading from the socket.
        # It basically tells untwisted core to start listening for
        # reading, writting processes.
        self.screen()

    def screen(self):
        # We use 200ms that's a good number.
        self.after(200, self.screen)

        # We will not block on select. So, we dont want to wait.
        core.gear.timeout = 0

        # It tells untwisted to listen for reading, writting on the
        # sockets.
        core.gear.update()

    def ask_address(self):
        host = askstring('Server', 'Type the server address.', initialvalue='freechess.org')
        if not host: return

        port = askinteger('Port', 'Type the port.', initialvalue=5000)
        if not port: return

        return host, int(port)

    def plug(self):
        # If it is connected then we have to unplug.
        if self.con: self.unplug()
        host, port = self.ask_address()         

        # We create our connection socket.
        sock = socket(AF_INET, SOCK_STREAM)

        # It wraps the socket so we can install protocols into it.
        self.con = Spin(sock)
        
        Client(self.con)
       
        # It maps CONNECT to send_ident.
        self.con.link(CONNECT, self.send_ident) 
        self.con.link(CONNECT_ERR, lambda con, err: lose(con))
        self.con.link(CONNECT_ERR, lambda con, err: self.update_text(con, 'Connection failed.'))

        self.con.connect_ex((host, port))

    def send_ident(self, con):
        # Basic untwisted protocols required by fics protocol.
        Stdin(self.con)
        Stdout(self.con)
        Shrug(self.con, '\n\r')

        # Finally we install fics protocol.
        fics.install(self.con)
        
        # If it happens of the server closing
        # the connection then we just close the socket
        # and destroy it.
        self.con.link(CLOSE, lambda con, err: lose(con))

         # Whenever it comes data we print it on our console.
        self.con.link(FOUND, self.update_text)

        # The '<12>' is an event issued by fics protocol
        # it means you are either playing a game or examining a
        # game. In both case we need to update the state of the
        # board.
        self.con.link('<12>', self.update_state)

        # It waits for the user sending login
        # when the session starts we can send style 12.

        event, args = yield hold(con, fics.START_SESSION)

        self.username = args[1]
        self.con.dump('set style 12\r\n')

    def play_best_move(self):
        from steinitz.utils import stockfish
        move = stockfish(self.last_state)
        self.con.dump('%s\r\n' % move)

    def black_last_move_score(self):
        pass

    def white_last_move_score(self):
        pass

    def unplug(self):
        self.con.dump('quit\r\n')
        self.con = None    

    def find(self):
        seek   = Seek(self)
        option = seek()
        data   = 'seek %s %s %s %s formula %s-%s\r\n' % option

        self.con.dump(data)

    def send_cmd(self, widget):
        data = self.entry.get()
        self.text.insert(END, '%s\n' % data)
        self.text.yview(MOVETO, 1.0)
        self.entry.delete(0, END)
        self.con.dump('%s\r\n' % data)

    def update_text(self, con, data):
        self.text.insert(END, '%s\n' % data)
        self.text.yview(MOVETO, 1.0)
        
    def update_state(self, con, *args):
        """ 
        Whenever '<12>' is issued this function
        is called with the respective arguments.
        """

        position   = args[:8]
        white_time = int(args[-9])
        black_time = int(args[-8])
        white      = args[16]
        black      = args[17]
        flip       = int(args[-3])
        turn       = args[8]
        
        # We update the title so we can know
        # which game we are playing.
        self.title('%s x %s' % (white, black))
        self.clock.click(turn, white_time, black_time)

        # It tells the board to update the position based
        # on the flip.
        self.board.update_position(position, flip)

        # It is interesting to have if you want to analyze games
        # with some engine.
        self.last_state = args

    def setup_engine(self):
        self_stockfish_depth = askstring('Stockfish Depth', 'Depth:', initialvalue='20')

    def set_rating_range(self):
        AskRating(self, self.con)
        
    def examine_game(self):
        num = askstring('Examine', 'Game Number:', initialvalue='')
        self.con.dump('examine %s %s\r\n' % (self.username, num))

    def examine_user_game(self):
        nick = askstring('Examine', 'Nick:', initialvalue='')
        num = askstring('Examine', 'Game Number:', initialvalue='')
        self.con.dump('examine %s %s\r\n' % (nick, num))

    def unexamine_game(self):
        self.con.dump('unexamine\r\n')

    def observe_game(self):
        num = askstring('Examine', 'Game Number/Nick', initialvalue='')
        self.con.dump('observe %s\r\n' % num)

    def unobserve_game(self):
        num = askstring('Examine', 'Game Number/Nick', initialvalue='')
        self.con.dump('unobserve %s\r\n' % num)

    def open_shouts_channel(self):
        chat = Chat(self, lambda data: self.con.dump('shout %s\r\n' % data), 'Shouts', self.username)
        self.con.link(fics.SHOUT, lambda con, nick, mode, msg: chat.update_text('%s shouts%s %s' % (nick, mode, msg)))

        # i must umap after the window is destroyed.
        # chat.protocol('WM_DELETE_WINDOW', self.cancel)

    def open_private_message(self):
        nick = askstring('Nick', 'Nick:')
        chat = Chat(self, lambda data: self.con.dump('tell %s %s\r\n' % (nick, data)), nick, self.username)

        self.con.link('%s tells you:' % nick, lambda con, mode, msg: chat.update_text('<%s>%s' % (nick, msg)))
        self.con.link('%s says:' % nick, lambda con, mode, msg: chat.update_text('<%s>%s' % (nick, msg)))

    def white_best_move(self):
        last_state    = list(self.last_state)
        last_state[8] = 'W'
        move          = stockfish(last_state, self.stockfish_depth)
        showinfo('White best move in the position', move)

    def black_best_move(self):
        last_state    = list(self.last_state)
        last_state[8] = 'B'
        move          = stockfish(last_state, self.stockfish_depth)
        showinfo('Black best move in the position', move)

    def open_channel_message(self):
        pass

    def view_statistics(self):
        pass

    def view_user_statistics(self):
        pass

    def view_history(self):
        pass

    def view_user_history(self):
        pass

    def find(self):
        seek = Seek(self)
        option = seek()
        data = 'seek %s %s %s %s formula %s-%s\r\n' % option
        self.con.dump(data)



    
if __name__ == '__main__':
    app = App()
    app.mainloop()
        









