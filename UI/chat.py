from .lib import tttk_tk as tk

class Chat(tk.Frame):
    """
    Chat window for the game. This class is used to display the chat window and send messages to the server. 
    It also listens for incoming chat messages from the server.
    """
    def __init__(self, master, root, chat='', *args, **kwargs):
        super().__init__(master)
        self.root = root
        self._create_widgets(chat)
        self._display_widgets()
        self.root.bind('<Return>', lambda *args: self._enter())
        self.root.network_events['chat/receive'] = self._chat_receive
        self.widget.bind('<Destroy>', lambda *args: self._on_destroy())

    def _create_widgets(self, chat):
        self.lblheading = tk.Label(self.widget, text="Chat")
        self.txtChat = tk.Text(self.widget, width=0)
        self.txtScroll = tk.Scrollbar(self.widget, command=self.txtChat.yview)
        self.txtChat.config(yscrollcommand=self.txtScroll.set)
        self.txtChat.insert(tk.END, chat)
        self.txtChat.config(state=tk.DISABLED)
        self.etrMessage = tk.Entry(self.widget)
        self.btnSend = tk.Button(self.widget, text="Send", command=lambda *args: self._send())

    def _display_widgets(self):
        self.widget.columnconfigure([0], weight=5)
        self.widget.columnconfigure([1], weight=1)
        self.widget.rowconfigure([0], weight=1)
        self.widget.rowconfigure([1,2], weight=0)
        self.widget.rowconfigure([0,2], weight=0)
        self.widget.rowconfigure([1], weight=1)
        self.lblheading.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=0, row=0, columnspan=3)
        self.txtChat.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=0, row=1, columnspan=2)
        self.txtScroll.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=1)
        self.etrMessage.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=0, row=2)
        self.btnSend.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=1, row=2, columnspan=2)

    def _send(self):
        list(self.root.out_queue.values())[0].put({'message_type': 'chat/message', 'args' : {'message': self.etrMessage.val}})
        self.etrMessage.val = ""

    def _chat_receive(self, queue):
        self.txtChat.config(state=tk.NORMAL)
        self.txtChat.insert(tk.END, f"{queue['sender'].display_name}: {queue['message']}\n")
        self.txtChat.config(state=tk.DISABLED)

    def _on_destroy(self):
        del self.root.network_events['chat/receive']

    def _enter(self):
        if(self.focus_get() == self.etrMessage.widget):
            self._send()